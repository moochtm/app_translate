import requests
import json

translate_api_endpoint = 'http://127.0.0.1:5000'

x = requests.get(translate_api_endpoint + '/translate?src_text=Can I have a choclate please.&dest_lang=zh')

if x.status_code == 201:
    print(json.loads(x.text))

test_dict = {
    "Str": "hello",
    "Str2": "This is a [protected] word!",
    "Int": 123,
    "Nest": {"Nest": "hello [protected text]"}
}

payload = {
    "src_json": test_dict,
    "dest_lang": "ko",
    "protected_text": "\[.*?\]"
}

x = requests.get(translate_api_endpoint + '/translate', json=payload)

if x.status_code == 201:
    print(json.loads(x.text))
