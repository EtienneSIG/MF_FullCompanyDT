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
    random.seed(seed)
    np.random.seed(seed)
    
    sales_config = config['sales']
    dim_customer = dimensions['DimCustomer']
    dim_product = dimensions['DimProduct']
    dim_employee = dimensions['DimEmployee']
    dim_date = dimensions['DimDate']
    
    # Filter to active entities
    active_customers = dim_customer[dim_customer['is_active']]['customer_id'].tolist()
    active_products = dim_product[dim_product['is_active']]['product_id'].tolist()
    sales_reps = dim_employee[
        (dim_employee['department'] == 'Sales') & (dim_employee['is_active'])
    ]['employee_id'].tolist()
    
    # Generate orders
    num_orders = sales_config['orders']['count']
    orders = []
    order_lines = []
    
    # Get date range
    dates = dim_date['date'].tolist()
    date_ids = dim_date['date_id'].tolist()
    
    for order_idx in range(num_orders):
        order_id = f"ORD_{order_idx:08d}"
        
        # Select customer
        customer_id = random.choice(active_customers)
        
        # Select sales rep
        employee_id = random.choice(sales_reps) if sales_reps else None
        
        # Order date (with seasonality - more orders in Q4)
        order_date = random.choice(dates)
        month = order_date.month
        # Q4 boost
        if month in [10, 11, 12] and random.random() < 0.3:
            # 30% chance to duplicate order in Q4 (simulates seasonality)
            order_date = random.choice([d for d in dates if d.month in [10, 11, 12]])
        
        order_date_id = int(order_date.strftime('%Y%m%d'))
        
        # Ship and delivery dates
        ship_days = random.randint(1, 5)
        delivery_days = random.randint(2, 10)
        ship_date = order_date + timedelta(days=ship_days)
        delivery_date = ship_date + timedelta(days=delivery_days)
        
        ship_date_id = int(ship_date.strftime('%Y%m%d'))
        delivery_date_id = int(delivery_date.strftime('%Y%m%d'))
        
        # Channel
        channel_dist = sales_config['orders']['channel_distribution']
        channel = random.choices(
            list(channel_dist.keys()),
            weights=list(channel_dist.values())
        )[0].replace('_', ' ').title()
        
        # Status
        status_dist = sales_config['orders']['status_distribution']
        status = random.choices(
            list(status_dist.keys()),
            weights=list(status_dist.values())
        )[0].title()
        
        # Number of line items
        num_lines = np.random.poisson(sales_config['orders']['lines_per_order']['average'])
        num_lines = max(1, min(num_lines, sales_config['orders']['lines_per_order']['max']))
        
        # Generate line items
        for line_idx in range(num_lines):
            order_line_id = f"{order_id}_L{line_idx:02d}"
            
            # Select product
            product_id = random.choice(active_products)
            product_row = dim_product[dim_product['product_id'] == product_id].iloc[0]
            
            # Quantity
            quantity = random.randint(1, 20)
            
            # Pricing
            list_price = product_row['list_price']
            cost = product_row['unit_cost']
            
            # Discount
            discount_percent = random.choice([0, 0, 0, 5, 10, 15, 20, 25])  # Most orders no discount
            discount_amount = round(list_price * quantity * discount_percent / 100, 2)
            
            # Amounts
            gross_amount = round(list_price * quantity, 2)
            net_amount = round(gross_amount - discount_amount, 2)
            cost_amount = round(cost * quantity, 2)
            gross_margin = round(net_amount - cost_amount, 2)
            tax_amount = round(net_amount * 0.08, 2)  # 8% tax
            total_amount = round(net_amount + tax_amount, 2)
            
            order_lines.append({
                'order_id': order_id,
                'order_line_id': order_line_id,
                'customer_id': customer_id,
                'product_id': product_id,
                'employee_id': employee_id,
                'order_date_id': order_date_id,
                'ship_date_id': ship_date_id,
                'delivery_date_id': delivery_date_id,
                'quantity': quantity,
                'unit_price': list_price,
                'discount_percent': discount_percent,
                'discount_amount': discount_amount,
                'net_amount': net_amount,
                'cost_amount': cost_amount,
                'gross_margin': gross_margin,
                'tax_amount': tax_amount,
                'total_amount': total_amount,
                'status': status,
                'channel': channel
            })
    
    fact_sales = pd.DataFrame(order_lines)
    
    # Generate returns (based on return rate)
    return_rate = sales_config['returns']['rate']
    num_returns = int(len(fact_sales) * return_rate)
    
    returns = []
    eligible_sales = fact_sales[fact_sales['status'] == 'Delivered'].sample(n=min(num_returns, len(fact_sales)))
    
    for idx, sale_row in eligible_sales.iterrows():
        return_id = f"RET_{idx:08d}"
        
        # Return date (1-90 days after delivery)
        order_date_id = sale_row['delivery_date_id']
        order_date = datetime.strptime(str(order_date_id), '%Y%m%d')
        return_date = order_date + timedelta(days=random.randint(1, 90))
        return_date_id = int(return_date.strftime('%Y%m%d'))
        
        # Return reason
        reason_dist = sales_config['returns']['reason_distribution']
        return_reason = random.choices(
            list(reason_dist.keys()),
            weights=list(reason_dist.values())
        )[0].replace('_', ' ').title()
        
        # Return quantity (usually partial)
        return_quantity = random.randint(1, sale_row['quantity'])
        
        # Refund amount
        refund_amount = round(sale_row['net_amount'] * return_quantity / sale_row['quantity'], 2)
        
        # Restocking fee (0-15%)
        restocking_fee = round(refund_amount * random.choice([0, 0, 0.05, 0.10, 0.15]), 2)
        
        # Condition
        condition = random.choices(
            ['New', 'Used', 'Damaged'],
            weights=[0.5, 0.3, 0.2]
        )[0]
        
        returns.append({
            'return_id': return_id,
            'order_id': sale_row['order_id'],
            'customer_id': sale_row['customer_id'],
            'product_id': sale_row['product_id'],
            'return_date_id': return_date_id,
            'return_reason': return_reason,
            'return_quantity': return_quantity,
            'refund_amount': refund_amount,
            'restocking_fee': restocking_fee,
            'condition': condition
        })
    
    fact_returns = pd.DataFrame(returns)
    
    return {
        'FactSales': fact_sales,
        'FactReturns': fact_returns
    }
