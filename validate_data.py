import pandas as pd
from pathlib import Path

RAW_DATA_PATH = Path("data/raw")

# Load datasets
fund_master_file = list(RAW_DATA_PATH.glob("*01_fund_master.csv"))[0]
nav_history_file = list(RAW_DATA_PATH.glob("*02_nav_history.csv"))[0]

fund_master = pd.read_csv(fund_master_file)
nav_history = pd.read_csv(nav_history_file)

print("\n===== AMFI CODE VALIDATION =====\n")

# Unique AMFI codes
fund_master_codes = set(fund_master["amfi_code"])
nav_history_codes = set(nav_history["amfi_code"])

print("Total unique AMFI codes in Fund Master:", len(fund_master_codes))
print("Total unique AMFI codes in NAV History:", len(nav_history_codes))

# Find missing codes
missing_codes = fund_master_codes - nav_history_codes

print("\nAMFI codes from Fund Master missing in NAV History:")

if missing_codes:
    print(sorted(missing_codes))
    print(f"\nTotal missing codes: {len(missing_codes)}")
else:
    print("None")
    print("\nSUCCESS: Every AMFI code in Fund Master exists in NAV History.")

# Check NAV records per scheme
nav_counts = nav_history.groupby("amfi_code").size()

print("\nNAV records per AMFI code:")
print(nav_counts.head())

print("\nMinimum NAV records for a scheme:", nav_counts.min())
print("Maximum NAV records for a scheme:", nav_counts.max())

print("\n===== VALIDATION COMPLETED =====")