# CitiBike NYC Data Pipeline

## 📁 Cleaned Data
Cleaned datasets are stored in Google Drive:  
🔗 https://drive.google.com/drive/folders/1C6lJWK8ttg8n7tYnzmK8YjthXxf8U6ip?usp=sharing

---

## 🧰 Script Overview
This repository contains scripts for processing **weather data** and **CitiBike trip data** into clean, analysis-ready daily datasets.

---

## 🌦️ Weather Data Processing

| Step | Description | Script |
|------|-------------|--------|
| 1 | Download hourly weather data and export to CSV | `meteostat_weather_hourly_to_csv.py` |
| 2 | Clean and preprocess weather columns | `weather_data_cleaning.py` |
| 3 | Map COCO weather condition codes | `coco_weather_mapping.py` |
| 4 | Aggregate hourly weather → daily values | `aggregate_hourly_to_daily_weather.py` |

---

## 🚲 Trip Data Processing  
*(Trip pipeline scripts listed here apply to 2013–2019; later years require adjusted cleaning steps due to changes in raw data schema.)*

| Step | Description | Script |
|------|-------------|--------|
| 1 | Initial batch cleaning of raw trip data | `data_batch_cleaning.py` |
| 2 | Secondary cleaning with reporting | `data_batch_cleaning_second_time_plus_report.py` |
| 3 | Aggregate hourly trip data → daily trip counts | `data_aggregation.py` |

---

## 🧼 Cleaning Report
Script for generating a summary of cleaning actions and statistics:  
- `cleaning_report.py`

---
