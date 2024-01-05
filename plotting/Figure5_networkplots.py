import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import mannwhitneyu

import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 1200

companies = pd.read_csv('./datasets/deals_nodes.tsv', sep='\t')
deals = pd.read_csv('./datasets/deals_edges.tsv', sep='\t')

degrees = []
for id in companies.Id:
  deal_count = 0
  for i in deals.Source:
    if i == id:
      deal_count +=1
  if deal_count == 0:
    for j in deals.Target:
      if j == id:
        deal_count +=1
  degrees.append(deal_count)

companies['Degree'] = degrees

biotech_companies = companies[companies['set'] == 'computational_biotech']
degrees = []
for id in biotech_companies.Id:
  deal_count = 0
  for i in deals.Source:
    if i == id:
      deal_count +=1
  if deal_count == 0:
    for j in deals.Target:
      if j == id:
        deal_count +=1
  degrees.append(deal_count)

biotech_companies['Degree'] = degrees

assoc_companies = companies[companies['set'] == 'associated']
degrees = []
for id in assoc_companies.Id:
  deal_count = 0
  for i in deals.Source:
    if i == id:
      deal_count +=1
  if deal_count == 0:
    for j in deals.Target:
      if j == id:
        deal_count +=1
  degrees.append(deal_count)

assoc_companies['Degree'] = degrees

fig, axs = plt.subplots(figsize = (9,7))

color = sns.color_palette("viridis",n_colors=3)
sns.violinplot(data=companies[companies['set'] == 'associated'].dropna(subset = ['Degree']), x="company_size", y="Degree", cut=0, ax=axs, order=[ "Mega", "Large", "Medium","Small","Micro"], color = color[1])
axs.set_title("Associated Partner Degree", fontsize = 18)
axs.set(xlabel=None)
axs.set_ylabel('Degree', fontsize=16)
axs.set_xlabel('Company Size', fontsize=16)
axs.set(ylim=(0, 6.5))
axs.grid(False)
axs.tick_params(axis='both', which='major', labelsize=15)

plt.gcf().text(0.09, 0.89, 'C', fontsize=24, fontweight='bold')

plt.savefig("./plotting/plots/Figure5C.png", bbox_inches = 'tight')

compbio_pub = biotech_companies[biotech_companies['private_public'] == 'Public']
compbio_priv = biotech_companies[biotech_companies['private_public'] == 'Private']

print('\nMean degree public: ', np.mean(compbio_pub.Degree))
print('SD degree public: ', np.std(compbio_pub.Degree))
print('Mean degree private: ', np.mean(compbio_priv.Degree))
print('SD degree private: ', np.std(compbio_priv.Degree))
U1, p = mannwhitneyu(compbio_pub.Degree, compbio_priv.Degree)
print('Mann-whitney U: ',U1)
print('Mann-whitney p: ',p)

compbio_mega = assoc_companies[assoc_companies['company_size'] == 'Mega']
compbio_large = assoc_companies[assoc_companies['company_size'] == 'Large']
compbio_medium = assoc_companies[assoc_companies['company_size'] == 'Medium']
compbio_small = assoc_companies[assoc_companies['company_size'] == 'Small']
compbio_micro = assoc_companies[assoc_companies['company_size'] == 'Micro']

print(stats.kruskal(compbio_mega.Degree, compbio_large.Degree, compbio_medium.Degree, compbio_small.Degree,compbio_micro.Degree))