"""Manufacturing Domain Generator"""
import pandas as pd
import numpy as np
from typing import Dict

def generate_manufacturing_data(config: dict, dimensions: Dict[str, pd.DataFrame], seed: int) -> Dict[str, pd.DataFrame]:
    """Generate Manufacturing domain: FactProduction"""
    np.random.seed(seed)
    
    mfg_config = config.get('manufacturing', {})
    num_orders = mfg_config.get('production', {}).get('work_orders', 5000)
    
    dim_product = dimensions['DimProduct']
    dim_date = dimensions['DimDate']
    
    print(f"  Generating {num_orders:,} work orders...")
    
    # Vectorized generation
    product_samples = dim_product.sample(n=num_orders, replace=True, random_state=seed)
    date_samples = dim_date.sample(n=num_orders, replace=True, random_state=seed + 1)
    
    planned_qty = np.random.randint(10, 1000, num_orders)
    actual_qty = (planned_qty * np.random.uniform(0.92, 1.02, num_orders)).astype(int)
    scrap_qty = (planned_qty * np.random.uniform(0, 0.05, num_orders)).astype(int)
    
    plants = [f'Plant-{i+1}' for i in range(5)]
    
    df_production = pd.DataFrame({
        'work_order_id': [f'WO-{i+1:08d}' for i in range(num_orders)],
        'product_id': product_samples['product_id'].values,
        'plant': np.random.choice(plants, num_orders),
        'production_date': date_samples['date'].values,
        'planned_quantity': planned_qty,
        'actual_quantity': actual_qty,
        'scrap_quantity': scrap_qty,
        'yield_pct': np.round(actual_qty / planned_qty * 100, 2),
        'oee_pct': np.round(np.random.uniform(75, 95, num_orders), 2)
    })
    
    return {'FactProduction': df_production}
