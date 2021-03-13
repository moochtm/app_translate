# built in
import re
import uuid
import logging
# third party
from google_trans_new import google_translator

# Initialize Translator
translator = google_translator()


def translate(text, dest_lang, src_lang, protected_text_regex=None):

    protected_strings = {}
    if protected_text_regex is not None:
        logging.debug("substituting protected strings")
        logging.debug(text)
        while re.search(protected_text_regex, text):
            # get uuid, convert to integer, use only first 12 characters (dict keys get shortened problem)
            new_uuid = str(uuid.uuid1().int)[-12:]
            protected_strings[new_uuid] = re.search(protected_text_regex, text).group()
            logging.debug(protected_strings)
            text = re.sub(protected_text_regex, new_uuid, text, 1)
            logging.debug(text)

    if src_lang is not None:
        translation = translator.translate(text, dest_lang, src_lang)
    else:
        translation = translator.translate(text, dest_lang)

    if type(translation) == list:
        translation = translation[0]

    logging.debug(translation)

    if protected_strings:
        logging.debug("replacing protected strings")
        logging.debug(protected_strings)
        for k in protected_strings:
            logging.debug("checking k: " + k)
            translation = translation.replace(k, protected_strings[k])

    logging.debug(translation)
    return translation.strip()