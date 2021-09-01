class Count_buffer():

    def __init__(self):
        """计数缓冲区的属性"""
        self.items = []  # 缓存值items=[flag,x,y,p, flag2,x2,y2,p2, ...]
        self.location_cell = []  # location_cell位置序列    last_ymin上一帧的最小值    increment细胞运动的增量
        self.last_ymin = 1000  # count_majorcell输出的细胞数
        self.increment = 30
        self.count_majorcell = 0

    def push(self, items):
        """缓存区增添数据"""
        self.items = items[:]

    def sort(self):
        """位置序列排序"""
        for n in range(0, len(self.items), 4):
            self.location_cell.append(self.items[n + 2])
        self.location_cell.sort()

    def process(self, increment):
        """计数处理，若位置序列为空，不增加计数；若位置序列不为空，则逐个跟最小值比较"""
        if len(self.location_cell) == 0:
            self.last_ymin = 1000
            self.increment = increment
            self.count_majorcell += 0
            return (self.count_majorcell)

        else:
            self.increment = increment
            num_increment = 0
            for n in range(0, len(self.location_cell)):
                if self.location_cell[n] < self.last_ymin + self.increment:
                    num_increment += 1
                else:
                    break
            self.last_ymin = self.location_cell[0]
            self.count_majorcell += num_increment
            while self.location_cell:
                self.location_cell.pop()
            return (self.count_majorcell)


