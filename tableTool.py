# @author jiangshiyi
# @python 3.6.4
#
#
# @time 2018.10.1
from pathlib import Path
import csv
import re
from common import print_infos,check_item_condition
import cross_platform_lock # 加入自定义的 跨平台 文件锁，实现共享锁，排它锁


base_dir = Path(__file__).cwd()
data = base_dir.joinpath("data")


def apply_database_table(database_name,table_name,content):
    global data
    table = data.joinpath(database_name,table_name+".csv")
    if not table.exists():
        print("ERROR : Unknown table '%s.%s'" % (current_database_name,table_name))
        return
    
    with open(table,"w") as fp:
        fp.write(content)

    print("OPERATOR SUCCESS")


def insert_into(current_database_name,table_name,values):
    global data
    table = data.joinpath(current_database_name,table_name+".csv")
    if not table.exists():
        print("ERROR : Unknown table '%s.%s'" % (current_database_name,table_name))
        return []
    
    with open(table,"r",newline="") as csvfile:
        reader = csv.reader(csvfile,delimiter="|")
        firstrow = next(reader)
        if len(firstrow) != len(values):
            print("ERROR : Column count doesn't match value count at row 1")
            return []
        id = 0
        for item in reader:
            id = int(item[0])
        values[0] = id + 1
    with open(table,"a",newline="") as csvfile:
        writer = csv.writer(csvfile,delimiter="|")
        writer.writerow(values)

    return_list = []
    result = None
    with open(table,"r",newline="") as csvfile:
        reader = csv.reader(csvfile,delimiter="|")
        for i in reader:
            result = i 
    return_list = [(table_name,i)]
    print("OPERATOR SUCCESS")
    return return_list

def delete_from(current_database_name,table_name,condition):
    global data
    table = data.joinpath(current_database_name,table_name+".csv")
    if not table.exists():
        print("ERROR : Unknown table '%s.%s'" % (current_database_name,table_name))
        return []
    
    # print(condition)
    # and or between and in
    # id between 1 and 3
    is_between_and = re.compile(r"(\w+) between (\w+) and (\w+)",re.IGNORECASE).match(condition)
    # id = 1
    is_single_condition = re.compile(r"([\w\s]+)([=<>]+)([\w\s]+)",re.IGNORECASE).match(condition)

    return_list = []

    if is_between_and:
        parm = is_between_and.group(1)
        begin = int(is_between_and.group(2))
        end = int(is_between_and.group(3))
        # print(begin)
        # print(end)
        firstrow = None
        with open(table,"r",newline="") as csvfile:
            reader = csv.reader(csvfile,delimiter="|")
            firstrow = next(reader)
        if parm not in firstrow:
            print("Error parm!")
            return return_list

        reader = csv.DictReader(table.open("r",newline=""),delimiter="|")
        read_list = []
        for i in reader:
            read_list.append(i)
        with open(table,"w",newline="") as csvfile:
            
            writer = csv.writer(csvfile,delimiter="|")
            writer.writerow(firstrow)
            for i in read_list:
                # print(i)
                if int(i[parm]) <= end and int(i[parm]) > begin:
                    return_list.append((table_name,i))
                    continue
                writer.writerow(i.values())

    if is_single_condition:
        left = is_single_condition.group(1).strip()
        right = is_single_condition.group(3).strip()
        operator = is_single_condition.group(2).strip()
 
        firstrow = None
        with open(table,"r",newline="") as csvfile:
            reader = csv.reader(csvfile,delimiter="|")
            firstrow = next(reader)
        if left not in firstrow:
            print("Error parm!")
            return return_list
        
        reader = csv.DictReader(table.open("r",newline=""),delimiter="|")
        read_list = []
        for i in reader:
            read_list.append(i)
        with open(table,"w",newline="") as csvfile:    
            writer = csv.writer(csvfile,delimiter="|")
            writer.writerow(firstrow)
            for item in read_list:
                if operator == "=" and item[left] == right:
                    return_list.append((table_name,item))
                    continue
                elif operator == ">" and item[left] > right:
                    return_list.append((table_name,item))
                    continue
                elif operator == "<" and item[left] < right:
                    return_list.append((table_name,item))
                    continue
                elif operator == ">=" and item[left] >= right:
                    return_list.append((table_name,item))
                    continue
                elif operator == "<=" and item[left] <= right:
                    return_list.append((table_name,item))
                    continue
                else:
                    writer.writerow(item.values())
    
    print("OPERATOR SUCCESS")
    return return_list


