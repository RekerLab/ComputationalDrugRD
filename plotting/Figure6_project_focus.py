import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from pySankey.sankey import sankey
import ast
from collections import defaultdict

mpl.rcParams['figure.dpi'] = 1200

data = pd.read_csv('./datasets/drugs.tsv', sep='\t')
data = data[data['indications'] != '[]']

count = len(data[data['phase_highest'] == 'Discovery']) + len(data[data['phase_highest'] == 'Preclinical'])
print('\nPercentage of companies in early development: ', count/len(data))

data2 = data.groupby(['phase_highest'])['drug_id'].count()
data_plot = {}
for i, value in data2.items():
    data_plot[i] = value

keyorder = ['Discovery', 'Preclinical', 'Phase 1 Clinical', 'Phase 2 Clinical','Phase 3 Clinical', 'Clinical', 'Pre-registration', 'Launched']
data_plot = {k: v for k, v in sorted(data_plot.items(), key=lambda i:keyorder.index(i[0]))}
drugs_phases = []
counts = []
for drugs_phase, n in data_plot.items():
    drugs_phases.append(drugs_phase)
    counts.append(n)

def check_data_matches_labels(labels, data, side):
    if len(labels > 0):
        if isinstance(data, list):
            data = set(data)
        if isinstance(data, pd.Series):
            data = set(data.unique().tolist())
        if isinstance(labels, list):
            labels = set(labels)
        if labels != data:
            msg = "\n"
            if len(labels) <= 20:
                msg = "Labels: " + ",".join(labels) + "\n"
            if len(data) < 20:
                msg += "Data: " + ",".join(data)

def get_std_technologies(technologies):
    technologies = ast.literal_eval(technologies)
    std_technologies = []
    is_bio_therapeutic = False
    for technology in technologies:
        if 'antibody' in technology.lower():
            std_technologies.append('Antibody')

        if 'cell therapy' in technology.lower():
            std_technologies.append('Cell therapy')

        if 'oligonucleotide' in technology.lower():
            std_technologies.append('Oligonucleotide')

        if 'Small molecule therapeutic' in technology:
            std_technologies.append('Small molecule\ntherapeutic')

        if 'Peptide' in technology:
            std_technologies.append('Peptide')

        if 'Virus recombinant' in technology:
            std_technologies.append('Virus recombinant')

        if 'Biological therapeutic' in technology:
            is_bio_therapeutic = True

    # Update others if no rules were applied
    if len(std_technologies) == 0:
        if is_bio_therapeutic:
            std_technologies.append('Other biological\ntherapeutics')
        else:
            std_technologies.append('Other therapeutics')
    if (len(std_technologies) > 1):
      std_technologies = list(set(std_technologies))

    return std_technologies

def get_tas(therapy_areas):
    tas = []
    therapy_area_list = ast.literal_eval(therapy_areas)
    for therapy_area_item in therapy_area_list:
        tas.append(therapy_area_item)
    return tas

tech_list = []
ther_list = []

for i, row in data.iterrows():
    std_technologies = get_std_technologies(row['technologies'])
    tas = get_tas(row['therapy_areas'])
    for j in tas:
      tech_list.append(std_technologies[0])
      ther_list.append(j)

expandedDF = pd.DataFrame(data = {'Tech': tech_list, 'Therapy': ther_list})

print('\nPercentage small mol: ', len(expandedDF[expandedDF.Tech == 'Small molecule\ntherapeutic'])/len(expandedDF))
print('\nPercentage oncology: ', len(expandedDF[expandedDF.Therapy == 'Cancer'])/len(expandedDF))
print('\nPercentage neuro: ', len(expandedDF[expandedDF.Therapy == 'Neurology/Psychiatric'])/len(expandedDF))

left = expandedDF["Tech"]
right = expandedDF["Therapy"]

leftLabels = []
rightLabels = []

