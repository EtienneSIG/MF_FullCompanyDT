"""IT Ops Domain Generator"""
import pandas as pd
import numpy as np
from typing import Dict
from datetime import timedelta

def generate_itops_data(config: dict, dimensions: Dict[str, pd.DataFrame], seed: int) -> Dict[str, pd.DataFrame]:
    """Generate IT Ops domain: FactIncidents"""
    np.random.seed(seed)
    
    it_config = config.get('it_ops', {})
    num_incidents = it_config.get('incidents', {}).get('count', 20000)
    
    dim_employee = dimensions['DimEmployee']
    dim_date = dimensions['DimDate']
    
    # IT staff only
    it_staff = dim_employee[dim_employee['department'] == 'Engineering'].copy()
    if len(it_staff) == 0:
        it_staff = dim_employee.sample(n=min(50, len(dim_employee)), random_state=seed)
    
    print(f"  Generating {num_incidents:,} IT incidents...")
    
    # Vectorized generation
    assignee_samples = it_staff.sample(n=num_incidents, replace=True, random_state=seed)
    date_samples = dim_date.sample(n=num_incidents, replace=True, random_state=seed + 1)
    
    severities = np.random.choice(['P1', 'P2', 'P3', 'P4'], size=num_incidents, p=[0.05, 0.15, 0.40, 0.40])
    categories = np.random.choice(['Infrastructure', 'Application', 'Network', 'Security', 'Database'], num_incidents)
    
    # Resolution time based on severity (hours)
    resolution_times = np.where(severities == 'P1', np.random.uniform(0.5, 4, num_incidents),
                       np.where(severities == 'P2', np.random.uniform(2, 24, num_incidents),
                       np.where(severities == 'P3', np.random.uniform(8, 72, num_incidents),
                                np.random.uniform(24, 240, num_incidents))))
    
    statuses = np.random.choice(['Resolved', 'In Progress', 'Open'], size=num_incidents, p=[0.80, 0.15, 0.05])
    
    df_incidents = pd.DataFrame({
        'incident_id': [f'INC-{i+1:08d}' for i in range(num_incidents)],
        'assignee_id': assignee_samples['employee_id'].values,
        'severity': severities,
        'category': categories,
        'create_date': date_samples['date'].values,
        'resolved_date': [date_samples.iloc[i]['date'] + timedelta(hours=resolution_times[i]) 
                         if statuses[i] == 'Resolved' else None 
                         for i in range(num_incidents)],
        'resolution_time_hours': [resolution_times[i] if statuses[i] == 'Resolved' else None for i in range(num_incidents)],
        'status': statuses,
        'description': [f"{severities[i]} - {categories[i]} issue" for i in range(num_incidents)]
    })
    
    return {'FactIncidents': df_incidents}
