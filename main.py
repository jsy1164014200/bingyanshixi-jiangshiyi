import csv
import sys
from getpass import getpass
import re
import baseTool

global current_database_name
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
    
    # is_create_table = re.compile(r"")

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
  
    #    create table tabname(col1 type1 [not null] [primary key],col2 type2 [not null],..) 
    if is_create_table:
        # print("===============begin====================")
        table_name = is_create_table.group(1)
        parms = is_create_table.group(2)
        baseTool.create_table(current_database_name,table_name,parms)
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