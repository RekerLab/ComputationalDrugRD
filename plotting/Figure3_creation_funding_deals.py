import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import accumulate
import operator

import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 1200

def cumulative_sum(input_list):
    cumulative_sum_iter = accumulate(input_list, operator.add)
    return list(cumulative_sum_iter)

companies = pd.read_excel('./datasets/2023-05-10-companies-reference.xlsx', engine='openpyxl')
companies = companies[(companies['Owns drugs'] == True) | (companies['Drug partnering'] == True)]
companies_of_interest = [x.lower() for x in companies['Name']]
companies['Name'] = companies_of_interest

subset_w_founding = companies[companies['Founded Date'].notnull()]
founding_dates = subset_w_founding['Founded Date'].to_list()
founding_dates = list(set(founding_dates))
founding_dates.sort()
founding_dates.append(2022)

grouped_data = subset_w_founding.groupby(['Founded Date'])['Name'].count()
data_plot = {}
for index, value in grouped_data.items():
    year = index
    if year not in data_plot:
        data_plot[year] = {0}
    data_plot[year] = value
data_plot[2022] = 0

years_creation = []
for founded_date in founding_dates:
    years_creation.append(data_plot[founded_date])

publicData = pd.read_csv('./datasets/2023-05-10-PublicComps.csv')
timeline_subset = publicData[publicData['Founded Date'].notnull()]
timeline_subset['Founded Date'] = [int(i) for i in timeline_subset['Founded Date']]
ipo_dates_pub = timeline_subset['IPO Date'].to_list()
ipo_dates_pub = list(set(ipo_dates_pub))
ipo_dates_pub.sort()

grouped_data_pub = timeline_subset.groupby(['Founded Date'])['Name'].count()
grouped_data_ipo = timeline_subset.groupby(['IPO Date'])['Name'].count()

year_ipo = {}
for index, value in grouped_data_ipo.items():
    year = index
    if year not in year_ipo:
        year_ipo[year] = {0}
    year_ipo[year] = value

ipo_years = []
for founded_date in ipo_dates_pub:
    ipo_years.append(year_ipo[founded_date])

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

subs = pd.read_csv('./datasets/company_subs_mapping.tsv', sep='\t')
new_names = []
for row in np.arange(0,len(subs)):
  current_name = subs.company_name[row].lower()
  cleaned_name = current_name.replace(' corp', '').replace(' inc', '').replace(' ltd', '').replace(' llc', '').replace(' plc', '').replace(' aps', '').replace(' group', '').replace(' co', '')
  cleaned_name = cleaned_name.replace('altos ', 'alto ').replace('arsenal biosciences', 'arsenalbio').replace('exscientia ai', 'exscientia').replace('hangzhou ', '').replace(' simulated cell technologies', '').replace(' suzhou limited','').replace(' usa','').replace('finch research and development', 'finch therapeutics').replace(' holdings', '')
  new_names.append(cleaned_name)
subs['company_name'] = new_names

deals_data = pd.read_csv('./datasets/deals.tsv', sep='\t')
new_names = []
for row in np.arange(0,len(deals_data)):
  current_name = deals_data.company_name[row].lower()
  cleaned_name = current_name.replace(' corp', '').replace(' inc', '').replace(' ltd', '').replace(' llc', '').replace(' plc', '').replace(' aps', '').replace(' group', '').replace(' co', '')
  cleaned_name = cleaned_name.replace('altos ', 'alto ').replace('arsenal biosciences', 'arsenalbio').replace('exscientia ai', 'exscientia').replace('hangzhou ', '').replace(' simulated cell technologies', '').replace(' suzhou limited','').replace(' usa','').replace('finch research and development', 'finch therapeutics').replace(' holdings', '')
  new_names.append(cleaned_name)
deals_data['company_name'] = new_names
active_deals_data = deals_data[deals_data['status'] == 'Active']

data_plot = {}
for i, row in active_deals_data.iterrows():
  company_name = row['company_name']
  if company_name in companies_of_interest:
    date = row['date_start']
    year = int(date[0:4])
    if year not in data_plot:
        data_plot[year] = 1
    else:
        data_plot[year] += 1

deals_years = list(data_plot.keys())
deals_years.sort()
deals_years.remove(2023)

n_deals = []
for year in deals_years:
    n_deals.append(data_plot[year])

