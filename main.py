from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout, QLabel, QLineEdit,
                             QVBoxLayout, QGroupBox, QTabWidget)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
import qdarkstyle
import resources.resources as Res
import constants
import sys

Res.qInitResources()


class MainPage(QWidget):


    def __init__(self):
        super().__init__(flags=Qt.Widget)

        self.startButton = QPushButton('Start')
        self.startButton.clicked.connect(self.startButtonPressed)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.startButton, alignment=Qt.AlignBottom)

        self.setLayout(main_layout)
        self.token_value = ''

    def startButtonPressed(self):
        print(self.token_value)

    def make_connection(self, connected_object):
        connected_object.tokenValue.connect(self.get_token_value)

    @pyqtSlot('QString')
    def get_token_value(self, val):
        self.token_value = val


class SettingsPage(QWidget):

    tokenValue = pyqtSignal('QString')

    def __init__(self):
        super().__init__(flags=Qt.Widget)

        self.tokenLabel = QLabel('Token:')

        self.tokenEdit = QLineEdit()
        self.tokenEdit.editingFinished.connect(self.token_edit_complete)
        token_layout = QVBoxLayout()
        token_layout.addWidget(self.tokenLabel, alignment=Qt.AlignLeft)
        token_layout.addWidget(self.tokenEdit, alignment=Qt.Alignment())

        self.tokenGroup = QGroupBox('Bot Settings')
        self.tokenGroup.setLayout(token_layout)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.tokenGroup, alignment=Qt.AlignTop)

        self.setLayout(main_layout)

    def token_edit_complete(self):
        self.tokenValue.emit(self.tokenEdit.text())


class MainWidget(QWidget):

    def __init__(self):
        super().__init__(flags=Qt.Widget)

        self.tabs = QTabWidget()
        main_page = MainPage()
        settings_page = SettingsPage()
        main_page.make_connection(settings_page)
        self.tabs.addTab(main_page, QIcon(":/home"), 'Home')
        self.tabs.addTab(settings_page,QIcon(":/settings"), 'Settings')

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.tabs, alignment=Qt.Alignment())
        self.setLayout(main_layout)


class MainWindow(QMainWindow):

    def __init__(self, center):
        super().__init__(flags=Qt.Window)

        self.setGeometry(center[0]-constants.mainWindowWidth/2,
                         center[1]-constants.mainWindowHeight/2,
                         constants.mainWindowWidth, constants.mainWindowHeight)
        self.setWindowIcon(QIcon(":/icon"))
        self.setCentralWidget(MainWidget())
        self.show()


def get_desktop_center(qapp):
    screen_geo = qapp.desktop().screenGeometry(qapp.desktop().primaryScreen()).center()
    return screen_geo.x(), screen_geo.y()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainWindow = MainWindow(get_desktop_center(app))
    sys.exit(app.exec_())
