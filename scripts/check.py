"""Check generated page structure, local resources, and fragment destinations."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
import json
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist'
class Page(HTMLParser):
    def __init__(self,path):
        super().__init__(convert_charrefs=True)
        self.path=path;self.ids=set();self.links=[];self.h1=0;self.main=0
        self.feed(path.read_text())
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids,f'Duplicate ID {a["id"]} in {self.path.name}'
            self.ids.add(a['id'])
        if tag=='h1':self.h1+=1
        if tag=='main':self.main+=1
        if tag=='html':assert a.get('lang')=='en'
        if tag=='img':assert a.get('alt'),f'Missing image description: {self.path.name}'
        for attr in ['href','src']:
            if a.get(attr):self.links.append(a[attr])
pages={p.resolve():Page(p) for p in OUT.glob('*.html')}
assert len(pages)==4,'Expected four complete pages'
checked=0
for path,page in pages.items():
    assert page.h1==1 and page.main==1,f'Page landmark structure: {path.name}'
    for href in page.links:
        url=urlsplit(href)
        if url.scheme or url.netloc:continue
        assert not url.path.startswith('/'),'Links must support GitHub project subpaths'
        target=(path.parent/unquote(url.path)).resolve() if url.path else path
        assert target.is_relative_to(OUT.resolve()),'Link leaves deploy directory'
        assert target.is_file(),f'Broken local resource: {path.name}: {href}'
        if url.fragment and target in pages:
            assert unquote(url.fragment) in pages[target].ids,f'Broken fragment: {href}'
        checked+=1
for path in (OUT/'assets').glob('*.svg'):ET.parse(path)
pubs=json.loads((ROOT/'content/publications.json').read_text())
assert len({p['id'] for p in pubs})==len(pubs)
for p in pubs:
    assert (OUT/'assets/citations'/f'{p["id"]}.bib').read_text().strip()==p['bibtex']
assert (OUT/'assets/Denisa-Qosja-CV.pdf').read_bytes().startswith(b'%PDF-')
print(f'PASS: 4 pages; {checked} local links, anchors, and assets; SVGs, citations, and CV.')
