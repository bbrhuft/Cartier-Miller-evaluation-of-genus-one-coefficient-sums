import sys, random
from common import *
from c1_cech import frobenius_cech
random.seed(int(sys.argv[2]) if len(sys.argv)>2 else 1)
p=int(sys.argv[1]); nsamp=int(sys.argv[3]) if len(sys.argv)>3 else 40
models=all_models(p); random.shuffle(models); models=models[:nsamp]
ok=0; fails=[]
for A,B in models:
    c,M=frobenius_cech(p,A,B); H,beta=hasse_beta(p,A,B)
    if M==[[0,(-beta)%p],[0,H]]: ok+=1
    else: fails.append((A,B,M,H,beta))
line=f"p={p}: random sample of {len(models)} nonsingular models: M==[[0,-beta],[0,H]] {ok}/{len(models)}; fails={fails[:5]}"
print(line); open('c1_cech_results.txt','a').write(line+'\n')
