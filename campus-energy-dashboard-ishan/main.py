import os
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# =========================================
# Task 3: OOP classes
# =========================================

class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh


class Building:
    def __init__(self, name):
        self.name = name
        self.meter_readings = []  # list of MeterReading objects

    def add_reading(self, meter_reading):
        self.meter_readings.append(meter_reading)

    def calculate_total_consumption(self):
        return sum(r.kwh for r in self.meter_readings)

    def generate_report(self):
        total = self.calculate_total_consumption()
        return f"Building {self.name}: total consumption = {total:.2f} kWh"


class BuildingManager:
    def __init__(self):
        self.buildings = {}  # name -> Building object

    def get_or_create_building(self, name):
        if name not in self.buildings:
            self.buildings[name] = Building(name)
        return self.buildings[name]

    def add_reading(self, building_name, timestamp, kwh):
        building = self.get_or_create_building(building_name)
        reading = MeterReading(timestamp, kwh)
        building.add_reading(reading)

    def generate_all_reports(self):
        return [b.generate_report() for b in self.buildings.values()]


# =========================================
# Task 1: Data ingestion and validation
# =========================================

def load_and_merge_data(data_dir, log_file_path):
    data_dir = Path(data_dir)
    csv_files = list(data_dir.glob("*.csv"))

    all_frames = []
    log_lines = []

    if not csv_files:
        log_lines.append("No CSV files found in data directory.\n")

    for file_path in csv_files:
        try:
            # building name from filename (e.g., building_A.csv -> building_A)
            building_name = file_path.stem

            df = pd.read_csv(
                file_path,
                on_bad_lines='skip'  # skip corrupt lines
            )

            if 'timestamp' not in df.columns or 'kwh' not in df.columns:
                log_lines.append(f"{file_path.name}: Missing required columns.\n")
                continue

            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            df = df.dropna(subset=['timestamp', 'kwh'])

            df['building'] = building_name

            all_frames.append(df)

        except FileNotFoundError:
            log_lines.append(f"{file_path.name}: File not found.\n")
        except Exception as e:
            log_lines.append(f"{file_path.name}: Error - {e}\n")

    if all_frames:
        df_combined = pd.concat(all_frames, ignore_index=True)
    else:
        df_combined = pd.DataFrame(columns=['timestamp', 'kwh', 'building'])

    # save log file
    with open(log_file_path, "w") as f:
        f.writelines(log_lines)

    return df_combined


# =========================================
# Task 2: Core aggregation logic
# =========================================

def calculate_daily_totals(df):
    df = df.set_index('timestamp')
    daily = df.resample('D')['kwh'].sum().reset_index()
    return daily


def calculate_weekly_aggregates(df):
    df = df.set_index('timestamp')
    weekly = df.resample('W')['kwh'].sum().reset_index()
    return weekly


def building_wise_summary(df):
    grouped = df.groupby('building')['kwh']
    summary = grouped.agg(['mean', 'min', 'max', 'sum']).reset_index()
    summary = summary.rename(columns={'sum': 'total'})
    return summary


# =========================================
# Task 4: Visualization (dashboard)
# =========================================

def create_dashboard(df, output_path):
    # make sure timestamp is index
    df = df.set_index('timestamp')

    # 1. Trend line: daily consumption over time for all buildings
    daily_all = df.resample('D')['kwh'].sum()

    # 2. Bar chart: average weekly usage across buildings
    weekly_building = df.groupby('building').resample('W')['kwh'].sum().reset_index()
    weekly_avg = weekly_building.groupby('building')['kwh'].mean()

    # 3. Scatter plot: peak-hour consumption vs. time
    hourly = df.resample('H')['kwh'].sum().reset_index()
    peak_hours = hourly.sort_values('kwh', ascending=False).head(50)  # top 50 highest hours

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Plot 1: daily trend (line)
    axes[0].plot(daily_all.index, daily_all.values, color='blue')
    axes[0].set_title("Daily Campus Consumption")
    axes[0].set_xlabel("Date")
    axes[0].set_ylabel("kWh")

    # Plot 2: weekly average bar (per building)
    axes[1].bar(weekly_avg.index, weekly_avg.values, color='green')
    axes[1].set_title("Average Weekly Usage per Building")
    axes[1].set_xlabel("Building")
    axes[1].set_ylabel("kWh")

    # Plot 3: scatter peak hours
    axes[2].scatter(peak_hours['timestamp'], peak_hours['kwh'], color='red', s=10)
    axes[2].set_title("Peak-hour Consumption (Top 50 Hours)")
    axes[2].set_xlabel("Time")
    axes[2].set_ylabel("kWh")

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


