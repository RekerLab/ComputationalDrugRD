import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from operator import truediv

mpl.rcParams['figure.dpi'] = 1200

data = pd.read_excel('./datasets/2023-05-10-companies-reference.xlsx', engine='openpyxl')

new_data = data[(data['Owns drugs'] == True) | (data['Drug partnering'] == True)]

comp_axis = ['Algorithm', 'Dataset', 'Hardware']
pharma_axis = ['Modality', 'Biology', 'Delivery', 'Safety', 'Clinical', 'Regulatory']

heatmap = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
]

x_map_ref = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5}
for i, row in new_data.iterrows():
    cells = row['Value Matrix'].split(',')
    for cell in cells:
        x = cell[0]
        y = cell[1]
        if int(y) == 3:
          yn = 1
        elif int(y) == 1:
          yn = 3
        else:
          yn = y
        x_map = x_map_ref[x]
        y_map = int(yn) - 1
        heatmap[y_map][x_map] += 1

df = pd.DataFrame(heatmap, index = comp_axis, columns = pharma_axis)
fig, ax = plt.subplots(figsize=(13,7))

# Add title to the Heat map
title = "Company Positioning Density"

# Set the font size and the distance of the title from the plot
plt.title(title,fontsize=18)
ttl = ax.title
ttl.set_position([0.5,1.05])

# Use the heatmap function from the seaborn package
sns.heatmap(df,annot=True,fmt="",cmap='Greens',linewidths=0.30,ax=ax, square=True)

plt.savefig("plotting/plots/SuppFig1.png", bbox_inches = 'tight')

heatmap2 = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
]   

x_map_ref = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5}
for i, row in new_data.iterrows():
    funding = row['Total funding amount']
    if pd.isna(funding):
        funding = 0
    funding = round(funding)
    cells = row['Value Matrix'].split(',')
    for cell in cells:
        x = cell[0]
        y = cell[1]
        if int(y) == 3:
          yn = 1
        elif int(y) == 1:
          yn = 3
        else:
          yn = y
        x_map = x_map_ref[x]
        y_map = int(yn) - 1
        heatmap2[y_map][x_map] += funding

df = pd.DataFrame(heatmap2, index = comp_axis, columns = pharma_axis)
fig, ax = plt.subplots(figsize=(13,7))

# Add title to the Heat map
title = "Cumulative Funding Density"

# Set the font size and the distance of the title from the plot
plt.title(title,fontsize=18)
ttl = ax.title
ttl.set_position([0.5,1.05])

# Use the heatmap function from the seaborn package
sns.heatmap(df,annot=True,fmt="",cmap='Greens',linewidths=0.30,ax=ax, square=True)

plt.savefig("plotting/plots/SuppFig2.png", bbox_inches = 'tight')

matrix3 = []
for i in [0,1,2]:
  new_row = []
  for j in np.arange(0,len(heatmap[i])):
    if heatmap[i][j] == 0:
      new_row.append(0)
    else:
      new_row.append(heatmap2[i][j]/heatmap[i][j])
  matrix3.append(new_row)

df = pd.DataFrame(matrix3, index = comp_axis, columns = pharma_axis)
df = df.round(1)
df = df. fillna(0) 
fig, ax = plt.subplots(figsize=(13,7))

# Add title to the Heat map
title = "Average Funding Density"

# Set the font size and the distance of the title from the plot
plt.title(title,fontsize=18)
ttl = ax.title
ttl.set_position([0.5,1.05])

# Use the heatmap function from the seaborn package
sns.heatmap(df,annot=True,fmt="",cmap='Greens',linewidths=0.30,ax=ax, square=True)

plt.savefig("./plotting/plots/SuppFig3.png", bbox_inches = 'tight')