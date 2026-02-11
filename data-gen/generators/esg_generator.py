"""ESG Domain Generator"""
import pandas as pd
import numpy as np
from typing import Dict
from datetime import datetime

def generate_esg_data(config: dict, dimensions: Dict[str, pd.DataFrame], seed: int) -> Dict[str, pd.DataFrame]:
    """Generate ESG domain: FactEmissions, FactEnergyConsumption"""
    np.random.seed(seed)
    
    esg_config = config.get('esg', {})
    facilities_count = esg_config.get('emissions', {}).get('facilities_count', 15)
    
    dim_date = dimensions['DimDate']
    dim_geography = dimensions['DimGeography']
    
    print(f"  Generating ESG data for {facilities_count} facilities...")
    
    # Get monthly dates
    monthly_dates = dim_date[dim_date['day_of_month'] == 1].copy()
    num_months = len(monthly_dates)
    
    # Create facility records
    facilities = dim_geography.sample(n=facilities_count, random_state=seed)
    
    # Generate emissions data (monthly per facility)
    total_records = facilities_count * num_months
    
    # Repeat facilities and dates
    facility_ids = np.repeat(facilities['city'].values, num_months)
    dates = np.tile(monthly_dates['date'].values, facilities_count)
    
    # Generate emission values (declining trend -5% annually)
    base_emissions = np.random.uniform(100, 5000, facilities_count)
    month_indices = np.tile(np.arange(num_months), facilities_count)
    reduction_factor = (1 - 0.05) ** (month_indices / 12)  # 5% annual reduction
    emissions = np.repeat(base_emissions, num_months) * reduction_factor * np.random.uniform(0.9, 1.1, total_records)
    
    # Split by scope
    scope_1 = emissions * 0.35
    scope_2 = emissions * 0.45
    scope_3 = emissions * 0.20
    
    df_emissions = pd.DataFrame({
        'facility_name': facility_ids,
        'measurement_date': dates,
        'scope_1_co2_tonnes': np.round(scope_1, 2),
        'scope_2_co2_tonnes': np.round(scope_2, 2),
        'scope_3_co2_tonnes': np.round(scope_3, 2),
        'total_co2_tonnes': np.round(emissions, 2),
        'renewable_energy_pct': np.random.uniform(10, 60, total_records).round(1)
    })
    
    return {
        'FactEmissions': df_emissions
    }
