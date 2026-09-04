-- =====================================================
-- BLUESTOCK MUTUAL FUND ANALYTICS PLATFORM
-- DAY 2 - SQLITE DATABASE SCHEMA
-- =====================================================


-- =====================================================
-- DIMENSION TABLE: FUND
-- =====================================================

CREATE TABLE dim_fund (
    amfi_code INTEGER PRIMARY KEY,
    fund_house TEXT,
    scheme_name TEXT,
    category TEXT,
    sub_category TEXT,
    plan TEXT,
    launch_date TEXT,
    benchmark TEXT,
    expense_ratio_pct REAL,
    exit_load_pct REAL,
    min_sip_amount INTEGER,
    min_lumpsum_amount INTEGER,
    fund_manager TEXT,
    risk_category TEXT,
    sebi_category_code TEXT
);


-- =====================================================
-- DIMENSION TABLE: DATE
-- =====================================================

CREATE TABLE dim_date (
    date TEXT PRIMARY KEY,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    quarter INTEGER,
    month_name TEXT,
    day_name TEXT
);


-- =====================================================
-- FACT TABLE: NAV HISTORY
-- =====================================================

CREATE TABLE fact_nav (
    amfi_code INTEGER,
    date TEXT,
    nav REAL,
    PRIMARY KEY (amfi_code, date),
    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (date)
        REFERENCES dim_date(date)
);


-- =====================================================
-- FACT TABLE: INVESTOR TRANSACTIONS
-- =====================================================

CREATE TABLE fact_transactions (
    transaction_id INTEGER PRIMARY KEY,
    investor_id TEXT,
    amfi_code INTEGER,
    transaction_date TEXT,
    transaction_type TEXT,
    amount REAL,
    units REAL,
    nav REAL,
    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code)
);


-- =====================================================
-- FACT TABLE: SCHEME PERFORMANCE
-- =====================================================

CREATE TABLE fact_performance (
    amfi_code INTEGER PRIMARY KEY,
    return_1y_pct REAL,
    return_3y_pct REAL,
    return_5y_pct REAL,
    benchmark_return_1y_pct REAL,
    benchmark_return_3y_pct REAL,
    benchmark_return_5y_pct REAL,
    sharpe_ratio REAL,
    alpha REAL,
    beta REAL,
    standard_deviation REAL,
    expense_ratio_pct REAL,
    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code)
);


-- =====================================================
-- FACT TABLE: AUM
-- =====================================================

CREATE TABLE fact_aum (
    fund_house TEXT,
    date TEXT,
    aum_crore REAL
);


-- =====================================================
-- INDEXES FOR ANALYTICAL QUERIES
-- =====================================================

CREATE INDEX idx_fund_amfi
ON dim_fund(amfi_code);

CREATE INDEX idx_nav_amfi
ON fact_nav(amfi_code);

CREATE INDEX idx_nav_date
ON fact_nav(date);

CREATE INDEX idx_transactions_amfi
ON fact_transactions(amfi_code);