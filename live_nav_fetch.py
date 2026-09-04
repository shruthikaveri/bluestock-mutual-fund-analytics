import pandas as pd
import requests
from pathlib import Path

RAW_DATA_PATH = Path("data/raw")

# Create folder if it does not exist
RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)

# Required schemes from Bluestock Day 1 task
schemes = {
    "sbi_bluechip": "119551",
    "icici_bluechip": "120503",
    "nippon_large_cap": "118632",
    "axis_bluechip": "119092",
    "kotak_bluechip": "120841"
}

print("\n===== LIVE NAV FETCHING STARTED =====\n")

for scheme_name, amfi_code in schemes.items():

    url = f"https://api.mfapi.in/mf/{amfi_code}"

    print(f"Fetching: {scheme_name}")
    print(f"AMFI Code: {amfi_code}")

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()

        # NAV history from API response
        nav_data = pd.DataFrame(data["data"])

        # Add scheme information
        nav_data["amfi_code"] = amfi_code
        nav_data["scheme_name"] = scheme_name

        # Save CSV
        output_file = RAW_DATA_PATH / f"live_nav_{scheme_name}.csv"

        nav_data.to_csv(output_file, index=False)

        print(f"SUCCESS: Saved {output_file}")
        print(f"Total NAV records: {len(nav_data)}")
        print("-" * 60)

    except requests.exceptions.RequestException as e:
        print(f"ERROR fetching {scheme_name}: {e}")

    except Exception as e:
        print(f"ERROR processing {scheme_name}: {e}")

print("\n===== LIVE NAV FETCHING COMPLETED =====")