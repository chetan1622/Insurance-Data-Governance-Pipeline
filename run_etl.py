import sqlite3
import pandas as pd
import os

print("Connecting to Data Warehouse (SQLite simulation of PostgreSQL)...")
# Connect to SQLite database (creates one if it doesn't exist)
os.makedirs('data/warehouse', exist_ok=True)
conn = sqlite3.connect('data/warehouse/insurance_dw.db')

print("Loading Raw CSV Data into Staging Area (Database)...")
# Load CSVs to Pandas DataFrames
try:
    df_policies = pd.read_csv('data/raw/policies_raw.csv')
    df_claims = pd.read_csv('data/raw/claims_raw.csv')
    df_renewals = pd.read_csv('data/raw/renewals_raw.csv')
except FileNotFoundError:
    print("Error: Raw CSV files not found. Please run 'python data_generator.py' first.")
    exit()

# Write Pandas DataFrames to SQLite (Staging Tables)
df_policies.to_sql('policies_raw', conn, if_exists='replace', index=False)
df_claims.to_sql('claims_raw', conn, if_exists='replace', index=False)
df_renewals.to_sql('renewals_raw', conn, if_exists='replace', index=False)
print("Raw data loaded into staging tables.")

print("Running ETL SQL Transformations...")
# Read and execute SQL queries
with open('etl_queries.sql', 'r') as file:
    sql_script = file.read()

cursor = conn.cursor()
cursor.executescript(sql_script)
conn.commit()

print("ETL Process Complete! Final 'fact_policy_lifecycle' table created.")

# Verify the data
print("\n--- Data Governance Check: First 5 Rows of Final Fact Table ---")
final_df = pd.read_sql_query("SELECT * FROM fact_policy_lifecycle LIMIT 5", conn)
print(final_df.to_markdown(index=False))

print("\nPipeline run successful. Database saved at 'data/warehouse/insurance_dw.db'")
conn.close()
