/* One search service for the combobox and the permanent result page. */
(() => {
  'use strict';
  const bar = document.querySelector('.sw-search-bar');
  function accessibleTables() {
    document.querySelectorAll('.md-typeset__table').forEach((table,i)=>{
      table.tabIndex=0;table.setAttribute('role','region');table.setAttribute('aria-label','Tabelle '+(i+1)+' – bei Bedarf seitlich scrollen');
    });
  }
  accessibleTables();
  // Material adds the scroll wrappers after the article has loaded.
  new MutationObserver(accessibleTables).observe(document.body,{childList:true,subtree:true});
  if (!bar) return;
  const root = new URL(bar.dataset.swRoot, location.href);
  const labels = {wiki:'Wiki', quellen:'Quellen', forschung:'Forschung', technik:'Technik', alles:'Alles'};
  const normalize = s => s.normalize('NFKC').toLocaleLowerCase('de').replace(/[_\s]+/g,' ').trim();
  let service;
  function load() {
    if (!service) service = Promise.all([
      import(new URL('pagefind/pagefind.js', root).href),
      fetch(new URL('assets/search-titles.json', root)).then(r => { if (!r.ok) throw Error('Index'); return r.json(); })
    ]).then(async ([engine, titles]) => { await engine.options({baseUrl:root.pathname}); return {engine,titles}; }).catch(e => {service=null; throw e;});
    return service;
  }
  function resultURL(url) { return new URL(url,root).href; }
  async function search(q,kind) {
    const {engine,titles}=await load();
    const exact=titles.filter(t => (kind==='alles'||t.kind===kind) && [t.title,...t.aliases].some(a=>normalize(a)===normalize(q)))
      .sort((a,b)=>(normalize(b.title)===normalize(q))-(normalize(a.title)===normalize(q)) || a.title.localeCompare(b.title,'de'));
    const match=await engine.search(q, kind==='alles'?{}:{filters:{bereich:kind}});
    const exactURLs=new Set(exact.map(t=>resultURL(t.url)));
    // Pagefind groups sections into one result. Exact titles/aliases are pinned ahead of mention matches.
    const rest=match.results.map(r=>({load:async()=>{
      const d=await r.data();
      const t=titles.find(t=>resultURL(t.url)===resultURL(d.url));
      return {url:resultURL(d.url),title:d.meta.title||t?.title||'Artikel',kind:t?.kind||kind,excerpt:d.plain_excerpt||d.excerpt||''};
    }}));
    const pinned=exact.map(t=>({load:async()=>({...t,url:resultURL(t.url),excerpt:''})}));
    return {items:[...pinned,...rest], exactURLs, pinned:pinned.length};
  }
  async function materialize(result,offset,size) {
    const rows=[]; const seen=new Set(); let accepted=0;
    for (let i=0;i<result.items.length;i++) {
      const d=await result.items[i].load();
      if (seen.has(d.url)) continue;
      seen.add(d.url);
      if (accepted++>=offset && rows.length<size) rows.push(d);
      if(rows.length===size+0 && accepted>offset+size) break;
    }
    return rows;
  }
  function searchURL(q,kind='wiki',page=1) {
    const url=new URL('suche/',root); url.searchParams.set('q',q); url.searchParams.set('bereich',kind);
    if(page>1) url.searchParams.set('seite',page);
    return url;
  }
  function node(tag,text,className) {const n=document.createElement(tag); if(text)n.textContent=text; if(className)n.className=className; return n;}
  const input=document.querySelector('#sw-query');
  const panel=document.querySelector('.sw-suggest-panel');
  const list=document.querySelector('#sw-suggestions');
  const status=document.querySelector('.sw-search-status');
  const all=document.querySelector('.sw-all-results');
  let request=0,timer,active=-1;
  function close(){panel.hidden=true; input.setAttribute('aria-expanded','false');input.removeAttribute('aria-activedescendant');active=-1;}
  async function suggest() {
    const id=++request,q=input.value.trim();
    list.replaceChildren(); active=-1; input.removeAttribute('aria-activedescendant');
    if(!q){close();return;}
    panel.hidden=false;input.setAttribute('aria-expanded','true');status.textContent='Suche läuft …';all.href=searchURL(q);
    try {
      const result=await search(q,'wiki'),rows=await materialize(result,0,5);
      if(id!==request)return;
      status.textContent=rows.length?'Passende Artikel':'Keine passenden Wikiartikel. Andere Bereiche findest du auf der Ergebnisseite.';
      rows.forEach((r,i)=>{const li=node('li');li.id='sw-option-'+i;li.setAttribute('role','option');li.setAttribute('aria-selected','false');const a=node('a',r.title);a.href=r.url;a.tabIndex=-1;li.append(a);list.append(li);});
    }catch(e){if(id===request)status.textContent='Die Suche konnte nicht geladen werden. Bitte erneut versuchen oder Themen A–Z öffnen.';}
  }
  input.addEventListener('input',()=>{++request;clearTimeout(timer);close();list.replaceChildren();timer=setTimeout(suggest,180);});
  input.addEventListener('focus',()=>{load().catch(()=>{});});
  input.addEventListener('keydown',e=>{
    const options=[...list.children];
    if(e.key==='Escape'){++request;clearTimeout(timer);close();e.preventDefault();}
    if((e.key==='ArrowDown'||e.key==='ArrowUp')&&options.length&&!panel.hidden){e.preventDefault();active=(active+(e.key==='ArrowDown'?1:-1)+options.length)%options.length;options.forEach((n,i)=>n.setAttribute('aria-selected',String(i===active)));input.setAttribute('aria-activedescendant',options[active].id);options[active].scrollIntoView({block:'nearest'});}
    if(e.key==='Enter'&&active>=0&&!panel.hidden){e.preventDefault();location.assign(options[active].querySelector('a').href);}
  });
  document.addEventListener('click',e=>{if(!bar.contains(e.target)){++request;clearTimeout(timer);close();}});
  document.addEventListener('focusin',e=>{if(!bar.contains(e.target)){++request;clearTimeout(timer);close();}});
  const page=document.querySelector('[data-sw-results]');
  if(!page) { if(new URL(location.href).searchParams.has('q'))location.replace(searchURL(new URL(location.href).searchParams.get('q'))); return; }
  const form=page.querySelector('form'),qfield=form.elements.q,filter=form.elements.bereich;
  const output=page.querySelector('.sw-result-list'),summary=page.querySelector('[role=status]'),pager=page.querySelector('.sw-pagination');
  let generation=0;
  async function render() {
    const id=++generation,params=new URL(location.href).searchParams,q=params.get('q')?.trim()||'',kind=Object.hasOwn(labels,params.get('bereich'))?params.get('bereich'):'wiki';
    const p=Math.max(1,Number.parseInt(params.get('seite')||'1',10)||1);
    qfield.value=q;filter.value=kind;input.value=q;output.replaceChildren();pager.replaceChildren();
    if(!q){summary.textContent='Gib einen Namen oder ein Thema ein.';return;}
    summary.textContent='Suche läuft …';
    try {
      const found=await search(q,kind);
      // Resolve once on the results page so the count and pagination describe unique destinations.
      const unique=new Map();
      for(let offset=0;offset<found.items.length;offset+=24){
        const batch=await Promise.all(found.items.slice(offset,offset+24).map(item=>item.load()));
        if(id!==generation)return;
        for(const r of batch)if(!unique.has(r.url))unique.set(r.url,r);
      }
      const rows=[...unique.values()],last=Math.max(1,Math.ceil(rows.length/20)),current=Math.min(p,last);
      if(current!==p)history.replaceState(null,'',searchURL(q,kind,current));
      summary.textContent=rows.length?rows.length+' Ergebnisse · '+labels[kind]:'Keine Ergebnisse. Versuche einen anderen Begriff oder den Bereich „Alles“.';
      rows.slice((current-1)*20,current*20).forEach(r=>{const li=node('li'),h=node('h2'),a=node('a',r.title);a.href=r.url;h.append(a);li.append(h,node('span',labels[r.kind]||r.kind,'sw-result-kind'));if(r.excerpt){const decoded=new DOMParser().parseFromString(r.excerpt,'text/html').body.textContent;li.append(node('p',decoded));}output.append(li);});
      if(last>1){for(const [label,number] of [['Zurück',current-1],['Weiter',current+1]]){const b=node('button',label);b.type='button';b.disabled=number<1||number>last;b.addEventListener('click',()=>{history.pushState(null,'',searchURL(q,kind,number));render();});pager.append(b);}pager.append(node('span','Seite '+current+' von '+last));}
    }catch(e){if(id===generation)summary.textContent='Die Suche konnte nicht geladen werden. Versuche es erneut. Über Themen A–Z kannst du weiterhin Artikel öffnen.';}
  }
  form.addEventListener('submit',e=>{e.preventDefault();history.pushState(null,'',searchURL(qfield.value.trim(),filter.value));render();});
  filter.addEventListener('change',()=>form.requestSubmit());
  addEventListener('popstate',render);render();
})();
