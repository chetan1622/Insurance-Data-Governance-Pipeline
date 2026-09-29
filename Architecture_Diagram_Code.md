# 🏗️ Data Architecture & Lineage Map

Here is the visual representation of our project. You can recreate this in Draw.io or take a screenshot of this diagram.

```mermaid
flowchart LR
    subgraph Data Lake - Raw Zone
        A1(policies_raw.csv)
        A2(claims_raw.csv)
        A3(renewals_raw.csv)
    end

    subgraph ETL Processing - Staging
        B1{{Python: run_etl.py}}
        B2[(SQLite / PostgreSQL)]
        B3{{SQL: etl_queries.sql}}
        
        B1 -.-> B2
        B2 -.-> B3
    end

    subgraph Data Warehouse - Curated
        C1[(fact_policy_lifecycle)]
        C2[BI Dashboards / Reporting]
    end

    %% Data Flow
    A1 -->|Extract & Load| B1
    A2 -->|Extract & Load| B1
    A3 -->|Extract & Load| B1
    
    B3 -->|Transform & Load| C1
    
    C1 -->|Calculate KPIs| C2
    
    style Data Lake - Raw Zone fill:#e1f5fe,stroke:#01579b
    style ETL Processing - Staging fill:#fff3e0,stroke:#e65100
    style Data Warehouse - Curated fill:#e8f5e9,stroke:#1b5e20
```

### Explanation for Interview:
1. **Raw Zone:** We ingest 50,000+ raw records generated via Python into our local Data Lake simulation.
2. **ETL Processing:** We use a Python runner script to load these CSVs into a relational staging database. Then, complex SQL queries handle the joining and data cleaning.
3. **Data Warehouse:** The transformed data is structured into a single, clean 'Fact Table' which is ready to be connected to PowerBI or Tableau for business reporting.
