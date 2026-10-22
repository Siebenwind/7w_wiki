"""Browser acceptance, invoked exclusively by ./7w_wiki.py test --suite reader-browser."""
import functools
import http.server
import json
import tempfile
import threading
import shutil
from pathlib import Path
from urllib.parse import quote
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[2]


def main():
    assert (ROOT/'site/build-info.json').exists(), 'A complete Pages build is required'
    output = Path(tempfile.mkdtemp(prefix="7w_reader_browser_"))
    shutil.copytree(ROOT/'site',output/'site')
    class Handler(http.server.SimpleHTTPRequestHandler):
        def translate_path(self, path):
            return super().translate_path(path.removeprefix('/7w_wiki'))
        def log_message(self, *args): pass
    server = http.server.ThreadingHTTPServer(('127.0.0.1',0), functools.partial(Handler,directory=str(output/'site')))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}/7w_wiki/'
    results = []
    titles = json.loads((ROOT/'site/assets/search-titles.json').read_text())
    wiki_titles=[r for r in titles if r['kind']=='wiki']
    alias = next((r,a) for r in wiki_titles for a in r['aliases']
                 if a.casefold()!=r['title'].casefold() and len(a)>4
                 and sum(any(v.casefold()==a.casefold() for v in [t['title'],*t['aliases']]) for t in wiki_titles)==1)
    with sync_playwright() as p:
        for engine in ['chromium','firefox','webkit']:
            browser = getattr(p,engine).launch()
            for width in [320,390,768,1024,1440]:
                for scheme in ['default','slate']:
                    page = browser.new_page(viewport={'width':width,'height':844})
                    page.set_default_timeout(8000)
                    name=f'{engine}-{width}-{scheme}'
                    try:
                        page.goto(base)
                        if scheme=='slate': page.locator('label[for="__palette_1"]').click()
                        expect(page.locator('body')).to_have_attribute('data-md-color-scheme',scheme)
                        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'horizontal page overflow'
                        assert page.locator('#sw-query').bounding_box()['height']>=44
                        # WCAG text contrast on the custom search controls in the actual theme.
                        contrast=page.locator('#sw-query').evaluate('''el => {
                          const c=getComputedStyle(el), rgb=s=>s.match(/[\\d.]+/g).slice(0,3).map(Number);
                          const lum=a=>a.map(x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4}).reduce((s,x,i)=>s+x*[.2126,.7152,.0722][i],0);
                          const a=lum(rgb(c.color)),b=lum(rgb(c.backgroundColor));return (Math.max(a,b)+.05)/(Math.min(a,b)+.05);
                        }''')
                        assert contrast>=4.5, f'search text contrast {contrast}'
                        if width==390:
                            assert page.locator('.portal-card').first.bounding_box()['y']<844,'no theme entry above fold'
                        page.screenshot(path=str(output/(name+'-home.png')))
                        for q in ['Astrael','Bellum']:
                            page.locator('#sw-query').fill(q)
                            expect(page.locator('#sw-suggestions a').first).to_have_text(q,timeout=20000)
                            assert 0<len(page.locator('#sw-suggestions a').all())<=5
                            assert page.locator('.sw-suggest-panel').bounding_box()['height']>44
                        page.screenshot(path=str(output/(name+'-search.png')))
                        page.locator('#sw-query').press('Escape')
                        expect(page.locator('.sw-suggest-panel')).to_be_hidden()
                        if width<1220:
                            page.locator('.md-header label[for="__drawer"]').click()
                            expect(page.locator('#__drawer')).to_be_checked()
                        if width==390:
                            page.goto(base+'Siebenwind_Wiki/10_Archiv/Wiki_Statistiken/')
                            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'article overflow'
                            table=page.locator('.md-typeset__table').first
                            expect(table).to_have_attribute('tabindex','0')
                            table.focus();page.keyboard.press('End')
                        results.append({'case':name,'status':'PASS'})
                    except Exception as e:
                        page.screenshot(path=str(output/(name+'-failure.png')))
                        results.append({'case':name,'status':'FAIL','reason':str(e)})
                    finally: page.close()
            page=browser.new_page(viewport={'width':390,'height':844})
            page.set_default_timeout(30000)
            try:
                for q in ['Astrael','Bellum','Brandenstein','Toran Dur',alias[1],'König','keintrefferxyz98765']:
                    page.goto(base+'suche/?q='+quote(q)+'&bereich=wiki')
                    expect(page.locator('[data-sw-results] [role=status]')).not_to_have_text('Suche läuft …',timeout=30000)
                    if q=='keintrefferxyz98765':
                        expect(page.locator('[data-sw-results] [role=status]')).to_contain_text('Keine Ergebnisse')
                    elif q in ['Astrael','Bellum','Brandenstein','Toran Dur',alias[1]]:
                        expected = next(r for r in titles if r['kind']=='wiki' and any(a.casefold()==q.casefold() for a in [r['title'],*r['aliases']]))
                        expect(page.locator('.sw-result-list h2 a').first).to_have_attribute('href',base+expected['url'],timeout=30000)
                    assert len(page.locator('.sw-result-list>li').all())<=20
                page.goto(base+'suche/?q=Bellum&bereich=wiki')
                expect(page.locator('.sw-result-list h2 a').first).to_have_text('Bellum',timeout=30000)
                urls=page.locator('.sw-result-list h2 a').evaluate_all('(links)=>links.map(a=>a.href)')
                assert len(urls)==len(set(urls)), 'duplicate canonical destinations'
                if page.get_by_role('button',name='Weiter',exact=True).count():
                    assert len(urls)==20, 'first page must contain 20 results'
                    page.get_by_role('button',name='Weiter',exact=True).click()
                    expect(page).to_have_url(base+'suche/?q=Bellum&bereich=wiki&seite=2')
                    page.go_back()
                    expect(page.locator('.sw-result-list h2 a').first).to_have_text('Bellum',timeout=30000)
                page.locator('select[name=bereich]').select_option('quellen')
                expect(page.locator('.sw-result-list .sw-result-kind').first).to_have_text('Quellen',timeout=30000)
                page.go_back()
                expect(page.locator('.sw-result-list .sw-result-kind').first).to_have_text('Wiki',timeout=30000)
                page.goto(base+'?q=Astrael')
                expect(page).to_have_url(base+'suche/?q=Astrael&bereich=wiki')
                expect(page.locator('.sw-result-list h2 a').first).to_have_text('Astrael',timeout=30000)
                page.goto(base)
                page.locator('#sw-query').fill('Bellum')
                page.locator('#sw-query').fill('Astrael')
                expect(page.locator('#sw-suggestions a').first).to_have_text('Astrael',timeout=30000)
                page.locator('#sw-query').press('ArrowDown')
                expect(page.locator('#sw-query')).to_have_attribute('aria-activedescendant','sw-option-0')
                page.locator('#sw-query').press('Enter')
                expect(page).to_have_url(base+'Siebenwind_Wiki/01_Pantheon/Astrael/')
                page.goto(base)
                page.locator('#sw-query').fill('Astrael')
                expect(page.locator('#sw-suggestions a').first).to_have_text('Astrael',timeout=30000)
                page.locator('#sw-query').press('ArrowDown')
                page.locator('#sw-query').fill('Bellum')
                page.locator('#sw-query').press('Enter')
                expect(page).to_have_url(base+'suche/?q=Bellum&bereich=wiki')
                results.append({'case':engine+'-search-behavior','status':'PASS'})
            except Exception as e: results.append({'case':engine+'-search-behavior','status':'FAIL','reason':str(e)})
            page.close()
            page=browser.new_page()
            try:
                page.route('**/pagefind/**',lambda route:route.abort())
                page.goto(base+'suche/?q=Bellum')
                expect(page.locator('[data-sw-results] [role=status]')).to_contain_text('nicht geladen')
                results.append({'case':engine+'-missing-index','status':'PASS'})
            except Exception as e: results.append({'case':engine+'-missing-index','status':'FAIL','reason':str(e)})
            page.close()
            page=browser.new_page()
            try:
                import time
                def delayed(route):
                    time.sleep(.4);route.continue_()
                page.route('**/pagefind/pagefind.js',delayed)
                page.goto(base)
                page.locator('#sw-query').fill('Astrael')
                expect(page.locator('.sw-search-status')).to_have_text('Suche läuft …')
                page.locator('#sw-query').fill('Bellum')
                expect(page.locator('#sw-suggestions a').first).to_have_text('Bellum',timeout=30000)
                page.locator('#sw-query').press('Enter')
                expect(page).to_have_url(base+'suche/?q=Bellum&bereich=wiki')
                results.append({'case':engine+'-delayed-index-enter','status':'PASS'})
            except Exception as e: results.append({'case':engine+'-delayed-index-enter','status':'FAIL','reason':str(e)})
            browser.close()
    server.shutdown()
    (output/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
    print(json.dumps({'artifact_directory':str(output),'pass':sum(r['status']=='PASS' for r in results),'failures':[r for r in results if r['status']=='FAIL'],'real_devices':'NOT_TESTED'},ensure_ascii=False,indent=2))
    return int(any(r['status']=='FAIL' for r in results))


if __name__=='__main__': raise SystemExit(main())
