import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import fisher_exact
import seaborn as sns
import numpy as np

import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 1200

data = pd.read_excel('./datasets/2023-05-10-companies-reference.xlsx', engine='openpyxl')

n_total = len(data)
public = data[data['Public'].notnull()]
private = data[data['Public'].isnull()]

n_public = len(public)
n_public_own = len(public[(public['Owns drugs']==True) & (public['Drug partnering']==False)])
n_public_partnered = len(public[(public['Owns drugs']==True) & (public['Drug partnering']==True)])
n_public_none = len(public[(public['Owns drugs']==False)])

n_private = len(private)
n_priv_own = len(private[(private['Owns drugs']==True) & (private['Drug partnering']==False)])
n_priv_partnered = len(private[(private['Owns drugs']==True) & (private['Drug partnering']==True)])
n_priv_none = len(private[(private['Owns drugs']==False)])

group_names=['Public', 'Private']
group_size=[n_public,n_private]
subgroup_names=['No Pipeline', 'Partnered', 'Proprietary', 'Proprietary ', 'Partnered', 'No Pipeline']
subgroup_size=[n_public_none,n_public_partnered,n_public_own,n_priv_own,n_priv_partnered,n_priv_none]

print('\nService providers: ', (n_priv_none + n_public_none)/(n_public + n_private) )
print('Non-service providers: ', 1 - ((n_priv_none + n_public_none)/(n_public + n_private)))

print('\nPartnered pipeline: ', (n_public_partnered + n_priv_partnered)/(n_public_own + n_public_partnered + n_priv_own + n_priv_partnered) )
print('Proprietary pipeline: ', ((n_public_own + n_priv_own)/(n_public + n_private)))

table = np.array([[len(private[(private['Owns drugs']==True) & (private['Drug partnering']==False)]), (len(private) - len(private[(private['Owns drugs']==True) & (private['Drug partnering']==False)]))],
                  [len(public[(public['Owns drugs']==True) & (public['Drug partnering']==False)]), (len(public) - len(public[(public['Owns drugs']==True) & (public['Drug partnering']==False)]))]])
res = fisher_exact(table, alternative='greater')
print('\nFisher result: ', res)

color = sns.color_palette("viridis",n_colors=2)
def lighter(color, percent):
    '''assumes color is rgb between (0, 0, 0) and (255, 255, 255)'''
    color = np.array(color)
    white = np.array([1, 1, 1])
    vector = white-color
    return color + vector * percent

# plot outter ring
fig, ax = plt.subplots()
ax.axis('equal')
mypie, _ = ax.pie(subgroup_size, radius=1.3, labels=subgroup_names, labeldistance=1.05, colors=[color[0], lighter(color[0],0.3), lighter(color[0],0.6), color[1], lighter(color[1],0.3), lighter(color[1],0.6)], textprops={'fontsize': 22})
plt.setp(mypie, width=0.3, edgecolor='white')
 
# plot inner ring
mypie2, _ = ax.pie(group_size, radius=1.3-0.3, labels=group_names, labeldistance=0.63, colors=[lighter(color[0],0.2), lighter(color[1],0.2)], textprops={'fontsize': 24})
plt.setp( mypie2, width=0.4, edgecolor='white')
plt.margins(0,0)

fig.set_size_inches(10, 10, forward=True)

plt.savefig("./plotting/plots/Figure1.png", bbox_inches = 'tight')