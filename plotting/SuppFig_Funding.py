import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import accumulate
import operator

import matplotlib as mpl
# mpl.rcParams['figure.dpi'] = 1200

def cumulative_sum(input_list):
    cumulative_sum_iter = accumulate(input_list, operator.add)
    return list(cumulative_sum_iter)

funding_dataset = pd.read_csv('./datasets/funding_timeline.tsv', sep='\t')
dataplot = {}
for i, row in funding_dataset.iterrows():
    year = int(row['date'][0:4])
    amount = row['amount']
    if year not in dataplot:
        dataplot[year] = amount
    else:
        dataplot[year] += amount

funding_years = list(dataplot.keys())
funding_years.sort()
funding_years.remove(2023)
total_amount = []
for year in funding_years:
    total_amount.append(dataplot[year])

total_amt_compbio = np.array(total_amount[-6:])
total_amot_biotech = np.array([1650000000, 2390000000, 2030000000, 3100000000, 4690000000, 1650000000])

growth_compbio = np.diff(total_amt_compbio) / total_amt_compbio[:-1] * 100.
growth_compbio = [round(x,2) for x in growth_compbio]
growth_biotech = np.diff(total_amot_biotech) / total_amot_biotech[:-1] * 100.
growth_biotech = [round(x,2) for x in growth_biotech]

##############################
fig, ax1 = plt.subplots(figsize = (9,9))

x = np.arange(len(funding_years[-5:]))
width = 0.25  # the width of the bars
multiplier = 0

my_dict = {
    'Computational\nBiotech': growth_compbio,
    'Biotech': growth_biotech,
}

c = ['tab:green', 'tab:blue']

for attribute, measurement in my_dict.items():
    offset = width * multiplier
    rects = ax1.bar(x + offset, measurement, width, label=attribute , color = c[multiplier])
    ax1.bar_label(rects, padding=3)
    multiplier += 1

ax1.set_ylabel('% Growth in Funding',fontsize=15)
ax1.set_title('YOY Funding Growth Between Industries',fontsize=15,fontweight='bold')
ax1.grid(False)

ax1.yaxis.set_tick_params(labelsize=12)
ax1.xaxis.set_tick_params(labelsize=12)

ax1.set_xticklabels([2017,2018,2019,2020,2021,2022], rotation=-30, ha='left')

ax1.axhline(y = 0, color = 'black', linestyle = '-') 
ax1.legend(loc='lower left', ncols=2)

plt.savefig("./plotting/plots/SuppFig4.png", bbox_inches = 'tight')