import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import time 
from pathlib import Path
import csv
import socket
from functools import partial  


current_database_name = None
current_table_name = None

ip = None
port = None
username = None
password = None

client = None  # 客户端的套接字


class Min_Gui_Client(QMainWindow):
    def __init__(self,parent=None):
        super(Min_Gui_Client,self).__init__()
        self.initUI()

    def initUI(self):
        
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        
        self.menuBar = QMenuBar(self)
        self.connect_menu = QMenu("连接")
        self.connect_action = QAction("建立连接")
        self.close_action = QAction("断开连接")
        self.connect_menu.addAction(self.connect_action)
        self.connect_menu.addAction(self.close_action)
        
        self.database_menu = QMenu("数据库")

        self.table_menu = QMenu("表")

        self.menuBar.addMenu(self.connect_menu)
        self.menuBar.addMenu(self.database_menu)
        self.menuBar.addMenu(self.table_menu)



        # self.model=QStandardItemModel(20,10)
        # #设置水平方向四个头标签文本内容
        # self.model.setHorizontalHeaderLabels(['标题1','标题2','标题3','标题4'])
        # self.model.appendRow([
        #     QStandardItem('row %s,column %s' % (0,0)),
        #     QStandardItem('row %s,column %s' % (0,1)),
        #     QStandardItem('row %s,column %s' % (0,2)),
        #     QStandardItem('row %s,column %s' % (0,3)),
        # ])
        # for row in range(4):
        #     for column in range(4):
        #         item=QStandardItem('row %s,column %s'%(row,column))
        #         #设置每个位置的文本值
        #         self.model.setItem(row,column,item)

        #实例化表格视图，设置模型为自定义的模型
        self.tableView=QTableView()
        self.tableView.horizontalHeader().setStretchLastSection(True)    
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tableView.setModel(self.model)

        self.add_button = QPushButton("添加数据")
        self.delete_button = QPushButton("删除数据")
        self.apply_button = QPushButton("确认修改并应用")

        # 在下面的 版中添加组件即可
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.menuBar)
        self.layout.addWidget(self.tableView)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.apply_button)

        self.main_widget.setLayout(self.layout)
        self.setWindowTitle('微型数据库查询工具')
        self.resize(910, 556)
        self.show()

        self.connect_action.triggered.connect(self.show_dialog)
        self.close_action.triggered.connect(self.close_connect)

        self.add_button.clicked.connect(self.add_row)
        self.delete_button.clicked.connect(self.delete_row)
        self.apply_button.clicked.connect(self.apply_app)

    def add_row(self,event):
        try:
            col_count = self.model.columnCount()
            self.model.appendRow([QStandardItem("") for i in range(col_count)])
        except:
            pass

    def delete_row(self,event):
        try:
            selections = self.tableView.selectionModel()
            selectedList = selections.selectedRows()
            self.model.removeRow(selectedList[0].row())
    
        # for r in selectedList:
        #     rows.append(r.row())
        # if len(rows) == 0:
        #     rows.append(curow)
        #     self.removeRows(rows, isdel_list = 1)
        # pass
        except:
            pass

    def apply_app(self,event):
        try:
            # 得到所有表格中的数据
            # 将所有的数据发送给 服务器
            # 服务器 将所有的内容写入表中
        
        # print(self.model.horizontalHeaderItem(1).text())
        # self.model.item(1,1).text()
        # 行数
            row_count = self.model.rowCount()
            col_count = self.model.columnCount()

            content = ""
            header = ("|".join([self.model.horizontalHeaderItem(i).text() for i in range(col_count)])) + "\n"
            content += header
            for i in range(row_count):
                string = ("|".join([self.model.item(i,j).text() for j in range(col_count)])) + "\n"
                content += string

            # print(content)

            global current_database_name
            global current_table_name
            # print(current_database_name)
            # print(current_table_name)
            client.recv(4096)
            client.send(("apply {} {} {};".format(current_database_name,current_table_name,content)).encode("utf-8"))
            client.recv(4096)
            # print(receive_message)
        except:
            pass

    def show_dialog(self,event):
        dialog = MyDialog(self,self)

    def close_connect(self,event):
        print(event)

    def modifiy_databases(self):
        global ip
        global port 
        global username
        global password
        global client 
        if client == None:
            return
        client.send("show databases;".encode("utf-8"))
        databases = client.recv(4096).decode("utf-8").split("\n")[1:-3]
        client.send("".encode("utf-8"))
        # 先初始化一下
        self.databases_actions = []
        self.database_menu = QMenu("数据库")
        self.menuBar.addMenu(self.connect_menu)
        self.menuBar.addMenu(self.database_menu)
        self.menuBar.addMenu(self.table_menu)


        for i in databases:
            self.databases_actions.append(QAction(i))

        for action in self.databases_actions:
            self.database_menu.addAction(action)
            action.triggered.connect(partial(self.modifiy_tables, action))
              
    def modifiy_tables(self,action):
        database_name = action.text()
        global client
        client.recv(4096)
        client.send(("use %s;" % database_name).encode("utf-8"))
        client.recv(4096)
 
        client.recv(4096)   
        client.send("show tables;".encode("utf-8"))
        tables = client.recv(4096).decode("utf-8").split("\n")
         
        global current_database_name
        current_database_name = database_name
        if len(tables) <= 4:
            tables = []
        else:
            tables = tables[1:-3]
        
        self.tables_actions = []
        self.table_menu = QMenu("表")
        self.menuBar.addMenu(self.connect_menu)
        self.menuBar.addMenu(self.database_menu)
        self.menuBar.addMenu(self.table_menu)

        for table_name in tables:
            self.tables_actions.append(QAction(table_name))
        
        for action in self.tables_actions:
            self.table_menu.addAction(action)
            action.triggered.connect(partial(self.show_table,action))

    
    def show_table(self,action):
        global client
        # 接收 mysql>>>
        # client.recv(4096)
        # client.send
        # client.recv(4096) 一次循环操作
        client.recv(4096)
        client.send(("select * from {};".format(action.text())).encode("utf-8"))
        receive_message = client.recv(4096).decode("utf-8").split("\n") # 每一行是一个元素
        headtitles = receive_message[0].split(",") # 标题组成一个列表
        infos = receive_message[1:-2] # 内容列表

        global current_table_name
        current_table_name = action.text()
        self.model = QStandardItemModel()
        self.tableView.setModel(self.model)
        self.model.setHorizontalHeaderLabels(headtitles)

        for info in infos:
            row = []
            for i in info.split(","):
                row.append(QStandardItem(i))
            self.model.appendRow(row)

        
        



