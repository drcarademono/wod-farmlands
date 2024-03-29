import json
import csv
import os
import math

def read_roads_tracks_csv(csv_filename):
    roads_tracks = {}
    try:
        with open(csv_filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                roads_tracks[row['json_filename']] = row
        print("CSV file read successfully.")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return roads_tracks

# Function to determine the direction of roads or tracks
def get_direction(row):
    directions = {
        'road': None,
        'track': None
    }

    # Check roads
    if any(row[f'road_{dir}'] == 'True' for dir in ['N', 'S']):
        directions['road'] = 'NS'
    elif any(row[f'road_{dir}'] == 'True' for dir in ['E', 'W']):
        directions['road'] = 'EW'
    elif any(row[f'road_{dir}'] == 'True' for dir in ['NE', 'SW']):
        directions['road'] = 'NESW'
    elif any(row[f'road_{dir}'] == 'True' for dir in ['NW', 'SE']):
        directions['road'] = 'SENW'

    # Check tracks
    if any(row[f'track_{dir}'] == 'True' for dir in ['N', 'S']):
        directions['track'] = 'NS'
    elif any(row[f'track_{dir}'] == 'True' for dir in ['E', 'W']):
        directions['track'] = 'EW'
    elif any(row[f'track_{dir}'] == 'True' for dir in ['NE', 'SW']):
        directions['track'] = 'NESW'
    elif any(row[f'track_{dir}'] == 'True' for dir in ['NW', 'SE']):
        directions['track'] = 'SENW'

    return directions

def should_replace_block(index, size, direction):
    middle = size // 2
    if direction == 'NS' and index % size == middle:
        return True
    if direction == 'EW' and index // size == middle:
        return True
    if direction in ['NESW', 'SENW']:
        if direction == 'NESW' and index // size == index % size:
            return True
        if direction == 'SENW' and index // size == size - 1 - (index % size):
            return True
    return False

def get_new_block_name(base_block, direction, path_type):
    new_suffix = f"_{path_type}{direction}.RMB"
    return base_block.split('.')[0] + new_suffix

def find_block_names(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'BlockNames' and isinstance(value, list):
                return value
            elif isinstance(value, (dict, list)):
                result = find_block_names(value)
                if result is not None:
                    return result
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                result = find_block_names(item)
                if result is not None:
                    return result
    return None

def process_json_files(directory, roads_tracks):
    print("Processing JSON files...")
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            json_path = os.path.join(directory, filename)
            try:
                with open(json_path, 'r') as json_file:
                    data = json.load(json_file)
                print(f"Reading JSON file: {filename}")

                block_names = find_block_names(data)
                if not block_names:
                    print(f"'BlockNames' not found in {filename}")
                    continue

                size = int(math.sqrt(len(block_names)))
                if filename not in roads_tracks:
                    print(f"No matching Roads/Tracks data for {filename}")
                    continue

                directions = get_direction(roads_tracks[filename])
                for i, block in enumerate(block_names):
                    path_type = 'R' if directions['road'] else 'T'
                    direction = directions['road'] if directions['road'] else directions['track']
                    if direction and should_replace_block(i, size, direction):
                        new_block = get_new_block_name(block, direction, path_type)
                        print(f"Replacing block '{block}' with '{new_block}' in '{filename}'")
                        block_names[i] = new_block

                with open(json_path, 'w') as json_file:
                    json.dump(data, json_file, indent=4)

            except json.JSONDecodeError as e:
                print(f"Error reading JSON file {filename}: {e}")
            except FileNotFoundError:
                print(f"File not found: {filename}")
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

csv_filename = 'RoadsTracks.csv'
roads_tracks = read_roads_tracks_csv(csv_filename)
process_json_files('.', roads_tracks)
