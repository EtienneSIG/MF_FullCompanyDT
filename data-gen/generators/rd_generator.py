"""R&D Domain Generator"""
import pandas as pd
import numpy as np
from typing import Dict

def generate_rd_data(config: dict, dimensions: Dict[str, pd.DataFrame], seed: int) -> Dict[str, pd.DataFrame]:
    """Generate R&D domain: FactExperiments (using DimProject)"""
    np.random.seed(seed)
    
    rd_config = config.get('rd', {})
    experiments_config = rd_config.get('experiments', {})
    experiments_per_year = experiments_config.get('count', 5000)
    
    dim_employee = dimensions['DimEmployee']
    dim_date = dimensions['DimDate']
    dim_project = dimensions['DimProject']
    
    # Calculate total experiments (experiments per year * 3 years)
    num_experiments = experiments_per_year * 3
    
    print(f"  Generating {num_experiments:,} R&D experiments across {len(dim_project)} projects...")
    
    # Sample projects for experiments (with replacement, multiple experiments per project)
    project_samples = dim_project.sample(n=num_experiments, replace=True, random_state=seed)
    
    # R&D staff for experiments
    rd_staff = dim_employee[dim_employee['department'] == 'R&D'].copy()
    if len(rd_staff) == 0:
        rd_staff = dim_employee.sample(n=min(80, len(dim_employee)), random_state=seed)
    
    researcher_samples = rd_staff.sample(n=num_experiments, replace=True, random_state=seed + 1)
    date_samples = dim_date.sample(n=num_experiments, replace=True, random_state=seed + 2)
    
    # Experiment types and outcomes
    exp_types = np.random.choice(
        ['Prototype', 'Performance', 'Durability', 'Safety'],
        num_experiments,
        p=[0.40, 0.30, 0.20, 0.10]
    )
    
    success_rate = experiments_config.get('success_rate', 0.35)
    is_successful = np.random.random(num_experiments) < success_rate
    
    experiment_costs = np.random.uniform(5000, experiments_config.get('average_cost', 15000) * 2, num_experiments)
    
    df_experiments = pd.DataFrame({
        'experiment_id': [f'EXP-{i+1:08d}' for i in range(num_experiments)],
        'project_id': project_samples['project_id'].values,
        'experiment_date': date_samples['date'].values,
        'researcher_id': researcher_samples['employee_id'].values,
        'experiment_type': exp_types,
        'is_successful': is_successful,
        'cost_usd': np.round(experiment_costs, 2),
        'duration_days': np.random.randint(1, 90, num_experiments)
    })
    
    return {'FactExperiments': df_experiments}
