"""
Conformed Dimensions Generator
Generates shared dimensions used across all business domains
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
import random


def generate_dim_date(start_date: str, end_date: str, fiscal_year_start_month: int = 7) -> pd.DataFrame:
    """
    Generate date dimension with fiscal calendar.
    
    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        fiscal_year_start_month: Month when fiscal year starts (1-12)
    
    Returns:
        DataFrame with date dimension
    """
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    df = pd.DataFrame({
        'date': date_range,
        'date_id': date_range.strftime('%Y%m%d').astype(int),
        'year': date_range.year,
        'quarter': date_range.quarter,
        'month': date_range.month,
        'month_name': date_range.strftime('%B'),
        'day_of_month': date_range.day,
        'day_of_week': date_range.dayofweek + 1,  # 1=Monday, 7=Sunday
        'day_name': date_range.strftime('%A'),
        'week_of_year': date_range.isocalendar().week,
        'is_weekend': date_range.dayofweek >= 5,
    })
    
    # Add fiscal calendar
    df['fiscal_year'] = df.apply(
        lambda row: row['year'] if row['month'] < fiscal_year_start_month else row['year'] + 1,
        axis=1
    )
    df['fiscal_quarter'] = ((df['month'] - fiscal_year_start_month) % 12) // 3 + 1
    df['fiscal_month'] = ((df['month'] - fiscal_year_start_month) % 12) + 1
    
    # Add US federal holidays (simplified)
    df['is_holiday'] = False
    # New Year's Day
    df.loc[(df['month'] == 1) & (df['day_of_month'] == 1), 'is_holiday'] = True
    # Independence Day
    df.loc[(df['month'] == 7) & (df['day_of_month'] == 4), 'is_holiday'] = True
    # Christmas
    df.loc[(df['month'] == 12) & (df['day_of_month'] == 25), 'is_holiday'] = True
    
    return df


def generate_dim_customer(config: dict, seed: int) -> pd.DataFrame:
    """Generate customer dimension."""
    random.seed(seed)
    np.random.seed(seed)
    fake = Faker()
    Faker.seed(seed)
    
    count = config['count']
    
    # Industry distribution
    industries = []
    for industry, pct in config['industry_distribution'].items():
        industries.extend([industry.title()] * int(count * pct))
    # Fill remainder
    while len(industries) < count:
        industries.append(random.choice(list(config['industry_distribution'].keys())).title())
    random.shuffle(industries)
    
    # Segment distribution
    segments = []
    for segment, pct in config['segment_distribution'].items():
        segments.extend([segment.upper()] * int(count * pct))
    while len(segments) < count:
        segments.append(random.choice(list(config['segment_distribution'].keys())).upper())
    random.shuffle(segments)
    
    # Region distribution
    regions = []
    for region, pct in config['region_distribution'].items():
        regions.extend([region.upper()] * int(count * pct))
    while len(regions) < count:
        regions.append(random.choice(list(config['region_distribution'].keys())).upper())
    random.shuffle(regions)
    
    # Generate customers
    customers = []
    for i in range(count):
        customer_id = f"CUST_{i:06d}"
        
        # Generate company name
        customer_name = fake.company()
        
        # Determine country based on region
        region = regions[i]
        if region == 'AMERICAS':
            country_choices = ['US', 'CA', 'MX', 'BR']
        elif region == 'EMEA':
            country_choices = ['GB', 'DE', 'FR', 'IT', 'ES']
        else:  # APAC
            country_choices = ['CN', 'JP', 'IN', 'AU', 'SG']
        country = random.choice(country_choices)
        
        # Credit limit based on segment
        segment = segments[i]
        if segment == 'ENTERPRISE':
            credit_limit = random.randint(1000000, 10000000)
        elif segment == 'STRATEGIC':
            credit_limit = random.randint(500000, 5000000)
        else:  # SMB
            credit_limit = random.randint(50000, 500000)
        
        # Customer since date
        customer_since = fake.date_between(start_date='-10y', end_date='-1y')
        
        # LTV tier based on credit limit
        if credit_limit >= 5000000:
            ltv_tier = 'High'
        elif credit_limit >= 500000:
            ltv_tier = 'Medium'
        else:
            ltv_tier = 'Low'
        
        is_active = random.random() < config['active_percentage']
        
        customers.append({
            'customer_id': customer_id,
            'customer_name': customer_name,
            'industry': industries[i],
            'segment': segment,
            'country': country,
            'region': region,
            'city': fake.city(),
            'account_manager': fake.name(),
            'customer_since': customer_since,
            'credit_limit': credit_limit,
            'is_active': is_active,
            'lifetime_value_tier': ltv_tier
        })
    
    return pd.DataFrame(customers)


def generate_dim_product(config: dict, seed: int) -> pd.DataFrame:
    """Generate product dimension."""
    random.seed(seed)
    np.random.seed(seed)
    fake = Faker()
    Faker.seed(seed)
    
    count = config['count']
    categories_config = config['categories']
    
    products = []
    product_counter = 0
    
    for cat_config in categories_config:
        category_name = cat_config['name']
        subcategories = cat_config['subcategories']
        cat_percentage = cat_config['percentage']
        products_in_category = int(count * cat_percentage)
        
        for _ in range(products_in_category):
            product_id = f"PROD_{product_counter:05d}"
            subcategory = random.choice(subcategories)
            
            # Generate product name
            product_name = f"{fake.word().title()} {random.choice(['Pro', 'Plus', 'Elite', 'Max', 'Ultra'])} {random.randint(100, 9999)}"
            
            # SKU
            sku = f"{category_name[:3].upper()}-{subcategory[:3].upper()}-{random.randint(1000, 9999)}"
            
            # Pricing
            unit_cost = round(random.uniform(10, 500), 2)
            list_price = round(unit_cost * random.uniform(1.5, 3.0), 2)
            
            # Lifecycle
            lifecycle_dist = config['lifecycle_distribution']
            lifecycle = random.choices(
                list(lifecycle_dist.keys()),
                weights=list(lifecycle_dist.values())
            )[0].title()
            
            # Launch date
            launch_date = fake.date_between(start_date='-5y', end_date='today')
            
            is_active = random.random() < config['active_percentage']
            
            products.append({
                'product_id': product_id,
                'product_name': product_name,
                'sku': sku,
                'category': category_name,
                'subcategory': subcategory,
                'brand': random.choice(['BrandA', 'BrandB', 'BrandC', 'BrandD']),
                'unit_cost': unit_cost,
                'list_price': list_price,
                'product_line': category_name,
                'launch_date': launch_date,
                'is_active': is_active,
                'lifecycle_stage': lifecycle,
                'supplier_id': f"SUP_{random.randint(1, 100):03d}",
                'weight_kg': round(random.uniform(0.1, 50.0), 2)
            })
            
            product_counter += 1
    
    return pd.DataFrame(products)


def generate_dim_employee(config: dict, seed: int, start_date: str, end_date: str) -> pd.DataFrame:
    """Generate employee dimension."""
    random.seed(seed)
    np.random.seed(seed)
    fake = Faker()
    Faker.seed(seed)
    
    count = config['count']
    departments_config = config['departments']
    
    employees = []
    employee_counter = 0
    
    for dept_config in departments_config:
        dept_name = dept_config['name']
        dept_percentage = dept_config['percentage']
        employees_in_dept = int(count * dept_percentage)
        
        for _ in range(employees_in_dept):
            employee_id = f"EMP_{employee_counter:05d}"
            full_name = fake.name()
            email = f"{full_name.lower().replace(' ', '.')}@company.com"
            
            # Job titles by department
            if dept_name == 'Sales':
                job_titles = ['Sales Rep', 'Sr Sales Rep', 'Account Executive', 'Sales Manager']
            elif dept_name == 'Engineering':
                job_titles = ['Software Engineer', 'Sr Software Engineer', 'Engineering Manager', 'Architect']
            elif dept_name == 'Customer Support':
                job_titles = ['Support Agent', 'Sr Support Agent', 'Support Manager']
            else:
                job_titles = [f'{dept_name} Specialist', f'Sr {dept_name} Specialist', f'{dept_name} Manager']
            
            job_title = random.choice(job_titles)
            
            # Hire date
            hire_date = fake.date_between(start_date='-10y', end_date='today')
            
            # Termination (based on attrition)
            is_active = random.random() < config['active_percentage']
            termination_date = None if is_active else fake.date_between(start_date=hire_date, end_date='today')
            
            # Manager (simplified - some random employee in same dept)
            manager_id = f"EMP_{random.randint(0, max(0, employee_counter - 1)):05d}" if employee_counter > 0 else None
            
            # Location
            location = random.choice(['Seattle, WA', 'New York, NY', 'Austin, TX', 'London, UK', 'Singapore'])
            
            # Employment type
            emp_type_dist = config['employment_type_distribution']
            employment_type = random.choices(
                list(emp_type_dist.keys()),
                weights=list(emp_type_dist.values())
            )[0].replace('_', '-').title()
            
            # Performance
            perf_dist = config['performance_distribution']
            performance_rating = random.choices(
                list(perf_dist.keys()),
                weights=list(perf_dist.values())
            )[0].title()
            
            employees.append({
                'employee_id': employee_id,
                'full_name': full_name,
                'email': email,
                'job_title': job_title,
                'department': dept_name,
                'manager_id': manager_id,
                'hire_date': hire_date,
                'termination_date': termination_date,
                'is_active': is_active,
                'location': location,
                'employment_type': employment_type,
                'salary_band': f"Band {random.randint(1, 5)}",
                'performance_rating': performance_rating
            })
            
            employee_counter += 1
    
    return pd.DataFrame(employees)


def generate_dim_geography(config: dict, dim_customer: pd.DataFrame, seed: int) -> pd.DataFrame:
    """Generate geography dimension based on customer distribution."""
    random.seed(seed)
    fake = Faker()
    Faker.seed(seed)
    
    # Extract unique locations from customers
    unique_locations = dim_customer[['country', 'region', 'city']].drop_duplicates()
    
    geographies = []
    for idx, row in unique_locations.iterrows():
        geography_id = f"GEO_{row['country']}_{row['city'][:3].upper()}_{idx:03d}"
        
        # Map country to region details
        country_code = row['country']
        region = row['region']
        
        # Sub-region mapping (simplified)
        if region == 'AMERICAS':
            if country_code in ['US', 'CA']:
                sub_region = 'North America'
            else:
                sub_region = 'Latin America'
        elif region == 'EMEA':
            if country_code in ['GB', 'DE', 'FR']:
                sub_region = 'Western Europe'
            else:
                sub_region = 'Eastern Europe'
        else:  # APAC
            sub_region = 'Asia Pacific'
        
        # Country name
        country_names = {
            'US': 'United States', 'CA': 'Canada', 'MX': 'Mexico', 'BR': 'Brazil',
            'GB': 'United Kingdom', 'DE': 'Germany', 'FR': 'France', 'IT': 'Italy', 'ES': 'Spain',
            'CN': 'China', 'JP': 'Japan', 'IN': 'India', 'AU': 'Australia', 'SG': 'Singapore'
        }
        
        geographies.append({
            'geography_id': geography_id,
            'country_code': country_code,
            'country_name': country_names.get(country_code, country_code),
            'region': region,
            'sub_region': sub_region,
            'state_province': fake.state() if country_code == 'US' else '',
            'city': row['city'],
            'postal_code': fake.postcode(),
            'latitude': round(random.uniform(-90, 90), 6),
            'longitude': round(random.uniform(-180, 180), 6)
        })
    
    return pd.DataFrame(geographies)
