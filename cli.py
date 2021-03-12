import click
import os
import json
import app.translator as translator

import logging
logging.basicConfig(level=logging.DEBUG)


@click.option('-s', '--src_lang', default='auto', help="2 letter lang code")
@click.option('-d', '--dest_lang', default='auto', help="2 letter lang code")
@click.option('-t', '--type', default='STRING', type=click.Choice(['STRING', 'JSON'], case_sensitive=False),
              help="input type")
# defaults to regex needed to ignore Red Bee MOTT keywords
@click.option('-pr', '--protected_text_regex', default="\{.*?\}", help="regex for text to ignore during translation")
# defaults to SUBTITLES per Red Bee standard approach
@click.option('-pk', '--protected_key', default=["SUBTITLES"], multiple=True, help="key to ignore (when processing JSON)")
@click.option('-if', '--input_file', help="path to input file")
@click.option('-of', '--output_file', help="path to output file")
@click.argument('text', default='None')
@click.command()
def translate(src_lang, dest_lang, type, text, protected_text_regex, protected_key, input_file=None,
              output_file=None):

    if type == 'JSON':
        if text is not "None":
            raise click.ClickException("input JSON as text not supported yet")
        if input_file:
            if not os.path.exists(input_file):
                raise click.ClickException("input_file path doesn't exist")
            if not os.path.isfile(input_file):
                raise click.ClickException("input_file pisn't a file")

            with open(input_file, 'r', encoding='utf8') as f:
                j = json.load(f)
                f.close()
            print(protected_key)
            jt = translator.translate_json(j, dest_lang, src_lang, regex=protected_text_regex,
                                           protected_keys=protected_key)

            if output_file:
                with open(output_file, 'w') as f:
                    json.dump(jt, f, indent=4, ensure_ascii=False)
                    f.close()

    else:
        # type == STRING
        if text is not "None":
            t = translator.translate(text=text, src_lang=src_lang, dest_lang=dest_lang)
            print(t)
        if input_file:
            raise click.ClickException("input text as file not supported yet")

        if output_file:
            with open(output_file, 'w') as f:
                f.write(t)
                f.close()


if __name__ == '__main__':
    translate()