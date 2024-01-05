import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 1200

companies = pd.read_excel('./datasets/2023-05-10-companies-reference.xlsx', engine='openpyxl')
companies = companies[(companies['Owns drugs'] == True) | (companies['Drug partnering'] == True)]
companies_of_interest = [x.lower() for x in companies['Name']]
companies['Name'] = companies_of_interest

deals_data = pd.read_csv('./datasets/deals.tsv', sep='\t')
new_names = []
for row in np.arange(0,len(deals_data)):
  current_name = deals_data.company_name[row].lower()
  cleaned_name = current_name.replace(' corp', '').replace(' inc', '').replace(' ltd', '').replace(' llc', '').replace(' plc', '').replace(' aps', '').replace(' group', '').replace(' co', '')
  cleaned_name = cleaned_name.replace('altos ', 'alto ').replace('arsenal biosciences', 'arsenalbio').replace('exscientia ai', 'exscientia').replace('hangzhou ', '').replace(' simulated cell technologies', '')
  new_names.append(cleaned_name)
deals_data['company_name'] = new_names

active_deals_data = deals_data[deals_data['status'] == 'Active']
active_deals_data = active_deals_data[active_deals_data['company_name'].isin(companies_of_interest)]
active_deals_data['deal_type_trim'] = active_deals_data['deal_type'].str.split(pat=' - ', n=1).str[0]
active_deals_data['deal_type_sub'] = active_deals_data['deal_type'].str.split(pat=' - ', n=1).str[1]
grouped_deals = active_deals_data.groupby(['deal_type'])['deal_id'].count()

data_plot = {}
for i, value in grouped_deals.items():
    data_plot[i] = value

data_plot = {k: v for k, v in sorted(data_plot.items(), key=lambda item: item[1])}

deal_cats = []
deal_types = []
counts = []
for deal_type, n in data_plot.items():
  deal_cats.append(deal_type.split(sep=' - ', maxsplit=1)[0])
  deal_types.append(deal_type.split(sep=' - ', maxsplit=1)[1])
  counts.append(n)

dealTypeDF = pd.DataFrame(data = {'Theme': deal_cats,
                                  'Name': deal_types,
                                  'Count': counts})

drugDeals = dealTypeDF.loc[dealTypeDF['Theme'] == 'Drug']
techDeals = dealTypeDF.loc[dealTypeDF['Theme'] == 'Technology']
patentDeals = dealTypeDF.loc[dealTypeDF['Theme'] == 'Patent']
companyDeals = dealTypeDF.loc[dealTypeDF['Theme'] == 'Company']

fig, ax = plt.subplots(figsize=(9,5))

my_cmap = plt.get_cmap("viridis")
rescale = lambda y: (y - np.min(y)) / (np.max(y) - np.min(y))
y = [1,2,3,4,5]
color=my_cmap(rescale(y))
colors = {'Drug': color[1], 'Technology': color[3], 'Patent': color[2], 'Company':color[0]}
ax.bar(dealTypeDF.Name, dealTypeDF.Count, color=[colors[i] for i in dealTypeDF['Theme']])

ax.set(ylim=(0, 75), yticks=np.arange(0,75,10))
ax.set_xticklabels(dealTypeDF.Name,rotation=30,
                   verticalalignment='top',
                   horizontalalignment='right')
ax.set_ylabel('Number of Deals',fontsize=15)
ax.yaxis.set_tick_params(labelsize=12)
ax.xaxis.set_tick_params(labelsize=12)
ax.set_title('Deal Type Distribution',fontsize=15)

labels = np.unique(dealTypeDF.Theme)
handles = [plt.Rectangle((0,0),1,1, color=colors[l]) for l in labels]
ax.legend(handles, labels, fontsize = 12)

plt.savefig("./plotting/plots/Figure4.png", bbox_inches = 'tight')

print('\nPerc underlying tech deals: ', dealTypeDF.loc[dealTypeDF.Theme == 'Technology', 'Count'].sum()/dealTypeDF['Count'].sum())