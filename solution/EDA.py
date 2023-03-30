############################################################################################################
### Script python para salvar as imagens do trabalho que dizem respeito a analise exploratoria dos dados ###
############################################################################################################

import base_2 as base
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import os
import random
import seaborn as sns
import warnings

# Set seaborn as the style for the plot
sns.set_style("whitegrid")

############################
### Grafico Scatter plot ###
############################
#data
  
x = np.array(base.no_filter().values)
y = np.array(base.get_price_total()[0:-28].values)

# Define colors based on positive or negative change in sell price
colors = ['orange' if val > 0 else 'blue' for val in y]

# Create figure and axes
fig, ax = plt.subplots(figsize=(10, 8))

# Create scatter plot with colors based on y values
ax.scatter(x, y, c=colors, alpha=0.5)

# Add title and labels
plt.title('Scatter plot for Walmart Sales and % Change in Sell Price')
plt.ylabel('% Change in Sell Price')
plt.xlabel('Walmart Daily Sales')

# Add trendline
z = np.polyfit(x, y, 1)
p = np.poly1d(z)
ax.plot(x, p(x), 'r--', label='Trendline')

# Set the legend labels
legend_labels = ['Positive % Change', 'Negative % Change']

# Create scatter plots for each color with the respective label
orange = ax.scatter(x[colors == 'orange'], y[colors == 'orange'],
                    c='orange', alpha=0.7, label=legend_labels[0])
blue = ax.scatter(x[colors == 'blue'], y[colors == 'blue'],
                c='blue', alpha=0.7, label=legend_labels[1])

# Add legend
ax.legend()

# Add gridlines
ax.grid(color='gray', linestyle='-', linewidth=0.25, alpha=0.5)

# save figure

plt.savefig(f"{base.INPUT_DIR}/images/scatter.png", dpi=300, bbox_inches='tight')


############################################
### Gráfico Total Daily Sales by Weekday ###
############################################
plt.clf()
# data
d = pd.DataFrame({'Total_daily_sales':base.no_filter().values, 'weekday':base.calendar['weekday'][0:-28].values})

weekday_sales = np.round(d.groupby('weekday')['Total_daily_sales'].sum()/1000000, 1).sort_values(ascending=False)

# plot the bar chart
ax = weekday_sales.plot(kind='bar', figsize=(8, 6), color="green", fontsize=13, alpha=0.8)

# Set the bar labels
for i in ax.containers:
    ax.bar_label(i, label_type='edge')

# Add chart title, x/y axis labels
ax.set_title('Total Daily Sales by Weekday', size=16)
ax.set_xlabel('Weekday', size=14)
ax.set_ylabel('Total Sales (millions)', size=14)

# Set the bar height for labels
ax.margins(y=0.15)

# Add gridlines
ax.grid(color='gray', linestyle='-', linewidth=0.25, alpha=0.5)

# save figure
plt.savefig(f"{base.INPUT_DIR}/images/barr_weekday.png", dpi=300, bbox_inches='tight')


###############################################
### Grafico Total Daily Sales by event type ###
###############################################
plt.clf()
# data
random.seed(22)

c = base.calendar.copy()
c = pd.Series(c['event_type_1'].values)
c.fillna('No_event', inplace =True)

d = pd.DataFrame({'Total_daily_sales':base.no_filter().values, 'Event_type':c[0:-28]})
random.seed(12)
releg = d[d['Event_type'] == 'Religious']['Total_daily_sales'].values
national = d[d['Event_type'] == 'National']['Total_daily_sales'].values
cult = d[d['Event_type'] == 'Cultural']['Total_daily_sales'].values
sport = d[d['Event_type'] == 'Sporting']['Total_daily_sales'].values
no = d[d['Event_type'] == 'No_event']['Total_daily_sales'].values

releg = random.sample(list(releg), 16)
national = random.sample(list(national), 16)
cult = random.sample(list(cult), 16)
no = random.sample(list(no), 16)

d = pd.DataFrame({'Religious':releg, 'National':national, 'Cultural':cult, 'Sporting':sport, 'No Event':no})

special_date_sales = np.round(d.sum().sort_values(ascending=False)[[0,1,2,4]]/1000, 1)

# plot the bar chart
ax = special_date_sales.plot(kind='bar', figsize=(8, 6), color="green", fontsize=13, alpha=0.8)

# Set the bar labels
for i in ax.containers:
    ax.bar_label(i, label_type='edge')

# Add chart title, x/y axis labels
ax.set_title('Total Daily Sales by event type', size=16)
ax.set_xlabel('Event type', size=14)
ax.set_ylabel('Total Sales (thousands)', size=14)

# Set the bar height for labels
ax.margins(y=0.15)

# Add gridlines
ax.grid(color='gray', linestyle='-', linewidth=0.25, alpha=0.5)

# save figure
plt.savefig(f"{base.INPUT_DIR}/images/barr_event.png", dpi=300, bbox_inches='tight')

#######################
### Grafico Boxplot ###
#######################
plt.clf()
plt.boxplot(d, labels = d.columns.values)

plt.title('Boxplot for Total Daily Sales by event type')
plt.xlabel('event type')
plt.ylabel('Total Daily Sales')
plt.grid(True)

# save figure
plt.savefig(f"{base.INPUT_DIR}/images/box_plot_event.png", dpi=300, bbox_inches='tight')
