import os,json,requests,time
from dotenv import load_dotenv
load_dotenv("/Users/panda/Development/private/youtube-study-shorts/.env")
B="https://core.premiss.ru/api/v2"; H={"Authorization":"Bearer "+os.environ["PREMISS_API_KEY"]}
D=os.path.expanduser("~/qwen-edit-lab/ep2")
CAM=" The camera stays still."
jobs=[
("S1","The rooster behind the counter holds the baguette and speaks proudly, nodding its head slowly and moving its beak a little. It keeps its white apron."+CAM),
("S2","The owl on the counter speaks indignantly but calmly, opening its beak only slightly and lifting one wing a little, keeping it close to its body. The pigeon beside it blinks."+CAM),
("S3","The rooster leans slightly forward and tilts its head, looking down curiously at the owl's feet. The owl looks down at its own feet, surprised, blinking. Keep the white apron."+CAM),
("S4","The owl shifts nervously on the counter, wings slightly raised. The pigeon beside it tilts its head and watches the owl's feet, bobbing its head gently. Both stay standing on the counter."+CAM),
("S5","The rooster explains kindly, nodding slowly and moving its beak a little. The owl and the pigeon listen, blinking calmly. Keep the white apron on the rooster."+CAM),
("S7","The pigeon proudly shifts its weight and bobs its head, wings staying raised and steady. The owl watches with a small smile and blinks."+CAM),
]
for name,p in jobs:
    out=f"{D}/anim/{name}.mp4"
    if os.path.exists(out): continue
    t={"steps":[{"name":"text-to-video","options":{"prompt":p,"resolution":"704x1280","durationSeconds":4}}]}
    r=requests.post(B+"/tasks",headers=H,data={"task":json.dumps(t)},files={"file":(name+".png",open(f"{D}/final/{name}.png","rb"),"image/png")},timeout=120)
    print(name,r.status_code,flush=True)
    if r.status_code>=300: print(r.text[:200],flush=True); continue
    i=r.json()["data"]["id"]; t0=time.time()
    while time.time()-t0<3000:
        try: d=requests.get(f"{B}/tasks/{i}",headers=H,timeout=30).json()["data"]
        except Exception: time.sleep(10); continue
        if d["status"] in("completed","failed"): break
        time.sleep(15)
    u=(d.get("output") or {}).get("text_to_video_url")
    print(name,d["status"],round(time.time()-t0),d.get("error"),flush=True)
    if u: open(out,"wb").write(requests.get(u,timeout=120).content)
print("ANIM_DONE",flush=True)
