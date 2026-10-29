import numpy as np
import mlx.core as mx
from mlx_audio.tts.models.kokoro.pipeline import KokoroPipeline
from mlx_audio.tts.utils import load_model
from mlx_audio.audio_io import write
from lines import LINES
M="mlx-community/Kokoro-82M-bf16"; SR=24000
SEG={"b1":[("a","This baguette? Made from moonlight. Very rare.")],
"b3":[("f","Ma jambe?"),("a","Your leg? Like this?")],
"b5":[("a","Ah! In French, we say,"),("f","vous me faites marcher."),("a","You make me walk.")],
"b6":[("a","Ha ha, close enough, my friend!")],
"b7":[("a","Yes, free baguette. Now walk!")],
"c8":[("f","Vous me faites marcher."),("a","It means, you're pulling my leg.")]}
model=load_model(model_path=M); pipes={}
def P(l):
    if l not in pipes: pipes[l]=KokoroPipeline(lang_code=l,model=model,repo_id=M)
    return pipes[l]
for sh,i,sp,v,l,s,txt,_ in LINES:
    if not l or i!='c8': continue
    out=[]
    for lg,t in SEG[i]:
        res=[r for r in P(lg)(t,voice=v,speed=s,split_pattern=r'\n') if r.audio is not None]
        out+=[np.concatenate([np.array(mx.flatten(r.audio)) for r in res]),np.zeros(int(0.25*SR),dtype=np.float32)]
    a=np.concatenate(out[:-1]); write(f"vo/{i}.wav",a,SR,format="wav"); print(i,len(a)/SR,flush=True)
print("K_DONE")
