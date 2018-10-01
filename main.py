# @author jiangshiyi
# @python 3.6.4
#
#
# @time 2018.10.1
import csv
import sys
from getpass import getpass
import re
import baseTool
import tableTool

current_database_name = None
def show_usage():
    print("Error usage!")
    print("Usage:python ./main.py -u | --user [user] -p | --password")
    print("Example:python ./main.py -u | --user root -p | --password")
    print("Then input your password!")


def handle_command(command):
    print(command)
    global current_database_name
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
    is_select_from = re.compile(r"select ([\s\S]+) from (\w+) where ([\s\S]+);",re.IGNORECASE).match(command)
    is_select_from_limit = re.compile(r"select ([\s\S]+) from (\w+) limit ([\s\S]+);",re.IGNORECASE).match(command)
    is_select_from_order_by = re.compile(r"select ([\s\S]+) from (\w+) order by (\w+);",re.IGNORECASE).match(command)
    is_select_from_group_by = re.compile(r"select ([\s\S]+) from (\w+) group by ([\s\S]+);",re.IGNORECASE).match(command)

    # CREATE DATABASE database-name 实现创建一个数据库的功能
    if is_create_database:
        database_name = is_create_database.group(1)
        baseTool.create_database(database_name)
        return

    # drop database dbname   实现删除一个数据库的功能
    if is_drop_database:
        database_name = is_drop_database.group(1)
        baseTool.drop_database(database_name)
        return

    if is_show_databases:
        baseTool.show_databases()
        return
    
    if is_use_database:
        database_name = is_use_database.group(1)
        current_database_name = baseTool.use_database(database_name)
        if current_database_name != None:
            print("Database changed : "+ current_database_name)
        return

    if is_show_tables:
        if current_database_name == None:
            print("ERROR : No database selected")
            return 
        baseTool.show_tables(current_database_name)
        return

    if is_drop_table:
        if current_database_name == None:
            print("ERROR : No database selected")
            return
        table_name = is_drop_table.group(1)
        baseTool.drop_table(current_database_name,table_name)
        return

        #    create table tabname(col1 type1 [not null] [primary key],col2 type2 [not null],..) 
  
    if is_create_table:
        if current_database_name == None:
            print("ERROR : No database selected")
            return
        # print("===============begin====================")
        table_name = is_create_table.group(1)
        parms = is_create_table.group(2)
        baseTool.create_table(current_database_name,table_name,parms)
        return

    if is_describe_table:
        if current_database_name == None:
            print("ERROR : No database selected")
            return
        table_name = is_describe_table.group(1)
        baseTool.describe_table(current_database_name,table_name)
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
        baseTool.alter_table_addcol(current_database_name,table_name,col_name,parm)
        return

    if is_insert_into:
        if current_database_name == None:
            print("ERROR : No database selected")
            return
        table_name = is_insert_into.group(1)
        values = is_insert_into.group(2).split(",")
        tableTool.insert_into(current_database_name,table_name,values)
        return

    if is_delete_from:
        if current_database_name == None:
            print("ERROR : No database selected")
            return
        table_name = is_delete_from.group(1)
        condition = is_delete_from.group(2)
        tableTool.delete_from(current_database_name,table_name,condition)
        return
    # update (\w+) set (\w+)=(\w+) where ([\s\S]+);
    if is_update_table:
        if current_database_name == None:
            print("ERROR : No database selected")
            return
        table_name = is_update_table.group(1)
        left = is_update_table.group(2).strip()
        right = is_update_table.group(3).strip()
        condition = is_update_table.group(4)
        tableTool.update_table(current_database_name,table_name,left,right,condition)
        return
    # select ([\s\S]+) from (\w+) where ([\s\S]+);
    if is_select_from:
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
            tableTool.select_from_where_limit(current_database_name,infos,table_name,condition,limit)
            return
        
        if is_select_from_where_order_by:
            infos = is_select_from_where_order_by.group(1)
            table_name = is_select_from_where_order_by.group(2)
            condition = is_select_from_where_order_by.group(3)
            order_key = is_select_from_where_order_by.group(4)
            tableTool.select_from_where_order_by(current_database_name,infos,table_name,condition,order_key)
            return            

        table_name = is_select_from.group(2).strip()
        infos = is_select_from.group(1).strip()
        condition = is_select_from.group(3).strip()
        tableTool.select_from(current_database_name,infos,table_name,condition)
        return

    # limit查询 select ([\s\S]+) from (\w+) where ([\s\S]+) limit ([\s\S]+);
    if is_select_from_limit:
        if current_database_name == None:
            print("ERROR : No database selected")
            return
        infos = is_select_from_limit.group(1)
        table_name = is_select_from_limit.group(2)
        limit = is_select_from_limit.group(3)
        tableTool.select_from_limit(current_database_name,infos,table_name,limit)
        return
    # orderby 查询
    if is_select_from_order_by:
        if current_database_name == None:
            print("ERROR : No database selected")
            return
        infos = is_select_from_order_by.group(1)
        table_name = is_select_from_order_by.group(2)
        order_key = is_select_from_order_by.group(3)
        tableTool.select_from_order_by(current_database_name,infos,table_name,order_key)
        return
    # group by 查询 select ([\s\S]+) from (\w+) group by ([\s\S]+); 
    if is_select_from_group_by:
        if current_database_name == None:
            print("ERROR : No database selected")
            return
        
        is_select_from_group_by_having = re.compile(r"select ([\s\S]+) from (\w+) group by ([\s\S]+) having ([\s\S]+);",re.IGNORECASE).match(command)
        if is_select_from_group_by_having:
            infos = is_select_from_group_by_having.group(1)
            table_name = is_select_from_group_by_having.group(2)
            parms = is_select_from_group_by_having.group(3)
            condition = is_select_from_group_by_having.group(4)
            tableTool.select_from_group_by_having(current_database_name,infos,table_name,parms,condition)
            return
        infos = is_select_from_group_by.group(1)
        table_name = is_select_from_group_by.group(2)
        parms = is_select_from_group_by.group(3)
        tableTool.select_from_group_by(current_database_name,infos,table_name,parms)
        return

def main():
    if (len(sys.argv) == 4) and (sys.argv[1] == "-u" or sys.argv[1] == "--user") and (sys.argv[3] == "-p" or sys.argv[3] == "--password"):
        password = getpass("Enter your password>>>")
        if password == "1":
            print("Welcome to the MySQL monitor.  Commands end with ; or \g.")
            while(True):
                command = input("mysql>>>")
                if(command == "exit;" or command == "quit;" or command == "\q;"):
                    print("Bye")
                    break         
                while(not command.endswith(";")):
                    command += input("    ->")
                handle_command(command)

    else:
        show_usage()



if __name__ == "__main__":
    main()