import os,json,requests,time
from dotenv import load_dotenv
load_dotenv("/Users/panda/Development/private/youtube-study-shorts/.env")
from lines import LINES
B="https://core.premiss.ru/api/v2"; H={"Authorization":"Bearer "+os.environ["PREMISS_API_KEY"]}
for sh,i,sp,v,l,sp_,txt,_ in LINES:
    if l: continue
    out=f"vo/{i}.wav"
    if os.path.exists(out): continue
    t={"steps":[{"name":"text-to-speech","options":{"voiceName":v,"speed":sp_,"phrase_gap":0.0}}],"input":txt}
    r=requests.post(B+"/tasks",headers={**H,"Content-Type":"application/json"},json=t,timeout=60)
    if r.status_code>=300: print(i,"POST fail",r.status_code,r.text[:200],flush=True); continue
    tid=r.json()["data"]["id"]; t0=time.time()
    while time.time()-t0<600:
        try: d=requests.get(f"{B}/tasks/{tid}",headers=H,timeout=30).json()["data"]
        except Exception: time.sleep(5); continue
        if d["status"] in("completed","failed"): break
        time.sleep(4)
    u=(d.get("output") or {}).get("tts_audio_url")
    print(i,d["status"],round(time.time()-t0),flush=True)
    if u: open(out,"wb").write(requests.get(u,timeout=60).content)
print("PM_DONE",flush=True)
