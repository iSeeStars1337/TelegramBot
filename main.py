from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout, QLabel, QLineEdit,
                             QVBoxLayout, QGroupBox, QTabWidget, QSystemTrayIcon, QMenu, QComboBox)
from PyQt5.QtGui import QIcon, QFont, QFontDatabase
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QSize
import qdarkstyle
import sys
from language import Translator
from config import Config
import  resources


class TrayIcon(QSystemTrayIcon):

    def __init__(self):
        super().__init__()
        # setting an icon from the resources.py
        self.setIcon(QIcon(":/icon"))
        # adding menu elements
        # TODO: add actions
        self.menu = QMenu()
        self.menu.addAction(self.tr("Start Bot"))
        self.menu.addAction(self.tr("Open Telegram Bot"))
        self.menu.addAction(self.tr("Disable Notifications"))
        self.menu.addSeparator()
        self.menu.addAction(self.tr("About"))
        self.menu.addAction(self.tr("Exit"))
        # setting a font from the resources.py
        self.menu.setFont(QFont("Titillium Web", 10, weight=QFont.Normal))
        # applying menu to a tray
        self.setContextMenu(self.menu)

    def make_connection(self, connected_object):
        connected_object.messageText.connect(self.show_popup)

    @pyqtSlot('QString')
    def show_popup(self, val):
        self.showMessage(cfg.appname, val)

class MainPage(QWidget):

    messageText = pyqtSignal('QString')

    def __init__(self):
        super().__init__(flags=Qt.Widget)

        self.startButton = QPushButton(self.tr("Start"))
        self.startButton.clicked.connect(self.start_button_pressed)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.startButton, alignment=Qt.AlignBottom)

        self.setLayout(main_layout)
        self.token_value = ''

    def start_button_pressed(self):
        self.messageText.emit(self.tr("Bot started"))
        self.startButton.setText(self.tr("Stop"))

    def make_connection(self, connected_object):
        connected_object.tokenValue.connect(self.get_token_value)

    @pyqtSlot('QString')
    def get_token_value(self, val):
        self.token_value = val


class SettingsPage(QWidget):

    tokenValue = pyqtSignal('QString')

    def __init__(self):
        super().__init__(flags=Qt.Widget)

        self.tokenLabel = QLabel(self.tr("Token:"))

        self.tokenEdit = QLineEdit()
        self.tokenEdit.editingFinished.connect(self.token_edit_complete)
        token_layout = QHBoxLayout()
        token_layout.addWidget(self.tokenLabel, alignment=Qt.AlignLeft)
        token_layout.addWidget(self.tokenEdit)
        token_layout.setContentsMargins(10, 25, 10, 25)

        self.tokenGroup = QGroupBox(self.tr("Bot Settings"))
        self.tokenGroup.setLayout(token_layout)

        self.languageLabel = QLabel(self.tr("Language"))

        self.languageCombBox = QComboBox()
        self.languageCombBox.currentIndexChanged.connect(self.language_combobox_changed)

        app_settings_layout = QHBoxLayout()
        app_settings_layout.addWidget(self.languageLabel)
        app_settings_layout.addWidget(self.languageCombBox)
        app_settings_layout.setContentsMargins(10, 25, 10, 25)

        self.appSettingGroup = QGroupBox(self.tr("Application Settings"))
        self.appSettingGroup.setLayout(app_settings_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tokenGroup, alignment=Qt.AlignTop)
        main_layout.addWidget(self.appSettingGroup, alignment=Qt.AlignTop)

        self.setLayout(main_layout)

        self.language_combobox_fill()

    def token_edit_complete(self):
        self.tokenValue.emit(self.tokenEdit.text())

    def language_combobox_add(self, lang_name):
        self.languageCombBox.addItem(lang_name)

    def language_combobox_changed(self, index):
        pass

    def language_combobox_fill(self):
        for i, lang in enumerate(trans.lang_list):
            self.languageCombBox.addItem(lang)
        self.languageCombBox.setCurrentIndex(trans.id)


class MainWidget(QWidget):

    def __init__(self):
        super().__init__(flags=Qt.Widget)

        self.tabs = QTabWidget()

        self.main_page = MainPage()
        self.settings_page = SettingsPage()

        self.main_page.make_connection(self.settings_page)
        # set icons to the tabs
        self.create_icons()
        self.tabs.addTab(self.main_page, self.home_icon, self.tr("Home"))
        self.tabs.addTab(self.settings_page, self.settings_icon, self.tr("Settings"))
        self.tabs.setIconSize(QSize(24, 24))

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.tabs, alignment=Qt.Alignment())
        self.setLayout(main_layout)

    def create_icons(self):

        self.home_icon = QIcon()
        self.home_icon.addFile(":/home_on", state=0)
        self.home_icon.addFile(":/home_off", state=1)

        self.settings_icon = QIcon()
        self.settings_icon.addFile(":/settings_on", state=0)
        self.settings_icon.addFile(":/settings_off", state=1)


class MainWindow(QMainWindow):

    def __init__(self, center):
        super().__init__(flags=Qt.Window)

        self.setGeometry(center[0]-cfg.window_width/2,
                         center[1]-cfg.window_height/2,
                         cfg.window_width, cfg.window_height)

        self.mainWidget = MainWidget()

        self.setWindowIcon(QIcon(":/icon"))

        self.setCentralWidget(self.mainWidget)

        self.Tray = TrayIcon()
        self.Tray.make_connection(self.mainWidget.main_page)
        self.Tray.show()
        self.show()


def get_desktop_center(qapp):
    screen_geo = qapp.desktop().screenGeometry(qapp.desktop().primaryScreen()).center()
    return screen_geo.x(), screen_geo.y()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    app.setFont(QFont("Titillium Web", 12, weight=QFont.Normal))

    cfg = Config()

    trans = Translator(cfg.language)
    app.installTranslator(trans.translator)

    fontDB = QFontDatabase()
    fontId = fontDB.addApplicationFont(":/fonts/TitilliumWeb")

    mainWindow = MainWindow(get_desktop_center(app))

    sys.exit(app.exec_())






