from PyQt5 import QtWidgets, QtGui,QtCore
from ui_py_files.main_window import Ui_MainWindow
from ui_py_files.first_add_window import Ui_Form4
from ui_py_files.choose_film_window import Ui_Form
from ui_py_files.warning_window import Ui_Form5
from PyQt5.QtGui import QDesktopServices
from ui_py_files.list_of_films_window import Ui_Form2
from ui_py_files.film_window import Ui_Form3
from ui_py_files.second_add_window import Ui_Form6
from ui_py_files.success_window import Ui_Form7
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QFileDialog
import multiprocessing
from bot import send_message, bot_start
import random 
import sys
import sqlite3
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from PIL import Image


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.first_add_window)
        self.ui.pushButton.clicked.connect(self.close)
        self.ui.pushButton_2.clicked.connect(self.open_choose_film_window)
        self.ui.pushButton_2.clicked.connect(self.close)
       
    def main_window(self, check):
        self.ui = mywindow()
        self.ui.show()
        if check == "ui4":
            self.ui4.close()
        else:
            self.ui8.close()

    def first_add_window(self):
        self.ui5 = mywindow5()
        self.ui5.show()
        self.ui5.ui5.pushButton.clicked.connect(self.checking)


    def checking(self):
        if self.ui5.ui5.lineEdit.text() == "":
            warning_text = "Вы не ввели название фильма"
            self.ui6 = mywindow6(warning_text)
            self.ui6.show()
            return False
        if self.ui5.ui5.lineEdit_2.text() == "":
            warning_text = "Вы не ввели год"
            self.ui6 = mywindow6(warning_text)
            self.ui6.show()
            return False
        if self.ui5.ui5.lineEdit_3.text() == "":
            warning_text = "Вы не ввели страну"
            self.ui6 = mywindow6(warning_text)
            self.ui6.show()
            return False
        if self.ui5.ui5.lineEdit_4.text() == "":
            warning_text = "Вы не ввели возрастное ограничение"
            self.ui6 = mywindow6(warning_text)
            self.ui6.show()
            return False
        if self.ui5.ui5.lineEdit_5.text() == "":
            warning_text = "Вы не ввели жанр"
            self.ui6 = mywindow6(warning_text)
            self.ui6.show()
            return False    
        if self.ui5.ui5.lineEdit_6.text() == "":
            warning_text = "Вы не ввели рейтинг"
            self.ui6 = mywindow6(warning_text)
            self.ui6.show()
            return False
        if self.ui5.ui5.lineEdit_7.text() == "":
            warning_text = "Вы не ввели длительность"
            self.ui6 = mywindow6(warning_text)
            self.ui6.show()
            return False
        else:
            self.second_add_window()


    def second_add_window(self):
        self.name = self.ui5.ui5.lineEdit.text()
        self.year = self.ui5.ui5.lineEdit_2.text()
        self.country = self.ui5.ui5.lineEdit_3.text()
        self.age = self.ui5.ui5.lineEdit_4.text()
        self.genre = self.ui5.ui5.lineEdit_5.text()
        self.rating = self.ui5.ui5.lineEdit_6.text()
        self.duration = self.ui5.ui5.lineEdit_7.text()
        self.ui5.close()
        self.ui7 = mywindow7()
        self.ui7.show()
        self.ui7.ui7.pushButton_2.clicked.connect(self.add_image)
        self.ui7.ui7.pushButton.clicked.connect(self.success)


    def success(self):
        actors = self.ui7.ui7.lineEdit.text()
        description = self.ui7.ui7.lineEdit_2.text()
        url_trailer = self.ui7.ui7.lineEdit_4.text()
        url_watch = self.ui7.ui7.lineEdit_5.text()
        self.photo = self.ui7.ui7.pushButton_2.text()
        if self.photo == "выбрать":
            self.photo = ""
        else:
            self.saiving_photo()
        self.data = (self.name, self.year, self.country, self.age, self.genre, self.rating, self.duration, actors, description, self.photo, url_trailer, url_watch)
        send_message(self.data)
        self.ui7.close()
        name = "film.sqlite"
        con = sqlite3.connect(name)
        cur = con.cursor()
        request = """INSERT INTO films VALUES(?, '', ?, '', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        cur.execute(request, self.data)
        con.commit()
        con.close()
        self.ui8 = mywindow8()
        self.ui8.show()
        self.ui8.ui8.pushButton.clicked.connect(lambda: self.main_window('ui8'))

    def saiving_photo(self):
        content = open(self.photo, "rb").read()
        out = open(f"pictures_for_films/{self.name}.jpg", "wb")
        out.write(content)
        width = 330
        img = Image.open(f"pictures_for_films/{self.name}.jpg")
        width_percent = (width / float(img.size[0]))
        height = int((float(img.size[1]) * float(width_percent)))
        img = img.resize((width, height))
        img.save(f"pictures_for_films/{self.name}.jpg")
        out.close()
        
    def add_image(self):
        fname = QFileDialog.getOpenFileName(
        self, 'Выбрать картинку', '',
        'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')[0]
        if fname:
            self.ui7.ui7.pushButton_2.setText(fname)
            self.photo = fname

    def open_choose_film_window(self):
        self.ui2 = mywindow2()
        self.ui2.show()
        self.ui2.ui2.pushButton.clicked.connect(self.open_show_films_window)
        self.ui2.ui2.pushButton.clicked.connect(self.ui2.close)

         
    def open_show_films_window(self):
        combo_text = {"genre": self.ui2.ui2.comboBox.currentText(), "years": self.ui2.ui2.comboBox_2.currentText(), "country": self.ui2.ui2.comboBox_3.currentText(), "duration": self.ui2.ui2.comboBox_4.currentText()}
        film_names = self.db_search(combo_text)
        self.ui3 = mywindow3(film_names)
        self.ui3.show()
        if self.ui3.ui3.pushButton.text() is not None:
            self.ui3.ui3.pushButton.clicked.connect(lambda: self.film_window(self.ui3.ui3.pushButton.text()))
            self.ui3.ui3.pushButton.clicked.connect(self.ui3.close)
        if self.ui3.ui3.pushButton_2.text() is not None:
            self.ui3.ui3.pushButton_2.clicked.connect(lambda: self.film_window(self.ui3.ui3.pushButton_2.text()))
            self.ui3.ui3.pushButton_2.clicked.connect(self.ui3.close)
        if self.ui3.ui3.pushButton_3.text() is not None:
            self.ui3.ui3.pushButton_3.clicked.connect(lambda: self.film_window(self.ui3.ui3.pushButton_3.text()))
            self.ui3.ui3.pushButton_3.clicked.connect(self.ui3.close)
        if self.ui3.ui3.pushButton_4.text() is not None:
            self.ui3.ui3.pushButton_4.clicked.connect(lambda: self.film_window(self.ui3.ui3.pushButton_4.text()))
            self.ui3.ui3.pushButton_4.clicked.connect(self.ui3.close)
        if self.ui3.ui3.pushButton_5.text() is not None:
            self.ui3.ui3.pushButton_5.clicked.connect(lambda: self.film_window(self.ui3.ui3.pushButton_5.text()))
            self.ui3.ui3.pushButton_5.clicked.connect(self.ui3.close)


    def db_search(self, text):
        name = "film.sqlite"
        con = sqlite3.connect(name)
        cur = con.cursor()
        request = "SELECT * FROM films"
        count = 0
        if text["genre"] != "любой" or text["years"] != "любой" or text["country"] != "любая" or text["duration"] != "любая":
            request += " WHERE"
        if text["genre"] != "любой":
            request += f" genres LIKE '%{text['genre']}%'"
            count += 1
        if text["years"] != "любой":
            if count > 0:
                request += " AND"
            beg = int(text["years"].split("-")[0])
            end = int(text["years"].split("-")[1])
            request += f" year > {beg} AND year < {end}"
            count += 1
        if text["country"] != "любая":
            if count > 0:
                request += " AND"
            request += f" country = '{text['country']}'"
            count += 1
        if text["duration"] != "любая":
            if count > 0:
                request += " AND"
            if text["duration"][0] == '>':
                beg = int(text["duration"][1:4])
                request += f" duration > {beg}"
            else:
                beg = int(text["duration"].split("-")[0])
                end = int(text["duration"].split("-")[1][:4])
                request += f" duration >= {beg} AND duration <= {end}"
            count += 1  
        result  = cur.execute(request).fetchall()
        result = [item[0] for item in result]
        random.shuffle(result)
        return result[:5]
    

    def film_window(self, film):
        name = "film.sqlite"
        con = sqlite3.connect(name)
        cur = con.cursor()
        request = f"SELECT * FROM films WHERE film LIKE '{film}'"
        result  = list(cur.execute(request).fetchone())
        self.ui4 = mywindow4(result)
        self.ui4.show()
        self.ui4.ui4.pushButton_3.clicked.connect(lambda: self.main_window('ui4'))
        if result [12] is not None:
            self.ui4.ui4.pushButton.clicked.connect(lambda: self.open_url(result[12]))
        if result [13] is not None:
            self.ui4.ui4.pushButton_2.clicked.connect(lambda: self.open_url(result[13]))

    def open_url(self, url):
        QDesktopServices.openUrl(QUrl(url))

class mywindow2(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow2, self).__init__()
        self.ui2 = Ui_Form()
        self.ui2.setupUi(self)

class mywindow3(QtWidgets.QMainWindow):
    def __init__(self, film_names):
        super(mywindow3, self).__init__()
        self.ui3 = Ui_Form2()
        self.ui3.setupUi(self)
        if len(film_names) > 0:
            self.ui3.pushButton.setText(film_names[0])
        if len(film_names) > 1:
            self.ui3.pushButton_2.setText(film_names[1])
        if len(film_names) > 2:
            self.ui3.pushButton_3.setText(film_names[2])
        if len(film_names) > 3:
            self.ui3.pushButton_4.setText(film_names[3])
        if len(film_names) > 4:
            self.ui3.pushButton_5.setText(film_names[4])


class mywindow4(QtWidgets.QMainWindow):
    def __init__(self, film_params):
        super(mywindow4, self).__init__()
        self.ui4 = Ui_Form3()
        self.ui4.setupUi(self)
        self.ui4.label_2.setText(film_params[0])
        self.ui4.label_5.setText(str(film_params[2]))
        self.ui4.label_9.setText(film_params[4])
        self.ui4.label_10.setText(film_params[6])
        self.ui4.label_11.setText(film_params[8])
        self.ui4.label_15.setText(film_params[7])
        self.ui4.label_13.setText(film_params[5])
        path = f"pictures_for_films/{film_params[0]}.jpg"
        self.ui4.label.setPixmap(QtGui.QPixmap(path))
        self.ui4.textEdit.setText(film_params[9])
        self.ui4.textEdit_2.setText(film_params[10])

class mywindow5(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow5, self).__init__()
        self.ui5 = Ui_Form4()
        self.ui5.setupUi(self)

class mywindow6(QtWidgets.QMainWindow):
    def __init__(self, warning):
        super(mywindow6, self).__init__()
        self.ui6 = Ui_Form5()
        self.ui6.setupUi(self)
        self.ui6.label.setText(warning)

class mywindow7(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow7, self).__init__()
        self.ui7 = Ui_Form6()
        self.ui7.setupUi(self)

class mywindow8(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow8, self).__init__()
        self.ui8 = Ui_Form7()
        self.ui8.setupUi(self)

if __name__ == '__main__':
    process = multiprocessing.Process(target=bot_start)
    process.start()
    app = QtWidgets.QApplication(sys.argv)
    w = mywindow()
    w.show()
    sys.exit(app.exec_())