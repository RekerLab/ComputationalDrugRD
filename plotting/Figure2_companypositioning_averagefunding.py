import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm

from operator import truediv


import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 1200

data = pd.read_excel('./datasets/2023-05-10-companies-reference.xlsx', engine='openpyxl')

new_data = data[(data['Owns drugs'] == True) | (data['Drug partnering'] == True)]

print('\nPercentage companies in algorithm:', len(new_data[(new_data['Value Matrix'].str.contains("3"))])/len(new_data))
print('\nPercentage companies in hardware:', len(new_data[(new_data['Value Matrix'].str.contains("1"))])/len(new_data))
print('\nNumber of companies in hardware:', len(new_data[(new_data['Value Matrix'].str.contains("1"))]))
print('\nPercentage companies in datasets:', len(new_data[(new_data['Value Matrix'].str.contains("2"))])/len(new_data))
print('\nPercentage companies in modality/bio:', len(new_data[(new_data['Value Matrix'].str.contains("A")) | (new_data['Value Matrix'].str.contains("B"))])/len(new_data))
print('\nPercentage companies in delivery/safety:', len(new_data[(new_data['Value Matrix'].str.contains("C")) | (new_data['Value Matrix'].str.contains("D"))])/len(new_data))
print('\nPercentage companies in clinical:', len(new_data[(new_data['Value Matrix'].str.contains("E"))])/len(new_data))
print('\nPercentage companies in regulatory:', len(new_data[(new_data['Value Matrix'].str.contains("F"))])/len(new_data))
print('\nNumber of service providers in regulatory:', len(data[(data['Value Matrix'].str.contains("F"))]), "\n")

print('\nPercentage companies in delivery:', len(new_data[(new_data['Value Matrix'].str.contains("C"))])/len(new_data))
print('\nPercentage companies in safety:', len(new_data[(new_data['Value Matrix'].str.contains("D"))])/len(new_data))


comp_axis = ['Hardware', 'Dataset', 'Algorithm']
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

matrix3 = []
for i in [0,1,2]:
  new_row = []
  for j in np.arange(0,len(heatmap[i])):
    if heatmap[i][j] == 0:
      new_row.append(0)
    else:
      new_row.append(heatmap2[i][j]/heatmap[i][j])
  matrix3.append(new_row)


new_companies = []
new_avgFunding = []
for i in [2,1,0]:
  new_row = []
  for j in np.arange(0,len(heatmap[i])):
    new_companies.append(heatmap[i][j])
    new_avgFunding.append(matrix3[i][j])

# setup the figure and axes
fig = plt.figure(figsize=(30,15))
ax1 = fig.add_subplot(121, projection='3d')

_x = np.arange(0,6)
_y = np.arange(0,3)
_xx, _yy = np.meshgrid(_x, _y)
x, y = _xx.ravel(), _yy.ravel()

top = np.array(new_companies)
bottom = np.zeros_like(top)
width = depth = 0.5

av_funding = np.array(new_avgFunding)

dz = av_funding
offset = dz + np.abs(dz.min())
fracs = offset.astype(float)/offset.max()
norm = colors.Normalize(fracs.min(), fracs.max())
color_values = cm.viridis_r(norm(fracs.tolist()))

p = ax1.bar3d(x, y, bottom, width, depth, top,  color=color_values, shade=True, edgecolor='white')
ax1.grid(False)
ax1.set_xticks(_x)
ax1.set_xticklabels(pharma_axis,rotation=-9,
                   verticalalignment='top',
                   horizontalalignment='left',fontsize=18)
ax1.set_yticks(_y)
ax1.set_yticklabels(comp_axis,rotation=56,
                   verticalalignment='bottom',
                   horizontalalignment='left',fontsize=18)

ax1.set_zlabel('Number of Companies',fontsize=16,labelpad=10)
ax1.set_xlabel('Drug R&D Focus',fontsize=16,labelpad=10)
ax1.set_ylabel('Computational Advantage',fontsize=16,labelpad=10)
ax1.tick_params(labelsize=12)


ax1.view_init(25,-70)

cax = fig.add_axes([ax1.get_position().x1+0.01,ax1.get_position().y0+0.1,0.02,ax1.get_position().height-0.2])

colourMap = plt.cm.ScalarMappable(cmap=plt.cm.viridis_r)
colourMap.set_array(av_funding)
colBar = plt.colorbar(colourMap,orientation = 'vertical', cax=cax)
colBar.set_label('Average Funding per Company (Million USD)',fontsize=16,labelpad=12)
colBar.ax.tick_params(labelsize=12)

plt.savefig("./plotting/plots/Figure2.png", bbox_inches = 'tight')

print('\nPercentage of companies algorithm/modality: ', len(new_data[(new_data['Value Matrix'].str.contains("3")) & ((new_data['Value Matrix'].str.contains("A")) | (new_data['Value Matrix'].str.contains("B")))])/len(new_data))
subset_funding = new_data.loc[((new_data['Value Matrix'].str.contains("A3")) | (new_data['Value Matrix'].str.contains("B3"))), 'Total funding amount'].sum()
total_funding = new_data['Total funding amount'].sum()
print('Funding per company in algorithm/modality: ', (subset_funding/len(new_data[(new_data['Value Matrix'].str.contains("3")) & ((new_data['Value Matrix'].str.contains("A")) | (new_data['Value Matrix'].str.contains("B")))])))
print('Percentage of all funding in algorithm/modality: ', subset_funding/total_funding)

subset_funding = new_data.loc[((new_data['Value Matrix'].str.contains("E3"))), 'Total funding amount'].sum()
total_funding = new_data['Total funding amount'].sum()
print('\nPercentage of companies algorithm/clinical: ', len(new_data.loc[(new_data['Value Matrix'].str.contains("E3")), 'Total funding amount'])/len(new_data))
print('Funding per company in algorithm/clinical: ', (subset_funding/len(new_data.loc[(new_data['Value Matrix'].str.contains("E3")), 'Total funding amount'])))
print('Percentage of all funding in algorithm/clinical: ', subset_funding/total_funding)

subset_funding = new_data.loc[(new_data['Value Matrix'].str.contains("1")), 'Total funding amount'].sum()
total_funding = new_data['Total funding amount'].sum()
print('\nPercentage of companies in hardware: ', len(new_data.loc[(new_data['Value Matrix'].str.contains("1")), 'Total funding amount'])/len(new_data))
print('Funding per company in hardware: ', (subset_funding/len(new_data.loc[(new_data['Value Matrix'].str.contains("1")), 'Total funding amount'])))
print('Percentage of all funding in hardware: ', subset_funding/total_funding)