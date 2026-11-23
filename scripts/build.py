#!/usr/bin/env python3
"""Build the complete, dependency-free GitHub Pages site from editable JSON."""
import html
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
OUT.mkdir(exist_ok=True)
def read(name):
    return json.loads((ROOT / 'content' / (name + '.json')).read_text())
p, pubs, projects = read('profile'), read('publications'), read('projects')
def e(s):
    return html.escape(str(s), quote=True)
def link(url, label, cls='', new_tab=False):
    attributes = ' target="_blank" rel="noopener noreferrer"' if new_tab else ''
    hint = '<span class="sr-only"> (opens in a new tab)</span>' if new_tab else ''
    return f'<a class="{cls}" href="{e(url)}"{attributes}>{e(label)}{hint}</a>'
def asset_version(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()[:12]
def profile_icon(url, label, new_tab=False):
    filenames = {'Email': 'email', 'LinkedIn': 'linkedin', 'GitHub': 'github', 'Google Scholar': 'scholar', 'CV': 'cv'}
    path = 'assets/icons/' + filenames[label] + '.svg'
    hint = ' (PDF, opens in a new tab)' if label == 'CV' else ''
    attributes = ' target="_blank" rel="noopener noreferrer"' if new_tab else ''
    return f'<a class="profile-resource" href="{e(url)}" aria-label="{e(label + hint)}" title="{e(label + hint)}"{attributes}><img src="{path}?v={asset_version(path)}" width="24" height="24" alt="" aria-hidden="true"></a>'
def tags(items):
    return '<ul class="tags">' + ''.join(f'<li>{e(x)}</li>' for x in items) + '</ul>'
def heading(kicker, title, intro=''):
    return f'<header class="page-heading"><p class="eyebrow">{kicker}</p><h1>{title}</h1>' + (f'<p class="lede">{intro}</p>' if intro else '') + '</header>'
def author_list(items):
    return ', '.join(f'<strong>{e(x)}</strong>' if x == p['name'] else e(x) for x in items)
def pub_row(x, compact=False):
    detail = '' if compact else f'''<details class="abstract"><summary>Abstract <span aria-hidden="true">+</span></summary><p>{e(x['abstract'])}</p><p class="small">Summary of the published abstract and paper. {link(x['url'], 'Read the original publication')}.</p></details>
    <details class="citation"><summary>BibTeX</summary><pre id="bib-{x['id']}">{e(x['bibtex'])}</pre><button type="button" class="text-button copy-citation" data-copy="bib-{x['id']}">Copy citation</button></details>'''
    pdf = link(x['pdf'], 'PDF', 'resource-link') if x.get('pdf') else ''
    return f'''<article class="publication" id="{x['id']}" data-search="{e((x['title']+' '+x['topic']+' '+str(x['year'])).lower())}">
      <a class="pub-image" href="publications.html#{x['id']}" aria-label="Details for {e(x['title'])}"><img src="assets/{x['image']}" alt="{e(x['alt'])}" width="640" height="400" loading="lazy"></a>
      <div class="pub-content"><p class="overline">{x['year']} <span>·</span> {e(x['topic'])}</p><h3>{link(x['url'], x['title'])}</h3>
      <p class="authors">{author_list(x['authors'])}</p><p class="venue">{e(x['venue'])}</p>
      {f'<p class="small">{e(x["note"])}</p>' if x.get('note') else ''}
      <p class="pub-summary">{e(x['summary'])}</p><div class="resource-links">{link(x['url'], 'Paper', 'resource-link')}{pdf}{link('https://doi.org/'+x['doi'], 'DOI', 'resource-link')}{link('assets/citations/'+x['id']+'.bib', 'Citation', 'resource-link')}</div>{detail}</div></article>'''
def timeline(items, education=False):
    return '<div class="timeline">' + ''.join(f'''<article class="timeline-entry"><p class="dates">{e(x['dates'])}</p><div><h3>{e(x['degree'] if education else x['role'])}</h3><p class="institution">{e(x['institution'])}</p><p class="small">{e(x['location'])}</p>{f'<p>{e(x["description"])}</p>' if x['description'] else ''}</div></article>''' for x in items) + '</div>'
def render(file, title, content):
    navigation = [
        ('index.html#about', 'About', 'index.html'),
        ('index.html#research', 'Research', None),
        ('publications.html', 'Publications', 'publications.html'),
        ('cv.html#experience', 'Experience', 'cv.html'),
        ('projects.html', 'Projects', 'projects.html'),
        ('cv.html#skills', 'Skills', None),
        ('index.html#contact', 'Contact', None),
    ]
    nav = ''.join(f'<a href="{href}"'+(' aria-current="page"' if current == file else '')+f'>{label}</a>' for href,label,current in navigation)
    nav += link('assets/Denisa-Qosja-CV.pdf', 'CV', new_tab=True)
    description = 'Denisa Qosja — machine learning for radar and remote sensing. Research, publications, projects, education, and CV.'
    (OUT/file).write_text(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{description}"><meta name="theme-color" content="#163f62"><meta property="og:title" content="{e(title)} | Denisa Qosja"><meta property="og:description" content="{description}"><meta property="og:type" content="website">
<title>{e(title)} | Denisa Qosja</title><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/styles.css?v={asset_version('web/styles.css')}"><script src="assets/main.js?v={asset_version('web/main.js')}" defer></script></head>
<body><a class="skip-link" href="#main">Skip to content</a><header class="site-header"><div class="header-inner"><a class="brand" href="index.html" aria-label="Denisa Qosja home">DQ<span>.</span></a><button class="nav-toggle" type="button" aria-controls="main-navigation" aria-expanded="false"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"/></svg><span>Menu</span></button><nav id="main-navigation" class="site-nav" aria-label="Main navigation">{nav}</nav></div></header>
<main id="main" class="container">{content}</main>
<footer class="site-footer container"><span>© 2026 Denisa Qosja</span><div>{link(p['scholar'],'Google Scholar')}{link(p['github'],'GitHub')}{link(p['orcid'],'ORCID')}</div><span>Updated November 2026</span></footer><p class="sr-only" id="announcement" role="status" aria-live="polite"></p></body></html>''')

home = f'''<section id="about" class="profile" aria-labelledby="name"><div class="profile-heading"><p class="eyebrow">About me</p><h1 id="name">{e(p['name'])}</h1><p class="profile-role">{e(p['headline'])}<span aria-hidden="true"> · </span>{link('https://www.fhr.fraunhofer.de/en.html',p['affiliation'])}</p></div><img class="profile-photo" src="assets/denisa-qosja.jpg" alt="Portrait of Denisa Qosja" width="640" height="720" fetchpriority="high"><div class="profile-bio">{''.join('<p>'+e(paragraph)+'</p>' for paragraph in p['about'])}</div><div id="research" class="profile-keywords" aria-label="Research keywords">{tags(p['interests'])}</div><div class="profile-meta"><nav class="profile-resources" aria-label="Profile links">{profile_icon('mailto:'+p['email'],'Email')}{profile_icon(p['scholar'],'Google Scholar',new_tab=True)}{profile_icon(p['github'],'GitHub',new_tab=True)}{profile_icon(p['linkedin'],'LinkedIn',new_tab=True)}{profile_icon('assets/Denisa-Qosja-CV.pdf','CV',new_tab=True)}</nav></div></section>
<section class="section"><div class="section-title"><div><p class="eyebrow">Research</p><h2 id="publications">Publications</h2></div>{link('publications.html','Abstracts & citations','section-link')}</div>{''.join(pub_row(x,True) for x in pubs)}</section>
<section class="section"><div class="section-title"><div><p class="eyebrow">From research to code</p><h2>Open-source projects</h2></div>{link('projects.html','Explore projects','section-link')}</div><div class="project-index">{''.join(f'<a href="projects.html#{x["id"]}"><h3>{e(x["title"])}</h3><p>{e(x["subtitle"])}</p><span>View project</span></a>' for x in projects)}</div></section>
<section class="section background-section"><div><h2>Background</h2><p>I joined Fraunhofer FHR in 2022 after completing my master’s at FAU Erlangen-Nürnberg. My earlier work at Fraunhofer IIS explored synthetic visual data, depth estimation, and image coding.</p>{link('cv.html','Education & experience','section-link')}</div><div id="contact" class="contact-note"><h2>Get in touch</h2><p>For research discussions and collaboration:</p>{link('mailto:'+p['email'],p['email'])}<p class="small">{link(p['linkedin'],'LinkedIn')} · {link(p['orcid'],'ORCID')}</p></div></section>'''
render('index.html',p['headline'],home)

publications = heading('Research','Publications','Research on learning from radar signals, generating SAR imagery, and recognising targets.') + f'''<div class="publication-tools"><a href="{p['scholar']}" class="section-link">Google Scholar profile</a><a href="assets/publications.bib" class="section-link" download>Download bibliography</a><label class="search-label" for="paper-search"><span>Filter publications</span><input id="paper-search" type="search" placeholder="Title, topic, or year…" aria-controls="publication-list"></label></div><p class="result-count" id="result-count" role="status">4 publications</p><div id="publication-list">{''.join(pub_row(x) for x in pubs)}</div><p id="no-results" hidden>No publications match your search. Try a title, topic, or year.</p><aside class="source-note">Abstracts are concise summaries written for this website. Paper links lead to the original publications. Method diagrams are illustrative; the SAR generation chart uses values reported in the paper.</aside>'''
render('publications.html','Publications',publications)

project_content = heading('Selected code & experiments','Projects','A closer look at the methods, data, and code behind my work.')
project_content += '<nav class="project-jumps" aria-label="Projects">'+''.join(link('#'+x['id'],x['title']) for x in projects)+'</nav>'
for x in projects:
    related = ''
    if x.get('related'):
        paper = next(y for y in pubs if y['id'] == x['related'])
        related = f'<p class="related"><strong>Related research:</strong> {link("publications.html#"+paper["id"],paper["title"])}.</p>'
    interactive = '''<div class="demo"><div class="demo-heading"><h3>Explore a Doppler response</h3><span>Interactive illustration</span></div><p>Change a point target’s radial velocity to see its Doppler peak shift.</p><label for="velocity">Radial velocity <output id="velocity-value" for="velocity">3.0 m/s</output></label><input id="velocity" type="range" min="-10" max="10" value="3" step="0.1"><svg id="doppler-demo" viewBox="0 0 760 240" role="img" aria-labelledby="demo-title demo-desc"><title id="demo-title">Illustrative Doppler response</title><desc id="demo-desc">A point target peak plotted against velocity, from minus ten to ten metres per second.</desc><g id="demo-grid"></g><path id="demo-path" fill="none" stroke="#187c81" stroke-width="3"/><text x="380" y="233" text-anchor="middle">Radial velocity (m/s)</text></svg><p class="small">Analytical, normalized sinc-squared response for a single point target, shown as an interactive concept illustration.</p><noscript><p>Enable JavaScript to use the velocity slider.</p></noscript></div>''' if x.get('interactive') else ''
    project_content += f'''<article id="{x['id']}" class="project-detail"><div class="project-heading"><p class="eyebrow">{e(x['subtitle'])}</p><h2>{e(x['title'])}</h2>{tags(x['tags'])}</div><div class="project-body"><div><h3>Abstract</h3><p>{e(x['abstract'])}</p><h3 class="subheading">What’s inside</h3><ul class="feature-list">{''.join('<li>'+e(d)+'</li>' for d in x['details'])}</ul><div class="resource-links">{link(x['repo'],'View repository','button')}{link(x['results'],'Reconstruction visualizations','resource-link') if x.get('results') else ''}</div></div><figure class="project-figure"><a href="assets/{x['image']}" aria-label="Open full-size visualization: {e(x['title'])}"><img src="assets/{x['image']}" alt="{e(x['alt'])}" width="840" height="520" loading="lazy"></a><figcaption>{e(x['caption'])}</figcaption></figure></div>{related}{interactive}</article>'''
render('projects.html','Projects',project_content)

cv = heading('Background & experience','Curriculum vitae','My path through signal processing, machine learning, and radar research.') + f'''<div class="cv-preview"><div><h2>CV at a glance</h2><p>Experience, education, selected publications, and technical skills.</p></div>{link('assets/Denisa-Qosja-CV.pdf','View CV (PDF)','button',new_tab=True)}</div><section id="experience" class="section"><h2>Experience</h2>{timeline(p['experience'])}</section><section id="education" class="section"><h2>Education</h2>{timeline(p['education'],True)}</section><section id="skills" class="section"><h2>Technical skills</h2><dl class="skills">{''.join(f'<dt>{e(k)}</dt><dd>{e(v)}</dd>' for k,v in p['skills'].items())}</dl></section><section class="section"><h2>Publications</h2><p>Explore the complete publication list, paper links, and downloadable citations.</p>{link('publications.html','View publications','section-link')}</section>'''
render('cv.html','Curriculum vitae',cv)
shutil.copytree(ROOT/'assets',OUT/'assets',dirs_exist_ok=True)
shutil.copytree(ROOT/'web',OUT/'assets',dirs_exist_ok=True)
(OUT/'.nojekyll').touch()
(OUT/'assets'/'citations').mkdir(exist_ok=True)
for x in pubs:
    (OUT/'assets'/'citations'/(x['id']+'.bib')).write_text(x['bibtex']+'\n')
(OUT/'assets'/'publications.bib').write_text('\n\n'.join(x['bibtex'] for x in pubs)+'\n')
print('Built 4 pages in '+str(OUT))
