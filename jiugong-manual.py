import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # 从文件中加载UI定义
        loadUi('jg-manual.ui', self)
        # self._startPos = None
        # self._endPos = None
        # self._tracking = False

        # 置顶
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("九宫手动计算器")

        # button-确定
        self.Button1.clicked.connect(self.on_click)

        # button-取消
        self.Button2.clicked.connect(self.close)

        # button-重置
        self.Button3.clicked.connect(self.resetNum)

        # text
        self.textEdit_1.setText("0")
        self.textEdit_2.setText("0")
        self.textEdit_3.setText("0")
        self.textEdit_4.setText("0")
        self.textEdit_5.setText("0")
        self.textEdit_6.setText("0")
        self.textEdit_7.setText("0")
        self.textEdit_8.setText("0")
        self.textEdit_9.setText("0")

    # def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
    #     if self._tracking:
    #         self._endPos = e.pos() - self._startPos
    #         self.move(self.pos() + self._endPos)
    #
    # def mousePressEvent(self, e: QMouseEvent):
    #     if e.button() == Qt.LeftButton:
    #         self._startPos = QPoint(e.x(), e.y())
    #         self._tracking = True
    #
    # def mouseReleaseEvent(self, e: QMouseEvent):
    #     if e.button() == Qt.LeftButton:
    #         self._tracking = False
    #         self._startPos = None
    #         self._endPos = None

    def resetNum(self):
        self.textEdit_1.setText("0")
        self.textEdit_2.setText("0")
        self.textEdit_3.setText("0")
        self.textEdit_4.setText("0")
        self.textEdit_5.setText("0")
        self.textEdit_6.setText("0")
        self.textEdit_7.setText("0")
        self.textEdit_8.setText("0")
        self.textEdit_9.setText("0")
        self.label_2.setText("")
        self.label_3.setText("")

    def on_click(self):
        # global killstr
        countlist = []
        correct_list = []
        kill_list = []
        killstr = ""
        killSuggestion = ""
        num1 = int(self.textEdit_1.toPlainText())
        num2 = int(self.textEdit_2.toPlainText())
        num3 = int(self.textEdit_3.toPlainText())
        num4 = int(self.textEdit_4.toPlainText())
        num5 = int(self.textEdit_5.toPlainText())
        num6 = int(self.textEdit_6.toPlainText())
        num7 = int(self.textEdit_7.toPlainText())
        num8 = int(self.textEdit_8.toPlainText())
        num9 = int(self.textEdit_9.toPlainText())
        countlist.append(num1)
        countlist.append(num2)
        countlist.append(num3)
        countlist.append(num4)
        countlist.append(num5)
        countlist.append(num6)
        countlist.append(num7)
        countlist.append(num8)
        countlist.append(num9)
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
            for idx in range(9):
                if countlist[idx] == 0:
                    continue
                elif countlist[idx] != sumlist[k][idx]:
                    break
                elif countlist[idx] == sumlist[k][idx]:
                    correct_num += 1
            if correct_num >= 4:
                correct_list = sumlist[k]
                break

        if len(correct_list) == 0:
            print("九宫错误！！！")
            self.label_3.setText("九宫错误！！！")
            return

        # 判断空余的顺序
        # print(countlist)
        for i in range(9):
            if countlist[i] == 0:
                kill_list.append(correct_list[i])
        # print("初始击杀顺序为", kill_list)
        killstr = str(kill_list[0]) + str(kill_list[1]) + str(kill_list[2]) + str(kill_list[3]) + str(kill_list[4])
        self.label_2.setText(killstr)

        # 改进击杀顺序
        # 前四位有6或者7
        # if 6 in [kill_list[0], kill_list[1], kill_list[2], kill_list[3]] or 7 in [kill_list[0], kill_list[1],
        #                                                                           kill_list[2], kill_list[3]]:
        #     killSuggestion = "不适合击杀"
        #     # print("不适合击杀")
        # # 前四位有359
        # elif 3 in kill_list and 5 in kill_list and 9 in kill_list:
        #     killSuggestion = "不适合击杀"
        # # 不以359结尾但可强开3
        # elif kill_list[4] not in [3, 5, 9] and 3 not in kill_list:
        #     kill_list[4] = 3
        #     killstr = str(kill_list[0]) + str(kill_list[1]) + str(kill_list[2]) + str(kill_list[3]) + str(kill_list[4])
        #     # print("建议击杀顺序", kill_list)
        #     killSuggestion = "建议顺序" + killstr
        # # 不以359结尾但可强开5
        # elif kill_list[4] not in [3, 5, 9] and 5 not in kill_list:
        #     kill_list[4] = 5
        #     killstr = str(kill_list[0]) + str(kill_list[1]) + str(kill_list[2]) + str(kill_list[3]) + str(kill_list[4])
        #     killSuggestion = "建议顺序" + killstr
        #     # print("建议击杀顺序", kill_list)
        # # 不以359结尾但可强开9
        # elif kill_list[4] not in [3, 5, 9] and 9 not in kill_list:
        #     kill_list[4] = 9
        #     killstr = str(kill_list[0]) + str(kill_list[1]) + str(kill_list[2]) + str(kill_list[3]) + str(kill_list[4])
        #     killSuggestion = "建议顺序" + killstr
        #     # print("建议击杀顺序", kill_list)
        # elif kill_list[4] in [3, 5, 9]:
        #     killSuggestion = "建议顺序" + killstr
        #     # print("建议击杀顺序", kill_list)
        # else:
        #     killSuggestion = "建议顺序" + killstr
        # self.label_3.setText(killSuggestion)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Jiugong = MainWindow()
    Jiugong.show()
    sys.exit(app.exec_())
