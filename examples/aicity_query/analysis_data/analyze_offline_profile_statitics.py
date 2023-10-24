import json


def top_k(lst, k):
    return sorted(lst, reverse=True)[:k]


file_path = '../resources/offline_profile_1.json'
read_data = None
with open(file_path, 'r') as file:
    read_data = json.load(file)
data1_color, data1_type, data1_direction = [], [], []
for key, value in read_data.items():
    data1_color.append(value['color_cost'])
    data1_type.append(value['type_cost'])
    data1_direction.append(value['direction_cost'])

file_path = '../resources/offline_profile_2.json'
read_data = None
with open(file_path, 'r') as file:
    read_data = json.load(file)
data2_color, data2_type, data2_direction = [], [], []
for key, value in read_data.items():
    data2_color.append(value['color_cost'])
    data2_type.append(value['type_cost'])
    data2_direction.append(value['direction_cost'])

file_path = '../resources/offline_profile_3.json'
read_data = None
with open(file_path, 'r') as file:
    read_data = json.load(file)
data3_color, data3_type, data3_direction = [], [], []
for key, value in read_data.items():
    data3_color.append(value['color_cost'])
    data3_type.append(value['type_cost'])
    data3_direction.append(value['direction_cost'])


data_color_ave = [(a + b + c) / 3 for a, b, c in zip(data1_color, data2_color, data3_color)]
data_type_ave = [(a + b + c) / 3 for a, b, c in zip(data1_type, data2_type, data3_type)]
data_direction_ave = [(a + b + c) / 3 for a, b, c in zip(data1_direction, data2_direction, data3_direction)]

data1_color_diff, data1_type_diff, data1_direction_diff = [], [], []
data2_color_diff, data2_type_diff, data2_direction_diff = [], [], []
data3_color_diff, data3_type_diff, data3_direction_diff = [], [], []

for i in range(len(data1_color)):
    data1_color_diff.append(abs(data1_color[i] - data_color_ave[i]) / data_color_ave[i])
    data1_type_diff.append(abs(data1_type[i] - data_type_ave[i]) / data_type_ave[i])
    data1_direction_diff.append(abs(data1_direction[i] - data_direction_ave[i]) / data_direction_ave[i])
    data2_color_diff.append(abs(data2_color[i] - data_color_ave[i]) / data_color_ave[i])
    data2_type_diff.append(abs(data2_type[i] - data_type_ave[i]) / data_type_ave[i])
    data2_direction_diff.append(abs(data2_direction[i] - data_direction_ave[i]) / data_direction_ave[i])
    data3_color_diff.append(abs(data3_color[i] - data_color_ave[i]) / data_color_ave[i])
    data3_type_diff.append(abs(data3_type[i] - data_type_ave[i]) / data_type_ave[i])
    data3_direction_diff.append(abs(data3_direction[i] - data_direction_ave[i]) / data_direction_ave[i])

print('max: ' + str(max(data1_color_diff)) + \
      ', min: ' + str(min(data1_color_diff)) + \
        ', ave: ' + str(sum(data1_color_diff)/len(data1_color_diff)) + \
            ', mid: ' + str(top_k(data1_color_diff, int(len(data1_color_diff)/2))[-1]))

print('max: ' + str(max(data1_type_diff)) + \
      ', min: ' + str(min(data1_type_diff)) + \
        ', ave: ' + str(sum(data1_type_diff)/len(data1_type_diff)) + \
            ', mid: ' + str(top_k(data1_type_diff, int(len(data1_type_diff)/2))[-1]))

print('max: ' + str(max(data1_direction_diff)) + \
      ', min: ' + str(min(data1_direction_diff)) + \
        ', ave: ' + str(sum(data1_direction_diff)/len(data1_direction_diff)) + \
            ', mid: ' + str(top_k(data1_direction_diff, int(len(data1_direction_diff)/2))[-1]))

print('max: ' + str(max(data2_color_diff)) + \
      ', min: ' + str(min(data2_color_diff)) + \
        ', ave: ' + str(sum(data2_color_diff)/len(data2_color_diff)) + \
            ', mid: ' + str(top_k(data2_color_diff, int(len(data2_color_diff)/2))[-1]))

print('max: ' + str(max(data2_type_diff)) + \
      ', min: ' + str(min(data2_type_diff)) + \
        ', ave: ' + str(sum(data2_type_diff)/len(data2_type_diff)) + \
            ', mid: ' + str(top_k(data2_type_diff, int(len(data2_type_diff)/2))[-1]))

print('max: ' + str(max(data2_direction_diff)) + \
      ', min: ' + str(min(data2_direction_diff)) + \
        ', ave: ' + str(sum(data2_direction_diff)/len(data2_direction_diff)) + \
            ', mid: ' + str(top_k(data2_direction_diff, int(len(data2_direction_diff)/2))[-1]))

print('max: ' + str(max(data3_color_diff)) + \
      ', min: ' + str(min(data3_color_diff)) + \
        ', ave: ' + str(sum(data3_color_diff)/len(data3_color_diff)) + \
            ', mid: ' + str(top_k(data3_color_diff, int(len(data3_color_diff)/2))[-1]))

print('max: ' + str(max(data3_type_diff)) + \
      ', min: ' + str(min(data3_type_diff)) + \
        ', ave: ' + str(sum(data3_type_diff)/len(data3_type_diff)) + \
            ', mid: ' + str(top_k(data3_type_diff, int(len(data3_type_diff)/2))[-1]))

print('max: ' + str(max(data3_direction_diff)) + \
      ', min: ' + str(min(data3_direction_diff)) + \
        ', ave: ' + str(sum(data3_direction_diff)/len(data3_direction_diff)) + \
            ', mid: ' + str(top_k(data3_direction_diff, int(len(data3_direction_diff)/2))[-1]))

