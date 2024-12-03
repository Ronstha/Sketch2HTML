import imagesize
import os
data={}
for typ in os.listdir('assets/sketch'):
    data[typ]=[]  
    for sketch in os.listdir(f'assets/sketch/{typ}'):
        iw,ih=imagesize.get(f'assets/sketch/{typ}/{sketch}')        
        data[typ].append({'file':f'assets/sketch/{typ}/{sketch}','w':iw,'h':ih})
import json
with open('assets/sketchinfo.json','w') as f:
    json.dump(data,f)