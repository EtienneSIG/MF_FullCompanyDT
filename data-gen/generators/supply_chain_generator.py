"""Supply Chain Domain Generator"""
import pandas as pd
import numpy as np
from typing import Dict

def generate_supply_chain_data(config: dict, dimensions: Dict[str, pd.DataFrame], seed: int) -> Dict[str, pd.DataFrame]:
    """Generate Supply Chain domain: FactInventory, FactPurchaseOrders"""
    np.random.seed(seed)
    
    sc_config = config.get('supply_chain', {})
    num_pos = sc_config.get('purchase_orders', {}).get('count', 10000)
    lines_per_po = sc_config.get('purchase_orders', {}).get('lines_per_po', 3)
    
    dim_product = dimensions['DimProduct']
    dim_date = dimensions['DimDate']
    
    print(f"  Generating {num_pos:,} purchase orders...")
    
    date_samples = dim_date.sample(n=num_pos, replace=True, random_state=seed)
    
    # Generate PO lines
    total_lines = num_pos * lines_per_po
    product_samples = dim_product.sample(n=total_lines, replace=True, random_state=seed + 1)
    po_ids = np.repeat([f'PO-{i+1:08d}' for i in range(num_pos)], lines_per_po)
    
    quantities = np.random.randint(10, 500, total_lines)
    unit_costs = np.random.uniform(10, 500, total_lines)
    
    df_po_lines = pd.DataFrame({
        'po_id': po_ids,
        'line_number': np.tile(np.arange(1, lines_per_po + 1), num_pos),
        'product_id': product_samples['product_id'].values,
        'quantity': quantities,
        'unit_cost': np.round(unit_costs, 2),
        'line_total': np.round(quantities * unit_costs, 2),
        'order_date': np.repeat(date_samples['date'].values, lines_per_po),
        'status': np.random.choice(['Received', 'In Transit', 'Pending'], total_lines, p=[0.70, 0.20, 0.10])
    })
    
    return {'FactPurchaseOrders': df_po_lines, 'FactInventory': pd.DataFrame()}
