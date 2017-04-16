import json


def relations(json_file_path):
    "reads a sped specification file and return a children-to-parent mapping"

    with open(json_file_path) as f:
        data = json.load(f)
    return dict((i['name'], i['parent_record']) for i in data)
