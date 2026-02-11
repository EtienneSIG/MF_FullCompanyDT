"""
Sales Domain Data Generator
Generates FactSales and FactReturns tables
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import Dict


def generate_sales_data(config: dict, dimensions: Dict[str, pd.DataFrame], seed: int) -> Dict[str, pd.DataFrame]:
    """
    Generate sales domain tables: FactSales and FactReturns.
    
    Args:
        config: Full configuration dictionary
        dimensions: Dictionary of conformed dimensions
        seed: Random seed for reproducibility
    
    Returns:
        Dictionary with 'FactSales' and 'FactReturns' DataFrames
    """
    np.random.seed(seed)
    
    sales_config = config['sales']
    dim_customer = dimensions['DimCustomer']
    dim_product = dimensions['DimProduct']
    dim_employee = dimensions['DimEmployee']
    dim_date = dimensions['DimDate']
    
    # Filter to active entities
    active_customers = dim_customer[dim_customer['is_active']].copy()
    active_products = dim_product[dim_product['is_active']].copy()
    sales_reps = dim_employee[(dim_employee['department'] == 'Sales') & (dim_employee['is_active'])].copy()
    
    if len(sales_reps) == 0:
        sales_reps = dim_employee.sample(n=min(50, len(dim_employee)), random_state=seed)
    
    num_orders = sales_config['orders']['count']
    avg_lines = sales_config['orders']['lines_per_order']['average']
    max_lines = sales_config['orders']['lines_per_order']['max']
    
    print(f"  Generating {num_orders:,} orders (vectorized)...")
    
    # Generate total order lines at once
    lines_per_order = np.random.poisson(avg_lines, num_orders)
    lines_per_order = np.clip(lines_per_order, 1, max_lines)
    total_lines = lines_per_order.sum()
    
    print(f"  Total order lines: {total_lines:,}")
    
    # Vectorized sampling
    customer_samples = active_customers.sample(n=total_lines, replace=True, random_state=seed)
    product_samples = active_products.sample(n=total_lines, replace=True, random_state=seed + 1)
    sales_rep_samples = sales_reps.sample(n=total_lines, replace=True, random_state=seed + 2)
    date_samples = dim_date.sample(n=total_lines, replace=True, random_state=seed + 3)
    
    # Generate order IDs
    order_ids = np.repeat([f"ORD_{i:08d}" for i in range(num_orders)], lines_per_order)
    line_numbers = np.concatenate([np.arange(1, n + 1) for n in lines_per_order])
    
    # Quantities
    quantities = np.random.randint(1, 21, total_lines)
    
    # Pricing
    list_prices = product_samples['list_price'].values
    costs = product_samples['unit_cost'].values
    
    # Discounts
    discount_pcts = np.random.choice([0, 0, 0, 5, 10, 15, 20, 25], size=total_lines, p=[0.5, 0.1, 0.1, 0.1, 0.1, 0.05, 0.03, 0.02])
    
    # Calculate amounts
    gross_amounts = list_prices * quantities
    discount_amounts = gross_amounts * discount_pcts / 100
    net_amounts = gross_amounts - discount_amounts
    cost_amounts = costs * quantities
    gross_margins = net_amounts - cost_amounts
    tax_amounts = net_amounts * 0.08
    total_amounts = net_amounts + tax_amounts
    
    # Channels and Status
    channel_dist = sales_config['orders']['channel_distribution']
    channels = np.random.choice(
        list(channel_dist.keys()),
        size=total_lines,
        p=list(channel_dist.values())
    )
    
    status_dist = sales_config['orders']['status_distribution']
    statuses = np.random.choice(
        list(status_dist.keys()),
        size=total_lines,
        p=list(status_dist.values())
    )
    
    # Date IDs
    order_dates = date_samples['date'].values
    order_date_ids = date_samples['date_id'].values
    
    # Create DataFrame
    fact_sales = pd.DataFrame({
        'order_id': order_ids,
        'order_line_id': [f"{order_ids[i]}_L{line_numbers[i]:02d}" for i in range(total_lines)],
        'customer_id': customer_samples['customer_id'].values,
        'product_id': product_samples['product_id'].values,
        'employee_id': sales_rep_samples['employee_id'].values,
        'order_date_id': order_date_ids,
        'ship_date_id': order_date_ids,  # Simplified
        'delivery_date_id': order_date_ids,  # Simplified
        'quantity': quantities,
        'unit_price': np.round(list_prices, 2),
        'discount_percent': discount_pcts,
        'discount_amount': np.round(discount_amounts, 2),
        'net_amount': np.round(net_amounts, 2),
        'cost_amount': np.round(cost_amounts, 2),
        'gross_margin': np.round(gross_margins, 2),
        'tax_amount': np.round(tax_amounts, 2),
        'total_amount': np.round(total_amounts, 2),
        'status': statuses,
        'channel': channels
    })
    
    # Generate returns (vectorized)
    return_rate = sales_config['returns']['rate']
    num_returns = int(len(fact_sales) * return_rate)
    
    print(f"  Generating {num_returns:,} returns...")
    
    eligible_sales = fact_sales[fact_sales['status'] == 'delivered'].copy()
    if len(eligible_sales) == 0:
        eligible_sales = fact_sales.copy()
    
    return_samples = eligible_sales.sample(n=min(num_returns, len(eligible_sales)), random_state=seed + 4)
    
    reason_dist = sales_config['returns']['reason_distribution']
    return_reasons = np.random.choice(
        list(reason_dist.keys()),
        size=len(return_samples),
        p=list(reason_dist.values())
    )
    
    return_quantities = np.random.randint(1, return_samples['quantity'].values + 1)
    refund_amounts = return_samples['net_amount'].values * return_quantities / return_samples['quantity'].values
    restocking_fees = refund_amounts * np.random.choice([0, 0, 0.05, 0.10, 0.15], len(return_samples))
    conditions = np.random.choice(['New', 'Used', 'Damaged'], size=len(return_samples), p=[0.5, 0.3, 0.2])
    
    fact_returns = pd.DataFrame({
        'return_id': [f"RET_{i:08d}" for i in range(len(return_samples))],
        'order_id': return_samples['order_id'].values,
        'customer_id': return_samples['customer_id'].values,
        'product_id': return_samples['product_id'].values,
        'return_date_id': return_samples['order_date_id'].values,  # Simplified
        'return_reason': return_reasons,
        'return_quantity': return_quantities,
        'refund_amount': np.round(refund_amounts, 2),
        'restocking_fee': np.round(restocking_fees, 2),
        'condition': conditions
    })
    
    return {
        'FactSales': fact_sales,
        'FactReturns': fact_returns
    }
