from pathlib import Path
import csv

base_dir = Path(__file__).cwd()
data = base_dir.joinpath("data")

def create_database(database_name):
    """
        database_name : 数据库的名字 type: str
        创建一个数据库，一个数据库就是一个文件夹
    """
    global data
    database = data.joinpath(database_name)
    if database.exists() and database.is_file():
        return
    database.mkdir()

def drop_database(database_name):
    """
        database_name : 数据库的名字 type: str
        删除一个数据库，一个数据库就是一个文件夹
    """
    global data
    database = data.joinpath(database_name)
    if not database.exists():
        print("ERROR 1008 (HY000): Can't drop database 'dkfj'; database doesn't exist")
        return
    # 先删除文件里面的所有文件，然后删除该目录，  ==========> 完成删除数据库的功能
    for child in database.iterdir():
        if child is not None:
            child.unlink()
    database.rmdir()
    # TODO 修改输出 语句
    #print("Query OK, 12 rows affected (0.22 sec)")

def show_databases():
    """
        显示所有数据库
    """
    global data
    # 22 
    databases_str = "DATABASES:\n"
    for child in data.iterdir():
        if(child.is_dir()):
            databases_str += child.name+"\n"
    count = len([child for child in data.iterdir() if child.is_dir()])        
    databases_str += str(count) + " rows in set"
    print(databases_str)

def use_database(database_name):
    global data
    current_database_name = data.joinpath(database_name)
    if current_database_name.exists():
        return current_database_name.name
    print("ERROR : Unknown database " + database_name)
    return None

def create_table(current_database_name,table_name,parms):
    if current_database_name == None:
        print("ERROR : No database selected")
        return
    global data
    table = data.joinpath(current_database_name,table_name + ".csv")
    table.touch()

    # 要写入的键
    keys = []
    # 根据参数 写入CSV文件
    parm_list = parms.split(",")
    for item in parm_list:
        keys.append(item.split(" ")[0])

    with open(table,"a",newline="") as csvfile:
        writer = csv.writer(csvfile,delimiter="|")
        writer.writerow(keys)

    