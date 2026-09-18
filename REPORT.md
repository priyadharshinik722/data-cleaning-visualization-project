# Data Cleaning & Visualization Report

## 1. Introduction
This project demonstrates the process of cleaning a raw sales dataset and extracting useful insights through visualization.

## 2. Data Cleaning
The dataset was checked for missing values and duplicate records. Missing categorical values were filled using the mode and missing numeric values using the median. Duplicate records were removed. Outliers in Quantity and Unit_Price were handled using the Interquartile Range (IQR) method.

## 3. Visualizations
Five visualizations were created:
1. Revenue by Product
2. Revenue Share by Sales Channel
3. Revenue by City
4. Revenue Distribution by Category
5. Monthly Revenue Trend

## 4. Key Insights
Run `python analysis.py` to generate the cleaned dataset and charts. The script also prints the top product, top city, best sales channel, and total revenue.

## 5. Conclusion
The project shows how data cleaning improves data quality and how visualizations can make business patterns easier to understand.
