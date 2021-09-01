import os
from count_buffer import Count_buffer
from flow_buffer import Flow_buffer, Sequence

adress_read = input("请输入分类网络的数据地址：\n")  # 输入为TXT文件夹的地址
files = os.listdir(adress_read)
files.sort(key=lambda x: int(x[:-4]))  # files为TXT内txt文件的名称列表
num = 0
for n in range(len(adress_read) - 1, 0, -1):  # 写入的地址有 count.txt flowsequence.txt
    if adress_read[n] == "\\":
        num = n
        break
adress_write = adress_read[0:num + 1]
print(adress_write)
adress_count = str(adress_write) + 'count.txt'
adress_flow = str(adress_write) + 'flowsequence.txt'
txt_count = open(adress_count, 'a')
txt_flow = open(adress_flow, 'a')
buffer_count = Count_buffer()
buffer_flow = Flow_buffer()
sequence = Sequence()

count_output = 0
frame = 0
increment = 120

flow_output = [0, 0]
flow_average = 0

for file in files:
    frame += 1
    frame_info = []
    flow_average = sequence.calculate(flow_output[0], frame)  # 流速的计算值必须在0.5*flow_average~1.5*flow_average
    print(file)
    txt_read = str(adress_read) + "/" + file
    txt = open(txt_read, 'r')
    str_info = txt.read()
    str_info = str_info.split()
    for n in range(0, len(str_info), 4):
        frame_info.append(int(str_info[n]))
        frame_info.append(int(str_info[n + 1]))
        frame_info.append(int(str_info[n + 2]))
        frame_info.append(1)
    # print(frame_info)
    buffer_count.push(frame_info)
    buffer_count.sort()
    count_output = buffer_count.process(increment)
    count_word = str(frame) + ' ' + str(count_output) + "\n"
    txt_count.write(count_word)  # 写入数目信息

    flow_output = buffer_flow.run(frame_info)
    if flow_output[0] >= 0.5 * flow_average and flow_output[0] <= 1.5 * flow_average:
        flow_vector = flow_output[0]
    flow_word = str(frame) + ' ' + str(flow_vector) + ' ' + str(flow_output[1]) + '\n'
    txt_flow.write(flow_word)  # 写入流速信息
    txt.close()

txt_count.close()
txt_flow.close()

