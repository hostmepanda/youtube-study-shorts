import json, subprocess, os, sys, yaml
HERE=os.path.expanduser('~/qwen-edit-lab/ep2'); os.chdir(HERE)
tag=sys.argv[1]
T=json.load(open('vo_tl.json')); D=3.5; X=0.5; OUTRO=5.0
audio_end=T[-1]['endSeconds']; total=D+audio_end+OUTRO
col={'pip':'{\\c&HFFB85B&}','hoot':'{\\c&H32C8FF&}','baker':'{\\c&HFFFFFF&}','tag':'{\\c&HFFFFFF&}'}
srcs=['anim/S1.mp4','anim/S2.mp4','anim/S3.mp4','anim/S4.mp4','anim/S5.mp4','kb_S6.mp4','anim/S7.mp4','kb_S8.mp4']
n=len(srcs)
first={};last={}
for k,t in enumerate(T): first.setdefault(t['shot'],k); last[t['shot']]=k
b=[0]+[D+(T[last[s-1]]['endSeconds']+T[first[s]]['startSeconds'])/2 for s in range(1,n)]+[total+0.3]
segs=[]
for i,src in enumerate(srcs):
    d=b[i+1]-b[i]+(X if i<n-1 else 0); out=f'seg_{i}.mp4'
    vf='scale=704:1280,fps=25,format=yuv420p'
    if src.startswith('anim'): vf+=',split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1:a=0,tpad=stop_mode=clone:stop_duration=8'
    else: vf+=',tpad=stop_mode=clone:stop_duration=8'
    vf+=f',trim=duration={d:.3f},setpts=PTS-STARTPTS'
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',src,'-vf',vf,'-an','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',out],check=True)
    print(i,src,round(b[i],2),round(d,2))
ins=[];f='';prev='0:v'
for i in range(n): ins+=['-i',f'seg_{i}.mp4']
for i in range(1,n):
    f+=f'[{prev}][{i}:v]xfade=transition=fade:duration={X}:offset={b[i]-X/2:.3f}[x{i}];'; prev=f'x{i}'
subprocess.run(['ffmpeg','-y','-loglevel','error']+ins+['-filter_complex',f.rstrip(';'),'-map',f'[{prev}]','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',f'bg_{tag}.mp4'],check=True)
OD=f'/Users/panda/Development/private/wooden-roll/output/audio/ep2_{tag}'; os.makedirs(OD,exist_ok=True)
subprocess.run(['cp','vo_full.wav',OD+'/full_audio.wav'],check=True)
tl=[{'index':i,'phrase':col[t['speaker']]+t['phrase'],'startSeconds':t['startSeconds'],'endSeconds':t['endSeconds']} for i,t in enumerate(T)]
json.dump(tl,open(OD+'/timeline.json','w'),indent=1,ensure_ascii=False)
y=yaml.safe_load(open(os.path.expanduser('~/qwen-edit-lab/spain/spain_v6.yaml')))
a=y['steps'][0]; v=y['steps'][1]
a.update({'outDir':OD,'skipIfExists':True,'text':'x'})
v['backgroundVideo']=f'{HERE}/bg_{tag}.mp4'; v['output']=f'{HERE}/ep2_{tag}.mp4'; v['audioDir']=OD
v['hookText']="Hoot pulled the baker's leg."
yaml.safe_dump({'steps':[a,v],'youtube':{}},open(f'ep2_{tag}.yaml','w'),allow_unicode=True,sort_keys=False)
