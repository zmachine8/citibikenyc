import pandas as pd
import matplotlib.pyplot as plt
import os

# 📁 Path to your cleaning report CSV
report_path = r"C:\Users\rzukk\Downloads\cleaning_report_2.csv"

# --- 1️⃣ Load the report ---
df = pd.read_csv(report_path)

print("📊 Cleaning Report Overview")
print(df.head())

# --- 2️⃣ Basic summary ---
total_files = len(df)
total_original = df['rows_original'].sum()
total_cleaned = df['rows_cleaned'].sum()
total_dropped = df['dropped_total'].sum()

print("\n--- Summary ---")
print(f"Files analyzed:          {total_files}")
print(f"Total rows (original):   {total_original:,}")
print(f"Total rows (cleaned):    {total_cleaned:,}")
print(f"Total dropped overall:   {total_dropped:,}")
print(f"Average % dropped/file:  {df['percent_dropped'].mean():.3f}%")

# --- 3️⃣ Where did most drops happen? ---
worst_files = df.sort_values('percent_dropped', ascending=False).head(10)
print("\n--- Top 10 files with highest % dropped ---")
print(worst_files[['file', 'percent_dropped', 'dropped_invalid_duration', 'dropped_duplicates']])

# --- 4️⃣ Plot percentage dropped per file ---
plt.figure(figsize=(10, 4))
plt.bar(df['file'], df['percent_dropped'], color='steelblue')
plt.xticks(rotation=90, fontsize=7)
plt.ylabel('% Dropped')
plt.title('Percent of Dropped Rows per File')
plt.tight_layout()
plt.show()

# --- 5️⃣ Plot counts of drop types ---
plt.figure(figsize=(8, 4))
df[['dropped_invalid_duration', 'dropped_duplicates']].sum().plot(kind='bar', color=['tomato', 'orange'])
plt.title('Total Dropped Rows by Reason')
plt.ylabel('Count')
plt.tight_layout()
plt.show()

# --- 6️⃣ Save a Markdown summary report ---

md_path = os.path.join(os.path.dirname(report_path), "cleaning_summary.md")

with open(md_path, "w", encoding="utf-8") as f:
    f.write("# 🧹 Citi Bike Data Cleaning Summary\n\n")
    f.write(f"**Files analyzed:** {total_files}\n\n")
    f.write(f"**Total rows (original):** {total_original:,}\n\n")
    f.write(f"**Total rows (cleaned):** {total_cleaned:,}\n\n")
    f.write(f"**Total rows dropped:** {total_dropped:,}\n\n")
    f.write(f"**Average % dropped per file:** {df['percent_dropped'].mean():.4f}%\n\n")

    f.write("## 🔟 Top 10 Files by Percent Dropped\n\n")
    f.write(worst_files[['file', 'percent_dropped', 'dropped_invalid_duration', 'dropped_duplicates']].to_markdown(index=False))
    f.write("\n\n---\n")
    f.write("_Generated automatically by cleaning_report.py_\n")

print(f"📝 Markdown report saved as: {md_path}")

