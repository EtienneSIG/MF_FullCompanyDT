"""CRM Domain Generator - Placeholder"""
import pandas as pd
from typing import Dict

def generate_crm_data(config: dict, dimensions: Dict[str, pd.DataFrame], seed: int) -> Dict[str, pd.DataFrame]:
    """Generate CRM domain: FactOpportunities, FactActivities"""
    # TODO: Implement CRM data generation
    # Return empty DataFrames for now
    return {
        'FactOpportunities': pd.DataFrame(),
        'FactActivities': pd.DataFrame()
    }
