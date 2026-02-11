"""HR Domain Generator"""
import pandas as pd
import numpy as np
from typing import Dict
from datetime import timedelta

def generate_hr_data(config: dict, dimensions: Dict[str, pd.DataFrame], seed: int) -> Dict[str, pd.DataFrame]:
    """Generate HR domain: FactAttrition, FactHiring"""
    np.random.seed(seed)
    
    hr_config = config.get('hr', {})
    attrition_rate = hr_config.get('attrition', {}).get('annual_rate', 0.07)
    num_hires = hr_config.get('hiring', {}).get('count', 800)
    
    dim_employee = dimensions['DimEmployee']
    dim_date = dimensions['DimDate']
    
    print(f"  Generating HR data...")
    
    # FactAttrition - employees who left
    num_attrition = int(len(dim_employee) * attrition_rate * 3)  # 3 years
    
    attrition_employees = dim_employee.sample(n=min(num_attrition, len(dim_employee)), random_state=seed)
    attrition_dates = dim_date.sample(n=len(attrition_employees), replace=True, random_state=seed + 1)
    
    attrition_types = np.random.choice(['Voluntary', 'Involuntary', 'Retirement'], 
                                       size=len(attrition_employees), p=[0.75, 0.20, 0.05])
    
    # Calculate tenure_years from hire_date (assuming termination date is the reference)
    tenure_years = np.random.uniform(0.5, 15.0, len(attrition_employees))
    
    df_attrition = pd.DataFrame({
        'employee_id': attrition_employees['employee_id'].values,
        'termination_date': attrition_dates['date'].values,
        'termination_type': attrition_types,
        'is_regrettable': np.random.random(len(attrition_employees)) < 0.60,
        'department': attrition_employees['department'].values,
        'tenure_years': np.round(tenure_years, 1)
    })
    
    # FactHiring - new hires
    hire_dates = dim_date.sample(n=num_hires, replace=True, random_state=seed + 2)
    
    time_to_fill = np.random.uniform(21, 120, num_hires)
    sources = np.random.choice(['Referral', 'LinkedIn', 'Job Board', 'Agency'], 
                               size=num_hires, p=[0.35, 0.30, 0.25, 0.10])
    
    df_hiring = pd.DataFrame({
        'req_id': [f'REQ-{i+1:06d}' for i in range(num_hires)],
        'position_title': np.random.choice(['Software Engineer', 'Sales Rep', 'Customer Support', 'Analyst', 'Manager'], num_hires),
        'hire_date': hire_dates['date'].values,
        'time_to_fill_days': np.round(time_to_fill, 0).astype(int),
        'source': sources,
        'department': np.random.choice(dim_employee['department'].unique(), num_hires)
    })
    
    return {
        'FactAttrition': df_attrition,
        'FactHiring': df_hiring
    }

