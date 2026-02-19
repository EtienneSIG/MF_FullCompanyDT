"""Manufacturing Domain Generator"""
import pandas as pd
import numpy as np
from typing import Dict
from datetime import timedelta

def generate_manufacturing_data(config: dict, dimensions: Dict[str, pd.DataFrame], seed: int) -> Dict[str, pd.DataFrame]:
    """Generate Manufacturing domain: FactProduction, FactWorkOrders"""
    np.random.seed(seed)
    
    mfg_config = config.get('manufacturing', {})
    num_orders = mfg_config.get('production', {}).get('work_orders', 5000)
    
    dim_product = dimensions['DimProduct']
    dim_date = dimensions['DimDate']
    dim_employee = dimensions['DimEmployee']
    dim_facility = dimensions.get('DimFacility', None)
    
    print(f"  Generating {num_orders:,} work orders and production records...")
    
    # Get manufacturing facilities
    if dim_facility is not None:
        plants = dim_facility[dim_facility['facility_type'] == 'Manufacturing'].copy()
        if len(plants) == 0:
            plants = dim_facility.sample(n=min(3, len(dim_facility)), random_state=seed)
        plant_ids = plants['facility_id'].values
        plant_names = plants['facility_name'].values
    else:
        plant_count = 5
        plant_ids = [f'PLANT_{i+1:02d}' for i in range(plant_count)]
        plant_names = [f'Plant {i+1}' for i in range(plant_count)]
    
    # ===== FactWorkOrders =====
    product_samples = dim_product.sample(n=num_orders, replace=True, random_state=seed)
    start_date_samples = dim_date.sample(n=num_orders, replace=True, random_state=seed + 1)
    
    # Work order status
    statuses = np.random.choice(
        ['Released', 'In Progress', 'Complete', 'On Hold', 'Cancelled'],
        num_orders,
        p=[0.15, 0.25, 0.50, 0.05, 0.05]
    )
    
    # Planned quantities
    planned_qty = np.random.randint(10, 1000, num_orders)
    
    # Duration in days (based on quantity)
    duration_days = (planned_qty / 100 * np.random.uniform(1, 5, num_orders)).astype(int)
    duration_days = np.maximum(duration_days, 1)  # At least 1 day
    
    # Calculate due dates
    start_dates = start_date_samples['date'].values
    due_dates = pd.to_datetime(start_dates) + pd.to_timedelta(duration_days, unit='D')
    
    # Assign supervisors from operations
    ops_staff = dim_employee[dim_employee['department'] == 'Operations'].copy()
    if len(ops_staff) == 0:
        ops_staff = dim_employee.sample(n=min(50, len(dim_employee)), random_state=seed)
    
    supervisor_samples = ops_staff.sample(n=num_orders, replace=True, random_state=seed + 2)
    
    # Priority
    priorities = np.random.choice(['Low', 'Normal', 'High', 'Urgent'], num_orders, p=[0.15, 0.60, 0.20, 0.05])
    
    df_work_orders = pd.DataFrame({
        'work_order_id': [f'WO-{i+1:08d}' for i in range(num_orders)],
        'product_id': product_samples['product_id'].values,
        'facility_id': np.random.choice(plant_ids, num_orders),
        'start_date': start_dates,
        'due_date': due_dates,
        'status': statuses,
        'planned_quantity': planned_qty,
        'priority': priorities,
        'supervisor_id': supervisor_samples['employee_id'].values
    })
    
    # ===== FactProduction =====
    # Only completed work orders have production records
    completed_wo = df_work_orders[df_work_orders['status'] == 'Complete'].copy()
    num_production = len(completed_wo)
    
    print(f"  Generated {num_production:,} production records from completed work orders")
    
    # Vectorized generation for production
    actual_qty = (completed_wo['planned_quantity'].values * np.random.uniform(0.92, 1.02, num_production)).astype(int)
    scrap_qty = (completed_wo['planned_quantity'].values * np.random.uniform(0, 0.05, num_production)).astype(int)
    
    # Actual completion dates (due date +/- some days)
    completion_dates = pd.to_datetime(completed_wo['due_date'].values) + pd.to_timedelta(
        np.random.randint(-3, 10, num_production), unit='D'
    )
    
    df_production = pd.DataFrame({
        'production_id': [f'PROD-{i+1:08d}' for i in range(num_production)],
        'work_order_id': completed_wo['work_order_id'].values,
        'product_id': completed_wo['product_id'].values,
        'facility_id': completed_wo['facility_id'].values,
        'production_date': completion_dates,
        'planned_quantity': completed_wo['planned_quantity'].values,
        'actual_quantity': actual_qty,
        'scrap_quantity': scrap_qty,
        'yield_pct': np.round(actual_qty / completed_wo['planned_quantity'].values * 100, 2),
        'oee_pct': np.round(np.random.uniform(75, 95, num_production), 2),
        'labor_hours': np.round(completed_wo['planned_quantity'].values / 10 * np.random.uniform(0.8, 1.2, num_production), 1),
        'machine_hours': np.round(completed_wo['planned_quantity'].values / 15 * np.random.uniform(0.8, 1.2, num_production), 1)
    })
    
    return {
        'FactWorkOrders': df_work_orders,
        'FactProduction': df_production
    }
