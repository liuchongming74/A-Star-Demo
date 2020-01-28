# coding: utf-8
import math
from area_block import get_cost
from area_block import save_result
from area_block import AreaBlock
from area_block import process_map
from queue import PriorityQueue

# 定义8个方向
direction = [[0, 1],
             [0, -1],
             [1, 0],
             [-1, 0],
             [1, 1],
             [-1, -1],
             [-1, 1],
             [1, -1]]


def heuristic(point, target):
    """
    用曼哈顿距离估值
    :param point:
    :param target:
    :type point: AreaBlock
    :type target: AreaBlock
    :return:
    """
    dis = (math.fabs(target.coordinate_row - point.coordinate_row) +
           math.fabs(target.coordinate_col - point.coordinate_col))
    return point.g * 5 + dis


def bound(row, col, max_row, max_col):
    """
    边界条件检测：
    1.如果该点坐标超出地图区域，则非法
    2.如果该点是障碍，则非法
    :param row:
    :param col:
    :param max_row:
    :param max_col:
    :return:
    """
    if row < 1 or row > max_row:
        return True
    if col < 1 or col > max_col:
        return True
    return False


def find_path(target_area_block):
    """
    回溯寻找路径
    :type target_area_block: AreaBlock
    :param target_area_block: 
    :return: 
    """
    print(target_area_block.g)
    # 用栈存储路径
    stack = [target_area_block.get_coordinate()]
    father_area_block = target_area_block.father
    while father_area_block is not None:
        stack.append(father_area_block.get_coordinate())
        father_area_block = father_area_block.father
    return stack


def search(game_map, start_pos, end_pos):
    """
    寻路算法
    :param game_map:
    :param start_pos:
    :param end_pos:
    :return:
    """
    # 确定边界
    max_row = len(game_map) - 1
    max_col = len(game_map[0]) - 1
    # 创建open表, close表
    opened_table = PriorityQueue()
    closed_table = set()
    # 初始化open表
    opened_table.put(start_pos)
    while not opened_table.empty():
        current_area_block = opened_table.get()
        for direct in direction:
            col_index = current_area_block.coordinate_col + direct[0]
            row_index = current_area_block.coordinate_row + direct[1]
            # 边界检测, 如果它不可通过或者已经在关闭列表中, 跳过
            if (row_index, col_index) in closed_table or bound(row_index, col_index, max_row=max_row, max_col=max_col):
                continue
            if game_map[row_index][col_index] == 'g':
                continue
            # 计算移动代价
            move_cost = 1
            if math.fabs(direct[0]) == 1 and math.fabs(direct[1]) == 1:
                move_cost *= math.sqrt(2)
            # 计算地形代价
            land_cost = get_cost(game_map[row_index][col_index])
            # 创建block
            next_area = AreaBlock(father=current_area_block,
                                  kind=game_map[row_index][col_index],
                                  g=current_area_block.g + move_cost + land_cost,  # 地形代价 + 移动代价
                                  row=row_index,
                                  col=col_index)
            # 如果当前节点是目标节点，则找到路径
            if col_index == end_pos.coordinate_col and row_index == end_pos.coordinate_row:
                # 向父节点开始回溯，输出路径
                return find_path(next_area)
            # 检查该点是否在open表中
            result = None
            tmp_queue = []
            while not opened_table.empty():
                tmp_block = opened_table.get()
                if tmp_block.get_coordinate() == next_area.get_coordinate():
                    result = tmp_block
                    break
                tmp_queue.append(tmp_block)
            while len(tmp_queue) != 0:
                opened_table.put(tmp_queue.pop())
            opened_table.task_done()
            # 检查该点是否在open表中, 如果不在则加入, 同时计算启发值 F = G + H
            next_area.f = heuristic(next_area, end_pos)
            if result is None:
                opened_table.put(next_area)
            else:
                """
                用G值为参考检查新的路径是否更好。更低的G值意味着更好的路径。
                """
                if next_area.g < result.g:
                    opened_table.put(next_area)
                else:
                    opened_table.put(result)
        closed_table.add(current_area_block.get_coordinate())
    return None


if __name__ == "__main__":
    startPoint = AreaBlock(None, 'w', g=0, row=11, col=5)
    endPoint = AreaBlock(None, 'y', g=0, row=1, col=36)
    game_map = process_map()
    path = search(game_map=game_map, start_pos=startPoint, end_pos=endPoint)
    if path is None:
        print("doesn't exist path")
    else:
        save_result(game_map, path)