def update_table(current_database_name,table_name,left,right,condition):
    global data
    table = data.joinpath(current_database_name,table_name+".csv")
    if not table.exists():
        print("ERROR : Unknown table '%s.%s'" % (current_database_name,table_name))
        return []

    # id between 1 and 3
    is_between_and = re.compile(r"(\w+) between (\w+) and (\w+)",re.IGNORECASE).match(condition)
    # id = 1
    is_single_condition = re.compile(r"([\w\s]+)([=<>]+)([\w\s]+)",re.IGNORECASE).match(condition)
    return_list = []

    if is_between_and:
        parm = is_between_and.group(1)
        begin = int(is_between_and.group(2))
        end = int(is_between_and.group(3))
        # print(begin)
        # print(end)
        firstrow = None
        with open(table,"r",newline="") as csvfile:
            reader = csv.reader(csvfile,delimiter="|")
            firstrow = next(reader)
        if parm not in firstrow:
            print("Error parm!")
            return  []

        reader = csv.DictReader(table.open("r",newline=""),delimiter="|")
        read_list = []
        for i in reader:
            read_list.append(i)
        with open(table,"w",newline="") as csvfile:
            
            writer = csv.writer(csvfile,delimiter="|")
            writer.writerow(firstrow)
            for item in read_list:
                # print(i)
                if int(item[parm]) <= end and int(item[parm]) > begin:
                    return_list.append((table_name,item))
                    item[left] = right
                writer.writerow(item.values())

    if is_single_condition:
        begin = is_single_condition.group(1).strip()
        end = is_single_condition.group(3).strip()
        operator = is_single_condition.group(2).strip()
  
        firstrow = None
        with open(table,"r",newline="") as csvfile:
            reader = csv.reader(csvfile,delimiter="|")
            firstrow = next(reader)
        if begin not in firstrow:
            print("Error parm!")
            return []
        
        reader = csv.DictReader(table.open("r",newline=""),delimiter="|")
        read_list = []
        for i in reader:
            read_list.append(i)
        with open(table,"w",newline="") as csvfile:    
            writer = csv.writer(csvfile,delimiter="|")
            writer.writerow(firstrow)
            for item in read_list:
                if operator == "=" and item[begin] == end:
                    return_list.append((table_name,item))
                    item[left] = right
                elif operator == ">" and item[begin] > end:
                    return_list.append((table_name,item))
                    item[left] = right
                elif operator == "<" and item[begin] < end:
                    return_list.append((table_name,item))
                    item[left] = right
                elif operator == ">=" and item[begin] >= end:
                    return_list.append((table_name,item))
                    item[left] = right
                elif operator == "<=" and item[begin] <= end:
                    return_list.append((table_name,item))
                    item[left] = right
                else:
                    pass
                writer.writerow(item.values())
                
    print("OPERATOR SUCCESS")
    return return_list


def select_from_no_condition(current_database_name,table_name):
    global data
    table = data.joinpath(current_database_name,table_name+".csv")
    if not table.exists():
        print("ERROR : Unknown table '%s.%s'" % (current_database_name,table_name))
        return

    with open(table,"r",newline="") as csvfile:
        reader = csv.DictReader(csvfile,delimiter="|")
        test = next(reader)
        print(",".join(test.keys()))
        print(",".join(test.values()))
        for item in reader:
            print(",".join(item.values()))

    print("OPERATOR SUCCESS")

def select_from(current_database_name,infos,table_name,condition):
    global data
    table = data.joinpath(current_database_name,table_name+".csv")
    if not table.exists():
        print("ERROR : Unknown table '%s.%s'" % (current_database_name,table_name))
        return
    
    # print(condition)
    # and or between and in
    # id between 1 and 3
    is_between_and = re.compile(r"(\w+) between (\w+) and (\w+)",re.IGNORECASE).match(condition)
    # id = 1
    is_single_condition = re.compile(r"([\w\s]+)([=<>]+)([\w\s]+)",re.IGNORECASE).match(condition)

    if is_between_and:
        parm = is_between_and.group(1)
        begin = int(is_between_and.group(2))
        end = int(is_between_and.group(3))
        # print(begin)
        # print(end)
        firstrow = None
        with open(table,"r",newline="") as csvfile:
            reader = csv.reader(csvfile,delimiter="|")
            firstrow = next(reader)
        if parm not in firstrow:
            print("Error parm!")
            return  

        reader = csv.DictReader(table.open("r",newline=""),delimiter="|")
        read_list = []
        for i in reader:
            read_list.append(i)
        
        for i in read_list:
            # print(i)
            if int(i[parm]) <= end and int(i[parm]) > begin:
                print_infos(infos,i)



    if is_single_condition:
        left = is_single_condition.group(1).strip()
        right = is_single_condition.group(3).strip()
        operator = is_single_condition.group(2).strip()
 
        firstrow = None
        with open(table,"r",newline="") as csvfile:
            reader = csv.reader(csvfile,delimiter="|")
            firstrow = next(reader)
        if left not in firstrow:
            print("Error parm!")
            return  
        
        reader = csv.DictReader(table.open("r",newline=""),delimiter="|")
        for item in reader:
            if operator == "=" and item[left] == right:
                print_infos(infos,item)
            elif operator == ">" and item[left] > right:
                print_infos(infos,item)
            elif operator == "<" and item[left] < right:
                print_infos(infos,item)
            elif operator == ">=" and item[left] >= right:
                print_infos(infos,item)
            elif operator == "<=" and item[left] <= right:
                print_infos(infos,item)
            else:
                pass
    print("OPERATOR SUCCESS")

