import os
import json

def read_json(path):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(script_dir, path)

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError, IOError) as e:
        # print(f"File not found: {file_path}: {e}")
        return None

