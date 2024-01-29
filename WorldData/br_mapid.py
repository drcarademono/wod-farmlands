import json
import os

def process_json_files(directory):
    seen_map_ids = set()
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            json_path = os.path.join(directory, filename)
            try:
                with open(json_path, 'r') as json_file:
                    data = json.load(json_file)

                map_id = data.get('MapTableData', {}).get('MapId')
                if map_id in seen_map_ids:
                    # Delete the file as it's a duplicate
                    os.remove(json_path)
                    print(f"Deleted duplicate file: {filename}")
                else:
                    # Add the MapID to the set of seen IDs
                    seen_map_ids.add(map_id)

            except json.JSONDecodeError as e:
                print(f"Error reading JSON file {filename}: {e}")
            except FileNotFoundError:
                print(f"File not found: {filename}")
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

process_json_files('.')

