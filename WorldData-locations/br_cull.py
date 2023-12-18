import csv
import os

def is_simple_path(road_or_track):
    # Check if path is simple (horizontal, vertical, or diagonal)
    return (
        # Horizontal (E-W)
        (road_or_track['E'] and road_or_track['W'] and not any([road_or_track['N'], road_or_track['S'], road_or_track['NE'], road_or_track['SE'], road_or_track['SW'], road_or_track['NW']])) or
        # Vertical (N-S)
        (road_or_track['N'] and road_or_track['S'] and not any([road_or_track['E'], road_or_track['W'], road_or_track['NE'], road_or_track['SE'], road_or_track['SW'], road_or_track['NW']])) or
        # Diagonal (NE-SW)
        (road_or_track['NE'] and road_or_track['SW'] and not any([road_or_track['N'], road_or_track['S'], road_or_track['E'], road_or_track['W'], road_or_track['SE'], road_or_track['NW']])) or
        # Diagonal (SE-NW)
        (road_or_track['SE'] and road_or_track['NW'] and not any([road_or_track['N'], road_or_track['S'], road_or_track['E'], road_or_track['W'], road_or_track['NE'], road_or_track['SW']]))
    )

def process_csv_and_delete_files(csv_file):
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            road_data = {dir: row['road_' + dir] == 'True' for dir in ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']}
            track_data = {dir: row['track_' + dir] == 'True' for dir in ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']}

            if not (is_simple_path(road_data) or is_simple_path(track_data)) or (any(road_data.values()) and any(track_data.values())):
                # Delete the corresponding JSON file
                json_filename = row['json_filename']
                try:
                    os.remove(json_filename)
                    print(f"Deleted file: {json_filename}")
                except OSError as e:
                    print(f"Error deleting file {json_filename}: {e}")

# Specify the CSV file name
csv_filename = 'RoadsTracks.csv'
process_csv_and_delete_files(csv_filename)

