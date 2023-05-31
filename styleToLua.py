import re
import math
from dataclasses import dataclass
@dataclass
class KeyFrame:
    #Class for keeping track of keyframes
    percent = list
    path = list
    display = str
    color = [200,200,200]


def ripFloats(str):
    #use a regex to find all floats in string
    return [float(x) for x in re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?",str)]



with open('style.css') as f:
    lines = f.readlines()
count = 0
indexs = []
index = 0
keyframes = {}
for line in lines:
    index=index+1
    if line.startswith('@keyframes'):
        indexs.append(index)
        count=count+1


keyframe = 0
count = 0
keyframes = []
print(indexs[-2:])
for indx in indexs:
    print(indx)
    keyframes.append([])
    i = indx
    while  i<len(lines) and not(lines[i].startswith('@keyframes')):
        ck = True
        if lines[i].startswith('    0% {') or lines[i].startswith('    0.00%, 0.00% {'):
            Kf = KeyFrame()
            Kf.percent = [0]
            ck=False
        if lines[i].startswith('        } '):
            keyframes[count].append(Kf)
            Kf = KeyFrame()
            Kf.color = [200,200,200]
            Kf.percent = ripFloats(lines[i])
            #print(Kf.percent)
            ck=False
        if lines[i].startswith('        display:'):
            Kf.display = lines[i][17:]
            #print(Kf.display)
            ck=False
        if lines[i].startswith('        clip-path: polygon('):
            LongPath = [math.floor(x*1.28) for x in ripFloats(lines[i])]
            ShortPath = []
            for x in range(0,len(LongPath)-2,2):
                if LongPath[x]!=LongPath[x+2] or LongPath[x+1]!=LongPath[x+3]:
                    ShortPath.append(LongPath[x])
                    ShortPath.append(LongPath[x+1])
            Kf.path = ShortPath    
            ck=False
        if lines[i].startswith('        background-color:'):
            Kf.color = ripFloats(lines[i])
            ck=False
        if ck:        
            keyframes[count].append(Kf)
            if Kf.percent[-1]!=100:
                print("Panic")
            ck=False
        i+=1
    keyframes[count]=keyframes[count][:-1]
    count+=1
count=0
LASTFRAME = 6572

print('\n START OF RENDERING \n')
print(len(keyframes))
with open("frameData.bin","wb") as file:
    for frame in range(math.floor(LASTFRAME)):
        time = frame/LASTFRAME*100
        print(time)
        for object in keyframes:
            #find keyframe in object that relates to time:
            closestFrame = object[0]
            i = 1
            while closestFrame.percent[0] < time:
                closestFrame = object[i]
                i+=1
            if closestFrame.path != [0,0] and closestFrame.color[0]>=200:
                x = 0
                path=[]    
                file.write(bytes(closestFrame.path))
                file.write(bytes([254])) # end of polygon
        file.write(bytes([255])) # end of frame
