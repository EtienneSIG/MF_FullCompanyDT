"""IT Ops Domain Generator - Placeholder"""
import pandas as pd
from typing import Dict

def generate_itops_data(config: dict, dimensions: Dict[str, pd.DataFrame], seed: int) -> Dict[str, pd.DataFrame]:
    """Generate IT Ops domain: FactIncidents"""
    return {'FactIncidents': pd.DataFrame()}
