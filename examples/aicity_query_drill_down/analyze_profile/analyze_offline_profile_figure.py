import json
import matplotlib.pyplot as plt


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

x = list(range(len(data1_color)))  # 数据点的序号

plt.figure(figsize=(10, 6))  # 设置图形大小
# the first data is outlier
plt.plot(x[1:], data1_color[1:], label="Data Group 1", marker='o', linestyle='-')
plt.plot(x[1:], data2_color[1:], label="Data Group 2", marker='s', linestyle='--')
plt.plot(x[1:], data3_color[1:], label="Data Group 3", marker='^', linestyle='-.')
plt.title("Comparison of Three Data Groups")
plt.xlabel("Data Point")
plt.ylabel("Time Cost")
plt.legend()
plt.grid(True)  # 添加网格线
plt.tight_layout()  # 调整图形布局
plt.savefig("color_cost.png", dpi=300)  # dpi 参数用于设置输出图像的分辨率

plt.figure(figsize=(10, 6))  # 设置图形大小
# the first data is outlier
plt.plot(x[1:], data1_type[1:], label="Data Group 1", marker='o', linestyle='-')
plt.plot(x[1:], data2_type[1:], label="Data Group 2", marker='s', linestyle='--')
plt.plot(x[1:], data3_type[1:], label="Data Group 3", marker='^', linestyle='-.')
plt.title("Comparison of Three Data Groups")
plt.xlabel("Data Point")
plt.ylabel("Time Cost")
plt.legend()
plt.grid(True)  # 添加网格线
plt.tight_layout()  # 调整图形布局
plt.savefig("type_cost.png", dpi=300)  # dpi 参数用于设置输出图像的分辨率

plt.figure(figsize=(10, 6))  # 设置图形大小
# the first data is outlier
plt.plot(x[1:], data1_direction[1:], label="Data Group 1", marker='o', linestyle='-')
plt.plot(x[1:], data2_direction[1:], label="Data Group 2", marker='s', linestyle='--')
plt.plot(x[1:], data3_direction[1:], label="Data Group 3", marker='^', linestyle='-.')
plt.title("Comparison of Three Data Groups")
plt.xlabel("Data Point")
plt.ylabel("Time Cost")
plt.legend()
plt.grid(True)  # 添加网格线
plt.tight_layout()  # 调整图形布局
plt.savefig("direction_cost.png", dpi=300)  # dpi 参数用于设置输出图像的分辨率