leftWeight = np.ones(len(left))
rightWeight = leftWeight

fig, (ax1, ax2) = plt.subplots(2,1,figsize=(12,18), height_ratios=[1, 2])

color = sns.color_palette("viridis",n_colors=3)
ax1.bar(drugs_phases, counts, color = color[1])

ax1.set_ylabel('Number of projects',fontsize=18)
ax1.set_xlabel('Pipeline Phase',fontsize=18)
ax1.set_ylim(0, 100) 
ax1.set_yticks(np.arange(0,120,20))
ax1.yaxis.set_tick_params(labelsize=15)
ax1.xaxis.set_tick_params(labelsize=15)
ax1.set_xticklabels(drugs_phases,rotation=25,
                   verticalalignment='top',
                   horizontalalignment='right')
ax1.grid(False)

# Create Dataframe
if isinstance(left, pd.Series):
    left = left.reset_index(drop=True)
if isinstance(right, pd.Series):
    right = right.reset_index(drop=True)
dataFrame = pd.DataFrame({'left': left, 'right': right, 'leftWeight': leftWeight,
                            'rightWeight': rightWeight}, index=range(len(left)))


# Identify all labels that appear 'left' or 'right'
allLabels = pd.Series(np.r_[dataFrame.left.unique(), dataFrame.right.unique()]).unique()

# Identify left labels
if len(leftLabels) == 0:
    leftLabels = pd.Series(dataFrame.left.unique()).unique()
else:
    check_data_matches_labels(leftLabels, dataFrame['left'], 'left')

# Identify right labels
if len(rightLabels) == 0:
    rightLabels = pd.Series(dataFrame.right.unique()).unique()
else:
    check_data_matches_labels(leftLabels, dataFrame['right'], 'right')
# If no colorDict given, make one
colorDict = {}
palette = "hls"
colorPalette = sns.color_palette("viridis_r",n_colors=len(allLabels))
for i, label in enumerate(allLabels):
    colorDict[label] = colorPalette[i]

# Determine widths of individual strips
ns_l = defaultdict()
ns_r = defaultdict()
for leftLabel in leftLabels:
    leftDict = {}
    rightDict = {}
    for rightLabel in rightLabels:
        leftDict[rightLabel] = dataFrame[(dataFrame.left == leftLabel) & (dataFrame.right == rightLabel)].leftWeight.sum()
        rightDict[rightLabel] = dataFrame[(dataFrame.left == leftLabel) & (dataFrame.right == rightLabel)].rightWeight.sum()
    ns_l[leftLabel] = leftDict
    ns_r[leftLabel] = rightDict

# Determine positions of left label patches and total widths
leftWidths = defaultdict()
for i, leftLabel in enumerate(leftLabels):
    myD = {}
    myD['left'] = dataFrame[dataFrame.left == leftLabel].leftWeight.sum()
    if i == 0:
        myD['bottom'] = 0
        myD['top'] = myD['left']
    else:
        myD['bottom'] = leftWidths[leftLabels[i - 1]]['top'] + 0.01 * dataFrame.leftWeight.sum()
        myD['top'] = myD['bottom'] + myD['left']
        topEdge = myD['top']
    leftWidths[leftLabel] = myD

# Determine positions of right label patches and total widths
rightWidths = defaultdict()
for i, rightLabel in enumerate(rightLabels):
    myD = {}
    myD['right'] = dataFrame[dataFrame.right == rightLabel].rightWeight.sum()
    if i == 0:
        myD['bottom'] = 0
        myD['top'] = myD['right']
    else:
        myD['bottom'] = rightWidths[rightLabels[i - 1]]['top'] + 0.01 * dataFrame.rightWeight.sum()
        myD['top'] = myD['bottom'] + myD['right']
        topEdge = myD['top']
    rightWidths[rightLabel] = myD

# Total vertical extent of diagram
xMax = topEdge / 4

