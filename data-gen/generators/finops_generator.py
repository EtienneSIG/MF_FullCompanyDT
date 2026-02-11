"""FinOps Domain Generator"""
import pandas as pd
import numpy as np
from typing import Dict

def generate_finops_data(config: dict, dimensions: Dict[str, pd.DataFrame], seed: int) -> Dict[str, pd.DataFrame]:
    """Generate FinOps domain: FactCloudCosts"""
    np.random.seed(seed)
    
    dim_date = dimensions['DimDate']
    dim_employee = dimensions['DimEmployee']
    
    daily_dates = dim_date.copy()
    num_days = len(daily_dates)
    
    services = ['Compute', 'Storage', 'Database', 'Networking', 'Analytics']
    num_services = len(services)
    total_records = num_days * num_services
    
    print(f"  Generating {total_records:,} cloud cost records...")
    
    dates = np.repeat(daily_dates['date'].values, num_services)
    service_names = np.tile(services, num_days)
    
    # Base costs with growth trend
    base_costs = {'Compute': 5000, 'Storage': 2000, 'Database': 3000, 'Networking': 1000, 'Analytics': 1500}
    day_indices = np.repeat(np.arange(num_days), num_services)
    growth = 1 + (day_indices / num_days * 0.15)  # 15% growth over period
    
    costs = np.array([base_costs[s] for s in service_names]) * growth * np.random.uniform(0.8, 1.2, total_records)
    
    df_costs = pd.DataFrame({
        'cost_date': dates,
        'service_name': service_names,
        'provider': 'Azure',
        'cost_usd': np.round(costs, 2),
        'region': np.random.choice(['East US', 'West Europe', 'Southeast Asia'], total_records)
    })
    
    return {'FactCloudCosts': df_costs}
