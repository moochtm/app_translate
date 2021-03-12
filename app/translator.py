# built in
import re
import uuid
import logging
# third party
from google_trans_new import google_translator

# Initialize Translator
translator = google_translator()


def translate(text, dest_lang, src_lang, regex=None):

    protected_strings = {}
    if regex is not None:
        logging.debug("substituting protected strings")
        logging.debug(text)
        while re.search(regex, text):
            # get uuid, convert to integer, use only first 12 characters (dict keys get shortened problem)
            new_uuid = str(uuid.uuid1().int)[-12:]
            protected_strings[new_uuid] = re.search(regex, text).group()
            logging.debug(protected_strings)
            text = re.sub(regex, new_uuid, text, 1)
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


def translate_json(my_dict, dest_lang, src_lang, regex=None, protected_keys=None):

    my_dict = iterate_multidimensional(my_dict, dest_lang, src_lang, regex, protected_keys)

    return my_dict


def iterate_multidimensional(my_dict, dest_lang, src_lang, regex, protected_keys):
    for k, v in my_dict.items():
        if k in protected_keys:
            logging.debug("found key in protected_keys: " + k)
            continue
        if isinstance(v, dict):
            iterate_multidimensional(v, dest_lang, src_lang, regex, protected_keys)
            continue
        if isinstance(v, str):
            my_dict[k] = translate(my_dict[k], dest_lang, src_lang, regex)

    return my_dict