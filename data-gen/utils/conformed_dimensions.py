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
    np.random.seed(seed)
    fake = Faker()
    Faker.seed(seed)
    
    count = config['count']
    
    print(f"  Generating {count:,} customers (vectorized)...")
    
    # Vectorized distribution generation
    industry_dist = config['industry_distribution']
    industries = np.random.choice(
        [k.title() for k in industry_dist.keys()],
        size=count,
        p=list(industry_dist.values())
    )
    
    segment_dist = config['segment_distribution']
    segments = np.random.choice(
        [k.upper() for k in segment_dist.keys()],
        size=count,
        p=list(segment_dist.values())
    )
    
    region_dist = config['region_distribution']
    regions = np.random.choice(
        [k.upper() for k in region_dist.keys()],
        size=count,
        p=list(region_dist.values())
    )
    
    # Generate customer data in batches
    customer_names = [fake.company() for _ in range(count)]
    cities = [fake.city() for _ in range(count)]
    account_managers = [fake.name() for _ in range(count)]
    
    # Countries based on region
    countries = np.where(regions == 'AMERICAS', np.random.choice(['US', 'CA', 'MX', 'BR'], count),
                 np.where(regions == 'EMEA', np.random.choice(['GB', 'DE', 'FR', 'IT', 'ES'], count),
                          np.random.choice(['CN', 'JP', 'IN', 'AU', 'SG'], count)))
    
    # Credit limits based on segment
    credit_limits = np.where(segments == 'ENTERPRISE', np.random.randint(1000000, 10000001, count),
                     np.where(segments == 'STRATEGIC', np.random.randint(500000, 5000001, count),
                              np.random.randint(50000, 500001, count)))
    
    # LTV tiers
    ltv_tiers = np.where(credit_limits >= 5000000, 'High',
                np.where(credit_limits >= 500000, 'Medium', 'Low'))
    
    is_active = np.random.random(count) < config['active_percentage']
    
    df = pd.DataFrame({
        'customer_id': [f"CUST_{i:06d}" for i in range(count)],
        'customer_name': customer_names,
        'industry': industries,
        'segment': segments,
        'country': countries,
        'region': regions,
        'city': cities,
        'account_manager': account_managers,
        'customer_since': [fake.date_between(start_date='-10y', end_date='-1y') for _ in range(count)],
        'credit_limit': credit_limits,
        'is_active': is_active,
        'lifetime_value_tier': ltv_tiers
    })
    
    return df


def generate_dim_product(config: dict, seed: int) -> pd.DataFrame:
    """Generate product dimension."""
    np.random.seed(seed)
    fake = Faker()
    Faker.seed(seed)
    
    count = config['count']
    categories_config = config['categories']
    
    print(f"  Generating {count:,} products (vectorized)...")
    
    # Pre-allocate arrays
    product_ids = [f"PROD_{i:05d}" for i in range(count)]
    categories = []
    subcategories = []
    
    # Distribute products across categories
    for cat_config in categories_config:
        cat_count = int(count * cat_config['percentage'])
        categories.extend([cat_config['name']] * cat_count)
        subcategories.extend([np.random.choice(cat_config['subcategories']) for _ in range(cat_count)])
    
    # Fill remainder
    while len(categories) < count:
        cat = np.random.choice(categories_config)
        categories.append(cat['name'])
        subcategories.append(np.random.choice(cat['subcategories']))
    
    # Vectorized generation
    product_names = [f"{fake.word().title()} {np.random.choice(['Pro', 'Plus', 'Elite', 'Max', 'Ultra'])} {np.random.randint(100, 9999)}" for _ in range(count)]
    brands = np.random.choice(['BrandA', 'BrandB', 'BrandC', 'BrandD'], count)
    supplier_ids = [f"SUP_{np.random.randint(1, 101):03d}" for _ in range(count)]
    
    unit_costs = np.random.uniform(10, 500, count)
    list_prices = unit_costs * np.random.uniform(1.5, 3.0, count)
    weights = np.random.uniform(0.1, 50.0, count)
    
    lifecycle_dist = config['lifecycle_distribution']
    lifecycles = np.random.choice(
        [k.title() for k in lifecycle_dist.keys()],
        size=count,
        p=list(lifecycle_dist.values())
    )
    
    is_active = np.random.random(count) < config['active_percentage']
    
    df = pd.DataFrame({
        'product_id': product_ids,
        'product_name': product_names,
        'sku': [f"{categories[i][:3].upper()}-{subcategories[i][:3].upper()}-{np.random.randint(1000, 10000)}" for i in range(count)],
        'category': categories,
        'subcategory': subcategories,
        'brand': brands,
        'unit_cost': np.round(unit_costs, 2),
        'list_price': np.round(list_prices, 2),
        'product_line': categories,
        'launch_date': [fake.date_between(start_date='-5y', end_date='today') for _ in range(count)],
        'is_active': is_active,
        'lifecycle_stage': lifecycles,
        'supplier_id': supplier_ids,
        'weight_kg': np.round(weights, 2)
    })
    
    return df


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
