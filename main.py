import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('5_continents_81.csv', index_col=0)

plt.figure(figsize=(12, 8))

colors = {
    'S Amer': '#1f77b4',    # Blue
    'N Amer': '#ff7f0e',    # Orange
    'Eur': '#2ca02c',       # Green
    'Asia': '#17becf',      # Light blue
    'Afr': '#9467bd'        # Purple
}

for continent in df.index:
    plt.plot(df.columns, df.loc[continent], 
             marker='o', linewidth=2, markersize=6,
             color=colors.get(continent, '#1f77b4'),
             label=continent)

plt.xlabel('Variables', fontsize=12)
plt.ylabel('Values', fontsize=12)
plt.title('81 start 23854', fontsize=14, loc='center')
plt.grid(True, alpha=0.3)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

plt.ylim(0, 100)

plt.tight_layout()

plt.savefig('5_continents_81_recreated.png', dpi=300, bbox_inches='tight')

plt.show()

print("Graph saved as '5_continents_81_recreated.png'")