# Draw vertical bars on left and right of each  label's section & print label
for leftLabel in leftLabels:
    ax2.fill_between(
        [-0.02 * xMax, 0],
        2 * [leftWidths[leftLabel]['bottom']],
        2 * [leftWidths[leftLabel]['bottom'] + leftWidths[leftLabel]['left']],
        color=colorDict[leftLabel],
        alpha=0.99
    )
    if leftLabel == 'Other therapeutics':
        ax2.text(
        -0.05 * xMax,
        leftWidths[leftLabel]['bottom'] + 1.4 * leftWidths[leftLabel]['left'],
        leftLabel, 
        {'ha': 'right', 'va': 'center'},
        fontsize=14
        )
    elif leftLabel == 'Virus recombinant':
        ax2.text(
        -0.05 * xMax,
        leftWidths[leftLabel]['bottom'] + -0.3 * leftWidths[leftLabel]['left'],
        leftLabel, 
        {'ha': 'right', 'va': 'center'},
        fontsize=14
        )
    else:
        ax2.text(
            -0.05 * xMax,
            leftWidths[leftLabel]['bottom'] + 0.5 * leftWidths[leftLabel]['left'],
            leftLabel, 
            {'ha': 'right', 'va': 'center'},
            fontsize=14
        )
for rightLabel in rightLabels:
    ax2.fill_between(
        [xMax, 1.02 * xMax], 2 * [rightWidths[rightLabel]['bottom']],
        2 * [rightWidths[rightLabel]['bottom'] + rightWidths[rightLabel]['right']],
        color=colorDict[rightLabel],
        alpha=0.99
    )
    ax2.text(
        1.05 * xMax,
        rightWidths[rightLabel]['bottom'] + 0.5 * rightWidths[rightLabel]['right'],
        rightLabel,
        {'ha': 'left', 'va': 'center'},
         fontsize=14
    )

# Plot strips
for leftLabel in leftLabels:
    for rightLabel in rightLabels:
        labelColor = leftLabel
        if len(dataFrame[(dataFrame.left == leftLabel) & (dataFrame.right == rightLabel)]) > 0:
            # Create array of y values for each strip, half at left value,
            # half at right, convolve
            ys_d = np.array(50 * [leftWidths[leftLabel]['bottom']] + 50 * [rightWidths[rightLabel]['bottom']])
            ys_d = np.convolve(ys_d, 0.05 * np.ones(20), mode='valid')
            ys_d = np.convolve(ys_d, 0.05 * np.ones(20), mode='valid')
            ys_u = np.array(50 * [leftWidths[leftLabel]['bottom'] + ns_l[leftLabel][rightLabel]] + 50 * [rightWidths[rightLabel]['bottom'] + ns_r[leftLabel][rightLabel]])
            ys_u = np.convolve(ys_u, 0.05 * np.ones(20), mode='valid')
            ys_u = np.convolve(ys_u, 0.05 * np.ones(20), mode='valid')

            # Update bottom edges at each label so next strip starts at the right place
            leftWidths[leftLabel]['bottom'] += ns_l[leftLabel][rightLabel]
            rightWidths[rightLabel]['bottom'] += ns_r[leftLabel][rightLabel]
            ax2.fill_between(
                np.linspace(0, xMax, len(ys_d)), ys_d, ys_u, alpha=0.65,
                color=colorDict[labelColor]
            )
ax2.axis('off')
plt.subplots_adjust(left=0.1,
                    bottom=0.05,
                    right=0.9,
                    top=0.9,
                    wspace=0.1,
                    hspace=0.1)

plt.gcf().text(-0.02, 0.89, 'A', fontsize=24, fontweight='bold')
plt.gcf().text(-0.02, 0.56, 'B', fontsize=24, fontweight='bold')

plt.subplots_adjust(hspace=0.17)

plt.savefig("./plotting/plots/Figure6.png", bbox_inches = 'tight')