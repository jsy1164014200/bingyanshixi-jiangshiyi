# @author jiangshiyi
# @python 3.6.4
#
#
# @time 2018.10.1
import csv
import sys
from io import StringIO
from getpass import getpass
from pathlib import Path
import re
import datetime
import time
import threading
import socket
import baseTool
import tableTool
import joinTool
import privilege



base_dir = Path(__file__).cwd()
userfile = base_dir.joinpath("user.csv")
current_database_name = None

log = base_dir.joinpath("log.txt")

affair_dir = base_dir.joinpath("affair")
current_affair_log_file = None
# 为了实现  能够事务回滚， 需要在缓存中放两个 字典列表，存放 删除的数据，以及更改的数据
insert_items = None
delete_items = None
update_items = None



user = None

def show_usage():
    print("Error usage!")
    print("Usage:python ./main.py -u | --user [user] -p | --password")
    print("Example:python ./main.py -u | --user root -p | --password")
    print("Then input your password!")




def handle_command(username,command):
    global current_database_name
    global log

    global affair_dir
    global current_affair_log_file
    global insert_items
    global delete_items
    global update_items

    with open(log,"a") as fp :
        fp.write(str(datetime.datetime.today().year) + ":" + str(datetime.datetime.today().month) + ":" + str(datetime.datetime.today().day) + ":" + str(datetime.datetime.today().hour) + ":" + str(datetime.datetime.today().minute) + ":" +"\n")
        fp.write(command+'\n')
    
    if current_affair_log_file != None:
        with open(current_affair_log_file,"a") as f:
            f.write(command+'\n')
    # 审核一下权限
    infos = None
    with open(userfile,"r",newline="") as csvfile:
        reader = csv.DictReader(csvfile,delimiter="|")
        for item in reader:
            if item["USERNAME"] == username:
                infos = item
                break
    
    database_table_list = infos["DATABASE_TABLE"].split(",")

    di = {}
    
    li = [ database_table.split(".") for database_table in database_table_list]
    # print(li)
    for i in li:
        if i[0] not in di.keys():
            di[i[0]] = []
            di[i[0]].append(i[1])
        else:
            di[i[0]].append(i[1])

    # print(di)


    is_create = int(infos["CREATE"])
    is_drop = int(infos["DROP"])
    is_insert = int(infos["INSERT"])
    is_delete = int(infos["DELETE"])
    is_update = int(infos["UPDATE"])
    is_select = int(infos["SELECT"])
    is_with_grant_option = int(infos["GRANTOPTION"])

    # 先列出所有的 匹配项
    is_create_database = re.compile(r"create database (\w+);",re.IGNORECASE).match(command)    
    is_drop_database = re.compile(r"drop database (\w+);",re.IGNORECASE).match(command)
    is_show_databases = re.compile(r"show databases;",re.IGNORECASE).match(command)
    is_use_database = re.compile(r"use (\w+);",re.IGNORECASE).match(command)
    is_create_table = re.compile(r"create table (\w+)\(([\S\s]+)\);",re.IGNORECASE).match(command)
    is_show_tables = re.compile(r"show tables;",re.IGNORECASE).match(command)
    is_drop_table = re.compile(r"drop table (\w+);",re.IGNORECASE).match(command)
    is_alter_table_addcol = re.compile(r"alter table (\w+) add column (\w+) ([\S\s]+);",re.IGNORECASE).match(command)
    is_describe_table = re.compile(r"describe (\w+)",re.IGNORECASE).match(command)

    # 下面是表的操作
    # 插入：insert into table1 values(value1,value2)
    # 删除：delete from table1 where 范围
    # 更新：update table1 set field1=value1 where 范围
    # 查找：select * from table1 where 
    is_insert_into = re.compile(r"insert into (\w+) values\(([\s\S]+)\);",re.IGNORECASE).match(command)
    is_delete_from = re.compile(r"delete from (\w+) where ([\s\S]+);",re.IGNORECASE).match(command)
    is_update_table = re.compile(r"update (\w+) set ([\s\w]+)=([\s\w]+) where ([\s\S]+);",re.IGNORECASE).match(command)

    is_select_from_no_condition = re.compile(r"select \* from (\w+);",re.IGNORECASE).match(command)
    is_select_from = re.compile(r"select ([\s\S]+) from (\w+) where ([\s\S]+);",re.IGNORECASE).match(command)
    is_select_from_limit = re.compile(r"select ([\s\S]+) from (\w+) limit ([\s\S]+);",re.IGNORECASE).match(command)
    is_select_from_order_by = re.compile(r"select ([\s\S]+) from (\w+) order by (\w+);",re.IGNORECASE).match(command)
    is_select_from_group_by = re.compile(r"select ([\s\S]+) from (\w+) group by ([\s\S]+);",re.IGNORECASE).match(command)

    # 实现连接查询
    is_inner_join = re.compile(r"select ([\s\S]+) from (\w+) inner join (\w+) on ([\s\S]+);",re.IGNORECASE).match(command)
    # 左边独有的数据 加上共有的
    is_left_join = re.compile(r"select ([\s\S]+) from (\w+) left join (\w+) on ([\s\S]+);",re.IGNORECASE).match(command)
    # 右边独有的数据，加上共有的
    is_right_join = re.compile(r"select ([\s\S]+) from (\w+) right join (\w+) on ([\s\S]+);",re.IGNORECASE).match(command)




    is_apply_database_table = re.compile(r"apply (\w+) (\w+) ([\s\S]+);",re.IGNORECASE).match(command)

    if is_apply_database_table and is_update and is_delete and is_insert:
        if current_database_name == None:
            print("ERROR : No database selected")
            return
        database_name = is_apply_database_table.group(1)
        table_name = is_apply_database_table.group(2)
        content = is_apply_database_table.group(3)

        if table_name in di.get(current_database_name,[]) or "*" in (di.get(current_database_name,[]) or di.get("*",[])):
            tableTool.apply_database_table(database_name,table_name,content)
        else:
            print("ERROR : Access denied for user '%s' to database '%s.%s'" % (username,current_database_name,table_name))

        return




    # 是否是设置用户，创建用户，设置权限的操作
    # grant all privileges on *.* to jack@'localhost' identified by "jack" with grant option;
    is_grant_privilege_on_user_host_password_is = re.compile(r"grant ([\s\S]+) on ([\s\S]+) to '(\w+)'@'([\s\S]+)' identified by '([\s\S]+)'([\s\S]*);",re.IGNORECASE).match(command)

    if is_grant_privilege_on_user_host_password_is and is_with_grant_option:
        chmod = is_grant_privilege_on_user_host_password_is.group(1).strip()
        d_t = is_grant_privilege_on_user_host_password_is.group(2).strip()
        user = is_grant_privilege_on_user_host_password_is.group(3).strip()
        host = is_grant_privilege_on_user_host_password_is.group(4).strip()
        pw = is_grant_privilege_on_user_host_password_is.group(5).strip()
        is_wgo = is_grant_privilege_on_user_host_password_is.group(6).strip()
        privilege.handle(chmod,d_t,user,host,pw,is_wgo)
        return


    # 进行事务操作
    is_begin = re.compile(r"begin;",re.IGNORECASE).match(command)
    is_commit = re.compile(r"commit;",re.IGNORECASE).match(command)
    is_rollback = re.compile(r"rollback;",re.IGNORECASE).match(command)

    if is_begin:
        hash_code = str(time.time())+".txt"
        current_affair_log_file = affair_dir.joinpath(hash_code)
        insert_items = []
        delete_items = []
        update_items = []
        return

    if is_commit:
        current_affair_log_file = None
        insert_items = None
        delete_items = None
        update_items = None
        return
    
    if is_rollback and current_affair_log_file != None:
        rollback(current_affair_log_file)
        current_affair_log_file = None
        insert_items = None
        delete_items = None
        update_items = None
        return




    # 加入权限信息
    # CREATE DATABASE database-name 实现创建一个数据库的功能  
    if is_create_database and is_create:
        database_name = is_create_database.group(1)
        baseTool.create_database(database_name)
        return

    # drop database dbname   实现删除一个数据库的功能
    if is_drop_database and is_drop:
        database_name = is_drop_database.group(1)
        baseTool.drop_database(database_name)
        return

    if is_show_databases:
        baseTool.show_databases()
        return
    
    if is_use_database:
        database_name = is_use_database.group(1)
        if database_name in di.keys() or "*" in di.keys(): 
            current_database_name = baseTool.use_database(database_name)
            if current_database_name:
                print("Database changed : "+ current_database_name)
        else:
            print("ERROR : Access denied for user '%s' to database '%s'" % (username,database_name))
        return

    if is_show_tables:
        if current_database_name == None:
            print("ERROR : No database selected")
            return 
        baseTool.show_tables(current_database_name)
        return

    if is_drop_table and is_drop:
        if current_database_name == None:
            print("ERROR : No database selected")
            return
        table_name = is_drop_table.group(1)
        if table_name in di.get(current_database_name,[]) or "*" in (di.get(current_database_name,[]) or di.get("*",[])):
            baseTool.drop_table(current_database_name,table_name)
        else:
            print("ERROR : Access denied for user '%s' to database '%s.%s'" % (username,current_database_name,table_name))
        return

        #    create table tabname(col1 type1 [not null] [primary key],col2 type2 [not null],..) 
  
    if is_create_table and is_create:
        if current_database_name == None:
            print("ERROR : No database selected")
            return
        
        table_name = is_create_table.group(1)
        parms = is_create_table.group(2)
        baseTool.create_table(current_database_name,table_name,parms)
        return

    if is_describe_table:
        if current_database_name == None:
            print("ERROR : No database selected")
            return
        table_name = is_describe_table.group(1)
        if table_name in di.get(current_database_name,[]) or "*" in (di.get(current_database_name,[]) or di.get("*",[])):
            baseTool.describe_table(current_database_name,table_name)
        else:
            print("ERROR : Access denied for user '%s' to database '%s.%s'" % (username,current_database_name,table_name))
        return

    # 基本查询功能
    # Alter table tabname add column col type
    if is_alter_table_addcol:
        if current_database_name == None:
            print("ERROR : No database selected")
            return
        table_name = is_alter_table_addcol.group(1)
        col_name = is_alter_table_addcol.group(2)
        parm = is_alter_table_addcol.group(3)
        if table_name in di.get(current_database_name,[]) or "*" in (di.get(current_database_name,[]) or di.get("*",[])):
            baseTool.alter_table_addcol(current_database_name,table_name,col_name,parm)
        else:
            print("ERROR : Access denied for user '%s' to database '%s.%s'" % (username,current_database_name,table_name))    
        return

    if is_insert_into and is_insert:
        if current_database_name == None:
            print("ERROR : No database selected")
            return
        table_name = is_insert_into.group(1)
        values = is_insert_into.group(2).split(",")
        if table_name in di.get(current_database_name,[]) or "*" in (di.get(current_database_name,[]) or di.get("*",[])):
            l = tableTool.insert_into(current_database_name,table_name,values)
            if insert_items != None:
                for i in l:
                    insert_items.append(i)
        else:
            print("ERROR : Access denied for user '%s' to database '%s.%s'" % (username,current_database_name,table_name))
        
        return

    if is_delete_from and is_delete:
        if current_database_name == None:
            print("ERROR : No database selected")
            return
        table_name = is_delete_from.group(1)
        condition = is_delete_from.group(2)
        if table_name in di.get(current_database_name,[]) or "*" in (di.get(current_database_name,[]) or di.get("*",[])):
            l = tableTool.delete_from(current_database_name,table_name,condition)
            if delete_items != None:
                for i in l:
                    delete_items.append(i)
        else:
            print("ERROR : Access denied for user '%s' to database '%s.%s'" % (username,current_database_name,table_name))
        return
    # update (\w+) set (\w+)=(\w+) where ([\s\S]+);
    if is_update_table and is_update:
        if current_database_name == None:
            print("ERROR : No database selected")
            return
        table_name = is_update_table.group(1)
        left = is_update_table.group(2).strip()
        right = is_update_table.group(3).strip()
        condition = is_update_table.group(4)
        if table_name in di.get(current_database_name,[]) or "*" in (di.get(current_database_name,[]) or di.get("*",[])):
            l = tableTool.update_table(current_database_name,table_name,left,right,condition)
            if update_items != None:
                for i in l:
                    update_items.append(i)
        else:
            print("ERROR : Access denied for user '%s' to database '%s.%s'" % (username,current_database_name,table_name))
        
        return
    
    if is_select_from_no_condition and is_select:
        if current_database_name == None:
            print("ERROR : No database selected")
            return
        table_name = is_select_from_no_condition.group(1).strip()
        if table_name in di.get(current_database_name,[]) or "*" in (di.get(current_database_name,[]) or di.get("*",[])):
            tableTool.select_from_no_condition(current_database_name,table_name)
        else:
            print("ERROR : Access denied for user '%s' to database '%s.%s'" % (username,current_database_name,table_name))
        
        return
        
    # select ([\s\S]+) from (\w+) where ([\s\S]+);
    if is_select_from and is_select:
        if current_database_name == None:
            print("ERROR : No database selected")
            return
        # 实现`limit` 限定返回条数SELECT * FROM table LIMIT 5,10;
        is_select_from_where_limit = re.compile(r"select ([\s\S]+) from (\w+) where ([\s\S]+) limit ([\s\S]+);",re.IGNORECASE).match(command)
        # 实现 限定条件下的 order by 
        is_select_from_where_order_by = re.compile(r"select ([\s\S]+) from (\w+) where ([\s\S]+) order by (\w+);",re.IGNORECASE).match(command)
        if is_select_from_where_limit:
            infos = is_select_from_where_limit.group(1)
            table_name = is_select_from_where_limit.group(2)
            condition = is_select_from_where_limit.group(3)
            limit = is_select_from_where_limit.group(4)
            if table_name in di.get(current_database_name,[]) or "*" in (di.get(current_database_name,[]) or di.get("*",[])):
                tableTool.select_from_where_limit(current_database_name,infos,table_name,condition,limit)
            else:
                print("ERROR : Access denied for user '%s' to database '%s.%s'" % (username,current_database_name,table_name))
            
            return
        
        if is_select_from_where_order_by:
            infos = is_select_from_where_order_by.group(1)
            table_name = is_select_from_where_order_by.group(2)
            condition = is_select_from_where_order_by.group(3)
            order_key = is_select_from_where_order_by.group(4)
            if table_name in di.get(current_database_name,[]) or "*" in (di.get(current_database_name,[]) or di.get("*",[])):
                tableTool.select_from_where_order_by(current_database_name,infos,table_name,condition,order_key)
            else:
                print("ERROR : Access denied for user '%s' to database '%s.%s'" % (username,current_database_name,table_name))
            
            return            

        table_name = is_select_from.group(2).strip()
        infos = is_select_from.group(1).strip()
        condition = is_select_from.group(3).strip()
        if table_name in di.get(current_database_name,[]) or "*" in (di.get(current_database_name,[]) or di.get("*",[])):
            tableTool.select_from(current_database_name,infos,table_name,condition)
        else:
            print("ERROR : Access denied for user '%s' to database '%s.%s'" % (username,current_database_name,table_name))
        
        return

    # limit查询 select ([\s\S]+) from (\w+) where ([\s\S]+) limit ([\s\S]+);
    if is_select_from_limit and is_select:
        if current_database_name == None:
            print("ERROR : No database selected")
            return
        infos = is_select_from_limit.group(1)
        table_name = is_select_from_limit.group(2)
        limit = is_select_from_limit.group(3)
        if table_name in di.get(current_database_name,[]) or "*" in (di.get(current_database_name,[]) or di.get("*",[])):
            tableTool.select_from_limit(current_database_name,infos,table_name,limit)
        else:
            print("ERROR : Access denied for user '%s' to database '%s.%s'" % (username,current_database_name,table_name))
        return
    # orderby 查询
    if is_select_from_order_by and is_select:
        if current_database_name == None:
            print("ERROR : No database selected")
            return
        infos = is_select_from_order_by.group(1)
        table_name = is_select_from_order_by.group(2)
        order_key = is_select_from_order_by.group(3)
        if table_name in di.get(current_database_name,[]) or "*" in (di.get(current_database_name,[]) or di.get("*",[])):
            tableTool.select_from_order_by(current_database_name,infos,table_name,order_key)
        else:
            print("ERROR : Access denied for user '%s' to database '%s.%s'" % (username,current_database_name,table_name))
        
        return
    # group by 查询 select ([\s\S]+) from (\w+) group by ([\s\S]+); 
    if is_select_from_group_by and is_select:
        if current_database_name == None:
            print("ERROR : No database selected")
            return
        
        is_select_from_group_by_having = re.compile(r"select ([\s\S]+) from (\w+) group by ([\s\S]+) having ([\s\S]+);",re.IGNORECASE).match(command)
        if is_select_from_group_by_having:
            infos = is_select_from_group_by_having.group(1)
            table_name = is_select_from_group_by_having.group(2)
            parms = is_select_from_group_by_having.group(3)
            condition = is_select_from_group_by_having.group(4)
            if table_name in di.get(current_database_name,[]) or "*" in (di.get(current_database_name,[]) or di.get("*",[])):
                tableTool.select_from_group_by_having(current_database_name,infos,table_name,parms,condition)
            else:
                print("ERROR : Access denied for user '%s' to database '%s.%s'" % (username,current_database_name,table_name))
            
            return
        infos = is_select_from_group_by.group(1)
        table_name = is_select_from_group_by.group(2)
        parms = is_select_from_group_by.group(3)
        if table_name in di.get(current_database_name,[]) or "*" in (di.get(current_database_name,[]) or di.get("*",[])):
            tableTool.select_from_group_by(current_database_name,infos,table_name,parms)
        else:
            print("ERROR : Access denied for user '%s' to database '%s.%s'" % (username,current_database_name,table_name))
        
        return

    # 实现连接查询 select ([\s\S]+) from (\w+) right join (\w+) on ([\s\S]+)
    if is_inner_join and is_select:
        if current_database_name == None:
            print("ERROR : No database selected")
            return
        infos = is_inner_join.group(1)
        left_table = is_inner_join.group(2)
        right_table = is_inner_join.group(3)
        condition = is_inner_join.group(4)
        if (left_table in di.get(current_database_name,[]) and right_table in di.get(current_database_name,[])) or "*" in (di.get(current_database_name,[]) or di.get("*",[])):
            joinTool.inner_join(current_database_name,infos,left_table,right_table,condition)
        else:
            print("ERROR : Access denied for user '%s' to database '%s.%s'" % (username,current_database_name,left_table))
            print("ERROR : Access denied for user '%s' to database '%s.%s'" % (username,current_database_name,right_table))
        
        return
        
    if is_left_join and is_select:
        if current_database_name == None:
            print("ERROR : No database selected")
            return
        infos = is_left_join.group(1)
        left_table = is_left_join.group(2)
        right_table = is_left_join.group(3)
        condition = is_left_join.group(4)
        if (left_table in di.get(current_database_name,[]) and right_table in di.get(current_database_name,[])) or "*" in (di.get(current_database_name,[]) or di.get("*",[])):
            joinTool.left_join(current_database_name,infos,left_table,right_table,condition)
        else:
            print("ERROR : Access denied for user '%s' to database '%s.%s'" % (username,current_database_name,left_table))
            print("ERROR : Access denied for user '%s' to database '%s.%s'" % (username,current_database_name,right_table))
        
        return
    
    if is_right_join and is_select:
        if current_database_name == None:
            print("ERROR : No database selected")
            return
        infos = is_right_join.group(1)
        left_table = is_right_join.group(2)
        right_table = is_right_join.group(3)
        condition = is_right_join.group(4)
        if (left_table in di.get(current_database_name,[]) and right_table in di.get(current_database_name,[])) or "*" in (di.get(current_database_name,[]) or di.get("*",[])):
            joinTool.right_join(current_database_name,infos,left_table,right_table,condition)
        else:
            print("ERROR : Access denied for user '%s' to database '%s.%s'" % (username,current_database_name,left_table))
            print("ERROR : Access denied for user '%s' to database '%s.%s'" % (username,current_database_name,right_table))
        
        return

    print("ERROR SYNTAX!")




