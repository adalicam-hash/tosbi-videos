import json, subprocess, numpy as np, soundfile as sf, espeakng_loader
from phonemizer.backend.espeak.wrapper import EspeakWrapper
EspeakWrapper.set_library(espeakng_loader.get_library_path()); EspeakWrapper.set_data_path(espeakng_loader.get_data_path())
from phonemizer.backend import EspeakBackend
from kokoro_onnx import Kokoro
tr=EspeakBackend("tr",preserve_punctuation=True,with_stress=True)
k=Kokoro("/home/claude/models/kokoro-v1.0.int8.onnx","/home/claude/models/voices-v1.0.bin")
V="af_heart"
lines={"01":[("tr","Merhaba arkadaşlar! Ben Tosbi!")],"02":[("tr","Bugün kabuğumda ne var acaba?")],
"03":[("tr","Hadi tıklatalım!"),("en","Knock, knock!")],"04":[("tr","Kırmızı bir top!"),("en","Red!")],
"05":[("tr","Sarı!"),("en","Yellow!")],"06":[("tr","Mavi!"),("en","Blue!")],"07":[("tr","Hadi İngilizce sayalım!")],
"08":[("en","One!")],"09":[("en","Two!")],"10":[("en","Three!")],"11":[("tr","Üç top!"),("en","Three balls!")],
"12":[("tr","Hoşça kalın!"),("en","Bye-bye!")]}
SR=24000; info={}
def trim(s):
    a=np.where(np.abs(s)>0.01)[0]; return s[max(0,a[0]-240):a[-1]+480] if len(a) else s
for key,parts in lines.items():
    segs=[]; en_off=None; cur=0
    for lang,t in parts:
        if lang=="tr": s,_=k.create(tr.phonemize([t])[0].strip().replace("ɫ","l"),voice=V,speed=0.9,is_phonemes=True)
        else: s,_=k.create(t,voice=V,speed=0.92,lang="en-us")
        s=trim(np.asarray(s))
        if lang=="en" and en_off is None: en_off=cur
        segs.append(s); gap=np.zeros(int(0.18*SR)); segs.append(gap); cur+=len(s)+len(gap)
    y=np.concatenate(segs[:-1]); sf.write(f"audio/trk_raw_{key}.wav",y,SR)
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",f"audio/trk_raw_{key}.wav","-af",f"asetrate={SR}*1.16,aresample=44100,atempo=0.95",f"audio/trk_{key}.wav"],check=True)
    f=1/(1.16*0.95)  # time scale after processing
    d=len(y)/SR*f
    info[key]={"dur":round(d,3),"en_off":None if en_off is None else round(en_off/SR*f,3)}
json.dump(info,open("trk_info.json","w"),indent=0); print(info)
