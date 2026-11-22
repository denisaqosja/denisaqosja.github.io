"""Generate a public CV from the same verified content used by the website."""
import json
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=json.loads((ROOT/'content/profile.json').read_text())
pubs=json.loads((ROOT/'content/publications.json').read_text())
def tex(text):
    changes={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}','–':'--','—':'---','’':"'"}
    return ''.join(changes.get(c,c) for c in text)
def section(title):return r'\section*{'+tex(title)+'}\n'
def entry(date,title,institution,description):
    return r'\noindent{\small\color{accent}'+tex(date)+r'}\par\nobreak'+ '\n' + r'\textbf{'+tex(title)+r'}\par\nobreak'+ '\n'+tex(institution)+r'\par\nobreak'+ '\n'+(r'{\small '+tex(description)+r'}\par' if description else '')+r'\vspace{9pt}'+'\n'
body=r'''\documentclass[10pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage[margin=21mm]{geometry}
\usepackage{xcolor}
\usepackage{titlesec}
\usepackage{enumitem}
\usepackage{hyperref}
\definecolor{accent}{HTML}{164D77}
\hypersetup{colorlinks=true,urlcolor=accent,pdftitle={Denisa Qosja - Curriculum Vitae},pdfauthor={Denisa Qosja}}
\titleformat{\section}{\large\color{accent}}{}{0pt}{}[\titlerule]
\titlespacing*{\section}{0pt}{14pt}{10pt}
\setlength{\parindent}{0pt}
\setlength{\parskip}{4pt}
\renewcommand{\baselinestretch}{1.09}
\begin{document}
{\Huge\color{accent} Denisa Qosja}\par
{\large Research Scientist | Machine Learning \& Radar}\par
\href{mailto:denisaqosja97@gmail.com}{denisaqosja97@gmail.com} \quad
\href{https://github.com/denisaqosja}{github.com/denisaqosja}\par
\href{https://orcid.org/0000-0003-3083-8253}{ORCID: 0000-0003-3083-8253}\par
\vspace{8pt}
'''
body+=tex(p['intro'])+'\n'+section('Experience')
for x in p['experience']:body+=entry(x['dates'],x['role'],x['institution']+' | '+x['location'],x['description'])
body+=section('Education')
for x in p['education']:body+=entry(x['dates'],x['degree'],x['institution'],x['description'])
body+=r'\newpage'+'\n'+section('Publications')
for x in pubs:
    body+=r'\textbf{'+tex(x['title'])+r'}\par\nobreak'+'\n'+tex(', '.join(x['authors']))+r'\par\nobreak'+'\n'+tex(x['venue']+' ('+str(x['year'])+').')+r'\par\nobreak'+'\n'+r'{\small\href{https://doi.org/'+x['doi']+'}{doi:'+tex(x['doi'])+r'}}\par\vspace{9pt}'+'\n'
body+=section('Selected projects')
for title,desc,url in [
    ('Complex-valued neural networks','PyTorch implementation of real- and complex-valued U-Net architectures for radar map reconstruction.','ComplexValuedNN'),
    ('Sentinel-2 semantic segmentation','Adapting DINOv3 and SegFormer for land-cover mapping with DFC2020 and SEN12MS.','Sentinel_SEN12MS_Segmentation'),
    ('Radar signal processing','Configurable, end-to-end pulse radar simulation, from chirp generation to range-Doppler processing.','RadarSignalProcessing')]:
    body+=r'\textbf{\href{https://github.com/denisaqosja/'+url+'}{'+tex(title)+r'}}\par\nobreak'+'\n'+tex(desc)+r'\par\vspace{7pt}'+'\n'
body+=section('Technical skills')
for label,skills in p['skills'].items():body+=r'\textbf{'+tex(label)+':} '+tex(skills)+r'\par'+'\n'
body+=section('Languages')+tex(p['languages'])+r'\vfill'+'\n'+r'{\footnotesize Updated November 2026.}'+ '\n'+r'\end{document}'
tmp=ROOT/'tmp'/'cv';tmp.mkdir(parents=True,exist_ok=True)
(tmp/'Denisa-Qosja-CV.tex').write_text(body)
for _ in range(2):
    result=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory',str(tmp),str(tmp/'Denisa-Qosja-CV.tex')],capture_output=True,text=True)
    if result.returncode:raise SystemExit(result.stdout[-4000:])
import shutil
shutil.copyfile(tmp/'Denisa-Qosja-CV.pdf',ROOT/'assets/Denisa-Qosja-CV.pdf')
print('Generated public CV: assets/Denisa-Qosja-CV.pdf')
