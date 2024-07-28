from configparser import ConfigParser
import os

class TranslationManager:
    def __init__(self, language='en'):
        self.language = language
        self.translation = ConfigParser()
        self.load_translation()

    def load_translation(self):
        translations_folder = 'translations'
        translation_file = os.path.join(translations_folder, f'{self.language}.ini')
        self.translation = ConfigParser()
        if os.path.exists(translation_file):
            with open(translation_file, 'r', encoding='utf-8') as file:
                self.translation.read_file(file)
            for key in self.translation['Settings']:
                self.translation['Settings'][key] = self.translation['Settings'][key].replace('\\n', '\n')
        else:
            raise FileNotFoundError(f"Translation file {translation_file} not found.")

    def t(self, key):
        return self.translation.get('Settings', key, fallback=key)

    def change_language(self, new_language):
        self.language = new_language
        self.load_translation()

