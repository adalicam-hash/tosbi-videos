import numpy as np, soundfile as sf
from render import LINES, KNOCKS, BALLS, COUNT, DUR
SR=44100
mix=np.zeros(int(DUR*SR)+SR)
def add(sig,t,g=1.0):
    i=int(t*SR); mix[i:i+len(sig)]+=sig[:len(mix)-i]*g
# voice (pitch-shifted copies made by ffmpeg)
for k,t in LINES.items():
    v,sr=sf.read(f"audio/{'p' if __import__('render').TL=='en' else 'ptr'}_{k}.wav"); 
    if v.ndim>1: v=v.mean(1)
    add(v,t,1.0)
# music: soft plucked I-V-vi-IV in C, 100 bpm
def pluck(f,d=0.6):
    n=int(d*SR); t=np.arange(n)/SR
    return (np.sin(2*np.pi*f*t)+0.3*np.sin(4*np.pi*f*t)+0.1*np.sin(6*np.pi*f*t))*np.exp(-t*5)
chords=[[261.6,329.6,392.0],[196.0,246.9,293.7],[220.0,261.6,329.6],[174.6,220.0,261.6]]
beat=60/100
mel=[523.3,659.3,784.0,659.3, 587.3,493.9,587.3,784.0, 523.3,659.3,523.3,440.0, 523.3,440.0,349.2,440.0]
t=0.0;b=0
while t<DUR-0.6:
    ch=chords[(b//4)%4]
    add(pluck(ch[0]/2,1.2),t,0.05)
    for j,f in enumerate(ch): add(pluck(f,0.5),t+beat*0.5+0.02*j,0.025)
    add(pluck(mel[b%16],0.4),t,0.03)
    t+=beat;b+=1
# sfx
def knock():
    n=int(0.12*SR);t=np.arange(n)/SR
    return np.sin(2*np.pi*140*t)*np.exp(-t*40)+0.3*np.random.randn(n)*np.exp(-t*80)
def pop():
    n=int(0.25*SR);t=np.arange(n)/SR
    f=300+1500*t/0.25
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*12)
def boing():
    n=int(0.4*SR);t=np.arange(n)/SR
    f=220+120*np.sin(2*np.pi*8*t)*np.exp(-t*4)+200*t
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*7)
for k in KNOCKS: add(knock(),k,0.5)
for tp,_,_ in BALLS: add(pop(),tp,0.3); add(boing(),tp+0.7,0.15)
for c in COUNT: add(boing(),c,0.2)
fade=int(0.5*SR); mix[int((DUR-0.5)*SR):int(DUR*SR)]*=np.linspace(1,0,fade)
mix=mix[:int(DUR*SR)]
mix=mix/np.max(np.abs(mix))*0.89
import render; sf.write(f"audio/mix_{render.TL}.wav",mix,SR)
