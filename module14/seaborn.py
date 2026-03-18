import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('avgIQpercountry.csv')

print(df.info())

# Histogram of Average IQ
plt.figure(figsize=(10, 6))
sns.histplot(df['Average IQ'])
plt.title('Histogram of Average IQ')
plt.xlabel('Average IQ')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# Heatmap

# Convert 'Population - 2023' to numeric, removing commas
df['Population - 2023'] = df['Population - 2023'].str.replace(',', '').astype(float)
print(df.info())

# Select only numeric columns for correlation calculation
numeric_iq_data_loc = df.select_dtypes(include=['number'])

sns.heatmap(numeric_iq_data_loc.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.tight_layout()
plt.show()

# Boxplot of Average IQ by Continent
plt.figure(figsize=(12, 6))
sns.set_style('darkgrid')  # Setting the style
sns.boxplot(data=df, x='Continent', y='Average IQ')
plt.title('Boxplot of Average IQ by Continent')
plt.xlabel('Continent')
plt.ylabel('Average IQ')
plt.tight_layout()
plt.show()