import pandas as pd
import datetime as dt

# Load your data
df = pd.read_csv("weather_daily_clean.csv", parse_dates=["time"])

# --- Add weekday info ---
df["day_name"] = df["time"].dt.day_name()
df["day_of_week"] = df["time"].dt.dayofweek
df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

# --- Add accurate season info (Northern Hemisphere) ---
def get_season(date):
    Y = date.year
    # Define start dates of each season (astronomical)
    spring = dt.date(Y, 3, 20)
    summer = dt.date(Y, 6, 21)
    fall   = dt.date(Y, 9, 22)
    winter = dt.date(Y, 12, 21)
    
    if date.date() >= spring and date.date() < summer:
        return "Spring"
    elif date.date() >= summer and date.date() < fall:
        return "Summer"
    elif date.date() >= fall and date.date() < winter:
        return "Fall"
    else:
        return "Winter"

df["season"] = df["time"].apply(get_season)

# --- Save to new CSV ---
df.to_csv("weather_with_days_20-23.csv", index=False)

print("✅ File saved as weather_with_days_20-23.csv")
print(df.head())
