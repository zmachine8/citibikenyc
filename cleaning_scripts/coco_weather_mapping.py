import pandas as pd

# Load dataset
df = pd.read_csv("nyc_weather_2013_2023_cleaned.csv", parse_dates=['time'])

# Ensure 'coco' is numeric (float -> Int64)
df['coco'] = pd.to_numeric(df['coco'], errors='coerce').astype('Int64')

# Replace 0 with NA (since Meteostat starts at 1)
df['coco'] = df['coco'].replace(0, pd.NA)

# Weather code mapping
weather_map = {
    1: 'Clear', 2: 'Fair', 3: 'Cloudy', 4: 'Overcast',
    5: 'Fog', 6: 'Freezing fog', 7: 'Light rain', 8: 'Rain',
    9: 'Heavy rain', 10: 'Freezing rain', 11: 'Heavy freezing rain',
    12: 'Sleet', 13: 'Heavy sleet', 14: 'Light snowfall', 15: 'Snowfall',
    16: 'Heavy snowfall', 17: 'Rain shower', 18: 'Heavy rain shower',
    19: 'Sleet shower', 20: 'Heavy sleet shower', 21: 'Snow shower',
    22: 'Heavy snow shower', 23: 'Lightning observed', 24: 'Hail observed',
    25: 'Thunderstorm observed', 26: 'Heavy thunderstorm observed', 27: 'Storm'
}

# Map to human-readable text
df['weather'] = df['coco'].map(weather_map).fillna('Unknown')

# Display results
print("✅ Unique weather codes:")
print(df['coco'].dropna().unique())

print("\n🌤️ Weather code counts:")
print(df['coco'].value_counts(dropna=False).sort_index())

# Save cleaned data
df.to_csv("nyc_weather_2013_2023_cleaned_mapped.csv", index=False)
print("✅ Cleaned weather data saved as 'nyc_weather_2013_2023_cleaned_mapped.csv'")
