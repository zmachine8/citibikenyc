import pandas as pd

# 📁 Path to your daily weather file
file_path = r"C:\Users\rzukk\Downloads\weather_daily_clean.csv"

# Load data
df = pd.read_csv(file_path, parse_dates=['time'])

# Sort by date (just in case)
df = df.sort_values('time')

# Create full expected date range
full_range = pd.date_range(start=df['time'].min(), end=df['time'].max(), freq='D')

# Find missing dates
missing = full_range.difference(df['time'])

# --- Report ---
print(f"🗓️ Date range: {df['time'].min().date()} → {df['time'].max().date()}")
print(f"✅ Total days expected: {len(full_range)}")
print(f"📊 Total days present:  {df['time'].nunique()}")
print(f"⚠️ Missing days:        {len(missing)}")

if len(missing) > 0:
    print("\nMissing dates:")
    print(missing[:20])  # print first 20
    # Save missing list to file
    pd.Series(missing).to_csv('missing_dates_report.csv', index=False, header=['missing_dates'])
    print("\n🧾 Full missing-date report saved as 'missing_dates_report.csv'")
else:
    print("\n✅ No missing dates found — your daily data is complete!")
