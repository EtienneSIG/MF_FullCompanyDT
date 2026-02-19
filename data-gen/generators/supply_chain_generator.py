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
    
    # Get weekly snapshot dates (use every 7th day for performance)
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
    
    # Optimize: Sample products once (30% of products in each warehouse for performance)
    products_per_warehouse = int(len(dim_product) * 0.30)  # Reduced from 0.60
    
    # Vectorized generation - sample products once per warehouse
    np.random.seed(seed + 10)
    
    # Pre-calculate total records
    total_inventory_records = num_snapshots * num_warehouses * products_per_warehouse
    print(f"  Generating {total_inventory_records:,} inventory records (vectorized)...")
    
    # Generate all combinations using numpy arrays (much faster)
    snapshot_dates_array = snapshot_dates['date'].values
    
    # Create arrays for each dimension
    all_snapshot_dates = []
    all_warehouse_ids = []
    all_warehouse_names = []
    all_product_ids = []
    all_unit_costs = []
    
    for wh_idx in range(num_warehouses):
        # Sample products for this warehouse once
        warehouse_products = dim_product.sample(n=products_per_warehouse, replace=False, 
                                               random_state=seed + wh_idx + 100)
        
        # Repeat for all snapshot dates
        all_snapshot_dates.extend(np.repeat(snapshot_dates_array, products_per_warehouse))
        all_warehouse_ids.extend([warehouse_ids[wh_idx]] * (num_snapshots * products_per_warehouse))
        all_warehouse_names.extend([warehouse_names[wh_idx]] * (num_snapshots * products_per_warehouse))
        all_product_ids.extend(np.tile(warehouse_products['product_id'].values, num_snapshots))
        all_unit_costs.extend(np.tile(warehouse_products['unit_cost'].values, num_snapshots))
    
    # Convert to numpy arrays for vectorized operations
    all_unit_costs = np.array(all_unit_costs)
    
    # Generate inventory levels (vectorized)
    reorder_points = np.random.randint(50, 500, total_inventory_records)
    max_levels = reorder_points * 3
    on_hand = np.random.randint(0, 1000, total_inventory_records)  # Simplified for speed
    
    # On order logic (vectorized)
    below_reorder = on_hand < reorder_points
    on_order = np.where(below_reorder, np.random.randint(0, 500, total_inventory_records), 0)
    
    # Create DataFrame in one shot (much faster than appending)
    df_inventory = pd.DataFrame({
        'snapshot_date': all_snapshot_dates,
        'warehouse_id': all_warehouse_ids,
        'warehouse_name': all_warehouse_names,
        'product_id': all_product_ids,
        'quantity_on_hand': on_hand,
        'quantity_on_order': on_order,
        'quantity_available': on_hand,
        'reorder_point': reorder_points,
        'unit_cost': np.round(all_unit_costs, 2),
        'inventory_value': np.round(on_hand * all_unit_costs, 2),
        'is_stockout': on_hand == 0
    })
    
    print(f"  Generated {len(df_inventory):,} inventory snapshot records")
    
    return {'FactPurchaseOrders': df_po_lines, 'FactInventory': df_inventory}
