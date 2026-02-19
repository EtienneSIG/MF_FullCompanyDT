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
    dim_account = dimensions['DimAccount']
    
    monthly_dates = dim_date[dim_date['day_of_month'] == 1].copy()
    num_months = len(monthly_dates)
    total_txns = txns_per_month * num_months
    
    print(f"  Generating {total_txns:,} GL transactions using {len(dim_account)} accounts...")
    
    # Sample accounts for transactions
    dates = np.repeat(monthly_dates['date'].values, txns_per_month)
    account_samples = dim_account.sample(n=total_txns, replace=True, random_state=seed)
    
    # Generate amounts - Revenue and Expense accounts tend to have higher transaction amounts
    amounts = np.where(
        account_samples['account_type'].values == 'Revenue',
        np.random.uniform(1000, 100000, total_txns),
        np.where(
            account_samples['account_type'].values == 'Expense',
            np.random.uniform(500, 50000, total_txns),
            np.random.uniform(100, 20000, total_txns)
        )
    )
    
    df_gl = pd.DataFrame({
        'transaction_id': [f'GL-{i+1:010d}' for i in range(total_txns)],
        'transaction_date': dates,
        'account_id': account_samples['account_id'].values,
        'account_code': account_samples['account_code'].values,
        'account_name': account_samples['account_name'].values,
        'account_type': account_samples['account_type'].values,
        'amount': np.round(amounts, 2),
        'description': [f"Transaction for {name}" for name in account_samples['account_name'].values]
    })
    
    # Generate Budget data (annual budget by account)
    years = dim_date['year'].unique()
    budget_records = []
    
    for year in years:
        for _, account in dim_account.iterrows():
            # Budget amounts vary by account type
            if account['account_type'] == 'Revenue':
                budget_amt = np.random.uniform(1000000, 5000000)
            elif account['account_type'] == 'Expense':
                budget_amt = np.random.uniform(500000, 2000000)
            else:
                budget_amt = 0  # No budget for Asset/Liability/Equity accounts
            
            budget_records.append({
                'budget_id': f"BUD-{year}-{account['account_code']}",
                'fiscal_year': year,
                'account_id': account['account_id'],
                'account_code': account['account_code'],
                'account_name': account['account_name'],
                'account_type': account['account_type'],
                'budget_amount': np.round(budget_amt, 2),
                'version': 'Original'
            })
    
    df_budget = pd.DataFrame(budget_records)
    
    return {'FactGeneralLedger': df_gl, 'FactBudget': df_budget}
