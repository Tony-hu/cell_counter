import numpy as np
from scipy.optimize import linear_sum_assignment
class Flow():
    """输入前后帧的信息，得出细胞流速的参数"""
    def __init__(self):
        self.info = []
        self.last = []             #self.last = [[x,y,w,h][c11,c12,c21,c22,c31,c32...]]


    def push(self,info1):
        """info= [x,y,w,h, x,y,w,h]  ,将一帧数据进行排序，并存储"""
        info = []
        for n in range(0,len(info1),5):
            info.extend(info1[n+1:n+5])
        n = len(info)
        for i in range(0,n-4,4):
            for j in range(i+4,n,4):
                if info[i+1] > info[j+1]:
                    info[i],info[i+1],info[i+2],info[i+3],info[j],info[j+1],info[j+2],info[j+3] =info[j],info[j+1],info[j+2],info[j+3],info[i],info[i+1],info[i+2],info[i+3]
        self.info = info[:]
    def select(self):
        """找到候选细胞的索引"""
        candi_index = []
        for n in range(0,len(self.info),4):
            value = self.iou(self.info[n]-self.info[n+2]//2,self.info[n]+self.info[n+2]//2)
            if value >0.5:
                candi_index.append(n)
        return candi_index

    def iou(self,x1,x2):
        """计算两个细胞横坐标的交并比"""
        x_items = []
        x_items.append(self.last[0][0]-self.last[0][2]//2)
        x_items.append(self.last[0][0]+self.last[0][2]//2)
        x_items.append(x1)
        x_items.append(x2)
        x_items.sort()
        value_iou = (x_items[2]-x_items[1])/(x_items[3]-x_items[0])
        return value_iou

    def abstract(self,index):
        """"提取细胞的拓扑信息"""
        topo = []
        flag = 1
        for n in range(0,len(self.info),4):
            if self.info[n+1] > self.info[index+1]-self.last[0][1] and self.info[n+1] < self.info[index+1]+400-self.last[0][1]:
                if self.info[n] <self.info[index]-self.info[index+2]//2:
                    x = -5
                if self.info[n] >= self.info[index] - self.info[index+2] // 2 and self.info[n] <= self.info[index] + self.info[index+2]//2:
                    x = 0
                if self.info[n] > self.info[index] + self.info[index+2]//2:
                    x = 5
                y = (self.info[n+1] - self.info[index+1])//20
                if x==0 and y==0 and flag==1:
                    flag += 1
                else:
                    topo.append(x)
                    topo.append(y)
        return topo

    def match(self,topo):
        """目标细胞与候选的细胞进行匹配"""
        #步骤一：建立代价矩阵  步骤二：枚举出全匹配的代价值 步骤三：找到最小的代价
        n1 = len(self.last[1])//2
        n2 = len(topo)//2
        if n1>n2:
            n1,n2 = n2,n1
        if n1 == 0:               #候选细胞没有拓扑信息的时候，不进行匹配
            print("周围没有细胞")
            return 100
        cost_matrix = [[0 for i in range(n2)]for j in range(n1)]        #n1*n3的二维列表
        for i in range(n1):
            for j in range(n2):
                if len(self.last[1])//2 == n1:
                    cost_matrix[i][j] = abs(self.last[1][i*2]-topo[j*2]) + abs(self.last[1][i*2+1]-topo[j*2+1])
                else:
                    cost_matrix[i][j] = abs(self.last[1][j*2]-topo[i*2]) + abs(self.last[1][j*2+1]-topo[i*2+1])
        cost_matrix = np.array(cost_matrix)                            #调用KM算法
        row, col = linear_sum_assignment(cost_matrix)
        correlation = cost_matrix[row, col].sum()
        return correlation

    def update(self):
        """在纵坐标分布在0~200的细胞群中，选取位置最靠近中央的细胞"""
        #1清空目标细胞的信息  2选取位置最中央的细胞  3添加topo信息到last【1】
        while len(self.last)!=0:
            self.last.pop()
        index = -1
        sum_400 = 0
        for n in range(0,len(self.info),4):
            #if self.info[n+1] > 400 :
            #    index = n//4                 #0-400内的细胞个数
            #    break
            #else:
            #    sum_400 += 1
            if self.info[n+1] <=400 :
                index = n//4 + 1
                sum_400 += 1
            else:
                break
        if sum_400 <= 3:                      #sum_400 的设置为了控制0-400内的细胞个数，最少为4
            return 0
        index = int(index//2*4)
        print("index:",str(index))
        self.last.append(self.info[index:index+4])
        print("self.info[index:index+4]:",self.info[index:index+4])
        temp = []
        flag = 1
        for n in range(0,len(self.info),4):
            if self.info[n+1] > 400:
                break
            else:
                if self.info[n] < self.info[index] - self.info[index+2]//2:
                    x = -5
                if self.info[n] >= self.info[index] - self.info[index+2]//2 and self.info[n] <= self.info[index] + self.info[index+2]//2:
                    x = 0
                if self.info[n] > self.info[index] + self.info[index + 2] // 2:
                    x = 5
                y = (self.info[n+1] - self.info[index+1])//20
                if x==0 and y==0 and  flag==1:
                    flag += 1
                else:
                    temp.append(x)
                    temp.append(y)
        self.last.append(temp[:])
        print("update:")
        print(self.last)       #1111111111111111111111111111

    def pop(self):
        """清空数据缓存"""
        while len(self.info)!=0:
            self.info.pop()

    def process(self):
        """将每一个候选细胞分别与目标细胞进行匹配，再更新目标细胞信息"""
        candidate = []
        goal = 15                           #匹配的阈值必须大于0.70
        right_num = -1
        print("self.select():")
        candidate.extend(self.select())       #挑选出候选细胞

        candidate_print = []
        for n in range(len(candidate)):
            candidate_print.append(candidate[n]//4+1)
        print(candidate_print)

        for num in candidate:
            topo=self.abstract(num)           #提取候选细胞的topo信息，并与目标细胞进行匹配
            print("topo of candidate:")
            print(topo)
            correlation = self.match(topo)
            print("correlation:")
            print(correlation)
            if correlation < goal :
                right_num = num
                goal = correlation

        result = []
        if right_num != -1:
            result.extend(self.info[right_num:right_num+4])
        print("result: ",result)
        return(result)

