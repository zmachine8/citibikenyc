import pandas as pd
import glob
import os

# 📁 Paths
input_folder = r"C:\Users\rzukk\Downloads\citibike_cleaned"  # input folder with started_at, tripduration
output_folder = r"C:\Users\rzukk\Downloads\citibike_daily"
os.makedirs(output_folder, exist_ok=True)

# 🧩 Collect all CSV files
files = glob.glob(os.path.join(input_folder, "*.csv"))
print(f"Found {len(files)} files")

all_daily = []

for file in files:
    print(f"Processing {os.path.basename(file)}...")

    # Load trip data
    df = pd.read_csv(file, parse_dates=['started_at'], low_memory=False)

    # --- 1️⃣ Extract date ---
    df['date'] = df['started_at'].dt.date

    # --- 2️⃣ Aggregate by date ---
    daily = (
        df.groupby(['date'])
          .agg(
              trips=('tripduration', 'count'),
              avg_duration=('tripduration', 'mean'),
              median_duration=('tripduration', 'median')
          )
          .reset_index()
    )

    # Convert durations to integers
    daily['avg_duration'] = daily['avg_duration'].astype(int)
    daily['median_duration'] = daily['median_duration'].astype(int)


    # Add source file (optional)
    daily['source_file'] = os.path.basename(file)

    # Save individual daily file
    out_path = os.path.join(output_folder, f"daily_{os.path.basename(file)}")
    daily.to_csv(out_path, index=False)

    # Save for global merge
    all_daily.append(daily)

# --- 3️⃣ Merge all daily summaries ---
combined = pd.concat(all_daily, ignore_index=True)

# --- 4️⃣ Combine rows with the same date ---
combined_daily = (
    combined.groupby("date")
            .agg(
                trips=('trips', 'sum'),
                avg_duration=('avg_duration', 'mean'),
                median_duration=('median_duration', 'median')
            )
            .reset_index()
)

# Convert to integers
combined_daily['avg_duration'] = combined_daily['avg_duration'].round().astype(int)
combined_daily['median_duration'] = combined_daily['median_duration'].round().astype(int)

# --- 5️⃣ Save final file ---
output_file = os.path.join(output_folder, "citibike_all_daily_combined.csv")
combined_daily.to_csv(output_file, index=False)

print("✅ All done! Final combined dataset saved.")
print(combined_daily.head())

