import numpy as np, subprocess, json, re
from lines import LINES
SR=24000; GAP=0.6; TARGET=-20.0
def load(p): return np.frombuffer(subprocess.check_output(['ffmpeg','-loglevel','error','-i',p,'-ac','1','-ar',str(SR),'-f','f32le','-']),dtype=np.float32)
def trim(x,th=0.002,pad=0.12):
    idx=np.where(np.abs(x)>th)[0]; p=int(pad*SR); return x[max(idx[0]-p,0):idx[-1]+p]
def lufs(x):
    r=subprocess.run(['ffmpeg','-nostats','-f','f32le','-ar',str(SR),'-ac','1','-i','-','-af','ebur128','-f','null','-'],input=x.tobytes(),capture_output=True)
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS',r.stderr.decode())[-1])
def norm(x):
    y=x*10**((TARGET-lufs(x))/20); pk=np.abs(y).max(); return y*0.95/pk if pk>0.95 else y
CUT={"h2":0.95,"h4":1.04,"h6":0.38,"p7":1.26}  # felix leaks the tail of its reference ("...hint of derision"): drop it
HOLD=2.0  # keep the last card on screen after the voice ends
parts=[];tl=[];t=0.0
for sh,i,sp,v,l,s,txt,disp in LINES:
    x=load(f"vo/{i}.wav"); x=x[int(CUT.get(i,0)*SR):]; x=trim(x); y=norm(x); d=len(y)/SR
    tl.append({"index":len(tl),"shot":sh,"speaker":sp,"phrase":disp,"startSeconds":round(t,4),"endSeconds":round(t+d,4)})
    print(i,round(lufs(x),1),round(d,2)); parts+=[y,np.zeros(int(GAP*SR),dtype=np.float32)]; t+=d+GAP
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','f32le','-ar',str(SR),'-ac','1','-i','-','vo_full.wav'],input=np.concatenate(parts[:-1]+[np.zeros(int(HOLD*SR),dtype=np.float32)]).astype(np.float32).tobytes(),check=True)
tl[-1]["endSeconds"]=round(tl[-1]["endSeconds"]+HOLD,4)
json.dump(tl,open("vo_tl.json","w"),indent=1,ensure_ascii=False); print("total",round(t-GAP,2))
