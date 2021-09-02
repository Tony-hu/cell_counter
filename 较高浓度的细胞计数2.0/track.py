from frame import Frame
class Track():
    """1、生成细胞的路径 2、终止细胞的路径"""
    def __init__(self):
        self.velocity = []
        self.locate = []
        self.active = False

    def gennerate(self,frame_num):
        """生成路径： 1、选取最顶端的细胞  2、与下一帧图像做匹配  """
        start = Frame(frame_num)
        if len(start.info) == 0:
            print(str(frame_num), "： 生成路径失败。")
        elif start.info[1] > 400:
            print(str(frame_num),"： 生成路径失败。")
        else:                   #0~400内含有细胞，则可以产生新的路径
            target = []
            target.append(start.info[0:4])
            target.append(start.abstract(0))
            print("target: ", target)
            next = Frame(frame_num+1)
            next.dessign_last(target)
            match_num = next.match()
            if match_num == -1:
                print("目标已建立，匹配失败")
            else:
                self.velocity.append(next.info[match_num+1] - start.info[1])
                self.locate = next.info[match_num:match_num+4]
                self.active = True
            print("next.info: ",next.info)
            print("match_num: ",match_num)
            print("track: ",self.locate,self.velocity,self.active)  #给track配置 第二帧的位置

    def predict(self,frame):
        """根据细胞的运动速度，预测下一帧的位置。若能在下一帧找到该细胞，则预测成功。"""
        next = Frame(frame+1)
        print("next_3:" ,next.info)
        candi = []
        for n in range(0,len(next.info),4):
            if next.info[n+1]<self.locate[1]+self.velocity[-1]*6//5 and next.info[n+1]>self.locate[1]+ self.velocity[-1]*4//5 and next.info[n]<self.locate[0]+self.locate[2]//2 and next.info[n]>self.locate[0]-self.locate[2]//2:
                candi.append(n)
                candi.append(next.info[n+1]-self.locate[1]-self.velocity[-1])       #实际距离与目标距离差值
        print("candi",candi)
        if len(candi)==0:
            self.active=False
            while len(self.velocity)!=0:
                self.velocity.pop()
            print(str(frame+1),": 细胞超出边界")
            self.active = False
            return False
        if len(candi)==2:
            self.velocity.append(next.info[candi[0]+1]-self.locate[1])
            self.locate= next.info[candi[0]:candi[0]+4]
            print("track: ", self.locate, self.velocity, self.active)
            return True
        if len(candi)>2:
            change = 50
            num=-1
            for n in range(0,len(candi),2):
                if  abs(candi[n+1]) < change:
                    num = candi[n]
                    change = abs(candi[n+1])
            self.velocity.append(next.info[num+1]-self.locate[1])
            self.locate = next.info[num:num+4]
            print("track: ", self.locate, self.velocity, self.active)
            return True







