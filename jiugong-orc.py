import sys

from PIL import Image
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
import cv2
import numpy as np
import pyautogui
import cv2
from deal_img import orc, correctPos

template1 = cv2.imread('num_img/1.png', cv2.IMREAD_GRAYSCALE)
ret1, template1 = cv2.threshold(template1, 127, 255, cv2.THRESH_BINARY)
template2 = cv2.imread('num_img/2.png', cv2.IMREAD_GRAYSCALE)
ret2, template2 = cv2.threshold(template2, 127, 255, cv2.THRESH_BINARY)
template3 = cv2.imread('num_img/3.png', cv2.IMREAD_GRAYSCALE)
ret3, template3 = cv2.threshold(template3, 127, 255, cv2.THRESH_BINARY)
template4 = cv2.imread('num_img/4.png', cv2.IMREAD_GRAYSCALE)
ret4, template4 = cv2.threshold(template4, 127, 255, cv2.THRESH_BINARY)
template5 = cv2.imread('num_img/5.png', cv2.IMREAD_GRAYSCALE)
ret5, template5 = cv2.threshold(template5, 127, 255, cv2.THRESH_BINARY)
template6 = cv2.imread('num_img/6.png', cv2.IMREAD_GRAYSCALE)
ret6, template6 = cv2.threshold(template6, 127, 255, cv2.THRESH_BINARY)
template7 = cv2.imread('num_img/7.png', cv2.IMREAD_GRAYSCALE)
ret7, template7 = cv2.threshold(template7, 127, 255, cv2.THRESH_BINARY)
template8 = cv2.imread('num_img/8.png', cv2.IMREAD_GRAYSCALE)
ret8, template8 = cv2.threshold(template8, 127, 255, cv2.THRESH_BINARY)
template9 = cv2.imread('num_img/9.png', cv2.IMREAD_GRAYSCALE)
ret9, template9 = cv2.threshold(template9, 127, 255, cv2.THRESH_BINARY)

