"""R&D Domain Generator"""
import pandas as pd
import numpy as np
from typing import Dict

def generate_rd_data(config: dict, dimensions: Dict[str, pd.DataFrame], seed: int) -> Dict[str, pd.DataFrame]:
    """Generate R&D domain: FactProjects"""
    np.random.seed(seed)
    
    dim_employee = dimensions['DimEmployee']
    dim_date = dimensions['DimDate']
    
    num_projects = 300
    
    print(f"  Generating {num_projects} R&D projects...")
    
    # R&D staff
    rd_staff = dim_employee[dim_employee['department'] == 'R&D'].copy()
    if len(rd_staff) == 0:
        rd_staff = dim_employee.sample(n=min(30, len(dim_employee)), random_state=seed)
    
    date_samples = dim_date.sample(n=num_projects, replace=True, random_state=seed)
    lead_samples = rd_staff.sample(n=num_projects, replace=True, random_state=seed + 1)
    
    budgets = np.random.uniform(50000, 2000000, num_projects)
    
    df_projects = pd.DataFrame({
        'project_id': [f'PRJ-{i+1:06d}' for i in range(num_projects)],
        'project_name': [f"Innovation Project {i+1}" for i in range(num_projects)],
        'start_date': date_samples['date'].values,
        'lead_id': lead_samples['employee_id'].values,
        'budget_usd': np.round(budgets, 2),
        'actual_spend_usd': np.round(budgets * np.random.uniform(0.5, 1.2, num_projects), 2),
        'phase': np.random.choice(['Research', 'Development', 'Testing', 'Completed'], num_projects, p=[0.25, 0.35, 0.25, 0.15]),
        'category': np.random.choice(['Product Innovation', 'Process Improvement', 'New Technology'], num_projects)
    })
    
    return {'FactProjects': df_projects}
