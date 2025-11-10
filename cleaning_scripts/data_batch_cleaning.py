import pandas as pd
import os
import glob

# 📁 Folder containing your CSV files
folder_path = r"C:\Users\rzukk\Downloads\andmed_citibike\2019"

# 🔁 Loop through all CSV files in the folder
for file_path in glob.glob(os.path.join(folder_path, "*.csv")):
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    year = int(file_name[:4])

    print(f"🚴 Processing {file_name}...")

    # --- Load data ---
    df = pd.read_csv(
        file_path,
        parse_dates=["starttime", "stoptime"],
        na_values=["\\N"],
        dtype={
            "tripduration": "int32",
            "start station id": "Int32",
            "end station id": "Int32",
            "bikeid": "Int32",
            "usertype": "category",
            "gender": "Int8"
        },
        low_memory=False
    )

    # --- Clean data ---
    df = df.dropna(subset=[
        "tripduration", "starttime", "bikeid", "usertype"
    ])

    df = df[df["tripduration"] > 0]

    # Convert and clean birth year
    df["birth year"] = pd.to_numeric(df["birth year"], errors="coerce").astype("Int16")

    # Compute age
    df["age"] = year - df["birth year"]

    # Map gender codes
    gender_map = {0: "Unknown", 1: "Male", 2: "Female"}
    df["gender"] = df["gender"].map(gender_map)

    # Create age groups (ASCII-safe labels)
    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 18, 25, 35, 45, 60, 120],
        labels=["<18", "18-25", "26-35", "36-45", "46-60", "60+"],
        right=False
    ).astype("object").fillna("Unknown")

    # Keep only selected columns
    df = df[["tripduration", "starttime", "bikeid", "usertype", "gender", "age_group"]]

    # --- Save cleaned file ---
    output_path = os.path.join(folder_path, f"{file_name}_cleaned.csv")
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"✅ Saved: {output_path}")

print("\n🎉 All files processed successfully!")
