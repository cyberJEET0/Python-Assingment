
#  Weather Data Visualizer

A beginner‑friendly Python project that analyzes and visualizes real‑world weather data using **Pandas**, **NumPy**, and **Matplotlib**.  
The project follows **Object‑Oriented Programming (OOP)** with **inheritance**, making the code modular and easy to understand.

---

## Project Features

- Load weather data from CSV  
- Clean missing or invalid values  
- Convert date column to datetime  
- Compute statistics using NumPy  
- Group data by month  
- Generate visualizations:
  - Daily temperature trend (line chart)
  - Monthly rainfall totals (bar chart)
  - Humidity vs temperature (scatter plot)
- Export cleaned dataset  
- Save all plots as PNG images  

---

## Technologies Used

- Python 3  
- Pandas  
- NumPy  
- Matplotlib  
- Visual Studio Code  
- Git & GitHub  

---

## How to Run the Project

### 1. Install required libraries

```bash
pip install pandas numpy matplotlib


2. Run the script
python weather.py


3. Output Files Generated
- cleaned_weather.csv
- temperature_trend.png
- monthly_rainfall.png
- humidity_vs_temperature.png

Dataset Description
The dataset must contain the following columns:
date, temperature, humidity, rainfall




✅ Project Structure
weather-data-visualizer-ishan/
│
├── weather.py
├── weather.csv
│
│
├── README.md
├── summary.md
└── .gitignore



✅ Author
Ishan Savarna
B.Tech CSE (AI & Robotics)
K.R. Mangalam University

---

```markdown
#  Weather Data Analysis – Summary Report

##  Overview

This project analyzes real‑world weather data to understand temperature patterns, rainfall distribution, and humidity relationships.  
The analysis is done using Pandas and NumPy, and visualized using Matplotlib.

---

##  Data Cleaning Steps

- Converted `date` column to datetime format  
- Removed rows with invalid dates  
- Filled missing values in:
  - temperature  
  - humidity  
  - rainfall  
  using column averages  
- Added a `month` column for grouping  

---

##  Statistical Insights

Using NumPy:

- **Mean Temperature:** (calculated from dataset)  
- **Maximum Temperature:**  
- **Minimum Temperature:**  
- **Standard Deviation:**  

*(Values depend on your dataset.)*

---

##  Monthly Summary

Using Pandas groupby:

- Average temperature per month  
- Total rainfall per month  
- Average humidity per month  

This helps identify:

- Hottest months  
- Rainiest months  
- Humidity trends  

---

##  Visualizations

Three plots were generated:

1. **Daily Temperature Trend**  
   - Shows how temperature changes day‑to‑day.

2. **Monthly Rainfall Bar Chart**  
   - Highlights rainfall distribution across months.

3. **Humidity vs Temperature Scatter Plot**  
   - Shows correlation between humidity and temperature.

---
