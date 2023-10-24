import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
plt.rc('font',family='Times New Roman')

# Load the data from the Excel file
data = pd.read_excel("result.xlsx")
data.head()

# Remove the "s" suffix and convert to integer
data['CVIP'] = data['CVIP'].str.replace('s', '').astype(int)
data['VQPy_PF'] = data['VQPy_PF'].str.replace('s', '').astype(int)
data['VQPy_PF_HD'] = data['VQPy_PF_HD'].str.replace('s', '').astype(int)

# Plotting
bar_width = 0.25
r1 = range(len(data))
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]

# Adjusting font sizes even further
plt.figure(figsize=(22, 14))
plt.grid(True, linestyle='---')

# Bar plots
plt.bar(r1, data['CVIP'], width=bar_width, color=(59/255, 98/255, 145/255), edgecolor='grey', label='CVIP')
plt.bar(r2, data['VQPy_PF'], width=bar_width, color=(148/255, 60/255, 57/255), edgecolor='grey', label='VQPy with PF')
plt.bar(r3, data['VQPy_PF_HD'], width=bar_width, color=(119/255, 144/255, 67/255), edgecolor='grey', label='VQPy with PF and HD')

# Title & Subtitle with even larger fonts
#plt.title('Comparison of Methods across Different Scenarios', fontweight='bold', fontsize=50)
plt.xlabel('Queries', fontweight='bold', fontsize=60)
plt.ylabel('Time (seconds)', fontweight='bold', fontsize=60)

# X axis with even larger fonts
plt.xticks([r + bar_width for r in range(len(data))], data['Unnamed: 0'], rotation=13, ha='center', fontsize=48)
plt.tick_params(axis='y', labelsize=48)

# Create legend with larger fonts
plt.legend(fontsize=45, )

# Adjust layout and show plot
plt.tight_layout()
plt.show()
plt.savefig("performance.pdf", dpi=600, format='pdf')