#!/usr/bin/python3

import gui
import pyperclip
import sys
from google_trans_new import google_translator
import google_trans_new
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QApplication, QFileDialog


class Main(QMainWindow, gui.Ui_Ztranslator):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setupUi(self)
        self.textEdit.clear()
        self.add_language()

        self.is_checked = True
        self.checkBox.setChecked(True)
        self.comboBox.setDisabled(True)

        self.pushButton.clicked.connect(self.translate)
        self.pushButton_2.clicked.connect(self.clear)
        self.pushButton_3.clicked.connect(self.copy)
        self.checkBox.stateChanged.connect(self.toggle)

        self.actionOpen.triggered.connect(self.open_file_browser_dialogue)
        self.actionSave.triggered.connect(self.saveFileDialog)
        self.actionCopy.triggered.connect(self.copy)

    def add_language(self):
        for lang in google_trans_new.LANGUAGES.values():
            self.comboBox.addItem(lang.capitalize())
            self.comboBox_2.addItem(lang.capitalize())

    def translate(self):
        try:
            self.pushButton.setCursor(QtCore.Qt.BusyCursor)
            text_1 = self.textEdit.toPlainText()
            if self.is_checked:
                lang_2 = self.comboBox_2.currentText()
                langs = list(google_trans_new.LANGUAGES.values())
                codes = list(google_trans_new.LANGUAGES.keys())
                dst_lng = codes[langs.index(lang_2.lower())]

                translator = google_translator()
                src_lang = translator.detect(text_1)
                translate = translator.translate(text_1, lang_tgt=dst_lng)
                self.label_4.setText(
                    f"Auto detected: {src_lang[1].capitalize()}")
                self.label_4.adjustSize()

            else:
                lang_1 = self.comboBox.currentText()
                lang_2 = self.comboBox_2.currentText()
                langs = list(google_trans_new.LANGUAGES.values())
                codes = list(google_trans_new.LANGUAGES.keys())
                src_lang = codes[langs.index(lang_1.lower())]
                dst_lng = codes[langs.index(lang_2.lower())]

                translator = google_translator()
                translate = translator.translate(
                    text_1, lang_src=src_lang, lang_tgt=dst_lng
                )
                self.label_4.setText("")

            self.textEdit_2.setText(translate)
            self.pushButton.setCursor(QtCore.Qt.PointingHandCursor)

        except Exception as e:
            self.error_message(e)

    def error_message(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setText(str(text))
        msg.exec_()

    def clear(self):
        self.textEdit.clear()

    def copy(self):
        pyperclip.copy(self.textEdit_2.toPlainText())
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Copied")
        msg.setText("Translated text has been copied to your clipboard.")
        msg.exec_()

    def toggle(self, checked):
        if checked:
            self.comboBox.setDisabled(True)
            self.is_checked = True

        else:
            self.comboBox.setDisabled(False)
            self.is_checked = False

    def open_file(self, path):
        with open(path, encoding="utf-8") as f:
            txt = f.read()
            self.textEdit.setText(str(txt))

    def save_file(self, path):
        if not path.endswith(".txt"):
            path = path + ".txt"
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(self.textEdit_2.toPlainText()))

    def open_file_browser_dialogue(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open Text File", "", "Text Files (*.txt)", options=options
        )
        if fileName:
            self.open_file(fileName)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save Translation To a File",
            "",
            "Text Files (*.txt)",
            options=options
        )
        if fileName:
            self.save_file(fileName)


if __name__ == "__main__":
    a = QApplication(sys.argv)
    app = Main()
    app.show()
    a.exec_()
