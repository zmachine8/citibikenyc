import pandas as pd
import os
import glob

# 📁 Folder containing your CSV files
#folder_path = r"C:\Users\rzukk\Downloads\test"
folder_path = r"C:\Users\rzukk\Downloads\andmed_citibike"

# 🔁 Loop through all CSV files in the folder
for file_path in glob.glob(os.path.join(folder_path, "*.csv")):
    
    # Extract file name
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    print(f"Processing: {file_name}.csv")
    
    # Load CSV (parse dates!)
    df = pd.read_csv(
        file_path,
        parse_dates=["started_at", "ended_at"]
    )
    
    # 🕒 Calculate trip duration in seconds
    df["tripduration"] = (df["ended_at"] - df["started_at"]).dt.total_seconds().astype(int)
    
    # Keep only selected columns
    df = df[["started_at", "tripduration"]]

    # 💾 Save updated file (overwrite or use new file name)
    output_path = os.path.join(folder_path, f"{file_name}_with_duration.csv")
    df.to_csv(output_path, index=False , encoding="utf-8-sig")

    print(f"Saved: {output_path}")