def select_from_where_limit(current_database_name,infos,table_name,condition,limit):
    global data
    table = data.joinpath(current_database_name,table_name+".csv")
    if not table.exists():
        print("ERROR : Unknown table '%s.%s'" % (current_database_name,table_name))
        return

    if len(limit.split(",")) == 1:
        limit_offset = 0
        limit_count = int(limit)
    else:
        limit_offset = int(limit.split(",")[0])
        limit_count = int(limit.split(",")[1])

    items = []
    with open(table,"r",newline="") as csvfile:
        reader = csv.DictReader(csvfile,delimiter="|")
        for i in reader:
            if check_item_condition(i,condition):
                items.append(i)
    items = iter(items)
    for i in range(limit_offset):
        try:
            next(items)
        except:
            return
    for i in range(limit_count):
        try:
            item = next(items)
            print_infos(infos,item)
        except:
            break
    print("OPERATOR SUCCESS")

def select_from_where_order_by(current_database_name,infos,table_name,condition,order_key):
    global data
    table = data.joinpath(current_database_name,table_name+".csv")
    if not table.exists():
        print("ERROR : Unknown table '%s.%s'" % (current_database_name,table_name))
        return
    def order_by_key(item):
        return item[order_key]
    l = []
    with open(table,"r",newline="") as csvfile:
        reader = csv.DictReader(csvfile,delimiter="|")
        for i in reader:
            if check_item_condition(i,condition):
                l.append(i)
    l.sort(key=order_by_key)
    for i in l:
        print_infos(infos,i)
    print("OPERATOR SUCCESS")

# 实现了 limit 方法
def select_from_limit(current_database_name,infos,table_name,limit):
    global data
    table = data.joinpath(current_database_name,table_name+".csv")
    if not table.exists():
        print("ERROR : Unknown table '%s.%s'" % (current_database_name,table_name))
        return

    if len(limit.split(",")) == 1:
        limit_offset = 0
        limit_count = int(limit)
    else:
        limit_offset = int(limit.split(",")[0])
        limit_count = int(limit.split(",")[1])
    with open(table,"r",newline="") as csvfile:
        reader = csv.DictReader(csvfile,delimiter="|")
        for i in range(limit_offset):
            next(reader)
        for i in range(limit_count):
            try:
                item = next(reader)
                print_infos(infos,item)
            except:
                break
    print("OPERATOR SUCCESS")

# 实现了 order by 方法
def select_from_order_by(current_database_name,infos,table_name,order_key):
    global data
    table = data.joinpath(current_database_name,table_name+".csv")
    if not table.exists():
        print("ERROR : Unknown table '%s.%s'" % (current_database_name,table_name))
        return

    def order_by_key(item):
        return item[order_key]
    l = None
    with open(table,"r",newline="") as csvfile:
        reader = csv.DictReader(csvfile,delimiter="|")
        l = sorted(reader,key=order_by_key)
    for item in l:
        print_infos(infos,item)
    print("OPERATOR SUCCESS")

def select_from_group_by(current_database_name,infos,table_name,parms):
    global data
    table = data.joinpath(current_database_name,table_name+".csv")
    if not table.exists():
        print("ERROR : Unknown table '%s.%s'" % (current_database_name,table_name))
        return 
    parms = parms.split(",")
    # 所有不同的种类
    cate = []
    with open(table,"r",newline="") as csvfile:
        reader = csv.DictReader(csvfile,delimiter="|")
        for item in reader:
            tup = tuple(item[parm] for parm in parms)
            if tup not in cate:
                cate.append(tup)
    # 对每一类，用一个列表装起来
    l = [[] for i in range(len(cate))]
    with open(table,"r",newline="") as csvfile:
        reader = csv.DictReader(csvfile,delimiter="|")
        for item in reader:
            for i in range(len(cate)):
                if tuple(item[parm] for parm in parms) == cate[i]:
                    l[i].append(item)
    
    for i in l:
        print_infos(infos,i[0])
    print("OPERATOR SUCCESS")

def select_from_group_by_having(current_database_name,infos,table_name,parms,condition):
    global data
    table = data.joinpath(current_database_name,table_name+".csv")
    if not table.exists():
        print("ERROR : Unknown table '%s.%s'" % (current_database_name,table_name))
        return 
    parms = parms.split(",")
    # 所有不同的种类
    cate = []
    with open(table,"r",newline="") as csvfile:
        reader = csv.DictReader(csvfile,delimiter="|")
        for item in reader:
            tup = tuple(item[parm] for parm in parms)
            if tup not in cate:
                cate.append(tup)
    # 对每一类，用一个列表装起来
    l = [[] for i in range(len(cate))]
    with open(table,"r",newline="") as csvfile:
        reader = csv.DictReader(csvfile,delimiter="|")
        for item in reader:
            for i in range(len(cate)):
                if tuple(item[parm] for parm in parms) == cate[i]:
                    l[i].append(item)
    
    for i in l:
        if check_item_condition(i[0],condition):
            print_infos(infos,i[0])
    print("OPERATOR SUCCESS")                






