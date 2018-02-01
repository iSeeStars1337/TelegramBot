from PyQt5.QtCore import QDir, QTranslator
import resources

# so duct taped #TODO: make it better
class Translator():

    def __init__(self, index):
        self.id = index
        self.gm_file_map = {}
        self.find_qm_files()
        self.translator = QTranslator()
        self.lang_list = []
        self.fill_lang_list()
        self.translator.load(self.get_qm_file())

    def fill_lang_list(self):
        for i in range(0, len(self.gm_file_map)):
            self.translator.load(self.gm_file_map[i])
            self.lang_list.append(self.get_lang_name())

    def find_qm_files(self):
        trans_dir = QDir(":/resources/translations")
        file_names = trans_dir.entryList(['*.qm'], QDir.Files, QDir.Name)

        gm_files = [trans_dir.filePath(fn) for fn in file_names]

        for i, qmf in enumerate(gm_files):
            self.gm_file_map[i] = qmf

    def get_qm_file(self):
        return self.gm_file_map[self.id]

    def get_lang_name(self):
        return self.translator.translate("SettingsPage", "English")

