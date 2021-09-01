import os
from track import Track
from frame import Frame
#基于二分图匹配的细胞追踪算法，每一帧都需要跟踪一个track，当判定细胞track超出观测区域时候，对本帧图像进行计数，并生成下一个track.
track = Track()
frame = 1
sum = 0   #细胞总数
while len(Frame(frame).info)==0:   #从有细胞的图像开始计数
    frame += 1
frame_0 = Frame(frame)
while frame <= 300:
    print("/nframe: ",frame)
    if track.active == False:            #没有跟踪到细胞，
        track.gennerate(frame)
        num = 0
        for n in range(0,len(Frame(frame).info),4):
            if Frame(frame).info[n+1] < 400:
               num += 1
        sum += num
        frame += 1
    elif track.active == True:
        if (track.predict(frame)) == False:
            num = 0
            for n in range(0,len(Frame(frame).info),4):
                if Frame(frame).info[n+1] < track.locate[1]:
                    num += 1
            sum += num
            track.gennerate(frame)
        else:
            print("predict： ",frame+1,track.locate)
        frame += 1
    print("sum: ",sum)

