from matplotlib import pyplot as plt
import pandas as pd

df = pd.read_csv('avgIQpercountry.csv')

avg_iq_by_continent = df.groupby('Continent')['Average IQ'].mean()

plt.figure(figsize=(10, 6))

plt.scatter(df['means years of schooling-2021'], df['average iq'], color='purple'