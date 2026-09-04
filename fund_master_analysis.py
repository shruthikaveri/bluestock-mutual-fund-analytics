import pandas as pd
from pathlib import Path

RAW_DATA_PATH = Path("data/raw")

fund_master_file = list(
    RAW_DATA_PATH.glob("*01_fund_master.csv")
)[0]

df = pd.read_csv(fund_master_file)

print("\n===== FUND MASTER ANALYSIS =====\n")

print("Dataset Shape:")
print(df.shape)

print("\nColumn Names:")
for column in df.columns:
    print("-", column)

print("\nData Types:")
print(df.dtypes)

print("\nFirst 5 Records:")
print(df.head())

print("\nFund Category Distribution:")
print(df["category"].value_counts())

print("\nFund House Distribution:")
print(df["fund_house"].value_counts())

print("\nRisk Category Distribution:")
print(df["risk_category"].value_counts())

print("\n===== ANALYSIS COMPLETED =====")