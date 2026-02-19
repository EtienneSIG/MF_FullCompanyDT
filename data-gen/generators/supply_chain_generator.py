"""Supply Chain Domain Generator"""
import pandas as pd
import numpy as np
from typing import Dict
from datetime import timedelta

def generate_supply_chain_data(config: dict, dimensions: Dict[str, pd.DataFrame], seed: int) -> Dict[str, pd.DataFrame]:
    """Generate Supply Chain domain: FactInventory, FactPurchaseOrders"""
    np.random.seed(seed)
    
    sc_config = config.get('supply_chain', {})
    num_pos = sc_config.get('purchase_orders', {}).get('count', 10000)
    lines_per_po = sc_config.get('purchase_orders', {}).get('lines_per_po', 3)
    
    dim_product = dimensions['DimProduct']
    dim_date = dimensions['DimDate']
    dim_facility = dimensions.get('DimFacility', None)
    
    print(f"  Generating {num_pos:,} purchase orders...")
    
    # ===== FactPurchaseOrders =====
    date_samples = dim_date.sample(n=num_pos, replace=True, random_state=seed)
    
    # Generate PO lines
    total_lines = num_pos * lines_per_po
    product_samples = dim_product.sample(n=total_lines, replace=True, random_state=seed + 1)
    po_ids = np.repeat([f'PO-{i+1:08d}' for i in range(num_pos)], lines_per_po)
    po_dates = np.repeat(date_samples['date'].values, lines_per_po)
    
    quantities = np.random.randint(10, 500, total_lines)
    unit_costs = product_samples['unit_cost'].values * np.random.uniform(0.9, 1.1, total_lines)
    
    # Delivery dates
    lead_times = np.random.randint(7, 90, total_lines)
    expected_delivery = pd.to_datetime(po_dates) + pd.to_timedelta(lead_times, unit='D')
    
    # Actual delivery (85% on time, 15% late or early)
    actual_delivery = expected_delivery + pd.to_timedelta(
        np.random.randint(-5, 15, total_lines), unit='D'
    )
    
    statuses = np.random.choice(['Received', 'In Transit', 'Pending'], total_lines, p=[0.70, 0.20, 0.10])
    
    # Supplier IDs
    supplier_ids = [f"SUP_{np.random.randint(1, 101):03d}" for _ in range(total_lines)]
    
    df_po_lines = pd.DataFrame({
        'po_id': po_ids,
        'po_line_id': np.tile(np.arange(1, lines_per_po + 1), num_pos),
        'supplier_id': supplier_ids,
        'product_id': product_samples['product_id'].values,
        'order_date': po_dates,
        'expected_delivery_date': expected_delivery,
        'actual_delivery_date': [actual_delivery[i] if statuses[i] == 'Received' else None 
                                for i in range(total_lines)],
        'quantity': quantities,
        'unit_price': np.round(unit_costs, 2),
        'total_amount': np.round(quantities * unit_costs, 2),
        'status': statuses,
        'days_late': [
            (actual_delivery[i] - expected_delivery[i]).days if statuses[i] == 'Received' else None
            for i in range(total_lines)
        ]
    })
    
    # ===== FactInventory =====
    print(f"  Generating inventory snapshots...")
    
    # Get daily snapshot dates (use every 7th day for performance)
    snapshot_dates = dim_date[dim_date['day_of_month'].isin([1, 8, 15, 22])].copy()
    num_snapshots = len(snapshot_dates)
    
    # Use facilities as warehouses (or generate default warehouses if DimFacility doesn't exist)
    if dim_facility is not None:
        warehouses = dim_facility[dim_facility['facility_type'] == 'Warehouse'].copy()
        if len(warehouses) == 0:
            warehouses = dim_facility.sample(n=min(5, len(dim_facility)), random_state=seed)
        warehouse_ids = warehouses['facility_id'].values
        warehouse_names = warehouses['facility_name'].values
    else:
        warehouse_count = sc_config.get('inventory', {}).get('warehouse_count', 10)
        warehouse_ids = [f"WH_{i:03d}" for i in range(warehouse_count)]
        warehouse_names = [f"Warehouse {i+1}" for i in range(warehouse_count)]
    
    num_warehouses = len(warehouse_ids)
    
    # Sample products (60% of products in each warehouse)
    products_per_warehouse = int(len(dim_product) * 0.60)
    
    # Generate inventory snapshots
    inventory_records = []
    
    for snapshot_date in snapshot_dates['date'].values:
        for wh_idx in range(num_warehouses):
            # Sample products for this warehouse
            warehouse_products = dim_product.sample(n=products_per_warehouse, replace=False, 
                                                   random_state=seed + wh_idx)
            
            for _, product in warehouse_products.iterrows():
                # Generate inventory levels
                reorder_point = np.random.randint(50, 500)
                max_level = reorder_point * 3
                on_hand = np.random.randint(0, max_level)
                on_order = np.random.randint(0, reorder_point * 2) if on_hand < reorder_point else 0
                
                inventory_records.append({
                    'snapshot_date': snapshot_date,
                    'warehouse_id': warehouse_ids[wh_idx],
                    'warehouse_name': warehouse_names[wh_idx],
                    'product_id': product['product_id'],
                    'quantity_on_hand': on_hand,
                    'quantity_on_order': on_order,
                    'quantity_available': on_hand,
                    'reorder_point': reorder_point,
                    'unit_cost': product['unit_cost'],
                    'inventory_value': np.round(on_hand * product['unit_cost'], 2),
                    'is_stockout': on_hand == 0
                })
    
    df_inventory = pd.DataFrame(inventory_records)
    print(f"  Generated {len(df_inventory):,} inventory snapshot records")
    
    return {'FactPurchaseOrders': df_po_lines, 'FactInventory': df_inventory}
