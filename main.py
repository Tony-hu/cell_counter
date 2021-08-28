import os
from count import Count
from flow import Flow
from draw_bbox import draw
#1 输入分类网络的数据地址
#adress_read = input("请输入分类网络的数据地址：\n")
#img_adress = input("请输入图片地址：\n")
adress_read = 'D:/poct_video/0708/pic_5_output/TXT1'
img_adress = 'D:/poct_video/0708/pic_5'
files = os.listdir(adress_read)
files.sort(key=lambda x:int(x[:-4]))
num =0
for n in range(len(adress_read)-1,0,-1):
    if adress_read[n]== "/":
        num=n
        break
adress = adress_read[0:num+1]   #adress_read的上一级目录
print("TXT的目录: ",adress)
adress_count = str(adress) + 'count.txt'
adress_flow  = str(adress) + 'flowsequence.txt'
txt_count = open(adress_count,'a')
txt_flow = open(adress_flow,'a')
frame = 0
count_buffer = Count()
flow_buffer = Flow()

for file in files:
#2 读取数据，生成一维列表frame_info. 该列表每四个数字代表一个细胞 [x,y,w,h, x2,y2,w2,h2 ...]
    frame += 1
    if frame >100:
        break
    print("\n",file)
    txt_read = str(adress_read) + "/" + file
    txt = open(txt_read, 'r',encoding='utf-8')
    frame_info = txt.read()
    frame_info = frame_info.split()
    frame_info = list(map(int,frame_info)) #生成的一维列表

#3 若前一帧不存在目标细胞，跳过匹配的过程。数据处理流程为 push(), update(), pop(), draw(),
    if len(flow_buffer.last)== 0 :
        flow_buffer.push(frame_info)
        print_info = []  #输出一帧图像中所有细胞的位置
        for n in range(0,len(flow_buffer.info),4):
            print_info.append(flow_buffer.info[n])
            print_info.append(flow_buffer.info[n+1])
            print_info.append("/")
        if len(print_info) != 0:
            print("所有细胞的位置：",print_info)
        flow_buffer.update()
        flow_buffer.pop()
        if len(flow_buffer.last) != 0: #0-400内至少含有四个细胞，才能找到一个目标细胞。
            last_box = flow_buffer.last[0]
            print("上一帧没有目标细胞 ,有:" ,last_box)
            draw(img_adress, frame, 1, last_box)
        else:
            print("上一帧没有目标细胞， 没有。")
 #4：前一帧已经存在目标细胞，执行匹配的过程，并更新这一帧的目标细胞。数据处理流程为 push(), process(), update(), pop(), draw()
    else:
        flow_buffer.push(frame_info)
        print_info = []  # 输出一帧图像中所有细胞的位置
        for n in range(0, len(flow_buffer.info), 4):
            print_info.append(flow_buffer.info[n])
            print_info.append(flow_buffer.info[n + 1])
            print_info.append("/")
        if len(print_info) != 0:
            print("所有细胞的位置：",print_info)
        this_box = flow_buffer.process()
        flow_buffer.update() #注意：执行完update() 之后，目标细胞已经更新了
        flow_buffer.pop()

        if len(flow_buffer.last) != 0 and len(this_box) !=0: #输出两个细胞
            last_box = flow_buffer.last[0]
            draw(img_adress, frame,0, last_box, this_box)
            print("上一帧有目标细胞， 有， 有:", this_box, "  " ,last_box)
            print("last_box:", last_box)
        if len(this_box) != 0 and len(flow_buffer.last) == 0: #输出一个细胞
            draw(img_adress, frame,2, this_box)
            print("上一帧有目标细胞， 有， 没有",this_box)
        if len(this_box) == 0 and len(flow_buffer.last) != 0:  #输出一个细胞
            draw(img_adress, frame,1, last_box)


