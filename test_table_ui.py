
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(910, 556)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(0, 0, 911, 471))
        self.tableView.setObjectName("tableView")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 470, 911, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.add_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.add_button.setObjectName("add_button")
        self.horizontalLayout.addWidget(self.add_button)
        self.delete_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.delete_button.setObjectName("delete_button")
        self.horizontalLayout.addWidget(self.delete_button)
        self.apply_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.apply_button.setObjectName("apply_button")
        self.horizontalLayout.addWidget(self.apply_button)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 910, 23))
        self.menubar.setObjectName("menubar")
        self.connect_menus = QtWidgets.QMenu(self.menubar)
        self.connect_menus.setObjectName("connect_menus")
        self.databases_menus = QtWidgets.QMenu(self.menubar)
        self.databases_menus.setObjectName("databases_menus")
        self.tables_menus = QtWidgets.QMenu(self.menubar)
        self.tables_menus.setObjectName("tables_menus")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionconnect = QtWidgets.QAction(MainWindow)
        self.actionconnect.setObjectName("actionconnect")
        self.actionnull_1 = QtWidgets.QAction(MainWindow)
        self.actionnull_1.setObjectName("actionnull_1")
        self.actionclose = QtWidgets.QAction(MainWindow)
        self.actionclose.setObjectName("actionclose")
        self.actionnull_2 = QtWidgets.QAction(MainWindow)
        self.actionnull_2.setObjectName("actionnull_2")
        self.actionnull_3 = QtWidgets.QAction(MainWindow)
        self.actionnull_3.setObjectName("actionnull_3")
        self.actionnull_4 = QtWidgets.QAction(MainWindow)
        self.actionnull_4.setObjectName("actionnull_4")
        self.actionnull_5 = QtWidgets.QAction(MainWindow)
        self.actionnull_5.setObjectName("actionnull_5")
        self.connect_menus.addAction(self.actionconnect)
        self.connect_menus.addAction(self.actionclose)
        self.databases_menus.addAction(self.actionnull_1)
        self.databases_menus.addAction(self.actionnull_5)
        self.tables_menus.addAction(self.actionnull_3)
        self.tables_menus.addAction(self.actionnull_4)
        self.menubar.addAction(self.connect_menus.menuAction())
        self.menubar.addAction(self.databases_menus.menuAction())
        self.menubar.addAction(self.tables_menus.menuAction())

        self.retranslateUi(MainWindow)
        self.actionconnect.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.add_button.setText(_translate("MainWindow", "add"))
        self.delete_button.setText(_translate("MainWindow", "delete"))
        self.apply_button.setText(_translate("MainWindow", "apply"))
        self.connect_menus.setTitle(_translate("MainWindow", "连接"))
        self.databases_menus.setTitle(_translate("MainWindow", "数据库"))
        self.tables_menus.setTitle(_translate("MainWindow", "表"))
        self.actionconnect.setText(_translate("MainWindow", "connect"))
        self.actionnull_1.setText(_translate("MainWindow", "null"))
        self.actionclose.setText(_translate("MainWindow", "close"))
        self.actionnull_2.setText(_translate("MainWindow", "null"))
        self.actionnull_3.setText(_translate("MainWindow", "null"))
        self.actionnull_4.setText(_translate("MainWindow", "null"))
        self.actionnull_5.setText(_translate("MainWindow", "null"))
        
    def show_inputDialog(self):
        username,ok = QtWidgets.QInputDialoggetText(self,"Input Dialog","Enter your username:")
        pass


    def add_operate(self,event):
        print("your clicked!")

def main():
    pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    mainwindow = QtWidgets.QMainWindow()
    Ui_MainWindow().setupUi(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())
