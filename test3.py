import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSettings
import sqlite3 as sql


class DB():
    def createDB(self, nameDB):
        self.conn = sql.connect(nameDB + ".db")
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS main (table_id integer primary key, arm text, number_inv text)''')
        self.conn.commit()
        self.conn.close()

    def insertDataMain(self, nameDB, arm, number_inv):
        self.conn = sql.connect(nameDB + ".db")
        self.c = self.conn.cursor()
        self.c.execute('''INSERT INTO main (arm, number_inv) VALUES (?, ?)''', (arm, number_inv))
        self.conn.commit()
        self.conn.close()

    def viewRecords(self, nameDB):
        self.conn = sql.connect(nameDB + ".db")
        self.c = self.conn.cursor()
        self.c.execute('''SELECT arm, number_inv FROM main''')
        result = self.c.fetchall()
        self.conn.close()
        return result

    def editDB(self, nameDB, value):
        self.conn = sql.connect(nameDB + ".db")
        self.c = self.conn.cursor()
        self.c.execute('''SELECT * from main WHERE arm=?''', (value,))
        resault = self.c.fetchall()
        return resault
        

class MyTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MyTab, self).__init__()
        self.parent = parent
        self.tableWidget = QtWidgets.QTableWidget(0, 2)
        self.tableWidget.setHorizontalHeaderLabels(['Номер АРМ', 'Инвентарный номер'])
        self.tableWidget.horizontalHeader().setDefaultSectionSize(150)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        vbox = QtWidgets.QVBoxLayout(self)
        vbox.addWidget(self.tableWidget)


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.db = DB()
# ??? 
# ???         self.table = MyTab()                           # ???        

        self.centralwidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralwidget)

        self.tabWidget = QtWidgets.QTabWidget()
        count = self.tabWidget.count()
        self.nb = QtWidgets.QToolButton(text="Добавить Вкладку", autoRaise=True)
        self.nb.clicked.connect(self.addDialog)        
        self.tabWidget.insertTab(count, QtWidgets.QWidget(), "")
        self.tabWidget.tabBar().setTabButton(count, QtWidgets.QTabBar.RightSide, self.nb)

# ???        self.tabWidget.tabBarClicked.connect(self.handle_tabbar_clicked)
        
        self.btnAddRow = QtWidgets.QPushButton('ДОбавить')
        self.btnAddRow.clicked.connect(self.addRowDialog)
        self.btnEdit = QtWidgets.QPushButton('Изменить')
        self.btnEdit.clicked.connect(self.editDialog)
        self.btnExit = QtWidgets.QPushButton('Выход')
        self.btnExit.clicked.connect(self.close)
        
        self.settings = QSettings('tabsettings.ini', QSettings.IniFormat)

        self.layout = QtWidgets.QGridLayout(self.centralwidget)
        self.layout.addWidget(self.tabWidget)
        self.layout.addWidget(self.btnAddRow)
        self.layout.addWidget(self.btnEdit)
        self.layout.addWidget(self.btnExit)

        self.loadTabs()

    def new_tab(self, tabName, nameDB):
        index = self.tabWidget.count() - 1

        tabPage = MyTab(self)
        self.tabWidget.insertTab(index, tabPage, f"{tabName}")
        self.tabWidget.setCurrentIndex(index)
        self.settings.beginGroup('Tabs')
        self.settings.setValue(str(index), nameDB)
        self.settings.endGroup()
        self.db.createDB(nameDB)
        with open("tablist", "a", encoding='utf-8') as fn:
            fn.write(tabName + '\n')
# !!! +++            
        self.tabPages[index] = tabPage                                # !!! +++

    def loadTabs(self):
        with open("tablist.txt", "r", encoding='utf-8') as fn:
            tabNames = fn.read().splitlines()

# !!! +++
            self.tabPages = {}                                        # !!! +++

            for tabName in tabNames:
                index = self.tabWidget.count() - 1

                self.tabPage = MyTab()
                self.settings.beginGroup('Tabs')

                nameDB = self.settings.value(str(index))

                self.settings.endGroup()
                self.tabWidget.insertTab(index, self.tabPage, f"{tabName}")
                
# !!! +++               
                self.tabPages[index] = self.tabPage                   # !!! +++

                try:
                    data = self.db.viewRecords(nameDB)

                    self.tabPage.tableWidget.setRowCount(len(data))
                    for row, items in enumerate(data):
                        self.tabPage.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(items[0]))
                        self.tabPage.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(items[1])))
                except(TypeError):
                    None
        self.tabWidget.setCurrentIndex(0)

# !!! + ---------->       vvvvvv
    def updateTable(self, nameDB):
        index = self.tabWidget.currentIndex()
        
#        nameDB = self.settings.value(str(index))
        
        data = self.db.viewRecords(nameDB)

#        self.tabPage.tableWidget.setRowCount(len(data))
# !!! + vvvvvvv
        tabPage = self.tabPages.get(index)                               # !!! +++
        tabPage.tableWidget.setRowCount(len(data))
                
        for row, items in enumerate(data):
#            self.tabPage.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(items[0]))
#            self.tabPage.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(items[1])))
# +++       vvvvvvv
            tabPage.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(items[0])))
            tabPage.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(items[1])))

    def addDialog(self):
        self.d = QtWidgets.QDialog()
        self.d.setWindowTitle("Добавить вкладку")
        self.d.setFixedSize(400, 150)
        self.tabNameLabel = QtWidgets.QLabel("Имя Вкладки", self.d)
        self.tabNameLabel.move(10, 10)
        self.tableNameLabel = QtWidgets.QLabel("Имя базы данных", self.d)
        self.tableNameLabel.move(10, 50)
        self.tabName = QtWidgets.QLineEdit(self.d)
        self.tabName.move(180, 10)
        self.nameDB = QtWidgets.QLineEdit(self.d)
        self.nameDB.move(180, 50)
        self.pbAdd = QtWidgets.QPushButton("Добавить", self.d)
        self.pbAdd.move(200, 100)
        self.pbClose = QtWidgets.QPushButton("Закрыть", self.d)
        self.pbClose.move(300, 100)
        self.pbAdd.clicked.connect(lambda: self.new_tab(self.tabName.text(), self.nameDB.text()) or
                                           self.d.close())
        self.pbClose.clicked.connect(self.d.close)
        self.d.exec_()

    def addRowDialog(self):
        self.d = QtWidgets.QDialog()
        self.d.setWindowTitle("Добавить строку")
        self.d.setFixedSize(400, 150)
        self.labelARM = QtWidgets.QLabel('Номер АРМ', self.d)
        self.labelARM.move(10, 10)
        self.leARM = QtWidgets.QLineEdit(self.d)
        self.leARM.move(180, 10)
        self.labelInv = QtWidgets.QLabel('Инвентарный номер', self.d)
        self.labelInv.move(10, 40)
        self.leInv = QtWidgets.QLineEdit(self.d)
        self.leInv.move(180, 40)
        self.btnClose = QtWidgets.QPushButton('Закрыть', self.d)
        self.btnClose.clicked.connect(self.d.close)
        self.btnClose.move(200, 80)
        self.btnSave = QtWidgets.QPushButton('Сохранить', self.d)
        self.btnSave.clicked.connect(
            lambda: self.addRow(nameDB) or self.d.close())
        self.btnSave.move(100, 80)

        self.settings.beginGroup('Tabs')
        index = self.tabWidget.currentIndex()
        nameDB = self.settings.value(str(index))
# !!! +++
        self.settings.endGroup()                                    # !!! +++
        
        self.d.exec_()

    def addRow(self, nameDB):
        arm = self.leARM.text()
        number_inv = self.leInv.text()

        self.db.insertDataMain(nameDB, arm, number_inv)
# +++                    vvvvvv
        self.updateTable(nameDB)

    def editDialog(self):
        self.d = QtWidgets.QDialog()
        self.d.setWindowTitle("Окно")
        self.d.setFixedSize(400, 150)
        self.btnClose = QtWidgets.QPushButton('Закрыть', self.d)
        self.btnClose.move(200, 80)
        self.labelInv = QtWidgets.QLabel(self.d)
        self.labelInv.move(10, 40)
        self.labelARM = QtWidgets.QLabel(self.d)
        self.labelARM.move(10, 10)

        index = self.tabWidget.currentIndex()
        
        self.settings.beginGroup('Tabs')
        keys = self.settings.allKeys()
        
        for key in keys:
            if key == str(index):
#                indexColumn = (self.tabPage.tableWidget.selectionModel().currentIndex())
# !!! +++
                tabPage = self.tabPages.get(index)                     # !!! +++
# !!! +++                
                indexColumn = (tabPage.tableWidget.selectionModel().currentIndex())                
                

                tableData = indexColumn.sibling(indexColumn.row(), 0).data()
                nameDB = self.settings.value(str(index))
                data = self.db.editDB(nameDB, tableData)

                for item in data:
                    self.labelARM.setText(item[1])
                    self.labelInv.setText(item[2])

        self.settings.endGroup()
        self.btnClose.clicked.connect(self.d.close)
        self.d.exec_()

# ??? # ???
    '''
    def handle_tabbar_clicked(self, index):
        self.settings.beginGroup('Tabs')
        keys = self.settings.allKeys()
        print(f'\nhandle_tabbar_clicked(self, index): self.settings.allKeys() = {keys}') #
        for key in keys:
            if index == int(key):
                value = self.settings.value(key)                           # ??? 
                print(f'value={value}; index={index}')
        self.settings.endGroup()
    '''
    

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setFont(QtGui.QFont("Tahoma", 10))

    win = MyWindow()
    win.resize(500, 400)
    win.show()
    sys.exit(app.exec_())