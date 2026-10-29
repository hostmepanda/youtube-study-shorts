import os,json,requests,time
from dotenv import load_dotenv
load_dotenv("/Users/panda/Development/private/youtube-study-shorts/.env")
B="https://core.premiss.ru/api/v2"; H={"Authorization":"Bearer "+os.environ["PREMISS_API_KEY"]}
D=os.path.expanduser("~/qwen-edit-lab"); O=D+"/ep2"
SC="exactly one Eiffel Tower (a single tower) in the distance, a small Paris street bakery stand with a wooden counter, a green striped awning and a basket of baguettes, cobblestones, and the Eiffel Tower clearly visible in the distance behind, soft morning light"
NO="Feathered wings only, absolutely no hands, no fingers, no dark gloves. No other animals: no extra owls, no chickens, no doves, no extra pigeons. There are no humans anywhere in the image, no human body parts, no human hands or fingers, birds have wings only. The only living creatures are birds."
HERO="The owl keeps its brown speckled plumage and yellow eyes exactly as in image 1; the pigeon keeps its grey plumage with green-purple neck exactly as in image 2."
RULE="Exactly three birds: the owl (image 1), the pigeon (image 2) and the rooster (image 3). Only the rooster wears a white apron; the owl and the pigeon wear nothing. Both the owl and the pigeon are small and stand ON TOP of the wooden counter in the foreground; the rooster stands behind the counter. "+HERO
def run(t,files):
    r=requests.post(B+"/tasks",headers=H,data={"task":json.dumps(t)},files=[("file",(os.path.basename(f),open(f,"rb"),"image/png")) for f in files],timeout=120)
    if r.status_code>=300:
        print("POST fail",r.status_code,r.text[:300],flush=True); time.sleep(60); return run(t,files)
    i=r.json()["data"]["id"]; t0=time.time()
    while time.time()-t0<1800:
        try: d=requests.get(f"{B}/tasks/{i}",headers=H,timeout=30).json()["data"]
        except Exception: time.sleep(10); continue
        if d["status"] in("completed","failed"): return d,round(time.time()-t0)
        time.sleep(8)
def go(name,p,files,seed):
    t={"steps":[{"name":"image-edit","options":{"prompt":p,"resolution":"704x1280","seed":seed}}]}
    d,s=run(t,files); u=(d.get("output") or {}).get("image_edit_url")
    print(name,d["status"],s,d.get("error"),flush=True)
    if u: open(f"{O}/{name}.png","wb").write(requests.get(u,timeout=60).content)
pg=D+"/data/pigeon.png"; ow=D+"/data/owl.png"; R=O+"/v2_generic/R1.png"
ON=" Both birds stand on the flat top surface of a wide wooden bakery counter that fills the bottom of the frame; all feet touch the wood; the pigeon keeps its wings folded against its body; nobody is flying or jumping. Two separate birds, each with its own body and two legs. Exactly two birds, no other animals, no rooster, no chicken."
SC2="a small Paris street bakery stand behind them with a green striped awning and a basket of baguettes, exactly one Eiffel Tower in the distance, cobblestones, soft morning light"
shots=[
("J4",[ow,pg],"The small owl from image 1, brown speckled plumage and yellow eyes, stands on the counter looking down at its own feet, flustered, wings slightly raised. The pigeon from image 2, grey plumage with green-purple neck, stands next to the owl on the counter and tilts its head, mischievously looking at the owl's feet."+ON+" "+SC2+". "+NO),
("J7",[ow,pg],"The pigeon from image 2, grey plumage with green-purple neck, walks proudly along the counter with its chest out, a baguette lies on the counter beside it. The small owl from image 1, brown speckled plumage and yellow eyes, stands on the counter watching the pigeon with a small amused smile."+ON+" "+SC2+". "+NO),
]
for name,files,p in shots:
    for sd in (101,102,103,104): go(f"{name}_s{sd}",p,files,sd)
print("FRAMES_DONE",flush=True)
