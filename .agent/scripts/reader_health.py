"""Shared, read-only health facts. Snapshot age is never a new measurement."""
import json
import re
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def rendered_links(site, site_url):
    """Check actual HTML hrefs, including cards, against files and fragment IDs."""
    from html.parser import HTMLParser
    from urllib.parse import urljoin, urlsplit, unquote, quote
    class Links(HTMLParser):
        def __init__(self):
            super().__init__(); self.hrefs=[]; self.ids=set()
        def handle_starttag(self, tag, attrs):
            attrs=dict(attrs)
            if attrs.get('id'): self.ids.add(attrs['id'])
            if tag=='a' and attrs.get('href'): self.hrefs.append(attrs['href'])
    parsed={}
    archive_pages=set()
    for file in site.rglob('*.html'):
        try:
            raw=file.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            raw=file.read_text(encoding='cp1252',errors='replace')
        parser=Links(); parser.feed(raw); parsed[file.resolve()]=parser
        if file.relative_to(site).parts[0] == 'Quellen' and 'data-sw-root=' not in raw:
            archive_pages.add(file.resolve())
    origin=urlsplit(site_url)
    missing=[] if parsed else [{'page':'index.html','href':'','reason':'missing_build'}]
    for file, parser in parsed.items():
        rel=file.relative_to(site.resolve()).as_posix()
        url=urljoin(site_url,quote(rel.removesuffix('index.html'),safe='/'))
        for href in set(parser.hrefs):
            dest=urlsplit(urljoin(url,href))
            if dest.scheme not in {'http','https'} or dest.netloc.casefold()!=origin.netloc.casefold(): continue
            if not dest.path.startswith(origin.path):
                missing.append({'page':rel,'href':href,'reason':'outside_publication_root'}); continue
            target=(site/unquote(dest.path[len(origin.path):])).resolve()
            if target.is_dir(): target=target/'index.html'
            if not target.is_file():
                missing.append({'page':rel,'href':href,'reason':'missing_file'})
            elif dest.fragment and target in parsed and unquote(dest.fragment) not in parsed[target].ids:
                missing.append({'page':rel,'href':href,'reason':'missing_fragment'})
    archive_names={p.relative_to(site.resolve()).as_posix() for p in archive_pages}
    archive_missing=[row for row in missing if row['page'] in archive_names]
    missing=[row for row in missing if row['page'] not in archive_names]
    return {'status':'FAIL' if missing else 'PASS','scope':'all generated HTML anchors, including navigation and cards; unmodified source HTML reported separately','pages':len(parsed)-len(archive_pages),'missing':missing,'archive_missing':archive_missing,'archive_pages':len(archive_pages)}


def bridge_lifecycle(root=ROOT, today=None):
    today = today or date.today()
    baseline_path = root / '.agent/config/bridge_lifecycle_baseline.json'
    baseline = json.loads(baseline_path.read_text(encoding='utf-8')).get('expired', {}) if baseline_path.exists() else {}
    expired, violations = [], []
    for path in sorted((root / 'docs/Siebenwind_Wiki').rglob('*.md')):
        raw = path.read_text(encoding='utf-8')
        if not raw.startswith('---\n'): continue
        front = raw.split('---', 2)[1]
        if not re.search(r'^bridge_(target|mode):', front, re.MULTILINE): continue
        match = re.search(r'^bridge_review_until:\s*([^\n]+)', front, re.MULTILINE)
        value = match.group(1).strip().strip('\"\'') if match else ''
        name = path.relative_to(root).as_posix()
        try:
            review = date.fromisoformat(value)
        except ValueError:
            violations.append({'path':name,'reason':'missing_or_invalid_date'}); continue
        if review < today:
            expired.append({'path':name,'review_until':value})
            if baseline.get(name) != value:
                violations.append({'path':name,'reason':'new_expired_bridge'})
        elif name in baseline:
            violations.append({'path':name,'reason':'legacy_deadline_extended_without_retirement'})
    return {'measured_at':today.isoformat(),'expired_total':len(expired),'expired':expired,'violations':violations,'status':'FAIL' if violations else 'WARN' if expired else 'PASS'}


def snapshot_health(root=ROOT):
    path = root / '.agent/data/pages_health.json'
    if not path.exists():
        return {'status':'UNKNOWN','measured_at':None,'age_days':None,
                'scope':'no full Pages validation available',
                'unresolved_total':None,'unallowlisted_total':None,
                'deployment_verified':False}
    data = json.loads(path.read_text(encoding='utf-8'))
    health = data.get('pages_health',data)
    measured = health.get('last_validated_at') or data.get('generated_at')
    try:
        age = max(0,(datetime.now(timezone.utc)-datetime.fromisoformat(measured.replace('Z','+00:00'))).days)
    except (TypeError,ValueError,AttributeError): age = None
    return {'status':health.get('status','UNKNOWN'),'measured_at':measured,'age_days':age,'scope':'last full local Pages validation', 'unresolved_total':health.get('unresolved_total'),'unallowlisted_total':health.get('unallowlisted_total'), 'deployment_verified':False}