class MyDialog(QDialog):
    def __init__(self,main_window,parent=None):
        super(MyDialog,self).__init__(parent)
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        
        
        self.username = QLabel("Username:")
        self.password = QLabel("password:")
        self.ip = QLabel("ip:")
        self.port = QLabel("port:")

        self.ip_line = QLineEdit()
        self.port_line = QLineEdit()
        self.username_line = QLineEdit()
        self.password_line = QLineEdit()
        self.password_line.setEchoMode(QLineEdit.Password)


        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.layout = QGridLayout()

        self.layout.addWidget(self.ip,0,0)
        self.layout.addWidget(self.ip_line,0,1)
        self.layout.addWidget(self.port,1,0)
        self.layout.addWidget(self.port_line,1,1)
        self.layout.addWidget(self.username,2,0)
        self.layout.addWidget(self.username_line,2,1)
        self.layout.addWidget(self.password,3,0)
        self.layout.addWidget(self.password_line,3,1)
        self.layout.addWidget(self.buttons,4,1)

        self.setLayout(self.layout)
        self.setWindowTitle("建立连接")
        self.setGeometry(400,400,200,200)
        self.show()

        self.buttons.accepted.connect(self.accept) # 这是两个自带的函数处理
        self.buttons.rejected.connect(self.reject)

    def get_data(self):
        return (self.ip_line.text(),self.port_line.text(),self.username_line.text(),self.password_line.text())

    def accept(self):
        global username
        global password
        global ip
        global port
        global client

        ip,port,username,password = self.get_data()
        try:
            port = int(port)
        except:
            QMessageBox.warning(self,"错误","端口号不合法")
            return

        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            # client.connect(("127.0.0.1",3300))
            client.connect((ip,port))
        except:
            QMessageBox.warning(self,"错误","该主机没有开启sql服务")
            return

        receive_message = client.recv(4096).decode("utf-8")
        # client.send("root".encode("utf-8"))
        client.send(username.encode("utf-8"))
        receive_message = client.recv(4096).decode("utf-8")
        # client.send("1".encode("utf-8"))
        client.send(password.encode("utf-8"))
        
        receive_message = client.recv(4096).decode("utf-8")
        receive_message = client.recv(4096).decode("utf-8")
        # print(receive_message)
        if receive_message == "BYE":
            QMessageBox.warning(self,"错误","账号或密码错误")
            return

        
        # 如果正确，修改 数据库菜单栏 显示成功连接
        self.main_window.modifiy_databases()
        QMessageBox.information(self,"成功","连接成功")
        super().accept()



def main():
    app = QApplication(sys.argv)
    main_window = Min_Gui_Client()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