##############################
color = sns.color_palette("viridis",n_colors=3)
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize = (9,18))

ax1.fill_between(founding_dates, cumulative_sum(years_creation), color = color[2], alpha = 0.7)
ax1.fill_between(ipo_dates_pub, cumulative_sum(ipo_years), color = color[2])
ax1.text(2014, 22, 'All\ncompanies', fontsize=15, horizontalalignment='right', color = 'black')
ax1.text(2019.5, 9, 'Public\ncompanies', fontsize=15, horizontalalignment='right', color = 'black')


# print(founding_dates)
# print(cumulative_sum(years_creation))

# create a df with the data
df1 = pd.DataFrame({'founding_dates': founding_dates, 'cumulative_sum(years_creation)': cumulative_sum(years_creation)})
# define the founding dates as the index
df1.set_index('founding_dates', inplace=True)
# print(df1)


# print(ipo_dates_pub)
# print(cumulative_sum(ipo_years))

# create a df with the data
df2 = pd.DataFrame({'ipo_dates_pub': ipo_dates_pub, 'cumulative_sum(ipo_years)': cumulative_sum(ipo_years)})
df2.set_index('ipo_dates_pub', inplace=True)
# print(df2)

# combine the two dfs, merging on the date
df3 = pd.merge(df1, df2, left_index=True, right_index=True, how='outer')
print(df3)

# save the df3 as excel
df3.to_excel('df3.xlsx')

ax1.set(xlim=(1990, 2022), xticks=np.arange(1990,2023,2))
ax1.set_ylabel('Number of Companies',fontsize=15)
ax1.set_title('Company Creation/IPO',fontsize=15,fontweight='bold')
ax1.grid(False)

ax1.yaxis.set_tick_params(labelsize=12)
ax1.xaxis.set_tick_params(labelsize=12)
ax1.set_ylim(bottom=0)
ax1.set_xticks([1990,1994,1998,2002,2006,2010,2014,2018,2022])
ax1.set_xticklabels(ax1.get_xticks(), rotation=-30, ha='left')
ax1.set_xlabel('Year',fontsize=15)

#######
ax2.fill_between(deals_years, cumulative_sum(n_deals), color = color[1])

ax2.set(xlim=(1990, 2022), xticks=np.arange(1990,2023,2))
ax2.set_ylabel('Number of deals',fontsize=15)
ax2.set_title('Cumulative number of drug discovery & development deals',fontsize=15,fontweight='bold')
ax2.grid(False)

ax2.yaxis.set_tick_params(labelsize=12)
ax2.xaxis.set_tick_params(labelsize=12)
ax2.set_ylim(bottom=0)
ax2.set_xticks([1990,1994,1998,2002,2006,2010,2014,2018,2022])
ax2.set_xticklabels(ax2.get_xticks(), rotation=-30, ha='left')
ax2.set_xlabel('Year',fontsize=15)

########
ax3.fill_between(funding_years, cumulative_sum(total_amount), color = color[0])

ax3.set(xlim=(1990, 2022), xticks=np.arange(1990,2023,2))
ax3.set_ylabel('Money raised (Billion USD)',fontsize=15)
ax3.set_title('Cumulative funding',fontsize=15,fontweight='bold')
ax3.grid(False)

ax3.yaxis.set_tick_params(labelsize=12)
ax3.xaxis.set_tick_params(labelsize=12)
ax3.set_ylim(bottom=0)
ax3.set_xticks([1990,1994,1998,2002,2006,2010,2014,2018,2022])
ax3.set_xticklabels(ax3.get_xticks(), rotation=-30, ha='left')
ax3.set_xlabel('Year',fontsize=15)

ax3.set_yticklabels([0,2,4,6,8], fontsize=12, color = 'black')
yticks = ax3.yaxis.get_major_ticks() 
yticks[0].label1.set_visible(False)

plt.subplots_adjust(hspace=0.27)

plt.gcf().text(0.06, 0.88, 'A', fontsize=24, fontweight='bold')
plt.gcf().text(0.06, 0.61, 'B', fontsize=24, fontweight='bold')
plt.gcf().text(0.06, 0.33, 'C', fontsize=24, fontweight='bold')
plt.savefig("./plotting/plots/Figure3.png", bbox_inches = 'tight')