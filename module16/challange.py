import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("tokyo_weather.csv")

# -----------------------------
# Clean column names
# -----------------------------
df.columns = df.columns.str.strip().str.lower()
print("Columns:", df.columns)

# -----------------------------
# Detect temperature column
# -----------------------------
if "temperature" in df.columns:
    temp_col = "temperature"
elif "temp" in df.columns:
    temp_col = "temp"
else:
    raise KeyError("No temperature column found")

# -----------------------------
# Detect date column
# -----------------------------
date_col = None
for col in df.columns:
    if "date" in col:
        date_col = col
        break

if date_col is None:
    raise KeyError(f"No date column found. Available columns: {df.columns}")

# Convert date column
df[date_col] = pd.to_datetime(df[date_col])
df["month"] = df[date_col].dt.month

# -----------------------------
# 1. Temperature Overview
# -----------------------------
avg_temp = df[temp_col].mean()
print(f"\nAverage Temperature: {avg_temp:.2f}")

# -----------------------------
# 2. Monthly Temperature
# -----------------------------
monthly_avg = df.groupby("month")[temp_col].mean()
print("\nMonthly Average Temperature:\n", monthly_avg)

# Bar plot
monthly_avg.plot(kind="bar", color="skyblue")
plt.title("Average Monthly Temperature")
plt.xlabel("Month")
plt.ylabel("Temperature")
plt.tight_layout()
plt.show()

# -----------------------------
# 3. Highs and Lows
# -----------------------------
hottest_day = df.loc[df[temp_col].idxmax()]
coldest_day = df.loc[df[temp_col].idxmin()]

print("\nHottest Day:\n", hottest_day)
print("\nColdest Day:\n", coldest_day)

# -----------------------------
# 4. Temperature Trends
# -----------------------------
df = df.sort_values(date_col)

plt.figure(figsize=(10, 5))
plt.plot(df[date_col], df[temp_col], color="orange")
plt.title("Temperature Over Time")
plt.xlabel("Date")
plt.ylabel("Temperature")
plt.tight_layout()
plt.show()

# -----------------------------
# 5. Seasonal Average Temperature
# -----------------------------
def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Fall"

df["season"] = df["month"].apply(get_season)

seasonal_avg = df.groupby("season")[temp_col].mean()

# Order seasons correctly
season_order = ["Winter", "Spring", "Summer", "Fall"]
seasonal_avg = seasonal_avg.reindex(season_order)

print("\nSeasonal Average Temperature:\n", seasonal_avg)

# Line plot
seasonal_avg.plot(kind="line", marker="o", color="green")
plt.title("Seasonal Average Temperature")
plt.xlabel("Season")
plt.ylabel("Temperature")
plt.tight_layout()
plt.show()