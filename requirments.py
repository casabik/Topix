import multiprocessing
import random
import sqlite3
import sys
from PIL import ImageFile
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QFileDialog
import asyncio
import telebot
from requests import get
from bot import send_message, bot_start
from ui_py_files.choose_film_window import Ui_Form
from ui_py_files.film_window import Ui_Form3
from ui_py_files.first_add_window import Ui_Form4
from ui_py_files.list_of_films_window import Ui_Form2
from ui_py_files.main_window import Ui_MainWindow
from ui_py_files.second_add_window import Ui_Form6
from ui_py_files.success_window import Ui_Form7
from ui_py_files.warning_window import Ui_Form5

