"""Regenerate original site figures. Requires matplotlib (only for this optional step)."""
import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/denisa-portfolio-matplotlib')
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT=Path(__file__).resolve().parents[1]/'assets'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
navy,teal,muted='#164d77','#177b80','#566575'
fig,ax=plt.subplots(figsize=(8.4,5.2),layout='constrained')
labels=['cDCGAN','cSAGAN','cWGAN','cDDPM','cDDPM\n+ pretraining']
values=[3.60,2.46,1.59,.38,.23]
y=np.arange(5)
ax.barh(y,values,color=['#b5c6d2']*3+[navy,teal],height=.56)
ax.set_yticks(y,labels);ax.invert_yaxis();ax.set_xlim(0,4.2)
for i,v in enumerate(values): ax.text(v+.08,i,f'{v:.2f}',va='center',color=navy,fontweight='bold')
ax.set_xlabel('Fréchet Inception Distance (lower is better)',labelpad=12)
ax.set_title('Conditional SAR image generation',loc='left',fontsize=17,color=navy,pad=22)
ax.grid(axis='x',color='#e7edf1');ax.set_axisbelow(True);ax.tick_params(length=0,pad=9)
for spine in ax.spines.values():spine.set_visible(False)
fig.text(.01,-.03,'MSTAR evaluation · Qosja et al., RadarConf 2024 · Tables I & II',fontsize=10,color=muted)
fig.savefig(OUT/'sar-fid.svg',bbox_inches='tight',metadata={'Date':None});plt.close(fig)

fig,axes=plt.subplots(1,2,figsize=(8.4,5.2),layout='constrained',sharey=True)
x=np.linspace(-3,3,500)
for ax,sigma,title in zip(axes,[.85,.22],['Unresolved response','Separated peaks']):
    z=np.exp(-((x-.55)/sigma)**2)+np.exp(-((x+.55)/sigma)**2)
    z/=z.max()
    ax.fill_between(x,z,alpha=.10,color=teal);ax.plot(x,z,color=teal,linewidth=2.5)
    ax.set_title(title,fontsize=13,color=navy,pad=16);ax.set_xlabel('Doppler (illustrative units)')
    ax.set_xticks([-2,0,2]);ax.set_ylim(0,1.15);ax.grid(color='#edf1f4')
axes[0].set_ylabel('Normalized response')
fig.suptitle('Resolving closely spaced targets',fontsize=18,color=navy)
fig.supxlabel('Concept illustration · not measured data or model output',fontsize=10,color=muted)
fig.savefig(OUT/'doppler.svg',metadata={'Date':None});plt.close(fig)

def diagram(name,title,stages,subtitle):
    fig,ax=plt.subplots(figsize=(8.4,5.2));ax.set_xlim(0,10);ax.set_ylim(0,6.2);ax.axis('off')
    ax.text(.05,5.7,title,color=navy,fontsize=19,fontweight='medium')
    n=len(stages); gap=.25;w=(9.8-gap*(n-1))/n
    for i,(label,detail) in enumerate(stages):
        px=.05+i*(w+gap)
        ax.add_patch(FancyBboxPatch((px,2.5),w,1.5,boxstyle='round,pad=0.02,rounding_size=.08',fc='#edf4f7',ec='#bbceda',lw=1))
        ax.text(px+w/2,3.4,label,ha='center',va='center',fontsize=11,color=navy,fontweight='bold')
        ax.text(px+w/2,2.9,detail,ha='center',va='center',fontsize=9,color=muted)
        if i<n-1:ax.annotate('',xy=(px+w+gap-.025,3.25),xytext=(px+w+.025,3.25),arrowprops={'arrowstyle':'->','color':teal,'lw':1.5})
    ax.text(.05,1.25,subtitle,color=muted,fontsize=11,linespacing=1.8)
    ax.text(.05,.4,'Conceptual method overview',color=teal,fontsize=10)
    fig.savefig(OUT/name,bbox_inches='tight',metadata={'Date':None});plt.close(fig)
diagram('complex-network.svg','Complex-valued reconstruction',[
    ('Complex input','real + imaginary'),('Complex U-Net','encoder / decoder'),('Reconstruction','magnitude + phase')],
    'Preserve the signal’s amplitude and phase structure.\nCompare complex-valued and real-valued architectures.')
diagram('radar-pipeline.svg','From waveform to range–Doppler map',[
    ('Waveform','chirp pulses'),('Transmit','TX chain'),('Channel','propagation'),('Receive','RX chain'),('Process','range / Doppler')],
    'Modular pulse-radar simulation in PyTorch.\nSystem and scenario parameters are configured in YAML.')
diagram('detection.svg','Learning the radar background',[
    ('Observation','radar profile'),('Autoencoder','background model'),('Residual','target evidence')],
    'Train on the background of a fixed scene.\nCompare the observation with its reconstructed background.')
diagram('classification.svg','Recognising targets in SAR imagery',[
    ('SAR images','three datasets'),('CNN backbone','ConvNeXt / baselines'),('Classification','target category')],
    'Compare recognition architectures and data augmentation.\nEvaluate how visual learning methods transfer to radar.')
print('Generated six original research visualizations.')
