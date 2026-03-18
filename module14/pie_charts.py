from matplotlib import pyplot as plt
import pandas as pd

avg_iq_by_continent = df.groupby('Continent')['Average IQ'].mean()


no_of_continents = nobel_prizes_by_continent.count()

print(no_of_continents)

colors = ['gold', 'lightcoral', 'yellow', 'thistle', 'orange', 'lightskyblue', 'aquamarine', 'burlywood']

plt.figure(figsize=(10, 10))

nobel_prizes_by_continent.plot(kind='pie', colors=colors, autopct='%1.1f%%')

plt.title('Distribution of Nobel Prizes by Continent')

plt.axis('equal')

plt.ylabel('')

plt.tight_layout()

plt.show()