# @author jiangshiyi
# @python 3.6.4
#
#
# @time 2018.10.1
from pathlib import Path
import csv
import re


base_dir = Path(__file__).cwd()
data = base_dir.joinpath("data")

def print_infos(infos,item):
    """
        infos: 一个字符串，表示要打印的 fields
        item : 一个有序字典
        更与信息打印出 结果
    """
    if infos == "*":
        for i in item:
            print(i + ":" + item[i],end=" ")
        print("")
    else:
        parms = infos.split(",")
        for parm in parms:
            print(parm + ":" + item[parm],end=" ")
        print("")

def check_item_condition(item,condition):
    """
        item : 一个有序字典
        condition : 字符串条件
        用于核查一个 item 是否符合该条件
    """
    is_between_and = re.compile(r"(\w+) between (\w+) and (\w+)",re.IGNORECASE).match(condition)
    # id = 1
    is_single_condition = re.compile(r"([\w\s]+)([=<>]+)([\w\s]+)",re.IGNORECASE).match(condition)

    if is_between_and:
        parm = is_between_and.group(1)
        begin = int(is_between_and.group(2))
        end = int(is_between_and.group(3))
        
        if parm not in item.keys():
            print("Error parm!")
            return False
        
        if int(item[parm]) <= end and int(item[parm]) > begin:
            return True
        else:
            return False
        
    if is_single_condition:
        left = is_single_condition.group(1).strip()
        right = is_single_condition.group(3).strip()
        operator = is_single_condition.group(2).strip()
 
        if left not in item.keys():
            print("Error parm!")
            return False
        
        if operator == "=" and item[left] == right:
            return True
        elif operator == ">" and item[left] > right:
            return True
        elif operator == "<" and item[left] < right:
            return True
        elif operator == ">=" and item[left] >= right:
            return True
        elif operator == "<=" and item[left] <= right:
            return True
        else:
            return False
