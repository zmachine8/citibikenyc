import pandas as pd
import os
import glob

# 📁 Folder containing your CSV files
folder_path = r"C:\Users\rzukk\Downloads\andmed_citibike\2023"

# 🔁 Loop through all CSV files in the folder
for file_path in glob.glob(os.path.join(folder_path, "*.csv")):
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    year = int(file_name[:4])

    print(f"🚴 Processing {file_name}...")

    # --- Load data ---
    df = pd.read_csv(
        file_path,
        parse_dates=["started_at", "ended_at"],
        na_values=["\\N"],
        low_memory=False
    )

    # --- Clean data ---
    df = df.dropna(subset=[
        "started_at", "ended_at", "ride_id", "member_casual"
    ])

    # Keep only selected columns
    df = df[["started_at", "ended_at", "ride_id", "member_casual"]]

    # --- Save cleaned file ---
    output_path = os.path.join(folder_path, f"{file_name}_cleaned.csv")
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"✅ Saved: {output_path}")

print("\n🎉 All files processed successfully!")
