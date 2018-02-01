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

    # signal-slot mechanism to interact with another widgets
    def make_connection(self, connected_object):
        connected_object.messageText.connect(self.show_popup)

    @pyqtSlot('QString')
    def show_popup(self, val):
        self.showMessage(cfg.appname, val)


class MainPage(QWidget):

    messageText = pyqtSignal('QString')

    def __init__(self):
        super().__init__(flags=Qt.Widget)

        # start button
        self.startButton = QPushButton(self.tr("Start"))


        # main layout of page
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.startButton, alignment=Qt.AlignBottom)

        # set layout as main
        self.setLayout(main_layout)

        # link methods with elements signals
        self.startButton.clicked.connect(self.start_button_pressed)

    def start_button_pressed(self):
        self.messageText.emit(self.tr("Bot started"))  # activate a signal to send a msg to trayicon obj
        self.startButton.setText(self.tr("Stop"))

    def make_connection(self, connected_object):
        connected_object.tokenValue.connect(self.get_token_value)   # activate a get_toke_value method when signal come

    @pyqtSlot('QString')
    def get_token_value(self, val):  # set token_value by received signal val
        self.token_value = val


class SettingsPage(QWidget):

    tokenValue = pyqtSignal('QString')  # a signal to send tokenValut to mainpage widget

    def __init__(self):
        super().__init__(flags=Qt.Widget)

        # create a token's edit block elements
        self.tokenLabel = QLabel(self.tr("Token:"))
        self.tokenEdit = QLineEdit()

        # create layout for this guys ^
        token_layout = QHBoxLayout()
        token_layout.addWidget(self.tokenLabel, alignment=Qt.AlignLeft)
        token_layout.addWidget(self.tokenEdit)

        # create a link label TODO: fix this link shit+translations
        token_link_label = QLabel('<a href="https://core.telegram.org/bots#3-how-do-i-create-a-bot">Check</a>')
        token_link_label.setOpenExternalLinks(True)

        # create layout for all token's edit group elements
        token_group_layout = QVBoxLayout()
        token_group_layout.addLayout(token_layout)
        token_group_layout.addWidget(token_link_label, alignment=Qt.AlignTop)
        token_group_layout.setContentsMargins(10, 25, 10, 25)

        # create a GroupBox for all this ^ stuff
        self.tokenGroup = QGroupBox(self.tr("Bot Settings"))
        self.tokenGroup.setLayout(token_group_layout)

        # create a language block elements
        language_label = QLabel(self.tr("Language"))
        self.languageCombBox = QComboBox()
        self.languageCombBox.currentIndexChanged.connect(self.language_combobox_changed)

        # create layout for this guys
        app_settings_layout = QHBoxLayout()
        app_settings_layout.addWidget(language_label, alignment=Qt.AlignLeft)
        app_settings_layout.addWidget(self.languageCombBox)
        app_settings_layout.setContentsMargins(10, 25, 10, 25)

        # create a group for this guys
        self.appSettingGroup = QGroupBox(self.tr("Application Settings"))
        self.appSettingGroup.setLayout(app_settings_layout)

        # create a settings page layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tokenGroup, alignment=Qt.AlignTop)
        main_layout.addWidget(self.appSettingGroup, alignment=Qt.AlignTop)

        # set this layouts as main
        self.setLayout(main_layout)

        # link methods with elements signals
        self.tokenEdit.editingFinished.connect(self.token_edit_complete)
        self.language_combobox_fill()

    def token_edit_complete(self):
        self.tokenValue.emit(self.tokenEdit.text())

    # TODO: make this shit working
    def language_combobox_changed(self, index):
        pass

    # TODO: fix this duct tape
    def language_combobox_fill(self):
        for i, lang in enumerate(trans.lang_list):
            self.languageCombBox.addItem(lang)
        self.languageCombBox.setCurrentIndex(trans.id)


class MainWidget(QWidget):

    def __init__(self):
        super().__init__(flags=Qt.Widget)

        # create a tab widget and tabs
        self.tabs = QTabWidget()

        self.main_page = MainPage()
        self.settings_page = SettingsPage()

        # set icons to the tabs
        self.create_icons()
        self.tabs.addTab(self.main_page, self.home_icon, self.tr("Home"))
        self.tabs.addTab(self.settings_page, self.settings_icon, self.tr("Settings"))
        self.tabs.setIconSize(QSize(24, 24))

        # crate main layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.tabs, alignment=Qt.Alignment())

        # set layout as main
        self.setLayout(main_layout)

        # linking main_page and settings_page with signals-slots mechanism
        self.main_page.make_connection(self.settings_page)

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

        # center window to screen and set size from cfg
        self.setGeometry(center[0]-cfg.window_width/2,
                         center[1]-cfg.window_height/2,
                         cfg.window_width, cfg.window_height)

        # creete and set central window widget
        self.mainWidget = MainWidget()
        self.setCentralWidget(self.mainWidget)

        self.setWindowIcon(QIcon(":/icon"))

        # create a trayicon widget and linking trayicon and main_page with signals-slots mechanism
        self.Tray = TrayIcon()
        self.Tray.make_connection(self.mainWidget.main_page)

        # show elements
        self.Tray.show()
        self.show()

# some duct-tape #TODO: fix this later
def get_desktop_center(qapp):
    screen_geo = qapp.desktop().screenGeometry(qapp.desktop().primaryScreen()).center()
    return screen_geo.x(), screen_geo.y()


if __name__ == "__main__":
    # create config and translator
    cfg = Config()
    trans = Translator(cfg.language)

    # create fontDB and add external font from file
    fontDB = QFontDatabase()
    fontId = fontDB.addApplicationFont(":/fonts/TitilliumWeb")

    #  init a main app #TODO: edit a stylesheet
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    app.setFont(QFont("Titillium Web", 12, weight=QFont.Normal))
    app.installTranslator(trans.translator)

    # init a mainwindow widget
    mainWindow = MainWindow(get_desktop_center(app))

    # start a main circle
    sys.exit(app.exec_())