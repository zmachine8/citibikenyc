import pandas as pd
import numpy as np

# 📁 Load hourly weather data
df = pd.read_csv('nyc_weather_2020_2023_cleaned_mapped.csv', parse_dates=['time'])

# --- 1️⃣ Optional: Convert suspicious Kelvin-like temps to °C ---
# (e.g., 249–273 K -> -24 to 0 °C)
kelvin_mask = df['temp'] > 150  # values above 150 are probably Kelvin
df.loc[kelvin_mask, 'temp'] = df.loc[kelvin_mask, 'temp'] - 273.15

# If precipitation > 200 mm → assume it's invalid and set to 0
df.loc[df['prcp'] > 200, 'prcp'] = 0

# --- 2️⃣ Remove obviously bad or misplaced values ---
mask_invalid = (
    (df['temp'] < -50) | (df['temp'] > 60) |   # unrealistic temperatures
    (df['prcp'] < 0) | (df['prcp'] > 200) |    # unrealistic precipitation
    (df['wspd'] < 0) | (df['wspd'] > 150)      # unrealistic wind speeds
)

# Save invalid rows for manual inspection
invalid_rows = df[mask_invalid]
invalid_rows.to_csv('invalid_weather_rows.csv', index=False)

# Drop invalid values
df = df[~mask_invalid]

# --- 3️⃣ Aggregate hourly → daily ---
daily = (
    df.resample('D', on='time')
      .agg({
          'temp': ['mean', 'min', 'max'],  # create daily averages
          'prcp': 'sum',
          'wspd': 'mean',
          'coco': 'last',
          'weather': 'last'
      })
)

# Flatten multi-level column names
daily.columns = ['tavg', 'tmin', 'tmax', 'prcp', 'wspd', 'coco', 'weather']

# Reset index to make 'time' a normal column
daily = daily.reset_index()

# --- 4️⃣ Round numeric columns ---
numeric_cols = ['tavg', 'tmin', 'tmax', 'prcp', 'wspd']
daily[numeric_cols] = daily[numeric_cols].round(1)

# --- 5️⃣ Save cleaned and aggregated file ---
daily.to_csv('weather_daily_clean.csv', index=False)

print("✅ Daily weather file created:", daily.shape)
print(daily.head())
print(daily.describe())