# =========================================
# Task 5: Persistence and summary
# =========================================

def generate_summary_text(df, building_summary_df, output_txt_path):
    total_campus = df['kwh'].sum()

    # highest consuming building
    highest_row = building_summary_df.sort_values('total', ascending=False).iloc[0]
    highest_building = highest_row['building']
    highest_total = highest_row['total']

    # peak load time
    peak_row = df.sort_values('kwh', ascending=False).iloc[0]
    peak_time = peak_row['timestamp']
    peak_value = peak_row['kwh']

    # daily & weekly trends
    daily_totals = calculate_daily_totals(df)
    weekly_totals = calculate_weekly_aggregates(df)

    text_lines = []
    text_lines.append("Campus Energy Use Summary\n")
    text_lines.append("=========================\n\n")
    text_lines.append(f"Total campus consumption: {total_campus:.2f} kWh\n")
    text_lines.append(f"Highest-consuming building: {highest_building} ({highest_total:.2f} kWh)\n")
    text_lines.append(f"Peak load time: {peak_time} with {peak_value:.2f} kWh\n\n")
    text_lines.append("Daily trend: data points = " + str(len(daily_totals)) + "\n")
    text_lines.append("Weekly trend: data points = " + str(len(weekly_totals)) + "\n")

    with open(output_txt_path, "w") as f:
        f.writelines(text_lines)

    # Optionally print to console
    print("".join(text_lines))


# =========================================
# Main script
# =========================================

if __name__ == "__main__":
    # 0. Paths
    base_dir = Path(__file__).parent
    data_dir = base_dir / "data"
    output_dir = base_dir / "output"
    output_dir.mkdir(exist_ok=True)

    log_file = output_dir / "ingestion_log.txt"
    cleaned_csv_path = output_dir / "cleaned_energy_data.csv"
    building_summary_csv_path = output_dir / "building_summary.csv"
    dashboard_png_path = output_dir / "dashboard.png"
    summary_txt_path = output_dir / "summary.txt"

    # 1. Load and merge data
    df_combined = load_and_merge_data(data_dir, log_file)
    if df_combined.empty:
        print("No valid data found. Check data/ folder and log file.")
        exit()

    # 2. Aggregations
    daily_totals = calculate_daily_totals(df_combined.copy())
    weekly_totals = calculate_weekly_aggregates(df_combined.copy())
    building_summary_df = building_wise_summary(df_combined.copy())

    # 3. OOP: fill BuildingManager from df
    manager = BuildingManager()
    for _, row in df_combined.iterrows():
        manager.add_reading(
            building_name=row['building'],
            timestamp=row['timestamp'],
            kwh=row['kwh']
        )

    for report in manager.generate_all_reports():
        print(report)

    # 4. Save cleaned data and summary CSV
    df_combined.to_csv(cleaned_csv_path, index=False)
    building_summary_df.to_csv(building_summary_csv_path, index=False)

    # 5. Visualization
    create_dashboard(df_combined.copy(), dashboard_png_path)

    # 6. Summary text
    generate_summary_text(df_combined.copy(), building_summary_df, summary_txt_path)

    print("All tasks completed. Check the output/ folder.")



