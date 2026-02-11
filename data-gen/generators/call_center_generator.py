"""Call Center Domain Generator"""
import pandas as pd
import numpy as np
from typing import Dict
from datetime import timedelta

def generate_call_center_data(config: dict, dimensions: Dict[str, pd.DataFrame], seed: int) -> Dict[str, pd.DataFrame]:
    """Generate Call Center domain: FactSupport"""
    np.random.seed(seed)
    
    cc_config = config.get('call_center', {})
    num_tickets = cc_config.get('support_tickets', {}).get('count', 25000)
    
    dim_customer = dimensions['DimCustomer']
    dim_employee = dimensions['DimEmployee']
    dim_date = dimensions['DimDate']
    
    # Support agents only
    agents = dim_employee[dim_employee['department'] == 'Customer Support'].copy()
    if len(agents) == 0:
        agents = dim_employee.sample(n=min(50, len(dim_employee)), random_state=seed)
    
    print(f"  Generating {num_tickets:,} support tickets...")
    
    # Vectorized ticket generation
    customer_samples = dim_customer.sample(n=num_tickets, replace=True, random_state=seed)
    agent_samples = agents.sample(n=num_tickets, replace=True, random_state=seed + 1)
    date_samples = dim_date.sample(n=num_tickets, replace=True, random_state=seed + 2)
    
    # Generate ticket attributes
    channels = np.random.choice(['Phone', 'Email', 'Chat', 'Portal'], size=num_tickets, p=[0.40, 0.35, 0.20, 0.05])
    categories = np.random.choice(['Technical', 'Billing', 'General Inquiry'], size=num_tickets, p=[0.50, 0.25, 0.25])
    priorities = np.random.choice(['Critical', 'High', 'Medium', 'Low'], size=num_tickets, p=[0.05, 0.15, 0.50, 0.30])
    
    # Resolution times based on priority (hours)
    resolution_times = np.where(priorities == 'Critical', np.random.uniform(0.5, 4, num_tickets),
                       np.where(priorities == 'High', np.random.uniform(2, 24, num_tickets),
                       np.where(priorities == 'Medium', np.random.uniform(8, 72, num_tickets),
                                np.random.uniform(24, 168, num_tickets))))
    
    # CSAT scores (only 40% respond)
    csat_scores = np.full(num_tickets, np.nan)
    csat_mask = np.random.random(num_tickets) < 0.40
    csat_scores[csat_mask] = np.random.choice([1, 2, 3, 4, 5], size=csat_mask.sum(), p=[0.05, 0.10, 0.15, 0.40, 0.30])
    
    # Status
    statuses = np.random.choice(['Resolved', 'Open', 'Pending'], size=num_tickets, p=[0.85, 0.10, 0.05])
    
    df_tickets = pd.DataFrame({
        'ticket_id': [f'TKT-{i+1:08d}' for i in range(num_tickets)],
        'customer_id': customer_samples['customer_id'].values,
        'agent_id': agent_samples['employee_id'].values,
        'channel': channels,
        'category': categories,
        'priority': priorities,
        'create_date': date_samples['date'].values,
        'resolved_date': [date_samples.iloc[i]['date'] + timedelta(hours=resolution_times[i]) 
                         if statuses[i] == 'Resolved' else None 
                         for i in range(num_tickets)],
        'resolution_time_hours': [resolution_times[i] if statuses[i] == 'Resolved' else None for i in range(num_tickets)],
        'status': statuses,
        'first_contact_resolution': np.random.random(num_tickets) < 0.70,
        'csat_score': csat_scores,
        'subject': [f"{categories[i]} issue - {customer_samples.iloc[i]['customer_name']}" for i in range(num_tickets)]
    })
    
    return {'FactSupport': df_tickets}

