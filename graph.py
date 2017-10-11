import pandas as pd
import seaborn as sns
import math
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from random import normalvariate

pt = []
tiers = ['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond']
ranks = []
divisions = ['V', 'IV', 'III', 'II', 'I'] * 5 + ['I', 'I']
lp = range(0, 2700, 25)

for tier in tiers:
    ranks += [tier] * 20

tiers += ['Master', 'Challanger']
ranks += ['Master'] * 4 + ['Challanger'] * 4

midtiers = [50 + i*100 for i in range(len(divisions))]

for i in lp:
    pt.append(max(min(normalvariate(0, 0.1) + (1 - math.exp(-(1 + i) / 1500)), 1), 0))

df = pd.DataFrame({'Rank': ranks, 'Alfabetismo': pt, 'LP': lp})

colors = ['xkcd:bronze', 'xkcd:silver', 'xkcd:gold', 'xkcd:aqua', 'xkcd:sky blue', 'xkcd:cloudy blue', 'xkcd:yellowish']
color_list = []
for i in lp:
    if i < 2600:
        color_list.append(colors[math.floor(i/500)])
    else:
        color_list.append(colors[6])


polygons = []
for tier in range(len(tiers)):
    if tier < 5:
        verts = [(tier*500, 0), (tier*500, 1), ((tier+1)*500, 1), ((tier+1)*500, 0)]
    elif tier == 5:
        verts = [(2500, 0), (2500, 1), (2600, 1), (2600, 0)]
    else:
        verts = [(2600, 0), (2600, 1), (2700, 1), (2700, 0)]

    poly = Polygon(verts, color=colors[tier], alpha=0.2)
    polygons.append(poly)



fig, ax = plt.subplots()

[ax.add_patch(poly) for poly in polygons]

sns.regplot(x="LP", y="Alfabetismo", data=df, order=2, scatter=False, truncate=True, color='gray', ax=ax)
ax.scatter(x=df["LP"], y=df["Alfabetismo"], c=color_list)

plt.xticks((250, 750, 1250, 1750, 2250, 2550, 2650), tiers)
plt.yticks((0, 0.2, 0.4, 0.6, 0.8, 1), ('0%', '20%', '40%', '60%', '80%', '100%'))

[t.set_color(i) for (i,t) in zip(colors,ax.xaxis.get_ticklabels())]
[tick.set_rotation(30) for tick in ax.xaxis.get_ticklabels()[-2:]]

plt.tick_params(axis='x', which='minor', direction='in', pad=-12)

ax.xaxis.set_minor_locator(ticker.FixedLocator(midtiers))
ax.xaxis.set_minor_formatter(ticker.FixedFormatter(divisions))

plt.ylim(0, 1)
plt.xlim(0, 2675)
plt.ylabel('Alfabetismo')
plt.title('Alfabetismo vs. Rank')

plt.grid(b=True, alpha=0.2)

plt.savefig('graph.svg')
