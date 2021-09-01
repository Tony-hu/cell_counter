class Flow_buffer():
    def __init__(self):
        self.items = []  # 缓存值
        self.pre_num = 0  # 上一帧与这一帧的细胞数目
        self.rig_num = 0
        self.pre_vector = [0, 0]  # 前一帧的流速信息,位置平均值

    def push(self, item):
        """将数据信息转换为self.item = [[ymin xmin], [ymin,xmin], [...] ]"""
        ymax = -1
        xmax = 0
        frame_info = []
        for num in range(0, len(item), 4):
            if item[num + 2] > ymax:
                ymax = item[num + 2]
                xmax = item[num + 1]
        frame_info = [ymax, xmax]
        self.items.append(frame_info[:])

    def run(self, item):
        """根据输入数据，分析出处理的流程，并调用process() , push()"""
        output = []
        self.rig_num = len(item) / 4
        if self.rig_num == self.pre_num and self.rig_num != 0:
            self.push(item)
            return (self.pre_vector[:])

        if self.rig_num == self.pre_num and self.rig_num == 0:
            return (self.pre_vector[:])

        if self.rig_num != self.pre_num and self.rig_num != 0:
            self.process()
            self.push(item)
            self.pre_num = self.rig_num
            return (self.pre_vector[:])

        if self.rig_num != self.pre_num and self.rig_num == 0:
            self.process()
            self.pre_num = 0
            return (self.pre_vector[:])

    def process(self):
        add = 0
        y_add = []
        x_sum = 0
        x_average = 0
        sum1 = 0
        if len(self.items) == 1:
            self.items.pop()  # 缓存值只有一个,清空缓存 ,不更改pre_vector
        else:
            for n in range(0, len(self.items) - 1):
                add = self.items[n + 1][0] - self.items[n][0]
                if add > 0:
                    y_add.append(add)

        if len(y_add) == 0:  # 缓存值多于一个,没有位移增加的情况,清空缓存，不更改pre_vector
            while self.items:
                self.items.pop()
        else:  # 缓存值多于一个,包含位移增加的情况,清空缓存，更改pre_vector
            for n in range(0, len(self.items)):
                x_sum = self.items[n][1]
            x_average = x_sum // len(self.items)
            v_average = sum(y_add) // len(y_add) * 30
            self.pre_vector[0] = v_average
            self.pre_vector[1] = x_average
            while self.items:
                self.items.pop()


class Sequence():
    def __init__(self):
        self.items = []
        self.sum_900 = 0
        self.average = 0

    def calculate(self, num, frame):
        if frame < 901:  # 0~900只存储数据
            self.items.append(num)
            self.sum_900 = self.sum_900 + num
            return (num)
        else:  # 计算平均值
            self.sum_900 = self.sum_900 - self.items[0] + num
            self.average = self.sum_900 / 900
            self.items.pop(0)
            self.items.append(num)
            return (self.average)














