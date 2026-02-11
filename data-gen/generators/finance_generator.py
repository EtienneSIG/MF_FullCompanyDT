"""Finance Domain Generator - Placeholder"""
import pandas as pd
from typing import Dict

def generate_finance_data(config: dict, dimensions: Dict[str, pd.DataFrame], seed: int) -> Dict[str, pd.DataFrame]:
    """Generate Finance domain: FactGeneralLedger, FactBudget"""
    return {'FactGeneralLedger': pd.DataFrame(), 'FactBudget': pd.DataFrame()}