templateList = [template1, template2, template3, template4, template5, template6, template7, template8, template9]


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # 从文件中加载UI定义
        loadUi('jg-orc.ui', self)
        self._startPos = None
        self._endPos = None
        self._tracking = False

        # 获取显示器分辨率并缩放
        # self.desktop = QApplication.desktop()
        # self.screenRect = self.desktop.screenGeometry()
        # self.screenwidth = self.screenRect.width()
        # self.screenheight = self.screenRect.height()
        #
        # self.frame.resize(int(self.screenwidth*0.2), int(self.screenheight*0.5))
        # self.frame_2.resize(int(self.screenwidth*0.2), int(self.screenheight*0.4))
        # self.frame_3.resize(int(self.screenwidth*0.2), int(self.screenheight*0.1))

        # 置顶,透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        # self.setWindowFlags( Qt.FramelessWindowHint)
        # self.frame.setAttribute(Qt.WA_TranslucentBackground)

        # button-确定
        self.Button1.clicked.connect(self.on_click)

        # button-关闭
        self.Button2.clicked.connect(self.close)

        # horizontalSlider
        self.horizontalSlider.setValue(49)
        self.horizontalSlider.valueChanged.connect(self.valueChange)

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        if self._tracking:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._startPos = QPoint(e.x(), e.y())
            self._tracking = True

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None

    def on_click(self):
        new_num = self.getCorrectSeq()
        print("进入计算击杀顺序函数")
        print(new_num)
        global killstr
        correct_list = []
        kill_list = []
        killstr = ""

        sumlist = [[2, 7, 6, 9, 5, 1, 4, 3, 8],
                   [2, 9, 4, 7, 5, 3, 6, 1, 8],
                   [4, 3, 8, 9, 5, 1, 2, 7, 6],
                   [4, 9, 2, 3, 5, 7, 8, 1, 6],
                   [6, 1, 8, 7, 5, 3, 2, 9, 4],
                   [6, 7, 2, 1, 5, 9, 8, 3, 4],
                   [8, 1, 6, 3, 5, 7, 4, 9, 2],
                   [8, 3, 4, 1, 5, 9, 6, 7, 2],
                   ]

        # 查找正确数组
        for k in range(8):
            correct_num = 0
            for idx1 in range(6):
                if sumlist[k][idx1] == new_num[0]:
                    correct_num += 1
                    for idx2 in range(idx1, 7):
                        if sumlist[k][idx2] == new_num[1]:
                            correct_num += 1
                            for idx3 in range(idx1, 7):
                                if sumlist[k][idx3] == new_num[2]:
                                    correct_num += 1
                                    for idx4 in range(idx1, 7):
                                        if sumlist[k][idx4] == new_num[3]:
                                            correct_num += 1
            if correct_num == 4:
                print(sumlist[k])
                break
        # 判断空余的顺序
        # print(countlist)

        # print("初始击杀顺序为", kill_list)

        # 改进击杀顺序
        if 6 in [kill_list[0], kill_list[1], kill_list[2], kill_list[3]] or 7 in [kill_list[0], kill_list[1],
                                                                                  kill_list[2], kill_list[3]]:
            killstr = "不适合击杀"
            print("不适合击杀")
        elif kill_list[4] not in [3, 5, 9] and 3 not in kill_list:
            kill_list[4] = 3
            killstr = str(kill_list[0]) + str(kill_list[1]) + str(kill_list[2]) + str(kill_list[3]) + str(kill_list[4])
            print("建议击杀顺序", kill_list)
        elif kill_list[4] not in [3, 5, 9] and 5 not in kill_list:
            kill_list[4] = 5
            killstr = str(kill_list[0]) + str(kill_list[1]) + str(kill_list[2]) + str(kill_list[3]) + str(kill_list[4])
            print("建议击杀顺序", kill_list)
        elif kill_list[4] not in [3, 5, 9] and 9 not in kill_list:
            kill_list[4] = 9
            killstr = str(kill_list[0]) + str(kill_list[1]) + str(kill_list[2]) + str(kill_list[3]) + str(kill_list[4])
            print("建议击杀顺序", kill_list)
        elif kill_list[4] in [3, 5, 9]:
            killstr = str(kill_list[0]) + str(kill_list[1]) + str(kill_list[2]) + str(kill_list[3]) + str(kill_list[4])
            print("建议击杀顺序", kill_list)
        else:
            killstr = str(kill_list[0]) + str(kill_list[1]) + str(kill_list[2]) + str(kill_list[3]) + str(kill_list[4])

        # killstr = str(kill_list[0]) + str(kill_list[1]) + str(kill_list[2]) + str(kill_list[3]) + str(kill_list[4])
        print(killstr)
        self.label_2.setText(killstr)

    def valueChange(self):
        # 输出当前地刻度值，利用刻度值来调节窗口大小
        radio = (self.horizontalSlider.value() + 1) / 100
        # 中心 (250, 300)
        # x  = 250 - 250*radio y =300 - 300*radio
        self.frame_5.move(int(250 - 250 * radio), int(300 - 300 * radio))
        self.frame_5.resize(int(500 * radio), int(600 * radio))

    def getImg(self):
        # 绝对坐标
        x = self.frameGeometry().x() + self.frame_5.frameGeometry().x()
        y = self.frameGeometry().y() + self.frame_5.frameGeometry().y() + 80
        w = self.frame_5.width()
        h = self.frame_5.height()

        # 截图
        # img = pyautogui.screenshot(region=[x, y, w, h])  # x,y,w,h
        img = Image.open('./screenshot.png')
        # img.save("./screenshot.png")

        # img = cv2.cvtColor(np.asarray(img), cv2.COLOR_BGR2GRAY)
        # orc
        res_num, res_pos = orc(screenshot=img, templateList=templateList)
        # print(res_num)
        # print(res_pos)
        return res_num, res_pos

    def getCorrectSeq(self):
        res_num, res_pos = self.getImg()
        new_num, new_pos = correctPos(res_num, res_pos)
        # print(new_num)
        return new_num


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Jiugong = MainWindow()
    Jiugong.show()
    sys.exit(app.exec_())
