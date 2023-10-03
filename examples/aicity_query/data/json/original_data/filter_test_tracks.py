import json

# Read the file containing JSON data.
with open('test-tracks.json', 'r') as file:
    data = json.load(file)

# Generate filtered names: /S01/c001-c005, /S03/c010-c015, /S04/c016-c040
name_list = []
for index in range(1, 6):
    name_list.append("c00" + str(index))
for index in range(10, 41):
    name_list.append("c0" + str(index))

for name in name_list:
    # Filter the data to keep only the parts containing "./train/S01/c001".
    filtered_data = {}
    for key, value in data.items():
        if any(name in frame for frame in value.get("frames", [])):
            filtered_data[key] = value

    # Write the filtered data to a new JSON file with custom formatting.
    output_filename = name + '.json'
    with open(output_filename, 'w') as output_file:
        json.dump(filtered_data, output_file, indent=4, separators=(',', ': '), ensure_ascii=False)

    print(f"Filtered data with custom formatting has been written to the file: {output_filename}")