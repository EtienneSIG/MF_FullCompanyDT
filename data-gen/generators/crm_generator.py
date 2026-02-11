"""CRM Domain Generator"""
import pandas as pd
import numpy as np
from typing import Dict
from datetime import datetime, timedelta

def generate_crm_data(config: dict, dimensions: Dict[str, pd.DataFrame], seed: int) -> Dict[str, pd.DataFrame]:
    """Generate CRM domain: FactOpportunities, FactActivities"""
    np.random.seed(seed)
    
    crm_config = config.get('crm', {})
    num_opportunities = crm_config.get('opportunities', {}).get('count', 10000)
    activities_per_opp = crm_config.get('activities', {}).get('per_opportunity', 3)
    
    dim_customer = dimensions['DimCustomer']
    dim_employee = dimensions['DimEmployee']
    dim_date = dimensions['DimDate']
    
    # Sales reps only (filter employees)
    sales_reps = dim_employee[
        dim_employee['department'].isin(['Sales', 'Business Development'])
    ].copy()
    
    if len(sales_reps) == 0:
        # If no sales dept, use random employees
        sales_reps = dim_employee.sample(n=min(100, len(dim_employee)), random_state=seed)
    
    print(f"  Generating {num_opportunities:,} opportunities...")
    
    # Vectorized approach - create all opportunities at once
    customer_samples = dim_customer.sample(n=num_opportunities, replace=True, random_state=seed)
    sales_rep_samples = sales_reps.sample(n=num_opportunities, replace=True, random_state=seed + 1)
    date_samples = dim_date.sample(n=num_opportunities, replace=True, random_state=seed + 2)
    
    # Generate stages
    stages = ['Prospecting', 'Qualification', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
    weights = [0.15, 0.20, 0.25, 0.20, 0.15, 0.05]
    stage_values = np.random.choice(stages, size=num_opportunities, p=weights)
    
    # Generate amounts based on segment
    amounts = np.zeros(num_opportunities)
    segments = customer_samples['segment'].values
    
    for i in range(num_opportunities):
        if segments[i] == 'ENTERPRISE':
            amounts[i] = np.random.uniform(50000, 500000)
        elif segments[i] == 'STRATEGIC':
            amounts[i] = np.random.uniform(25000, 200000)
        else:  # SMB
            amounts[i] = np.random.uniform(1000, 25000)
    
    # Probability mapping
    prob_map = {
        'Prospecting': 10, 'Qualification': 25, 'Proposal': 50,
        'Negotiation': 75, 'Closed Won': 100, 'Closed Lost': 0
    }
    probabilities = [prob_map[s] for s in stage_values]
    
    # Create DataFrame
    df_opportunities = pd.DataFrame({
        'opportunity_id': [f'OPP-{i+1:06d}' for i in range(num_opportunities)],
        'customer_id': customer_samples['customer_id'].values,
        'sales_rep_id': sales_rep_samples['employee_id'].values,
        'opportunity_name': [f"{customer_samples.iloc[i]['customer_name']} - {np.random.choice(['Product A', 'Product B', 'Service Package', 'Enterprise Solution'])}" 
                            for i in range(num_opportunities)],
        'stage': stage_values,
        'amount': np.round(amounts, 2),
        'probability_pct': probabilities,
        'create_date': date_samples['date'].values,
        'close_date': [date_samples.iloc[i]['date'] + timedelta(days=np.random.randint(30, 180)) 
                      if stage_values[i] in ['Closed Won', 'Closed Lost'] else None 
                      for i in range(num_opportunities)],
        'is_closed': [s in ['Closed Won', 'Closed Lost'] for s in stage_values],
        'is_won': [s == 'Closed Won' for s in stage_values],
        'expected_revenue': np.round(amounts * np.array(probabilities) / 100, 2),
        'lead_source': np.random.choice(['Website', 'Referral', 'Cold Call', 'Event', 'Partner'], size=num_opportunities),
        'region': customer_samples['region'].values
    })
    
    print(f"  Generating activities (max {num_opportunities * activities_per_opp:,})...")
    
    # Generate activities - only for 60% of opportunities for speed
    num_opps_with_activities = int(num_opportunities * 0.6)
    activities = []
    
    for i in range(num_opps_with_activities):
        opp = df_opportunities.iloc[i]
        num_acts = np.random.randint(1, activities_per_opp + 1)
        
        for j in range(num_acts):
            activities.append({
                'activity_id': f"ACT-{len(activities)+1:08d}",
                'opportunity_id': opp['opportunity_id'],
                'customer_id': opp['customer_id'],
                'employee_id': opp['sales_rep_id'],
                'activity_type': np.random.choice(['Call', 'Email', 'Meeting', 'Demo', 'Proposal Sent', 'Follow-up']),
                'activity_date': opp['create_date'] + timedelta(days=np.random.randint(0, 90)),
                'duration_minutes': np.random.choice([15, 30, 60, 90]),
                'outcome': np.random.choice(['Completed', 'No Answer', 'Rescheduled', 'Cancelled'], p=[0.7, 0.15, 0.1, 0.05]),
                'notes': f"Activity for {opp['opportunity_name']}"
            })
    
    df_activities = pd.DataFrame(activities)
    
    return {
        'FactOpportunities': df_opportunities,
        'FactActivities': df_activities
    }
