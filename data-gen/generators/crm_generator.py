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
    activities_per_opp = crm_config.get('activities', {}).get('per_opportunity', 5)
    
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
    
    # FactOpportunities
    opportunities = []
    
    for i in range(num_opportunities):
        customer = dim_customer.sample(n=1, random_state=seed + i).iloc[0]
        sales_rep = sales_reps.sample(n=1, random_state=seed + i).iloc[0]
        
        # Create date - random date in last 2 years
        create_date = dim_date.sample(n=1, random_state=seed + i).iloc[0]['date']
        
        # Close date - 30-180 days after create
        days_to_close = np.random.randint(30, 180)
        close_date = create_date + timedelta(days=days_to_close)
        
        # Stage
        stages = ['Prospecting', 'Qualification', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
        weights = [0.15, 0.20, 0.25, 0.20, 0.15, 0.05]
        stage = np.random.choice(stages, p=weights)
        
        # Amount based on customer segment
        if customer['segment'] == 'ENTERPRISE':
            amount = np.random.uniform(50000, 500000)
        elif customer['segment'] == 'STRATEGIC':
            amount = np.random.uniform(25000, 200000)
        else:  # SMB
            amount = np.random.uniform(1000, 25000)
        
        # Probability
        prob_map = {
            'Prospecting': 10,
            'Qualification': 25,
            'Proposal': 50,
            'Negotiation': 75,
            'Closed Won': 100,
            'Closed Lost': 0
        }
        probability = prob_map[stage]
        
        is_closed = stage in ['Closed Won', 'Closed Lost']
        is_won = stage == 'Closed Won'
        
        opportunities.append({
            'opportunity_id': f'OPP-{i+1:06d}',
            'customer_id': customer['customer_id'],
            'sales_rep_id': sales_rep['employee_id'],
            'opportunity_name': f"{customer['customer_name']} - {np.random.choice(['Product A', 'Product B', 'Service Package', 'Enterprise Solution'])}",
            'stage': stage,
            'amount': round(amount, 2),
            'probability_pct': probability,
            'create_date': create_date,
            'close_date': close_date if is_closed else None,
            'is_closed': is_closed,
            'is_won': is_won,
            'expected_revenue': round(amount * probability / 100, 2),
            'lead_source': np.random.choice(['Website', 'Referral', 'Cold Call', 'Event', 'Partner']),
            'region': customer['region']
        })
    
    df_opportunities = pd.DataFrame(opportunities)
    
    # FactActivities
    activities = []
    activity_types = ['Call', 'Email', 'Meeting', 'Demo', 'Proposal Sent', 'Follow-up']
    
    for opp in opportunities[:int(num_opportunities * 0.8)]:  # 80% of opps have activities
        num_activities = np.random.randint(1, activities_per_opp + 1)
        
        for j in range(num_activities):
            activity_date = opp['create_date'] + timedelta(days=np.random.randint(0, 90))
            
            activities.append({
                'activity_id': f"ACT-{len(activities)+1:08d}",
                'opportunity_id': opp['opportunity_id'],
                'customer_id': opp['customer_id'],
                'employee_id': opp['sales_rep_id'],
                'activity_type': np.random.choice(activity_types),
                'activity_date': activity_date,
                'duration_minutes': np.random.choice([15, 30, 60, 90]),
                'outcome': np.random.choice(['Completed', 'No Answer', 'Rescheduled', 'Cancelled'], p=[0.7, 0.15, 0.1, 0.05]),
                'notes': f"Activity for {opp['opportunity_name']}"
            })
    
    df_activities = pd.DataFrame(activities)
    
    return {
        'FactOpportunities': df_opportunities,
        'FactActivities': df_activities
    }