def rollback(current_affair_log_file):
    # print(current_affair_log_file.name) 
    # insert into (\w+) values\(([\s\S]+)\);
    # delete from (\w+) where ([\s\S]+);
    # update (\w+) set ([\s\w]+)=([\s\w]+) where ([\s\S]+);
    #
    print(insert_items)
    print(delete_items)
    print(update_items)
    for table_data in insert_items:
        table_name,data = table_data
        handle_command("root","delete from %s where id = %s;" % (table_name,data[0]) )
    
    for table_data in delete_items:
        table_name,data = table_data
        handle_command("root","insert into %s values(%s);" % (table_name,",".join(data.values())) )

    for table_data in update_items:
        table_name,data = table_data
        handle_command("root","delete from %s where id = %s;" % (table_name,data["id"]) )
        handle_command("root","insert into %s values(%s);" % (table_name,",".join(data.values())) )

    



def main(client_socket,remote_host,remote_port):
    client_socket.send("input your username>>>".encode("utf-8"))
    username = client_socket.recv(4096).decode("utf-8")
    client_socket.send("input your password>>>".encode("utf-8"))
    password = client_socket.recv(4096).decode("utf-8")


    
    
    # if (len(sys.argv) == 4) and (sys.argv[1] == "-u" or sys.argv[1] == "--user") and (sys.argv[3] == "-p" or sys.argv[3] == "--password"):
    #     username = sys.argv[2]
    #     password = getpass("Enter your password>>>")  
    real_username = ""
    real_password = ""
    global user
    global userfile
    with open(userfile,"r",newline="") as csvfile:
        reader = csv.DictReader(csvfile,delimiter="|")
        for row in reader:
            if username == row["USERNAME"]:
                real_username = row["USERNAME"]
                real_password = row["PASSWORD"]
    # 如果用户名不存在 
    if real_password != password or real_username == "":
        client_socket.send(("ERROR : Access denied for user '%s'" % username).encode("utf-8"))
        client_socket.send("BYE".encode("utf-8"))
        return
    user = real_username
    client_socket.send("Welcome to the MySQL monitor.  Commands end with ; or \g.".encode("utf-8"))
    while(True):
        try:
            client_socket.send("mysql>>>".encode("utf-8"))
            command = client_socket.recv(4096).decode("utf-8")
            while(not command.endswith(";")):
                client_socket.send("    ->".encode("utf-8"))
                # if len(client_socket.recv(4096).decode("utf-8")) == 0:
                #     client_socket.send("    ->".encode("utf-8"))
                command += client_socket.recv(4096).decode("utf-8")
            if(command == "exit;" or command == "quit;" or command == "\q;"):
                client_socket.send("BYE".encode("utf-8"))
                return
            
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            handle_command(real_username,command)
            s = sys.stdout.getvalue()
            sys.stdout = old_stdout
            client_socket.send(s.encode("utf-8"))
            
        except:
            client_socket.close()
            pass

    # 结束的条件
    # client_socket.send("BYE".encode("utf-8"))


