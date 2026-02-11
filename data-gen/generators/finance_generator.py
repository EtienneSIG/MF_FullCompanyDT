"""Finance Domain Generator"""
import pandas as pd
import numpy as np
from typing import Dict

def generate_finance_data(config: dict, dimensions: Dict[str, pd.DataFrame], seed: int) -> Dict[str, pd.DataFrame]:
    """Generate Finance domain: FactGeneralLedger, FactBudget"""
    np.random.seed(seed)
    
    fin_config = config.get('finance', {})
    txns_per_month = fin_config.get('general_ledger', {}).get('transactions_per_month', 5000)
    
    dim_date = dimensions['DimDate']
    monthly_dates = dim_date[dim_date['day_of_month'] == 1].copy()
    num_months = len(monthly_dates)
    total_txns = txns_per_month * num_months
    
    print(f"  Generating {total_txns:,} GL transactions...")
    
    accounts = [
        ('1000', 'Cash', 'Asset'), ('1100', 'AR', 'Asset'), ('1200', 'Inventory', 'Asset'),
        ('2000', 'AP', 'Liability'), ('3000', 'Equity', 'Equity'),
        ('4000', 'Revenue', 'Revenue'), ('5000', 'COGS', 'Expense'), ('6000', 'OpEx', 'Expense')
    ]
    
    dates = np.repeat(monthly_dates['date'].values, txns_per_month)
    account_samples = [accounts[i] for i in np.random.randint(0, len(accounts), total_txns)]
    amounts = np.random.uniform(100, 50000, total_txns)
    
    df_gl = pd.DataFrame({
        'transaction_id': [f'GL-{i+1:010d}' for i in range(total_txns)],
        'transaction_date': dates,
        'account_number': [acc[0] for acc in account_samples],
        'account_name': [acc[1] for acc in account_samples],
        'account_type': [acc[2] for acc in account_samples],
        'amount': np.round(amounts, 2)
    })
    
    return {'FactGeneralLedger': df_gl, 'FactBudget': pd.DataFrame()}
