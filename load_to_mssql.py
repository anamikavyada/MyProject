"""
Loads the CSVs from output_data/ into the MedNovaClaims SQL Server database.
Run schema.sql in SSMS FIRST to create the tables, then run this script.

Before running, edit SERVER_NAME below to match your SQL Server instance
(the same name you used to connect in SSMS - e.g. "localhost" or
"localhost\\SQLEXPRESS" or your PC name + "\\SQLEXPRESS").
"""

import pandas as pd
from sqlalchemy import create_engine
import urllib

# ---------------------------------------------------------------
# EDIT THIS: match the server name you used to connect in SSMS
# ---------------------------------------------------------------
SERVER_NAME = r"IBM-H1DB1C4\SQLEXPRESS"   # <-- change if needed
DATABASE_NAME = "MedNovaClaims"

# Build the connection string (Windows Authentication - Trusted_Connection)
params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={SERVER_NAME};"
    f"DATABASE={DATABASE_NAME};"
    f"Trusted_Connection=yes;"
    f"TrustServerCertificate=yes;"
)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}", fast_executemany=True)

# Load order matters: dimensions first, then facts (foreign key dependencies)
tables_in_order = [
    "dim_date",
    "dim_payers",
    "dim_providers",
    "dim_procedures",
    "dim_patients",
    "fact_claims",
    "fact_denial_appeals",
]

for table in tables_in_order:
    print(f"Loading {table}...")
    df = pd.read_csv(f"output_data/{table}.csv")
    # Chunk large tables so SQL Server doesn't choke on one giant insert
    df.to_sql(table, engine, if_exists="append", index=False, chunksize=1000)
    print(f"  -> {len(df)} rows loaded into {table}")

print("\nAll tables loaded successfully into", DATABASE_NAME)
print("Go back to SSMS and run: SELECT COUNT(*) FROM dbo.fact_claims;  to verify.")
