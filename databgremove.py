import cv2
import numpy as np
import os
import shutil
try:
    shutil.rmtree('assets/sketch')
except:
    pass
os.mkdir('assets/sketch')
data={}
for i in os.listdir('assets/raw_sketch'):
    data[i.strip()]=[]
    os.makedirs(f'assets/sketch/{i}',exist_ok=True)
    for img in os.listdir(f'assets/raw_sketch/{i}'):
       
        im=cv2.imread(f'assets/raw_sketch/{i}/{img}',cv2.IMREAD_GRAYSCALE)
        t,thresh=cv2.threshold(im,210,255,cv2.THRESH_BINARY_INV)
        coords=cv2.findNonZero(thresh)
        x, y, w, h = cv2.boundingRect(coords)
        thresh=thresh[y:y+h,x:x+w]
        thresh=np.invert(thresh)
        image_rgba = cv2.cvtColor(thresh, cv2.COLOR_RGB2RGBA)
        white_pixels = np.all(image_rgba[:, :, :3] == 255, axis=-1)
        image_rgba[white_pixels, 3] = 0
     
        path=f'assets/sketch/{i}/{img.split(".")[0]}.png'
        data[i.strip()].append({'key':i,'w':image_rgba.shape[0],'h':image_rgba.shape[1]})
        cv2.imwrite(path,image_rgba)