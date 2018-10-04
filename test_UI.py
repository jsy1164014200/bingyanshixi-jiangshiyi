# import os 
# import sys

# from PyQt5.QtCore import (QFile,QVariant,Qt)
# from PyQt5.QtWidgets import (QApplication,QMainWindow,QWidget,QDialog,
# QDialogButtonBox,QMenu,QMessageBox,QTableView,QVBoxLayout)

# from PyQt5.QtSql import (QSqlDatabase,QSqlQuery,QSqlTableModel)


# class MAIN(QMainWindow):

#     def __init__(self):
#         super(MAIN,self).__init__()
#         self.mainwidget = QWidget(self)
#         self.dialog = QDialog(self.mainwidget)

#         self.model = QSqlTableModel()
#         self.model.setTable("reference")
#         self.model.setSort(1,Qt.AscendingOrder)
#         self.model.setHeaderData(1,Qt.Horizontal,"ID")
#         self.model.setHeaderData(2,Qt.Horizontal,"NAME")
#         self.model.setHeaderData(3,Qt.Horizontal,"Description")
#         self.model.setHeaderData(4,Qt.Horizontal,"AGE")
#         self.model.select()

#         self.view = QTableView()
#         self.view.setModel(self.model)
#         self.view.setSelectionMode(QTableView.SingleSelection)
#         self.view.setSelectionBehavior(QTableView.SelectRows)
#         self.view.setColumnHidden(1,True)
#         self.view.resizeColumnsToContents()

#         buttonBox = QDialogButtonBox()
#         addButton = buttonBox.addButton("&Add",QDialogButtonBox.ActionRole)
#         deleteButton = buttonBox.addButton("&Delete",QDialogButtonBox.ActionRole)
#         sortButton = buttonBox.addButton("&Sort",QDialogButtonBox.ActionRole)

#         menu = QMenu()
#         sortByNAMEAction = menu.addAction("Sort by &NAME")
#         sortByDescriptionAction = menu.addAction("Sort by &Description")
#         sortByIDAction = menu.addAction("Sort by &ID")
#         sortButton.setMenu(menu)

#         closeButton = buttonBox.addButton(QDialogButtonBox.Close)

#         layout = QVBoxLayout()
#         layout.addWidget(self.view)
#         layout.addWidget(buttonBox)

        
#         self.dialog.setLayout(layout)
#         self.setWindowTitle("HELLO!")
        
#         self.show()


# def main():
#     app = QApplication(sys.argv)
#     mainwindow = MAIN()
#     sys.exit(app.exec_())





# if __name__ == "__main__":
#     main()



import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Table(QWidget):
    def __init__(self,parent=None):
        super(Table, self).__init__(parent)
        #设置标题与初始大小
        self.setWindowTitle('QTableView表格视图的例子')
        self.resize(500,300)

        #设置数据层次结构，4行4列
        self.model=QStandardItemModel(4,4)
        #设置水平方向四个头标签文本内容
        self.model.setHorizontalHeaderLabels(['标题1','标题2','标题3','标题4'])


        # #Todo 优化2 添加数据
        # self.model.appendRow([
        #     QStandardItem('row %s,column %s' % (11,11)),
        #     QStandardItem('row %s,column %s' % (11,11)),
        #     QStandardItem('row %s,column %s' % (11,11)),
        #     QStandardItem('row %s,column %s' % (11,11)),
        # ])
        for row in range(4):
            for column in range(4):
                item=QStandardItem('row %s,column %s'%(row,column))
                #设置每个位置的文本值
                self.model.setItem(row,column,item)

        #实例化表格视图，设置模型为自定义的模型
        self.tableView=QTableView()
        self.tableView.setModel(self.model)

        # 水平方向标签拓展剩下的窗口部分，填满表格
        self.tableView.horizontalHeader().setStretchLastSection(True)
        # 水平方向，表格大小拓展到适当的尺寸      
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


        self.btn = QPushButton("print")



        layout=QVBoxLayout()
        layout.addWidget(self.tableView)
        layout.addWidget(self.btn)
        self.setLayout(layout)


        self.btn.clicked.connect(self.show_btn)

    def show_btn(self,event):
        print(self.model.horizontalHeaderItem(1).text())
        print(self.model.item(0,0).text())


if __name__ == '__main__':
    app=QApplication(sys.argv)
    table=Table()
    table.show()
    sys.exit(app.exec_())