def server_loop(local_host,local_port):
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        server_socket.bind((local_host,local_port))
    
    except:
        print("[!!]Failed to listen on %s:%d" % (local_host,local_port))
        print("[!!]Check for other listening sockets or correct permissions.")
        sys.exit(0)
    
    try:
        server_socket.listen(10)
        print("[*]Listening on %s:%d" % (local_host,local_port))
        while True:
            client_socket,addr = server_socket.accept()
            # 打印出本地的连接信息
            print("[==>]Received incoming connection from %s:%d" % (addr[0],addr[1]))
            # 开启一个线程与远程主机进行通讯

            proxy_thread = threading.Thread(target=main,args=(client_socket,addr[0],addr[1]))
            proxy_thread.start()
    except:
        pass

def show_server_usage():
    print("Error usage!")
    print("Usage:python mysql-server.py -h|--host host -p|--port port")
    print("Example:python ./main.py -h 127.0.0.1 -p 3300")

if __name__ == "__main__":
    if len(sys.argv) == 5 and (sys.argv[1] == "-h" or sys.argv[1] == "--host") and (sys.argv[3] == "-p" or sys.argv[3] == "--port"):
        local_host = sys.argv[2]
        local_port = int(sys.argv[4])
        server_loop(local_host,local_port)
    else:
        show_server_usage()