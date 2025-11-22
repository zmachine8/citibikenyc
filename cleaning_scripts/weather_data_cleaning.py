import pandas as pd

df = pd.read_csv("nyc_weather_2020_2023.csv", parse_dates=['time'])

#df.info()
#df.isna().sum()

# Dropping columns
df.drop(columns=['dwpt', 'rhum', 'snow', 'wdir', 'wpgt', 'tsun', 'pres'], inplace=True)

# Fill missing precipitation with 0 (no rain = 0)
df['prcp'] = df['prcp'].fillna(0)

# Optional: drop dew point if not needed
# df.drop(columns=['dwpt'], inplace=True)

# Optional: weather code — fill missing with 0 to represent unknown
df['coco'] = df['coco'].fillna(0) 
df['coco'] = df['coco'].astype('Int64')

# Save cleaned data
df.to_csv("nyc_weather_2020_2023_cleaned.csv", index=False)
print("✅ Cleaned weather data saved as 'nyc_weather_2020_2023_cleaned.csv'")