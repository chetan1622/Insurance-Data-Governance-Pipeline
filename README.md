# 🏥 Insurance Customer Lifecycle & Data Governance Pipeline

## 🎯 Project Overview
This project demonstrates an end-to-end data processing, ETL pipeline, and data governance framework for an insurance company. It simulates the ingestion of raw policy and claims data into a Data Lake, transforming it via SQL/Python, and documenting it for enterprise reporting.

**Domain:** Insurance (Property & Casualty or Health)  
**Tech Stack:** Python (Pandas, Faker), SQL (SQLite/PostgreSQL simulation), Data Lake Concepts, Data Governance, Draw.io (Architecture Mapping).

---

## 🏗️ Architecture & Data Lineage

![Data Architecture Diagram](architecture.png)

### 1. Data Ingestion (Raw Layer)
*   **Action:** Generated a mock dataset of **50,000+ policyholder records** using Python (`Faker` library).
*   **Mock Files Generated:** `policies_raw.csv`, `claims_raw.csv`, `renewals_raw.csv`
*   **Concept:** Simulates the raw ingestion zone in an enterprise Data Lake.

### 2. Data Transformation (ETL Staging & Curated Layer)
*   **Action:** Developed Python and SQL scripts to clean, map, and transform data into a relational database.
*   **Key Transformations:**
    *   Aggregated total claim amounts per policy.
    *   Calculated Business KPIs: **Loss Ratio** (Claims / Premiums) and **Churn Rate**.
    *   Stored the final transformed data in `fact_policy_lifecycle` for BI dashboards.

### 3. Data Governance & Documentation
*   **Data Dictionary:** Created a comprehensive catalog defining every table, column, data type, and business definition.
*   **Data Lineage:** Documented the source-to-target mapping of how data moves from raw CSVs to the final Fact Table.

---

## 🚀 How to Run Locally

1. Clone this repository.
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Generate the dummy data (50,000 records):
   ```bash
   python data_generator.py
   ```
4. Run the ETL Pipeline & SQL queries:
   ```bash
   python run_etl.py
   ```

---

## 📁 Repository Structure
*   `data_generator.py`: Python script for data generation.
*   `run_etl.py`: Pipeline execution and database loading script.
*   `etl_queries.sql`: SQL transformations and table creations.
*   `Data_Dictionary.md`: FSD and Data Catalog.
*   `architecture.png`: Visual Data Lineage map.
