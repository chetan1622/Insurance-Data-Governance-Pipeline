import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os

fake = Faker()

# Create data directory
os.makedirs('data/raw', exist_ok=True)

print("Generating 50,000 Policyholder records...")

# 1. Generate Policies
policy_ids = [f"POL-{fake.unique.random_int(min=100000, max=999999)}" for _ in range(50000)]
policies = []
for pid in policy_ids:
    start_date = fake.date_between(start_date='-3y', end_date='today')
    end_date = start_date + timedelta(days=365)
    policies.append({
        'policy_id': pid,
        'customer_name': fake.name(),
        'policy_type': random.choice(['Auto', 'Home', 'Health', 'Life']),
        'premium_amount': round(random.uniform(500, 5000), 2),
        'start_date': start_date,
        'end_date': end_date,
        'status': random.choice(['Active', 'Expired', 'Cancelled'])
    })

df_policies = pd.DataFrame(policies)
df_policies.to_csv('data/raw/policies_raw.csv', index=False)
print("Policies generated.")

# 2. Generate Claims (Not everyone has a claim)
print("Generating Claims...")
claims = []
claim_policy_ids = random.sample(policy_ids, 15000) # 15k policies have claims
for pid in claim_policy_ids:
    claim_date = fake.date_between(start_date='-2y', end_date='today')
    claims.append({
        'claim_id': f"CLM-{fake.unique.random_int(min=100000, max=999999)}",
        'policy_id': pid,
        'claim_date': claim_date,
        'claim_amount': round(random.uniform(100, 20000), 2),
        'claim_status': random.choice(['Approved', 'Rejected', 'Pending', 'Under Review'])
    })

df_claims = pd.DataFrame(claims)
df_claims.to_csv('data/raw/claims_raw.csv', index=False)
print("Claims generated.")

# 3. Generate Renewals
print("Generating Renewals...")
renewals = []
renewal_policy_ids = random.sample(policy_ids, 30000) 
for pid in renewal_policy_ids:
    renewals.append({
        'policy_id': pid,
        'renewal_date': fake.date_between(start_date='-1y', end_date='+1y'),
        'renewal_status': random.choice(['Renewed', 'Lapsed']),
        'churn_reason': random.choice(['Competitor Pricing', 'Poor Service', 'Not Needed', 'High Premium']) 
    })

df_renewals = pd.DataFrame(renewals)
# Fixing churn reason logic: If renewed, churn reason should be None
df_renewals.loc[df_renewals['renewal_status'] == 'Renewed', 'churn_reason'] = None
df_renewals.to_csv('data/raw/renewals_raw.csv', index=False)
print("Renewals generated.")

print("Data Generation Complete! Files saved in 'data/raw/' folder.")
