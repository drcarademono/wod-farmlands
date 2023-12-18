import json

def read_json_file(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")
        return None
    except FileNotFoundError:
        print(f"File not found: {filename}")
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

# Read JSON file
json_data = read_json_file('locationnew-randomfarm0-1.json')

# Check if json_data is not None and has the expected keys in the nested structure
if json_data and 'MapTableData' in json_data and 'Latitude' in json_data['MapTableData'] and 'Longitude' in json_data['MapTableData']:
    # Extract and transform coordinates
    latitude = json_data['MapTableData']['Latitude']
    longitude = json_data['MapTableData']['Longitude']
    y = 499 - (latitude // 128)
    x = longitude // 128

    # Read road and track data
    road_data = read_bytes_file('roadData.bytes')
    track_data = read_bytes_file('trackData.bytes')
    width = 1000  # Width of the Daggerfall map

    # Check paths at the coordinates
    paths = check_coordinate(x, y, road_data, track_data, width)
    print(paths)
else:
    print("JSON data is invalid or missing 'MapTableData', 'Latitude', or 'Longitude' keys.")

