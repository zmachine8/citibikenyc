import pandas as pd
import os
import glob

# 📁 Folder containing your CSV files
folder_path = r"C:\Users\rzukk\Downloads\andmed_citibike\2019"

# Define the exact mapping of old → new column names
rename_map = {
    "Trip Duration": "tripduration",
    "Start Time": "starttime",
    "Stop Time": "stoptime",
    "Start Station ID": "start station id",
    "Start Station Name": "start station name",
    "Start Station Latitude": "start station latitude",
    "Start Station Longitude": "start station longitude",
    "End Station ID": "end station id",
    "End Station Name": "end station name",
    "End Station Latitude": "end station latitude",
    "End Station Longitude": "end station longitude",
    "Bike ID": "bikeid",
    "User Type": "usertype",
    "Birth Year": "birth year",
    "Gender": "gender"
}

# 🔁 Loop through all CSV files in the folder
for file_path in glob.glob(os.path.join(folder_path, "*.csv")):
    file_name = os.path.basename(file_path)
    print(f"🛠️ Renaming headers in {file_name}...")

    # Read only the first row to get headers quickly
    df_header = pd.read_csv(file_path, nrows=0)
    current_cols = df_header.columns.tolist()

    # Rename using mapping (if the name matches, replace it)
    new_cols = [rename_map.get(col.strip(), col.strip()) for col in current_cols]

    # Read full CSV
    df = pd.read_csv(file_path)

    # Apply new headers
    df.columns = new_cols

    # Save the updated file (overwrite original)
    df.to_csv(file_path, index=False, encoding="utf-8-sig")

    print(f"✅ Headers renamed in {file_name}")

print("\n🎉 All files have been updated with standardized headers!")
