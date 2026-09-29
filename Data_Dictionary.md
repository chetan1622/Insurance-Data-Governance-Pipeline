# 📖 Data Dictionary & Functional Specification

## 1. Business Rules (Functional Specification)
*   **Loss Ratio:** This is a key metric calculated as `(Total Claim Amount / Premium Amount)`. A loss ratio > 1 means the company is paying more in claims than it's earning in premiums.
*   **Churn:** A policy is considered churned if `renewal_status` is 'Lapsed'.
*   **Claim Validity:** Only claims with `claim_status = 'Approved'` are included in the final aggregation to calculate `total_claim_amount`.

---

## 2. Data Dictionary (Source & Target)

### A. Raw Layer (Source: CSVs)

**Table: `policies_raw`**
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `policy_id` | VARCHAR | Unique identifier for the policy (Primary Key) |
| `customer_name` | VARCHAR | Full name of the policyholder |
| `policy_type` | VARCHAR | Category (Auto, Home, Health, Life) |
| `premium_amount` | FLOAT | Annual premium paid by the customer |
| `start_date` | DATE | Policy initiation date |
| `end_date` | DATE | Policy expiration date |
| `status` | VARCHAR | Current status (Active, Expired, Cancelled) |

**Table: `claims_raw`**
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `claim_id` | VARCHAR | Unique identifier for the claim (Primary Key) |
| `policy_id` | VARCHAR | Foreign Key linking to policies_raw |
| `claim_date` | DATE | Date the claim was filed |
| `claim_amount` | FLOAT | Amount requested in the claim |
| `claim_status` | VARCHAR | Status (Approved, Rejected, Pending, Under Review) |

**Table: `renewals_raw`**
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `policy_id` | VARCHAR | Foreign Key linking to policies_raw |
| `renewal_date` | DATE | Date of renewal decision |
| `renewal_status` | VARCHAR | Status (Renewed, Lapsed) |
| `churn_reason` | VARCHAR | Reason for leaving (Null if renewed) |

---

### B. Curated Layer (Target: PostgreSQL/SQLite Data Warehouse)

**Table: `fact_policy_lifecycle`** (Final Reporting Table)
| Column Name | Data Type | Source Mapping | Business Definition |
| :--- | :--- | :--- | :--- |
| `policy_id` | VARCHAR | `policies_raw.policy_id` | Unique policy identifier |
| `customer_name` | VARCHAR | `policies_raw.customer_name` | Customer Name |
| `policy_type` | VARCHAR | `policies_raw.policy_type` | Type of insurance |
| `premium_amount` | FLOAT | `policies_raw.premium_amount` | Base premium |
| `policy_status` | VARCHAR | `policies_raw.status` | Current active status |
| `total_claims_count` | INT | `COUNT(claims_raw.claim_id)` | Total number of **Approved** claims |
| `total_claim_amount` | FLOAT | `SUM(claims_raw.claim_amount)` | Total money paid out for **Approved** claims |
| `loss_ratio` | FLOAT | Calculated via SQL | `total_claim_amount` / `premium_amount` |
| `renewal_status` | VARCHAR | `renewals_raw.renewal_status` | Did they renew? |
| `churn_reason` | VARCHAR | `renewals_raw.churn_reason` | Why did they leave? |
