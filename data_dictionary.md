\# BLUESTOCK MUTUAL FUND ANALYTICS PLATFORM



\## Data Dictionary



This document describes the tables and columns used in the Bluestock Mutual Fund Analytics Platform. The database is designed to store and analyze mutual fund information, NAV history, investor transactions, scheme performance, and Assets Under Management (AUM).



\---



\# 1. dim\_fund



The `dim\_fund` table contains master information about mutual fund schemes.



| Column Name | Data Type | Description |

|---|---|---|

| amfi\_code | INTEGER | Unique AMFI code used to identify a mutual fund scheme |

| fund\_house | TEXT | Name of the mutual fund company |

| scheme\_name | TEXT | Name of the mutual fund scheme |

| category | TEXT | Main category of the fund such as Equity or Debt |

| sub\_category | TEXT | More specific classification of the fund |

| plan | TEXT | Fund plan type |

| launch\_date | TEXT | Date on which the mutual fund scheme was launched |

| benchmark | TEXT | Benchmark index used to compare fund performance |

| expense\_ratio\_pct | REAL | Percentage charged by the fund for managing investments |

| exit\_load\_pct | REAL | Percentage charged when an investor exits the fund early |

| min\_sip\_amount | INTEGER | Minimum amount required for SIP investment |

| min\_lumpsum\_amount | INTEGER | Minimum amount required for lump sum investment |

| fund\_manager | TEXT | Name of the fund manager |

| risk\_category | TEXT | Risk level associated with the fund |

| sebi\_category\_code | TEXT | SEBI category classification code |



\---



\# 2. dim\_date



The `dim\_date` table contains date-related information used for time-based analysis.



| Column Name | Data Type | Description |

|---|---|---|

| date | TEXT | Calendar date |

| year | INTEGER | Year extracted from the date |

| month | INTEGER | Month number |

| day | INTEGER | Day of the month |

| quarter | INTEGER | Quarter of the year |

| month\_name | TEXT | Name of the month |

| day\_name | TEXT | Name of the day |



\---



\# 3. fact\_nav



The `fact\_nav` table stores historical Net Asset Value information for mutual fund schemes.



| Column Name | Data Type | Description |

|---|---|---|

| amfi\_code | INTEGER | AMFI code identifying the mutual fund scheme |

| date | TEXT | Date of the NAV value |

| nav | REAL | Net Asset Value of the mutual fund on the specified date |



\---



\# 4. fact\_transactions



The `fact\_transactions` table stores investor mutual fund transaction information.



| Column Name | Data Type | Description |

|---|---|---|

| investor\_id | TEXT | Unique identifier of the investor |

| transaction\_date | TEXT | Date on which the transaction occurred |

| amfi\_code | INTEGER | AMFI code of the mutual fund scheme |

| transaction\_type | TEXT | Type of transaction |

| amount\_inr | INTEGER | Transaction amount in Indian Rupees |

| state | TEXT | State of the investor |

| city | TEXT | City of the investor |

| city\_tier | TEXT | Classification of the city based on tier |

| age\_group | TEXT | Age group of the investor |

| gender | TEXT | Gender category recorded in the dataset |

| annual\_income\_lakh | REAL | Annual income of the investor in lakhs |

| payment\_mode | TEXT | Method used to make the payment |

| kyc\_status | TEXT | KYC verification status of the investor |



\---



\# 5. fact\_performance



The `fact\_performance` table stores mutual fund performance and risk metrics.



| Column Name | Data Type | Description |

|---|---|---|

| amfi\_code | INTEGER | AMFI code identifying the mutual fund scheme |

| scheme\_name | TEXT | Name of the mutual fund scheme |

| fund\_house | TEXT | Name of the mutual fund company |

| category | TEXT | Category of the mutual fund |

| plan | TEXT | Plan type of the mutual fund |

| return\_1yr\_pct | REAL | One-year return percentage |

| return\_3yr\_pct | REAL | Three-year return percentage |

| return\_5yr\_pct | REAL | Five-year return percentage |

| benchmark\_3yr\_pct | REAL | Three-year return percentage of the benchmark |

| alpha | REAL | Measure of excess return compared with the benchmark |

| beta | REAL | Measure of fund volatility compared with the market |

| sharpe\_ratio | REAL | Risk-adjusted return measurement |

| sortino\_ratio | REAL | Downside risk-adjusted return measurement |

| std\_dev\_ann\_pct | REAL | Annualized standard deviation percentage |

| max\_drawdown\_pct | REAL | Maximum decline in fund value from a peak |

| aum\_crore | INTEGER | Assets Under Management in crores |

| expense\_ratio\_pct | REAL | Percentage charged for fund management |

| morningstar\_rating | INTEGER | Mutual fund rating value |

| risk\_grade | TEXT | Risk classification or grade of the scheme |



\---



\# 6. fact\_aum



The `fact\_aum` table stores Assets Under Management information for mutual fund houses.



| Column Name | Data Type | Description |

|---|---|---|

| date | TEXT | Date associated with the AUM record |

| fund\_house | TEXT | Name of the mutual fund house |

| aum\_lakh\_crore | REAL | Assets Under Management measured in lakh crores |

| aum\_crore | INTEGER | Assets Under Management measured in crores |

| num\_schemes | INTEGER | Number of schemes managed by the fund house |



\---



\# Database Relationships



The main relationship in the database is based on the `amfi\_code`.



\- `dim\_fund.amfi\_code` identifies each mutual fund scheme.

\- `fact\_nav.amfi\_code` connects NAV history with the corresponding fund.

\- `fact\_transactions.amfi\_code` connects investor transactions with the corresponding fund.

\- `fact\_performance.amfi\_code` connects fund performance data with the corresponding fund.



The `dim\_date` table supports time-based analysis of NAV data.



\---



\# Summary



The Bluestock Mutual Fund Analytics database contains dimension and fact tables that support analysis of:



\- Mutual fund schemes

\- Fund houses

\- NAV history

\- Investor transactions

\- Investment patterns

\- Fund performance

\- Risk metrics

\- Assets Under Management

\- Time-based mutual fund trends



This data dictionary provides a reference for understanding the database structure and supporting further SQL analysis and dashboard development.

