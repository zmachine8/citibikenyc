import pandas as pd
import glob
import os

# 📁 Paths
input_folder = r"C:\Users\rzukk\Downloads\citibike_cleaned"  # cleaned input folder
output_folder = r"C:\Users\rzukk\Downloads\citibike_daily"
os.makedirs(output_folder, exist_ok=True)

# 🧩 Collect all CSV files
files = glob.glob(os.path.join(input_folder, "*.csv"))
print(f"Found {len(files)} files")

all_daily = []

for file in files:
    print(f"Processing {os.path.basename(file)}...")

    # Load trip data
    df = pd.read_csv(file, parse_dates=['starttime'], low_memory=False)

    # --- 1️⃣ Extract date ---
    df['date'] = df['starttime'].dt.date

    # --- 2️⃣ Aggregate by date, gender, and age group ---
    daily = (
        df.groupby(['date', 'gender', 'age_group'])
          .agg(
              trips=('tripduration', 'count'),       # total rides
              avg_duration=('tripduration', 'mean'), # average duration (s)
              median_duration=('tripduration', 'median'),
              unique_bikes=('bikeid', 'nunique'),
              subscribers=('usertype', lambda x: (x == 'Subscriber').sum()),
              customers=('usertype', lambda x: (x == 'Customer').sum())
          )
          .reset_index()
    )

    # Round durations
    daily['avg_duration'] = daily['avg_duration'].round(1)
    daily['median_duration'] = daily['median_duration'].round(1)

    # Add file name (optional)
    daily['source_file'] = os.path.basename(file)

    # Save individual daily file
    out_path = os.path.join(output_folder, f"daily_{os.path.basename(file)}")
    daily.to_csv(out_path, index=False)

    # Append to global list
    all_daily.append(daily)

# --- 3️⃣ Merge all daily summaries ---
combined = pd.concat(all_daily, ignore_index=True)

# Sort by date for clarity
combined = combined.sort_values('date')

# 🚫 Drop the source_file column (no longer needed)
if 'source_file' in combined.columns:
    combined = combined.drop(columns=['source_file'])

# --- 4️⃣ Save combined file ---
output_file = os.path.join(output_folder, "citibike_all_daily_by_gender_age.csv")
combined.to_csv(output_file, index=False)

print("✅ All done!")
print(f"Saved combined daily dataset to: {output_file}")
print(combined.head())
