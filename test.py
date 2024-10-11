import sys
from PyQt5.QtWidgets import QApplication, QWidget,  QFormLayout, QGridLayout, QTabWidget, QLineEdit, QDateEdit, QPushButton
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('PyQt QTabWidget')

        main_layout = QGridLayout(self)
        self.setLayout(main_layout)
        self.setFixedSize(QSize(800, 500))
        
        # create a tab widget
        tab = QTabWidget(self)
        tab.setTabShape(QTabWidget.TabShape.Triangular)
        self.setWindowTitle("Загрузка и анализ резюме из интернета") 
        
        # page загружаемые каналы
        canals_page = QWidget(self)
        layout = QFormLayout()
        canals_page.setLayout(layout)
        # self.createTable(canals_page)
        
        layout.addRow('First Name:', QLineEdit(self))
        layout.addRow('Last Name:', QLineEdit(self))
        layout.addRow('DOB:', QDateEdit(self))

        # contact pane
        summary_page = QWidget(self)
        layout = QFormLayout()
        summary_page.setLayout(layout)
        layout.addRow('Phone Number:', QLineEdit(self))
        layout.addRow('Email Address:', QLineEdit(self))

        # add pane to the tab widget
        tab.addTab(canals_page, 'Загружаемые каналы')
        tab.addTab(summary_page, 'Сводка данных')

        main_layout.addWidget(tab, 0, 0, 2, 1)
        main_layout.addWidget(QPushButton('Save'), 2, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        
        buttonCancel = QPushButton('Cancel')
        main_layout.addWidget(buttonCancel, 2, 0, alignment=Qt.AlignmentFlag.AlignRight)

        buttonCancel.clicked.connect(self.the_button_cancel)

        self.show()

        
    def the_button_cancel(self):
        print("Clicked!")
        QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())