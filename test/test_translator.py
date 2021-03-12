import unittest
import app.translator as translator

import logging
logging.basicConfig(level=logging.DEBUG)


class TestingApi(unittest.TestCase):

    def test_hello_world_translation(self):
        translation = translator.translate("Bonjour", dest_lang='en', src_lang='fr')
        self.assertEqual('Hello', translation)

    def test_json_translation(self):
        test_dict = {
            "test": {"test": "Bonjour"}
        }
        result_dict = {
            "test": {"test": "Hello"}
        }
        translation = translator.translate_json(test_dict, dest_lang='en', src_lang='fr')
        self.assertEqual(result_dict, test_dict)

    def test_json_translation_with_protected_text(self):
        test_dict = {
            "test": {"test": "Bonjour {Bonjour}"}
        }
        result_dict = {
            "test": {"test": "Hello {Bonjour}"}
        }
        translation = translator.translate_json(test_dict, dest_lang='en', src_lang='fr', regex="\{.*?\}")
        self.assertEqual(result_dict, test_dict)
