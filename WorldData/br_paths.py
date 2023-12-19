import json
import os
import csv

def read_json_file(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        return None

def read_bytes_file(filename):
    with open(filename, 'rb') as file:
        return file.read()

def get_byte_at_position(data, x, y, width):
    index = x + (y * width)
    return data[index]

def interpret_byte(byte_value):
    paths = {'N': False, 'NE': False, 'E': False, 'SE': False, 
             'S': False, 'SW': False, 'W': False, 'NW': False}

    if byte_value & 0b10000000:  # N
        paths['N'] = True
    if byte_value & 0b01000000:  # NE
        paths['NE'] = True
    if byte_value & 0b00100000:  # E
        paths['E'] = True
    if byte_value & 0b00010000:  # SE
        paths['SE'] = True
    if byte_value & 0b00001000:  # S
        paths['S'] = True
    if byte_value & 0b00000100:  # SW
        paths['SW'] = True
    if byte_value & 0b00000010:  # W
        paths['W'] = True
    if byte_value & 0b00000001:  # NW
        paths['NW'] = True

    return paths

def check_coordinate(x, y, road_data, track_data, width):
    road_byte = get_byte_at_position(road_data, x, y, width)
    track_byte = get_byte_at_position(track_data, x, y, width)

    road_paths = interpret_byte(road_byte)
    track_paths = interpret_byte(track_byte)

    return {'roads': road_paths, 'tracks': track_paths}

def process_json_files(directory):
    results = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            json_data = read_json_file(os.path.join(directory, filename))
            if json_data and 'MapTableData' in json_data and 'Latitude' in json_data['MapTableData'] and 'Longitude' in json_data['MapTableData']:
                latitude = json_data['MapTableData']['Latitude']
                longitude = json_data['MapTableData']['Longitude']
                y = 499 - (latitude // 128)
                x = longitude // 128

                paths = check_coordinate(x, y, road_data, track_data, width)
                results.append([filename, *paths['roads'].values(), *paths['tracks'].values()])
    return results

def write_to_csv(data, filename):
    headers = ['json_filename', *['road_' + dir for dir in ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']], *['track_' + dir for dir in ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']]]
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

# Load road and track data
road_data = read_bytes_file('roadData.bytes')
track_data = read_bytes_file('trackData.bytes')
width = 1000  # Width of the Daggerfall map

# Process all JSON files and write results to CSV
results = process_json_files('.')
write_to_csv(results, 'RoadsTracks.csv')
