import pandas as pd
import glob
import os

# 📁 Paths
input_folder = r"C:\Users\rzukk\Downloads\andmed_citibike"  # raw input folder
output_folder = r"C:\Users\rzukk\Downloads\citibike_cleaned" # cleaned output folder
report_file = os.path.join(output_folder, "cleaning_report.csv")

os.makedirs(output_folder, exist_ok=True)

files = glob.glob(os.path.join(input_folder, "*.csv"))
print(f"Found {len(files)} files")

# 🧾 List to collect cleaning summary
report = []

for file in files:
    name = os.path.basename(file)
    print(f"\n🧽 Cleaning {name}...")

    # --- Load file ---
    raw_df = pd.read_csv(file, low_memory=False)
    total_rows = len(raw_df)

    # --- Convert columns & drop invalid ---
    df = raw_df.copy()
    df['starttime'] = pd.to_datetime(df['starttime'], errors='coerce')
    df = df.dropna(subset=['starttime', 'bikeid', 'tripduration'])

    # --- Clean tripduration ---
    before = len(df)
    df = df[(df['tripduration'] > 0) & (df['tripduration'] <= 86400)]  # <= 24h
    dropped_duration = before - len(df)

    # --- Normalize categorical values ---
    df['usertype'] = df['usertype'].astype(str).str.title().replace({'Nan': 'Unknown'})
    df['gender'] = df['gender'].astype(str).str.title().replace({'Nan': 'Unknown'})
    df['age_group'] = df['age_group'].fillna('Unknown')

    # --- Drop duplicates ---
    before = len(df)
    df = df.drop_duplicates()
    dropped_dupes = before - len(df)

    # --- Save cleaned version ---
    out_path = os.path.join(output_folder, name)
    df.to_csv(out_path, index=False)
    cleaned_rows = len(df)

    # --- Log summary ---
    dropped_total = total_rows - cleaned_rows
    percent_dropped = round((dropped_total / total_rows) * 100, 2)

    print(f"✅ {cleaned_rows:,}/{total_rows:,} rows kept ({percent_dropped}% dropped)")
    print(f"   - Dropped {dropped_duration} invalid durations")
    print(f"   - Dropped {dropped_dupes} duplicates")

    report.append({
        'file': name,
        'rows_original': total_rows,
        'rows_cleaned': cleaned_rows,
        'dropped_total': dropped_total,
        'percent_dropped': percent_dropped,
        'dropped_invalid_duration': dropped_duration,
        'dropped_duplicates': dropped_dupes
    })

# --- Combine report into a DataFrame ---
report_df = pd.DataFrame(report)
report_df.to_csv(report_file, index=False)

print("\n📊 Cleaning summary (first few files):")
print(report_df.head())

print(f"\n🧾 Full cleaning report saved to: {report_file}")
print(f"🎉 All {len(files)} files cleaned and saved in: {output_folder}")
