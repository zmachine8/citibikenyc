from meteostat import Point, Hourly
import pandas as pd
from datetime import datetime

# Define location: NYC (Central Park)
nyc = Point(40.7812, -73.9665)

# Define time range
start = datetime(2013, 1, 1)
end = datetime(2023, 12, 31)

# Fetch hourly weather data
data = Hourly(nyc, start, end)
data = data.fetch()

# Reset index for easier CSV export
data.reset_index(inplace=True)

# Save to CSV
data.to_csv("nyc_weather_2013_2023.csv", index=False)

print("✅ Weather data saved as 'nyc_weather_2013_2023.csv'")
print(data.head())
