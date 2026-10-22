"""Isolated regression fixtures; called by the canonical test runner."""
import argparse
import json
import tempfile
from datetime import date
from pathlib import Path
from unittest.mock import patch
from reader_health import bridge_lifecycle, rendered_links, snapshot_health
import agent_mail
from reader_catalog import activity_html


def run_checks():
    card = activity_html([{'date':'2026-09-12','title':'Einstieg','summary':'Lesen','articles':['Siebenwind_Wiki/index.md']}])
    assert 'href="Siebenwind_Wiki/"' in card and '/index/' not in card
    with tempfile.TemporaryDirectory(prefix='7w_reader_contract_') as tmp:
        root=Path(tmp)
        empty_snapshot = snapshot_health(root)
        assert empty_snapshot == {
            'status':'UNKNOWN','measured_at':None,'age_days':None,
            'scope':'no full Pages validation available',
            'unresolved_total':None,'unallowlisted_total':None,
            'deployment_verified':False,
        }
        wiki=root/'docs/Siebenwind_Wiki'; wiki.mkdir(parents=True)
        config=root/'.agent/config'; config.mkdir(parents=True)
        bridge=wiki/'Alias.md'
        bridge.write_text('---\nbridge_mode: temporary\nbridge_target: Ziel\nbridge_review_until: 2026-06-30\n---\n# Alias\n')
        baseline=config/'bridge_lifecycle_baseline.json'
        baseline.write_text(json.dumps({'expired':{'docs/Siebenwind_Wiki/Alias.md':'2026-06-30'}}))
        assert bridge_lifecycle(root,date(2026,9,9))['status']=='WARN'
        baseline.write_text('{"expired":{}}')
        assert bridge_lifecycle(root,date(2026,9,9))['status']=='FAIL'
        baseline.write_text(json.dumps({'expired':{'docs/Siebenwind_Wiki/Alias.md':'2026-06-30'}}))
        bridge.write_text(bridge.read_text().replace('2026-06-30','2027-06-30'))
        assert bridge_lifecycle(root,date(2026,9,9))['status']=='FAIL'
        bridge.unlink()
        assert bridge_lifecycle(root,date(2026,9,9))['status']=='PASS'
        site=root/'site';site.mkdir()
        (site/'index.html').write_text('<a class="card" href="architecture.md">Technik</a>')
        assert rendered_links(site,'https://example.org/wiki/')['status']=='FAIL'
        (site/'index.html').write_text('<a href="other/#ziel">Ziel</a>')
        (site/'other').mkdir();(site/'other/index.html').write_text('<h1 id="ziel">Ziel</h1>')
        assert rendered_links(site,'https://example.org/wiki/')['status']=='PASS'
        # Source filenames may contain literal query punctuation and umlauts.
        (site/'Frage? ä').mkdir()
        (site/'Frage? ä/index.html').write_text('<a href="../other/#ziel">Ziel</a>')
        (site/'index.html').write_text('<a href="Frage%3F%20%C3%A4/">Frage</a>')
        assert rendered_links(site,'https://example.org/wiki/')['status']=='PASS'
        meta={'id':'MSG-2026-9999','status':'OPEN','kind':'TASK','subject':'Test','report_path':'report.md'}
        roundtrip,_=agent_mail.parse_frontmatter(agent_mail.render_frontmatter(meta,'\n# Test\n'))
        assert roundtrip['kind']=='TASK' and roundtrip['report_path']=='report.md'
        saved={}
        def mutate(message_id,updater):
            saved['body']=updater(meta,'\n# Test\n');return 0
        with patch.object(agent_mail,'_mutate_status',mutate):
            agent_mail.cmd_classify(argparse.Namespace(id=meta['id'],kind='INFO',agent='Technician',note='Nachweis: fixture'))
        assert meta['kind']=='INFO' and meta['status']=='DONE' and 'Nachweis: fixture' in saved['body']
    return 'PASS: missing clean-checkout snapshot, baseline ratchet, retirement, HTML card/fragment targets, dispatch metadata and evidenced classification'
