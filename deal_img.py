import cv2
import numpy as np
from PIL import Image
import copy

# 读取原图像和模板图像

# screenshot = cv2.imread('./screenshot.png', cv2.IMREAD_GRAYSCALE)
screenshot = Image.open('./screenshot.png')

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


# 进行模板匹配
def orc(screenshot, templateList):
    # screenshot = cv2.imread('./screenshot.png', cv2.IMREAD_GRAYSCALE)
    screenshot = cv2.cvtColor(np.asarray(screenshot), cv2.COLOR_BGR2GRAY)
    ret, img = cv2.threshold(screenshot, 138, 255, cv2.THRESH_BINARY)

    res_num = []
    res_pos = []
    # max = 0
    print("start orc -------------------------------")
    for i in range(0, 9):
        h, w = img.shape[:2]
        # print(h, w)
        h, w = int(w // 4), int(w // 4)
        # print(h, w)
        template = cv2.resize(templateList[i], dsize=(h, w))

        result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

        # 寻找匹配程度最高的位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # print(max_val, max_loc)

        # if max_val > max and max_val > 0.45:
        #     res_num = i + 1
        #     max = max_val

        # 定位目标区域
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        # 在原图像中标记目标区域
        if max_val > 0.45:
            res_num.append(i + 1)
            # res_pos.append([top_left[0], top_left[1]])
            res_pos.append(top_left)
            # cv2.rectangle(img, top_left, bottom_right, (0, 0, 0), 2)
            # cv2.putText(img, str(i + 1), (top_left[0], top_left[1] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            print(i + 1, max_val, "匹配成功")
        # else:
            # print(i + 1, max_val)
    print("End orc -------------------------------")
    return res_num, res_pos


# 单独匹配
def orc2(screenshot, templateList):
    # screenshot = cv2.cvtColor(np.asarray(screenshot), cv2.COLOR_BGR2GRAY)
    ret, img = cv2.threshold(screenshot, 138, 255, cv2.THRESH_BINARY)
    h, w = img.shape[:2]
    max = 0
    res_num = 0
    # print(h, w)
    h, w = int(w // 1), int(w // 1)
    # print(h, w)
    for i in range(0, 9):
        template = cv2.resize(templateList[i], dsize=(h, w))

        result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

        # 寻找匹配程度最高的位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print(max_val, max_loc)

        if max_val > max and max_val > 0.45:
            res_num = i + 1
            max = max_val
        # 定位目标区域
        # top_left = max_loc
        # bottom_right = (top_left[0] + w, top_left[1] + h)

        # 在原图像中标记目标区域

        # cv2.rectangle(img, top_left, bottom_right, (0, 0, 0), 2)
        # cv2.putText(img, str(i + 1), (top_left[0], top_left[1] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        #     print(i + 1, max_val, "匹配成功")
        # else:
        #         print(i + 1, max_val)
    print(res_num)


def correctPos(res_num, res_pos):
    new_num = []
    new_pos = []
    bk = copy.deepcopy(res_pos)
    l = len(res_pos)
    for i in range(l):
        j = i
        for j in range(l):
            if (res_pos[i][0] < res_pos[j][0]):
                res_pos[i], res_pos[j] = res_pos[j], res_pos[i]
            if (res_pos[i][1] < res_pos[j][1]):
                res_pos[i], res_pos[j] = res_pos[j], res_pos[i]

    for k in range(len(res_pos)):
        new_pos.append(res_pos[k])

    for k in range(4):
        index = bk.index(new_pos[k])
        new_num.append(res_num[index])
    return new_num, new_pos

if __name__ == '__main__':

    print(type(screenshot))
    res_num, res_pos = orc(screenshot=screenshot, templateList=templateList)

    print(res_num)
    print(res_pos)
    print("-----------------------------")
    new_num, new_pos = correctPos(res_num, res_pos)

    print(new_num)
    print(new_pos)
    # 显示结果
    # cv2.imshow('result1', screenshot)
    # # cv2.imshow('result2', screenshot_bw)
    # # cv2.imshow('result1', thresh2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
