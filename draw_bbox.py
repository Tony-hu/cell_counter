import cv2 as cv
def draw(imgadress,frame,num,*boxs):
    #画图函数，将目标细胞和追踪细胞分别用矩形框圈起来， num==0,1,2  0表示两个细胞，1表示目标细胞，2表示追踪细胞
    outputadress = 'D:/poct_video/0708' + "/output/" + str(frame) + ".jpg"
    imgadress = imgadress + "/" + str(frame) + ".jpg"
    img = cv.imread(imgadress)
    color_red = (0,0,255)       #红色
    color_green = (0,255,0)     #绿色
    thickness = 1
    lineType = 4
    for box in boxs:
        leftbox = (box[0] - box[2] // 2, box[1] - box[3] // 2)
        rightbottom = (box[0] + box[2] // 2, box[1] + box[3] // 2)
        cv.rectangle(img,leftbox,rightbottom,color_red,thickness,lineType)
    cv.imwrite(outputadress,img)


