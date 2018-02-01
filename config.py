from PyQt5.QtCore import QSettings, QFile, QVariant


class Config(QSettings):
    def __init__(self):
        super().__init__("config.ini", QSettings.IniFormat)

        if not QFile("config.ini").exists():
            self.set_defaults()
        self.read_cfg()

    def set_defaults(self):

        self.appname = "Telegram Bot"
        self.version = "v0.3"
        self.language = 1
        self.bot_token = ""
        self.notifications_toggle = 1
        self.window_width = 800
        self.window_height = 600

        self.setValue("appname", self.appname)
        self.setValue("version", self.version)
        self.setValue("language", self.language)
        self.setValue("bot_token", self.bot_token)
        self.setValue("notifications_toggle", self.notifications_toggle)
        self.setValue("window_width", self.window_width)
        self.setValue("window_height", self.window_height)

        self.sync()

    def read_cfg(self):

        self.sync()

        self.appname = self.value("appname")
        self.version = self.value("version")
        self.language = int(self.value("language"))
        self.bot_token = self.value("bot_token")
        self.notifications_toggle = int(self.value("notifications_toggle"))
        self.window_width = int(self.value("window_width"))
        self.window_height = int(self.value("window_height"))

    def write_cfg(self):

        self.setValue("appname", self.appname)
        self.setValue("version", self.version)
        self.setValue("language", self.language)
        self.setValue("bot_token", self.bot_token)
        self.setValue("notifications_toggle", self.notifications_toggle)
        self.setValue("window_width", self.window_width)
        self.setValue("window_height", self.window_height)

        self.sync()
