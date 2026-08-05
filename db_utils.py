"""
db_utils.py
Shared connection helper so every Phase 3 script connects to your
MedNovaClaims SQL Server database the same way.

EDIT SERVER_NAME below to match your SSMS server name if it changes.
"""

import pandas as pd
from sqlalchemy import create_engine
import urllib

SERVER_NAME = r"IBM-H1DB1C4\SQLEXPRESS"   # <-- same one you used in load_to_mssql.py
DATABASE_NAME = "MedNovaClaims"


def get_engine():
    params = urllib.parse.quote_plus(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={SERVER_NAME};"
        f"DATABASE={DATABASE_NAME};"
        f"Trusted_Connection=yes;"
        f"TrustServerCertificate=yes;"
    )
    return create_engine(f"mssql+pyodbc:///?odbc_connect={params}")


def load_claims_clean():
    """Loads the cleaned view you built in Phase 2 (vw_claims_clean),
    joined with payer and provider info - this is the main analysis table."""
    engine = get_engine()
    query = """
        SELECT
            vc.claim_id, vc.patient_id, vc.provider_id, vc.payer_id, vc.procedure_code,
            vc.date_submitted, vc.date_processed, vc.claim_amount, vc.paid_amount,
            vc.status_clean AS status, vc.denial_reason_code, vc.days_in_ar,
            dp.payer_name, dp.payer_type,
            dpr.department, dpr.years_experience, dpr.hospital_id
        FROM dbo.vw_claims_clean vc
        JOIN dbo.dim_payers dp ON vc.payer_id = dp.payer_id
        JOIN dbo.dim_providers dpr ON vc.provider_id = dpr.provider_id
    """
    df = pd.read_sql(query, engine)
    df["date_submitted"] = pd.to_datetime(df["date_submitted"])
    df["date_processed"] = pd.to_datetime(df["date_processed"])
    return df


def load_table(table_name):
    """Generic loader for any dimension table."""
    engine = get_engine()
    return pd.read_sql(f"SELECT * FROM dbo.{table_name}", engine)
