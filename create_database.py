import pandas as pd
import sqlite3
from pathlib import Path

# ==========================================
# PATH CONFIGURATION
# ==========================================

PROCESSED_FOLDER = Path("data/processed")
DATABASE_FILE = "bluestock_mf.db"

print("\n===== BLUESTOCK SQLITE DATABASE CREATION STARTED =====\n")

# ==========================================
# CONNECT TO SQLITE DATABASE
# ==========================================

conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()

print(f"Connected to database: {DATABASE_FILE}")


# ==========================================
# REMOVE OLD TABLES (FOR SAFE RE-RUNS)
# ==========================================

tables = [
    "dim_fund",
    "dim_date",
    "fact_nav",
    "fact_transactions",
    "fact_performance",
    "fact_aum"
]

for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table}")

conn.commit()

print("Old tables removed if they existed.\n")


# ==========================================
# 1. LOAD FUND MASTER
# ==========================================

print("Loading Fund Master...")

fund_master = pd.read_csv(
    PROCESSED_FOLDER / "fund_master_cleaned.csv"
)

fund_master.to_sql(
    "dim_fund",
    conn,
    if_exists="replace",
    index=False
)

print("dim_fund created")
print("Rows:", len(fund_master))
print()


# ==========================================
# 2. LOAD NAV HISTORY
# ==========================================

print("Loading NAV History...")

nav = pd.read_csv(
    PROCESSED_FOLDER / "nav_history_cleaned.csv"
)

nav.to_sql(
    "fact_nav",
    conn,
    if_exists="replace",
    index=False
)

print("fact_nav created")
print("Rows:", len(nav))
print()


# ==========================================
# 3. LOAD INVESTOR TRANSACTIONS
# ==========================================

print("Loading Investor Transactions...")

transactions = pd.read_csv(
    PROCESSED_FOLDER / "investor_transactions_cleaned.csv"
)

transactions.to_sql(
    "fact_transactions",
    conn,
    if_exists="replace",
    index=False
)

print("fact_transactions created")
print("Rows:", len(transactions))
print()


# ==========================================
# 4. LOAD SCHEME PERFORMANCE
# ==========================================

print("Loading Scheme Performance...")

performance = pd.read_csv(
    PROCESSED_FOLDER / "scheme_performance_cleaned.csv"
)

performance.to_sql(
    "fact_performance",
    conn,
    if_exists="replace",
    index=False
)

print("fact_performance created")
print("Rows:", len(performance))
print()


# ==========================================
# 5. LOAD AUM DATA
# ==========================================

print("Loading AUM By Fund House...")

aum = pd.read_csv(
    PROCESSED_FOLDER / "aum_by_fund_house_cleaned.csv"
)

aum.to_sql(
    "fact_aum",
    conn,
    if_exists="replace",
    index=False
)

print("fact_aum created")
print("Rows:", len(aum))
print()


# ==========================================
# 6. CREATE DATE DIMENSION
# ==========================================

print("Creating Date Dimension...")

nav_dates = pd.read_csv(
    PROCESSED_FOLDER / "nav_history_cleaned.csv"
)

nav_dates["date"] = pd.to_datetime(
    nav_dates["date"],
    errors="coerce"
)

date_dimension = pd.DataFrame()

date_dimension["date"] = (
    nav_dates["date"]
    .dropna()
    .drop_duplicates()
    .sort_values()
)

date_dimension["year"] = (
    date_dimension["date"].dt.year
)

date_dimension["month"] = (
    date_dimension["date"].dt.month
)

date_dimension["day"] = (
    date_dimension["date"].dt.day
)

date_dimension["quarter"] = (
    date_dimension["date"].dt.quarter
)

date_dimension["month_name"] = (
    date_dimension["date"].dt.month_name()
)

date_dimension["day_name"] = (
    date_dimension["date"].dt.day_name()
)

# Convert date to string before SQLite storage
date_dimension["date"] = (
    date_dimension["date"]
    .dt.strftime("%Y-%m-%d")
)

date_dimension.to_sql(
    "dim_date",
    conn,
    if_exists="replace",
    index=False
)

print("dim_date created")
print("Rows:", len(date_dimension))
print()


# ==========================================
# CREATE USEFUL INDEXES
# ==========================================

print("Creating indexes...")

try:
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_fund_amfi "
        "ON dim_fund(amfi_code)"
    )

    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_nav_amfi "
        "ON fact_nav(amfi_code)"
    )

    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_nav_date "
        "ON fact_nav(date)"
    )

    conn.commit()

    print("Indexes created successfully.\n")

except Exception as e:
    print("Index creation warning:", e)
    print()


# ==========================================
# VERIFY TABLES
# ==========================================

print("===== DATABASE TABLE VERIFICATION =====\n")

cursor.execute(
    """
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    ORDER BY name;
    """
)

database_tables = cursor.fetchall()

for table in database_tables:

    table_name = table[0]

    cursor.execute(
        f"SELECT COUNT(*) FROM {table_name}"
    )

    row_count = cursor.fetchone()[0]

    print(
        f"{table_name}: {row_count} rows"
    )


# ==========================================
# CLOSE DATABASE
# ==========================================

conn.commit()
conn.close()

print("\n===== DATABASE CREATION COMPLETED =====")
print(f"Database saved as: {DATABASE_FILE}")