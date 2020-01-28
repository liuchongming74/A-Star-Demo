# coding: utf-8
from PIL import Image
import math
import numpy as np

GRAY = (127, 127, 127, 255)
BLUE = (75, 174, 234, 255)
YELLOW = (246, 193, 67, 255)
WHITE = (255, 255, 255, 255)
RED = (255, 0, 0, 255)
BORDER = (0, 0, 0, 255)


def convert_array_to_pixel(arr, path):
    """
    将字符数组转化为像素
    :param arr:
    :param path:
    :return:
    """
    width = 20
    height = 20
    pixels = []
    for i in range(1, len(arr)):
        line = []
        for j in range(1, len(arr[i])):
            if arr[i][j] == 'g':
                line.append(GRAY)
            elif arr[i][j] == 'b':
                line.append(BLUE)
            elif arr[i][j] == 'y':
                line.append(YELLOW)
            elif arr[i][j] == 'w':
                line.append(WHITE)
        pixels.append(line)
    # 绘制路径
    for point in path:
        x, y = point
        pixels[x - 1][y - 1] = RED
    # 处理分辨率，放大
    result = [[BORDER] * ((len(pixels[0])) * width + (len(pixels[0]) + 1))]
    for i in range(len(pixels)):
        line = [BORDER]
        for j in range(len(pixels[i])):
            line.extend([pixels[i][j]] * width)
            line.append(BORDER)
        for j in range(height):
            result.append(line)
        result.append([BORDER] * len(line))
    del pixels
    return result


def save_result(game_map, path):
    """
    将结果保存为图片
    :param game_map:
    :param path:
    :return:
    """
    pix = convert_array_to_pixel(game_map, path)
    array = np.asarray(pix, dtype=np.uint8)
    image = Image.fromarray(array, 'RGBA')
    image.save("result.png")


def get_cost(kind):
    """
    y: 沙漠
    b: 溪流
    g: 障碍
    w: 普通道路
    :param kind:
    :return:
    """
    cost = {"y": 4, "b": 2, "g": -1, "w": 0}
    return cost[kind]


def process_map():
    """
    将图片变化为字符矩阵
    :return:
    """
    game_map = [[0] * 41]
    im = Image.open('map.png')
    pix = im.load()
    width = im.size[0]
    height = im.size[1]
    """
    取样点坐标
    """
    start_x = int(math.floor(width / 40)) - 10
    x_step = int(round(width / 40))
    start_y = int(math.floor(height / 20)) - 10
    y_step = int(round(height / 20))
    for i in range(20):
        row = [0]
        y = start_y + i * y_step
        for j in range(40):
            x = start_x + j * x_step
            if pix[x, y] == GRAY:
                row.append('g')
            elif pix[x, y] == BLUE:
                row.append('b')
            elif pix[x, y] == YELLOW:
                row.append('y')
            elif pix[x, y] == WHITE:
                row.append('w')
            else:
                print("error")
        game_map.append(row)
    return game_map


class AreaBlock(object):
    def __init__(self, father, kind, g, row, col):
        self.father = father
        self.kind = kind
        self.coordinate_row = row
        self.coordinate_col = col
        self.g = g
        self.f = 0.0

    def get_coordinate(self):
        return self.coordinate_row, self.coordinate_col

    def __lt__(self, other):
        """
        operator <
        :param other:
        :return:
        """
        return self.f < other.f


if __name__ == "__main__":
    arr = []
    arr.extend([RED] * 3)
    print(arr)
