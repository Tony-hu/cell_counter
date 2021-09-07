import numpy as np
from scipy.optimize import linear_sum_assignment
class Frame():
    """帧处理类，负责前后两帧的匹配"""
    def __init__(self,frame):
        self.info=[]
        self.push(frame)
        self.last = []                          #self.last = [[x,y,w,h],[topo矩阵]]

    def push(self,frame):
        """获取第frame帧数据，并按照y坐标从小到大排序"""
        adress = 'D:/poct_video/0826/TXT_0826_pic3'
        adress = adress + "/" + str(frame) + ".txt"
        txt = open(adress, "r", encoding="utf-8")
        # 生成的一维列表
        frame_info = txt.read()
        frame_info = frame_info.split()
        frame_info = list(map(int, frame_info))
        info = []
        for n in range(0, len(frame_info), 5):
            if frame_info[n]!=2 and frame_info[n+1]<200:
                info.extend(frame_info[n + 1:n + 5])
        n = len(info)
        # 将图像中的细胞位置，从小到大排序
        for i in range(0, n - 4, 4):
            for j in range(i + 4, n, 4):
                if info[i+1] > info[j+1]:
                    info[i], info[i + 1], info[i + 2], info[i + 3], info[j], info[j + 1], info[j + 2], info[j + 3] = \
                        info[j], info[j + 1], info[j + 2], info[j + 3], info[i], info[i + 1], info[i + 2], info[i + 3]
        self.info = info[:]

    def dessign_last(self,last):
        """输入目标细胞的位置信息，拓扑特征"""
        self.last = last[:]

    def get_info(self):
        """输出这一帧的细胞信息"""
        return self.info

    def select(self):
        """根据细胞的x坐标 和 IOU值，选取候选的细胞"""
        candi_index = []
        for n in range(0, len(self.info), 4):
            if self.info[n+1] > self.last[0][1]:
                value = self.iou(self.info[n] - self.info[n + 2] // 2, self.info[n] + self.info[n + 2] // 2)
                if value > 0.7:
                    candi_index.append(n)
        return candi_index

    def iou(self, x1, x2):
        """计算两个细胞横坐标的交并比"""
        if (x1>self.last[0][0] + self.last[0][2] // 2) or (x2<self.last[0][0] - self.last[0][2] // 2):
            return 0
        x_items = []
        x_items.append(self.last[0][0] - self.last[0][2] // 2)
        x_items.append(self.last[0][0] + self.last[0][2] // 2)
        x_items.append(x1)
        x_items.append(x2)
        x_items.sort()
        value_iou = (x_items[2] - x_items[1]) / (x_items[3] - x_items[0])
        return value_iou

    def abstract(self, index):
        """"提取细胞的topo信息，topo信息包含指定细胞与其它细胞的相对位置信息，并且需要从指定细胞下方的0~300区域内选取其它细胞"""
        topo = []
        flag = 1
        for n in range(0, len(self.info), 4):
            if self.info[n + 1] > self.info[index + 1]  and self.info[n + 1] < self.info[ index + 1] + 300 :
                if self.info[n] < self.info[index] - self.info[index + 2] // 2:
                    x = -5
                if self.info[n] >= self.info[index] - self.info[index + 2] // 2 and \
                        self.info[n] <= self.info[index] + self.info[index + 2] // 2:
                    x = 0
                if self.info[n] > self.info[index] + self.info[index + 2] // 2:
                    x = 5
                y = (self.info[n + 1] - self.info[index + 1]) // 20
                if x == 0 and y == 0 and flag == 1:
                    flag += 1
                else:
                    topo.append(x)
                    topo.append(y)
        return topo

    def match(self):
        """目标细胞与候选的多个细胞进行匹配"""
        candidate = []
        goal =20
        right_num = -1
        candidate.extend(self.select())
        if len(candidate)==1 :           #情况一：candi_index只有一个细胞时，则匹配成功
            return (candidate[0])
        elif len(candidate)==0 :         #情况二：没有细胞匹配时，返回-1
            return -1
        else:                           #情况三：candi——index有多个细胞时，利用KM算法筛选得分最高的细胞
            if len(self.last[1]) == 0:
                for num in candidate:
                    topo = self.abstract(num)  #提取候选细胞的topo信息，并与目标细胞进行匹配,topo可能为空
                    if len(topo) == 0:
                        return num
                return -1
            else:                        #topo不为空，则比较候选细胞的correlation，匹配值最小的细胞
                for num in candidate:
                    topo = self.abstract(num)
                    if len(topo) == 0:
                        correlation = 19
                    else:
                        n1 = len(self.last[1]) // 2
                        n2 = len(topo) // 2
                        if n1 > n2: n1, n2 = n2, n1
                        cost_matrix = [[0 for i in range(n2)] for j in range(n1)]  # n1*n3的二维列表
                        for i in range(n1):
                            for j in range(n2):
                                if len(self.last[1]) // 2 == n1:
                                    cost_matrix[i][j] = abs(self.last[1][i * 2] - topo[j * 2]) + abs(
                                        self.last[1][i * 2 + 1] - topo[j * 2 + 1])
                                else:
                                    cost_matrix[i][j] = abs(self.last[1][j * 2] - topo[i * 2]) + abs(
                                        self.last[1][j * 2 + 1] - topo[i * 2 + 1])
                        cost_matrix = np.array(cost_matrix)  # 调用KM算法
                        row, col = linear_sum_assignment(cost_matrix)
                        correlation = cost_matrix[row, col].sum() + (n2-n1)*2
                        print("num:",num,"topo:",topo,"correlation",correlation)
                        if correlation < goal :
                            goal = correlation
                            right_num = num
                return right_num #right_num=-1 匹配失败，否则匹配成功
