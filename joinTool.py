# @author jiangshiyi
# @python 3.6.4
#
#
# @time 2018.10.1
from pathlib import Path
import csv
import re
from common import print_infos,check_item_condition

base_dir = Path(__file__).cwd()
data = base_dir.joinpath("data")


def inner_join(current_database_name,infos,left_table_name,right_table_name,condition):
    global data
    left_table = data.joinpath(current_database_name,left_table_name+".csv")
    right_table = data.joinpath(current_database_name,right_table_name+".csv") 
    if (not left_table.exists()) or (not right_table.exists()):
        print("Error : Unknown table")
        return

    left_reader = csv.DictReader(left_table.open("r",newline=""),delimiter="|")
    right_reader = csv.DictReader(right_table.open("r",newline=""),delimiter="|")

    is_single_condition = re.compile(r"([\w\s\.]+)=([\w\s\.]+)",re.IGNORECASE).match(condition)
    if not is_single_condition:
        print("ERROR!")
        return
    
    left = is_single_condition.group(1).strip()
    right = is_single_condition.group(2).strip()
    tableA,parmA = left.split(".")
    tableB,parmB = right.split(".")
    if tableA == left_table_name:
        parm_left = parmA
        parm_right = parmB
    else:
        parm_left = parmB
        parm_right = parmA

    # infos
    left_info = []
    right_info = []
    infos = infos.split(",")
    for info in infos:
        table,parm = info.split(".")
        if table == left_table_name:
            left_info.append(parm)
        else:
            right_info.append(parm)

    left_info = ",".join(left_info)
    right_info = ",".join(right_info)

    l = []
    for i in left_reader:
        l.append(i)
    r = []
    for j in right_reader:
        r.append(j)

    for left_row in l:
        for right_row in r:
            if left_row[parm_left] == right_row[parm_right]:
                print_infos(left_info,left_row)
                print_infos(right_info,right_row)

    print("OPERATOR SUCCESS")

def left_join(current_database_name,infos,left_table_name,right_table_name,condition):
    global data
    left_table = data.joinpath(current_database_name,left_table_name+".csv")
    right_table = data.joinpath(current_database_name,right_table_name+".csv") 
    if (not left_table.exists()) or (not right_table.exists()):
        print("Error : Unknown table")
        return

    left_reader = csv.DictReader(left_table.open("r",newline=""),delimiter="|")
    right_reader = csv.DictReader(right_table.open("r",newline=""),delimiter="|")

    is_single_condition = re.compile(r"([\w\s\.]+)=([\w\s\.]+)",re.IGNORECASE).match(condition)
    if not is_single_condition:
        print("ERROR!")
        return
    
    left = is_single_condition.group(1).strip()
    right = is_single_condition.group(2).strip()
    try:
        tableA,parmA = left.split(".")
        tableB,parmB = right.split(".")
        if tableA == left_table_name:
            parm_left = parmA
            parm_right = parmB
        else:
            parm_left = parmB
            parm_right = parmA
    
        # infos
        left_info = []
        right_info = []
        infos = infos.split(",")
        for info in infos:
            table,parm = info.split(".")
            if table == left_table_name:
                left_info.append(parm)
            else:
                right_info.append(parm)
                
        left_info = ",".join(left_info)
        right_info = ",".join(right_info)
    except:
        left_info = "*"
        right_info = "*"
    

    l = []
    for i in left_reader:
        l.append(i)
    r = []
    for j in right_reader:
        r.append(j)

    for left_row in l:
        print_infos(left_info,left_row)
        for right_row in r:
            if left_row[parm_left] == right_row[parm_right]:
                print_infos(right_info,right_row)

    print("OPERATOR SUCCESS")


def right_join(current_database_name,infos,left_table_name,right_table_name,condition):
    global data
    left_table = data.joinpath(current_database_name,left_table_name+".csv")
    right_table = data.joinpath(current_database_name,right_table_name+".csv") 
    if (not left_table.exists()) or (not right_table.exists()):
        print("Error : Unknown table")
        return

    left_reader = csv.DictReader(left_table.open("r",newline=""),delimiter="|")
    right_reader = csv.DictReader(right_table.open("r",newline=""),delimiter="|")

    is_single_condition = re.compile(r"([\w\s\.]+)=([\w\s\.]+)",re.IGNORECASE).match(condition)
    if not is_single_condition:
        print("ERROR!")
        return
    
    left = is_single_condition.group(1).strip()
    right = is_single_condition.group(2).strip()
    try:
        tableA,parmA = left.split(".")
        tableB,parmB = right.split(".")
        if tableA == left_table_name:
            parm_left = parmA
            parm_right = parmB
        else:
            parm_left = parmB
            parm_right = parmA
    
        # infos
        left_info = []
        right_info = []
        infos = infos.split(",")
        for info in infos:
            table,parm = info.split(".")
            if table == left_table_name:
                left_info.append(parm)
            else:
                right_info.append(parm)
                
        left_info = ",".join(left_info)
        right_info = ",".join(right_info)
    except:
        left_info = "*"
        right_info = "*"
    

    l = []
    for i in left_reader:
        l.append(i)
    r = []
    for j in right_reader:
        r.append(j)

    for right_row in l:
        print_infos(right_info,left_row)
        for left_row in r:
            if left_row[parm_left] == right_row[parm_right]:
                print_infos(left_info,right_row)

    print("OPERATOR SUCCESS")
