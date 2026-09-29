-- etl_queries.sql
-- This script simulates the transformation layer in a Data Warehouse

-- 1. Drop existing final table if it exists
DROP TABLE IF EXISTS fact_policy_lifecycle;

-- 2. Create the final Curated Fact Table by joining all data
CREATE TABLE fact_policy_lifecycle AS
SELECT 
    p.policy_id,
    p.customer_name,
    p.policy_type,
    p.premium_amount,
    p.status AS policy_status,
    COALESCE(c.total_claims, 0) AS total_claims_count,
    COALESCE(c.total_claim_amount, 0) AS total_claim_amount,
    
    -- Calculate Loss Ratio (Total Claims / Premium)
    CASE 
        WHEN p.premium_amount > 0 THEN ROUND(COALESCE(c.total_claim_amount, 0) / p.premium_amount, 2)
        ELSE 0 
    END AS loss_ratio,
    
    r.renewal_status,
    r.churn_reason
FROM policies_raw p

-- Join Claims Data (Aggregated per policy)
LEFT JOIN (
    SELECT 
        policy_id, 
        COUNT(claim_id) as total_claims, 
        SUM(claim_amount) as total_claim_amount
    FROM claims_raw
    WHERE claim_status = 'Approved'
    GROUP BY policy_id
) c ON p.policy_id = c.policy_id

-- Join Renewals Data
LEFT JOIN renewals_raw r ON p.policy_id = r.policy_id;
