# built in
import os
import json
# third party
import click
# this package
import functions.translator as translator
# logging
import logging
logging.basicConfig(level=logging.INFO)

##########################################################################################
# CLI built using click
# https://click.palletsprojects.com/en/7.x/
##########################################################################################


@click.option('-s', '--src_lang', default='auto', help="2 letter lang code")
@click.option('-d', '--dest_lang', default='auto', help="2 letter lang code")
@click.option('-t', '--type', default='STRING', type=click.Choice(['STRING', 'JSON'], case_sensitive=False),
              help="input type")
# defaults to regex needed to ignore Red Bee MOTT keywords
@click.option('-pr', '--protected_text_regex', default="\{.*?\}", help="regex for text to ignore during translation")
# defaults to SUBTITLES per Red Bee standard approach
@click.option('-pk', '--protected_key', default=["SUBTITLES"], multiple=True,
              help="key to ignore (when processing JSON)")
@click.option('-if', '--input_file', help="path to input file")
@click.option('-of', '--output_file', help="path to output file")
@click.argument('text', default='None')
@click.command()
def translate(src_lang, dest_lang, type, text, protected_text_regex, protected_key, input_file=None,
              output_file=None):
    """
    Main CLI command. Sifts through the provided parameters
    and hands over to other functions to do the main work.
    :param src_lang:
    :param dest_lang:
    :param type:
    :param text:
    :param protected_text_regex:
    :param protected_key:
    :param input_file:
    :param output_file:
    :return:
    """

    if type == 'JSON':

        if text is not "None":
            raise click.ClickException("input JSON as text not supported yet")
        if input_file:
            # give input file to functions that do stuff, get back translation
            jt = process_json_file(input_file, src_lang, dest_lang, protected_text_regex, protected_key)

            # JSON specific writing to output file
            if output_file:
                with open(output_file, 'w') as f:
                    json.dump(jt, f, indent=4, ensure_ascii=False)
                    f.close()
            else:
                click.echo(json.dumps(jt, indent=4, ensure_ascii=False))

    else:
        # type == STRING
        if text is not "None":
            t = translator.translate(text=text, src_lang=src_lang, dest_lang=dest_lang)
        if input_file:
            raise click.ClickException("input text as file not supported yet")

        # text specific writing to output file
        if output_file:
            with open(output_file, 'w') as f:
                f.write(t)
                f.close()

##########################################################################################
# Other Click-using functions
##########################################################################################


def process_json_file(input_file_path, src_lang, dest_lang, protected_text_regex, protected_keys):
    # return false
    click.echo("Processing JSON file: {0}".format(input_file_path))

    check_input_file(input_file_path)

    # open JSON file
    with open(input_file_path, 'r', encoding='utf8') as f:
        # create JSON object and close file
        j = json.load(f)
        f.close()

    # get total keys in JSON file, for click.progressbar
    total_keys = get_total_keys(j, protected_keys)

    with click.progressbar(label="Processing JSON",
                           length=total_keys,
                           show_eta=True,
                           show_pos=True,
                           show_percent=True) as progress_bar:
        jt = process_json(j, dest_lang, src_lang, regex=protected_text_regex,
                                protected_keys=protected_keys, progress_bar=progress_bar)
    return jt


def process_json(my_dict, dest_lang, src_lang, regex, protected_keys, progress_bar=None):
    """
    Iterates through JSON, translating string values
    :param my_dict: JSON dict
    :param dest_lang: target language
    :param src_lang: source language
    :param regex: regular expression used to recognise sub-strings to ignore
    :param protected_keys: list of keys to ignore
    :param progress_bar: click.progressbar
    :return: translated JSON dict
    """

    for k, v in my_dict.items():
        if k in protected_keys:
            continue
        if isinstance(v, dict):
            process_json(v, dest_lang, src_lang, regex, protected_keys, progress_bar=progress_bar)
            continue
        if isinstance(v, str):
            if progress_bar:
                progress_bar.update(1)
            my_dict[k] = translator.translate(my_dict[k], dest_lang, src_lang, regex)

    return my_dict


def check_input_file(input_file_path):
    """
    Checks whether file path seems to be good.
    :param input_file_path: file path to check
    :return:
    """
    if not os.path.exists(input_file_path):
        raise click.ClickException("input_file path doesn't exist")
    if not os.path.isfile(input_file_path):
        raise click.ClickException("input_file isn't a file")


##########################################################################################
# Non-Click-using functions
##########################################################################################


def get_total_keys(my_dict, keys_to_ignore=None, count=0):
    """
    Iterating function that counts all keys with string value in dict.
    :param my_dict: dict
    :param keys_to_ignore: keys to ignore
    :param count: running count of keys
    :return: total count of keys
    """

    for k, v in my_dict.items():
        if keys_to_ignore and k in keys_to_ignore:
            continue
        if isinstance(v, dict):
            count = get_total_keys(v, keys_to_ignore, count)
            continue
        count = count + 1

    return count


if __name__ == '__main__':
    translate()
