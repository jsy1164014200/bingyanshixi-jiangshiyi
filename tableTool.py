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


def insert_into(current_database_name,table_name,values):
    global data
    table = data.joinpath(current_database_name,table_name+".csv")
    if not table.exists():
        print("ERROR : Unknown table '%s.%s'" % (current_database_name,table_name))
        return
    
    with open(table,"r",newline="") as csvfile:
        reader = csv.reader(csvfile,delimiter="|")
        firstrow = next(reader)
        if len(firstrow) != len(values):
            print("ERROR : Column count doesn't match value count at row 1")
            return
        id = 0
        for item in reader:
            id = int(item[0])
        values[0] = id + 1
    with open(table,"a",newline="") as csvfile:
        writer = csv.writer(csvfile,delimiter="|")
        writer.writerow(values)

    # with open(table,"r",newline="") as csvfile:
    #     reader = csv.DictReader(csvfile,delimiter="|")
    #     for row in reader:
    #         print(row['id'])
    #         print(row['phone'])

def delete_from(current_database_name,table_name,condition):
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
        with open(table,"w",newline="") as csvfile:
            
            writer = csv.writer(csvfile,delimiter="|")
            writer.writerow(firstrow)
            for i in read_list:
                # print(i)
                if int(i[parm]) <= end and int(i[parm]) > begin:
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
            return  
        
        reader = csv.DictReader(table.open("r",newline=""),delimiter="|")
        read_list = []
        for i in reader:
            read_list.append(i)
        with open(table,"w",newline="") as csvfile:    
            writer = csv.writer(csvfile,delimiter="|")
            writer.writerow(firstrow)
            for item in read_list:
                if operator == "=" and item[left] == right:
                    continue
                elif operator == ">" and item[left] > right:
                    continue
                elif operator == "<" and item[left] < right:
                    continue
                elif operator == ">=" and item[left] >= right:
                    continue
                elif operator == "<=" and item[left] <= right:
                    continue
                else:
                    writer.writerow(item.values())

def update_table(current_database_name,table_name,left,right,condition):
    global data
    table = data.joinpath(current_database_name,table_name+".csv")
    if not table.exists():
        print("ERROR : Unknown table '%s.%s'" % (current_database_name,table_name))
        return

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
        with open(table,"w",newline="") as csvfile:
            
            writer = csv.writer(csvfile,delimiter="|")
            writer.writerow(firstrow)
            for item in read_list:
                # print(i)
                if int(item[parm]) <= end and int(item[parm]) > begin:
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
            return  
        
        reader = csv.DictReader(table.open("r",newline=""),delimiter="|")
        read_list = []
        for i in reader:
            read_list.append(i)
        with open(table,"w",newline="") as csvfile:    
            writer = csv.writer(csvfile,delimiter="|")
            writer.writerow(firstrow)
            for item in read_list:
                if operator == "=" and item[begin] == end:
                    item[left] = right
                elif operator == ">" and item[begin] > end:
                    item[left] = right
                elif operator == "<" and item[begin] < end:
                    item[left] = right
                elif operator == ">=" and item[begin] >= end:
                    item[left] = right
                elif operator == "<=" and item[begin] <= end:
                    item[left] = right
                else:
                    pass
                writer.writerow(item.values())

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
                    






