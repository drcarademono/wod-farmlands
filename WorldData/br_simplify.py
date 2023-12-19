import json
import os
import re

def find_and_update_block_names(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'BlockNames' and isinstance(value, list):
                update_block_names(value)
                return True
            elif isinstance(value, (dict, list)):
                if find_and_update_block_names(value):
                    return True
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                if find_and_update_block_names(item):
                    return True
    return False

def update_block_names(block_names):
    for i, block_name in enumerate(block_names):
        if '_R' in block_name or '_T' in block_name:
            block_names[i] = re.sub(r'\d+', '00', block_name)

def process_json_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            json_path = os.path.join(directory, filename)
            try:
                with open(json_path, 'r') as json_file:
                    data = json.load(json_file)

                if find_and_update_block_names(data):
                    with open(json_path, 'w') as json_file:
                        json.dump(data, json_file, indent=4)

            except json.JSONDecodeError as e:
                print(f"Error reading JSON file {filename}: {e}")
            except FileNotFoundError:
                print(f"File not found: {filename}")
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

process_json_files('.')

