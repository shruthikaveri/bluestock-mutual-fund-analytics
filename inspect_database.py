import sqlite3

# Connect to the database
conn = sqlite3.connect("bluestock_mf.db")
cursor = conn.cursor()

print("\n===== DATABASE TABLE STRUCTURE =====\n")

# Get all user-created tables
cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type = 'table'
AND name NOT LIKE 'sqlite_%'
ORDER BY name
""")

tables = cursor.fetchall()

# Print columns for every table
for table in tables:

    table_name = table[0]

    print(f"\nTABLE: {table_name}")
    print("-" * 50)

    cursor.execute(
        f"PRAGMA table_info({table_name})"
    )

    columns = cursor.fetchall()

    for column in columns:
        column_name = column[1]
        data_type = column[2]

        print(f"{column_name} ({data_type})")


conn.close()

print("\n===== INSPECTION COMPLETED =====")