import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA = BASE / "data" / "raw_sales_data.csv"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

# 1. Load raw data
df = pd.read_csv(DATA)
print("Original shape:", df.shape)
print("\nMissing values before cleaning:\n", df.isnull().sum())
print("\nDuplicate rows before cleaning:", df.duplicated().sum())

# 2. Clean data
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Remove duplicate records
df = df.drop_duplicates().copy()

# Convert numeric columns
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce")

# Fill missing categorical values with the mode
for col in ["Product", "Category", "City", "Sales_Channel"]:
    if df[col].isna().any():
        df[col] = df[col].fillna(df[col].mode()[0])

# Fill missing numeric values with the median
for col in ["Quantity", "Unit_Price"]:
    df[col] = df[col].fillna(df[col].median())

# Re-create category if needed
category_map = {
    "Laptop": "Electronics", "Smartphone": "Electronics", "Tablet": "Electronics",
    "Headphones": "Accessories", "Keyboard": "Accessories", "Monitor": "Electronics"
}
df["Category"] = df["Product"].map(category_map).fillna(df["Category"])

# Handle outliers using IQR capping
for col in ["Quantity", "Unit_Price"]:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    df[col] = df[col].clip(lower=lower, upper=upper)

# Create derived field
df["Revenue"] = df["Quantity"] * df["Unit_Price"]

# Save cleaned data
clean_path = OUT / "cleaned_sales_data.csv"
df.to_csv(clean_path, index=False)

# 3. Summary
summary = df.describe(include="all").transpose()
summary.to_csv(OUT / "data_summary.csv")

# 4. Visualizations
sns.set_theme(style="whitegrid")

plt.figure(figsize=(9, 5))
product_revenue = df.groupby("Product")["Revenue"].sum().sort_values(ascending=False)
product_revenue.plot(kind="bar")
plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(OUT / "01_revenue_by_product.png", dpi=150)
plt.close()

plt.figure(figsize=(8, 5))
channel_revenue = df.groupby("Sales_Channel")["Revenue"].sum()
channel_revenue.plot(kind="pie", autopct="%1.1f%%")
plt.title("Revenue Share by Sales Channel")
plt.ylabel("")
plt.tight_layout()
plt.savefig(OUT / "02_revenue_by_channel.png", dpi=150)
plt.close()

plt.figure(figsize=(9, 5))
city_revenue = df.groupby("City")["Revenue"].sum().sort_values(ascending=False)
city_revenue.plot(kind="bar")
plt.title("Revenue by City")
plt.xlabel("City")
plt.ylabel("Revenue")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(OUT / "03_revenue_by_city.png", dpi=150)
plt.close()

plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="Category", y="Revenue")
plt.title("Revenue Distribution by Category")
plt.tight_layout()
plt.savefig(OUT / "04_revenue_distribution.png", dpi=150)
plt.close()

plt.figure(figsize=(9, 5))
monthly = df.groupby(df["Date"].dt.to_period("M"))["Revenue"].sum()
monthly.index = monthly.index.astype(str)
monthly.plot(marker="o")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(OUT / "05_monthly_revenue_trend.png", dpi=150)
plt.close()

print("\nCleaning completed.")
print("Cleaned shape:", df.shape)
print("\nMissing values after cleaning:\n", df.isnull().sum())
print("\nKey findings:")
print("Top product by revenue:", product_revenue.index[0])
print("Top city by revenue:", city_revenue.index[0])
print("Best sales channel:", channel_revenue.index[0])
print("Total revenue: ₹{:,.2f}".format(df["Revenue"].sum()))
