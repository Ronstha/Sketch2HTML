import numpy as np
import cv2
import imutils
import imagesize
import os
import random
import json
levels=[
    {
        'paragraph':np.array([193,188,192]),
        'text':np.array([255,255,255]),
        'button':np.array([19,247,47]),
        'navlink':np.array([255,0,0]),
        'carousel':np.array([255,165,0]),
        'table':np.array([165,42,42]),
        'input':np.array([255,159,252]),
        'image':np.array([0,0,255]),
    },
    {
     "header":np.array([0,255,255]),
     "footer":np.array([154,128,235]),
     "card":np.array([0,128,128]),
    }
]



def insertElement(elm,sketch,sketchpath):
    key=list(elm.keys())[0]
    x, y, w, h = elm[key]
    imagepath=getBestFitImage(key,(x,y,w,h),sketchpath)
    elementImage = cv2.imread(imagepath, cv2.IMREAD_UNCHANGED)
    iw,ih,ch=elementImage.shape
    interp = cv2.INTER_CUBIC
    if w*h < iw*ih:
            interp = cv2.INTER_AREA
    if elm == 'img':
            if (ih > iw and h-y < w-x):
                elementImage = imutils.rotate_bound(elementImage, 90)
            elif (ih < iw and h-y > w-x):
                elementImage = imutils.rotate_bound(elementImage, -90)
    resizedElement = cv2.resize(elementImage , (w, h), interpolation = interp)
    for i in range(resizedElement.shape[0]):
            for j in range(resizedElement.shape[1]):
                if resizedElement[i][j][3] > 0:
                    try:
                        sketch[y+i][x+j] = resizedElement[i][j]
                    except:
                        pass
with open('assets/sketchinfo.json','r') as f:
    sketchinfo=json.load(f)

def getBestFitImage(key,rect,sketchpath):
    sketchpath=os.path.join(sketchpath,key)
    difference=[]
    x,y,w,h=rect
    aspect=w/h
    # for i in os.listdir(sketchpath):
    #     impath=os.path.join(sketchpath,i)
    #     iw,ih=imagesize.get(impath)
    #     imageAspect=iw/ih
    #     difference.append([abs(imageAspect-aspect),impath])
    for i in sketchinfo[key]:
  
        imageAspect=i['w']/i['h']
        difference.append([abs(imageAspect-aspect),i['file']])
    difference.sort(key=lambda x:x[0])
    limit=min(len(difference),5)
    return random.choice(difference[:limit])[1]

def generate_sketch(imagepath,sketchpath,savepath):
    im=cv2.imread(imagepath)
    image=cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
    objects=[]
    for level in levels:
        objects.append([])
        for elm in level.keys():
            color=level[elm]
            maskedImage = cv2.inRange(image, color, color)
     
            contours= cv2.findContours(maskedImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours=imutils.grab_contours(contours)

            for contour in contours:
              
                x, y, w, h =cv2.boundingRect(contour)
                objects[-1].append({elm: [x, y, w,h]})
    sketch= np.full((image.shape[0], image.shape[1], 4), np.array([255,255,255,255]), dtype=np.uint8)
    for level in objects:
        for elm in level:
            
            insertElement(elm,sketch,sketchpath)
    cv2.imwrite(savepath,sketch)
if __name__=='__main__':
   
    generate_sketch('1.png')

