import sqlite3
from numpy import delete
import qdarkstyle
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtUiTools import QUiLoader



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.id = 0

        loader = QUiLoader()
        self.ui = loader.load("design.ui")
        self.ui.show()

        self.connection = sqlite3.connect("database.db")
        self.my_cursor = self.connection.cursor()
        self.load_data()

        self.ui.btn_add.clicked.connect(self.add_contact)
        self.ui.btn_delete.clicked.connect(self.delete_contact)
        self.ui.btn_deleteAll.clicked.connect(self.delete_all)
        self.ui.btn_darkMode.clicked.connect(self.dark_mode)


    def load_data(self):
        self.my_cursor.execute("SELECT * FROM Contacts")
        result = self.my_cursor.fetchall()
        
        for item in result:
            self.id += 1
            check_box = QCheckBox()

            if item[1] != None and item[2] != None:
                if item[3] == None:
                    check_box.setText(f"{item[1]} {item[2]}\n{item[4]}")
                else:
                    check_box.setText(f"{item[1]} {item[2]}\n{item[3]}")
            
            elif item[1] == None and item[2] != None:
                if item[3] == None:
                    check_box.setText(f"{item[2]}\n{item[4]}")
                else:
                    check_box.setText(f"{item[2]}\n{item[3]}")

            elif item[1] != None and item[2] == None:
                if item[3] == None:
                    check_box.setText(f"{item[1]}\n{item[4]}")
                else:
                    check_box.setText(f"{item[1]}\n{item[3]}")

            self.ui.verticalLayout.addWidget(check_box)
        print("Data loaded successfully!")


    def add_contact(self):
        self.id += 1
        
        self.my_cursor.execute(f"INSERT INTO Contacts VALUES({self.id}, '{self.ui.firstName.text()}', '{self.ui.lastName.text()}', '{self.ui.mobile.text()}', '{self.ui.phone.text()}', '{self.ui.email.text()}')")
        self.connection.commit()
            
        check_box = QCheckBox()
        if self.ui.firstName.text() != "" and self.ui.lastName.text() != "":
            if self.ui.mobile.text() == "":
                check_box.setText(f"{self.ui.firstName.text()} {self.ui.lastName.text()}\n{self.ui.phone.text()}")
                self.ui.verticalLayout.addWidget(check_box)
            else:
                check_box.setText(f"{self.ui.firstName.text()} {self.ui.lastName.text()}\n{self.ui.mobile.text()}")
                self.ui.verticalLayout.addWidget(check_box)

        elif self.ui.firstName.text() == "" and self.ui.lastName.text() != "":
            if self.ui.mobile.text() == "":
                check_box.setText(f"{self.ui.lastName.text()}\n{self.ui.phone.text()}")
                self.ui.verticalLayout.addtWidget(check_box)
            else:
                check_box.setText(f"{self.ui.lastName.text()}\n{self.ui.mobile.text()}")
                self.ui.verticalLayout.addWidget(check_box)

        elif self.ui.firstName.text() != "" and self.ui.lastName.text() == "":
            if self.ui.mobile.text() == "":
                check_box.setText(f"{self.ui.firstName.text()}\n{self.ui.phone.text()}")
                self.ui.verticalLayout.addWidget(check_box)
            else:
                check_box.setText(f"{self.ui.firstName.text()}\n{self.ui.mobile.text()}")
                self.ui.verticalLayout.addWidget(check_box)

        self.ui.firstName.setText("")
        self.ui.lastName.setText("")
        self.ui.mobile.setText("")
        self.ui.phone.setText("")
        self.ui.email.setText("")


    def delete_contact(self):
        for check_box in self.ui.findChildren(QCheckBox):
            if check_box.isChecked():
                check_box.setParent(None)
                delete_info = check_box.text().split('\n')
                self.my_cursor.execute(f"DELETE FROM Contacts WHERE mobile_number = '{delete_info[1]}' OR phone_number = '{delete_info[1]}'")
                self.connection.commit()   


    def delete_all(self):
        for check_box in self.ui.findChildren(QCheckBox):
            check_box.setParent(None)
    
        self.my_cursor.execute(f"DELETE FROM Contacts")
        self.connection.commit() 


    def dark_mode(self):
        app.setStyleSheet(qdarkstyle.load_stylesheet())



app = QApplication()
main_window = MainWindow()
app.exec()
