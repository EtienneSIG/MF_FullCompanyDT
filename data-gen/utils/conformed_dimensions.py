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
    """Generate employee dimension (vectorized)."""
    np.random.seed(seed)
    fake = Faker()
    Faker.seed(seed)
    
    count = config['count']
    departments_config = config['departments']
    
    print(f"  Generating {count:,} employees (vectorized)...")
    
    # Pre-allocate arrays
    employee_ids = [f"EMP_{i:05d}" for i in range(count)]
    departments = []
    
    # Distribute employees across departments
    for dept_config in departments_config:
        dept_count = int(count * dept_config['percentage'])
        departments.extend([dept_config['name']] * dept_count)
    
    # Fill remainder
    while len(departments) < count:
        dept = np.random.choice([d['name'] for d in departments_config])
        departments.append(dept)
    
    # Vectorized generation
    full_names = [fake.name() for _ in range(count)]
    emails = [f"{name.lower().replace(' ', '.')}@company.com" for name in full_names]
    
    # Job titles by department (vectorized)
    job_titles = []
    for dept in departments:
        if dept == 'Sales':
            titles = ['Sales Rep', 'Sr Sales Rep', 'Account Executive', 'Sales Manager']
        elif dept == 'Engineering':
            titles = ['Software Engineer', 'Sr Software Engineer', 'Engineering Manager', 'Architect']
        elif dept == 'Customer Support':
            titles = ['Support Agent', 'Sr Support Agent', 'Support Manager']
        else:
            titles = [f'{dept} Specialist', f'Sr {dept} Specialist', f'{dept} Manager']
        job_titles.append(np.random.choice(titles))
    
    # Vectorized dates
    hire_dates = [fake.date_between(start_date='-10y', end_date='today') for _ in range(count)]
    is_active = np.random.random(count) < config['active_percentage']
    termination_dates = [None if active else fake.date_between(start_date=hire_dates[i], end_date='today') 
                        for i, active in enumerate(is_active)]
    
    # Vectorized locations, employment types, performance
    locations = np.random.choice(
        ['Seattle, WA', 'New York, NY', 'Austin, TX', 'London, UK', 'Singapore'],
        count
    )
    
    emp_type_dist = config['employment_type_distribution']
    employment_types = np.random.choice(
        [k.replace('_', '-').title() for k in emp_type_dist.keys()],
        size=count,
        p=list(emp_type_dist.values())
    )
    
    perf_dist = config['performance_distribution']
    performance_ratings = np.random.choice(
        [k.title() for k in perf_dist.keys()],
        size=count,
        p=list(perf_dist.values())
    )
    
    manager_ids = [f"EMP_{np.random.randint(0, max(1, i)):05d}" if i > 0 else None for i in range(count)]
    salary_bands = [f"Band {np.random.randint(1, 6)}" for _ in range(count)]
    
    df = pd.DataFrame({
        'employee_id': employee_ids,
        'full_name': full_names,
        'email': emails,
        'job_title': job_titles,
        'department': departments,
        'manager_id': manager_ids,
        'hire_date': hire_dates,
        'termination_date': termination_dates,
        'is_active': is_active,
        'location': locations,
        'employment_type': employment_types,
        'salary_band': salary_bands,
        'performance_rating': performance_ratings
    })
    
    return df


def generate_dim_geography(config: dict, dim_customer: pd.DataFrame, seed: int) -> pd.DataFrame:
    """Generate geography dimension based on customer distribution (vectorized)."""
    np.random.seed(seed)
    fake = Faker()
    Faker.seed(seed)
    
    print(f"  Generating geography dimension (vectorized)...")
    
    # Extract unique locations from customers (vectorized)
    unique_locations = dim_customer[['country', 'region', 'city']].drop_duplicates().reset_index(drop=True)
    geo_count = len(unique_locations)
    
    # Vectorized ID generation
    geography_ids = [f"GEO_{unique_locations.iloc[i]['country']}_{unique_locations.iloc[i]['city'][:3].upper()}_{i:03d}" 
                    for i in range(geo_count)]
    
    # Vectorized sub-region mapping
    def get_sub_region(row):
        if row['region'] == 'AMERICAS':
            return 'North America' if row['country'] in ['US', 'CA'] else 'Latin America'
        elif row['region'] == 'EMEA':
            return 'Western Europe' if row['country'] in ['GB', 'DE', 'FR'] else 'Eastern Europe'
        else:
            return 'Asia Pacific'
    
    sub_regions = unique_locations.apply(get_sub_region, axis=1)
    
    # Country name mapping (vectorized)
    country_names = {
        'US': 'United States', 'CA': 'Canada', 'MX': 'Mexico', 'BR': 'Brazil',
        'GB': 'United Kingdom', 'DE': 'Germany', 'FR': 'France', 'IT': 'Italy', 'ES': 'Spain',
        'CN': 'China', 'JP': 'Japan', 'IN': 'India', 'AU': 'Australia', 'SG': 'Singapore'
    }
    country_name_mapped = unique_locations['country'].map(country_names).fillna(unique_locations['country'])
    
    # Generate state/province only for US (vectorized)
    state_provinces = [fake.state() if country == 'US' else '' 
                      for country in unique_locations['country']]
    
    # Vectorized random coordinates
    latitudes = np.round(np.random.uniform(-90, 90, geo_count), 6)
    longitudes = np.round(np.random.uniform(-180, 180, geo_count), 6)
    postal_codes = [fake.postcode() for _ in range(geo_count)]
    
    df = pd.DataFrame({
        'geography_id': geography_ids,
        'country_code': unique_locations['country'],
        'country_name': country_name_mapped,
        'region': unique_locations['region'],
        'sub_region': sub_regions,
        'state_province': state_provinces,
        'city': unique_locations['city'],
        'postal_code': postal_codes,
        'latitude': latitudes,
        'longitude': longitudes
    })
    
    return df
