
import json

test_dict = {
    "boo": "ackashah",
    "test": {"test2": "Bonjour"},
    "boo2": "ackashah",
    "SUBTITLES": 123
}


# Utility function to perform task
def get_total_keys(my_dict, keys_to_ignore=None, keys_count=0, char_count=0):

    for k, v in my_dict.items():
        print(k)
        if k in keys_to_ignore:
            print("ignoring")
            continue
        if isinstance(v, dict):
            print("nest")
            keys_count, char_count = get_total_keys(v, keys_to_ignore, keys_count, char_count)
            continue
        if isinstance(v, str):
            print("counting")
            keys_count = keys_count + 1
            char_count = char_count + len(v)
            print(keys_count)

    return keys_count, char_count


# open JSON file
with open("../en.json", 'r', encoding='utf8') as f:
    # create JSON object and close file
    j = json.load(f)
    f.close()


print(get_total_keys(j, ["SUBTITLES"]))
