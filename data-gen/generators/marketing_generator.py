"""Marketing Domain Generator"""
import pandas as pd
import numpy as np
from typing import Dict

def generate_marketing_data(config: dict, dimensions: Dict[str, pd.DataFrame], seed: int) -> Dict[str, pd.DataFrame]:
    """Generate Marketing domain: FactCampaigns"""
    np.random.seed(seed)
    
    mkt_config = config.get('marketing', {})
    num_campaigns = mkt_config.get('campaigns', {}).get('count', 500)
    
    dim_date = dimensions['DimDate']
    
    print(f"  Generating {num_campaigns:,} marketing campaigns...")
    
    # Vectorized campaign generation
    date_samples = dim_date.sample(n=num_campaigns, replace=True, random_state=seed)
    
    channels = np.random.choice(['Email', 'Social', 'Display', 'Search', 'Events'], 
                                size=num_campaigns, p=[0.30, 0.25, 0.20, 0.15, 0.10])
    
    # Budget varies by channel
    budgets = np.where(channels == 'Events', np.random.uniform(10000, 100000, num_campaigns),
              np.where(channels == 'Display', np.random.uniform(5000, 50000, num_campaigns),
              np.random.uniform(1000, 25000, num_campaigns)))
    
    # Generate metrics
    impressions = (budgets / np.random.uniform(0.5, 2.0, num_campaigns) * 1000).astype(int)
    clicks = (impressions * np.random.uniform(0.01, 0.05, num_campaigns)).astype(int)
    conversions = (clicks * np.random.uniform(0.02, 0.10, num_campaigns)).astype(int)
    revenue = conversions * np.random.uniform(50, 500, num_campaigns)
    
    df_campaigns = pd.DataFrame({
        'campaign_id': [f'CMP-{i+1:06d}' for i in range(num_campaigns)],
        'campaign_name': [f"{channels[i]} Campaign {i+1}" for i in range(num_campaigns)],
        'channel': channels,
        'start_date': date_samples['date'].values,
        'budget': np.round(budgets, 2),
        'impressions': impressions,
        'clicks': clicks,
        'conversions': conversions,
        'revenue': np.round(revenue, 2),
        'ctr': np.round(clicks / impressions * 100, 2),
        'cpc': np.round(budgets / np.maximum(clicks, 1), 2),
        'roas': np.round(revenue / budgets, 2)
    })
    
    return {'FactCampaigns': df_campaigns}
