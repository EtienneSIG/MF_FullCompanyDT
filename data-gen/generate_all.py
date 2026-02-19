"""
Full Enterprise Data Platform - Main Data Generator
Generates synthetic data for 15+ business domains

Usage:
    python generate_all.py
    python generate_all.py --config custom_config.yml
    python generate_all.py --domains sales,crm --output test_output/
"""

import os
import sys
import yaml
import argparse
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
import pandas as pd
from tqdm import tqdm

# Add utils to path
sys.path.insert(0, os.path.dirname(__file__))

from utils.conformed_dimensions import (
    generate_dim_date,
    generate_dim_customer,
    generate_dim_product,
    generate_dim_employee,
    generate_dim_geography,
    generate_dim_facility,
    generate_dim_project,
    generate_dim_account
)
from utils.data_quality import validate_referential_integrity, validate_business_rules
from utils.text_generator import generate_unstructured_files

# Import domain generators
from generators.crm_generator import generate_crm_data
from generators.sales_generator import generate_sales_data
from generators.product_generator import generate_product_data
from generators.marketing_generator import generate_marketing_data
from generators.hr_generator import generate_hr_data
from generators.supply_chain_generator import generate_supply_chain_data
from generators.manufacturing_generator import generate_manufacturing_data
from generators.finance_generator import generate_finance_data
from generators.esg_generator import generate_esg_data
from generators.call_center_generator import generate_call_center_data
from generators.itops_generator import generate_itops_data
from generators.finops_generator import generate_finops_data
from generators.risk_compliance_generator import generate_risk_compliance_data
from generators.rd_generator import generate_rd_data
from generators.quality_security_generator import generate_quality_security_data


# Configure logging with UTF-8 encoding
file_handler = logging.FileHandler('data_generation.log', encoding='utf-8')
stream_handler = logging.StreamHandler(sys.stdout)

# Set encoding for stream handler to UTF-8 (if supported)
try:
    import io
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
except:
    pass  # Fallback to default encoding

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[file_handler, stream_handler]
)
logger = logging.getLogger(__name__)


def load_config(config_path: str = 'config.yml') -> Dict[str, Any]:
    """Load configuration from YAML file."""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        logger.info(f"Configuration loaded from {config_path}")
        return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        logger.error(f"Error parsing configuration: {e}")
        sys.exit(1)


def create_output_directories(config: Dict[str, Any]) -> tuple:
    """Create output directories for structured and unstructured data with Bronze layer structure."""
    structured_path = Path(config['output']['structured_path'])
    unstructured_path = Path(config['output']['unstructured_path'])
    
    # Create base directories
    structured_path.mkdir(parents=True, exist_ok=True)
    unstructured_path.mkdir(parents=True, exist_ok=True)
    
    # Create Bronze layer domain directories
    bronze_domains = [
        'dimensions',  # For conformed dimensions
        'crm',
        'sales', 
        'product',
        'marketing',
        'hr',
        'supply_chain',
        'manufacturing',
        'finance',
        'esg',
        'call_center',
        'itops',
        'finops',
        'risk_compliance',
        'rd',
        'quality_security'
    ]
    
    for domain in bronze_domains:
        domain_path = structured_path / domain
        domain_path.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Output directories created:")
    logger.info(f"  Structured: {structured_path}")
    logger.info(f"  Unstructured: {unstructured_path}")
    logger.info(f"  Bronze domains: {len(bronze_domains)} folders")
    
    return structured_path, unstructured_path


def save_dataframe(df: pd.DataFrame, name: str, output_path: Path, config: Dict[str, Any], domain: str = 'dimensions') -> None:
    """Save DataFrame to CSV or Parquet based on configuration in Bronze layer structure."""
    format_type = config['output']['format']
    compression = config['output'].get('compression', False)
    
    # Create domain-specific path (Bronze layer structure)
    domain_path = output_path / domain
    domain_path.mkdir(parents=True, exist_ok=True)
    
    if format_type in ['csv', 'both']:
        if compression:
            csv_path = domain_path / f"{name}.csv.gz"
            df.to_csv(csv_path, index=False, compression='gzip')
            logger.info(f"  Saved {domain}/{name}.csv.gz ({len(df):,} rows)")
        else:
            csv_path = domain_path / f"{name}.csv"
            df.to_csv(csv_path, index=False)
            logger.info(f"  Saved {domain}/{name}.csv ({len(df):,} rows)")
    
    if format_type in ['parquet', 'both']:
        parquet_path = domain_path / f"{name}.parquet"
        df.to_parquet(parquet_path, index=False, compression='snappy')
        logger.info(f"  Saved {domain}/{name}.parquet ({len(df):,} rows)")


def generate_conformed_dimensions(config: Dict[str, Any], output_path: Path) -> Dict[str, pd.DataFrame]:
    """Generate all conformed dimensions."""
    logger.info("=" * 80)
    logger.info("STEP 1: Generating Conformed Dimensions")
    logger.info("=" * 80)
    
    dimensions = {}
    seed = config['seed']
    
    # DimDate
    logger.info("Generating DimDate...")
    dim_date = generate_dim_date(
        start_date=config['start_date'],
        end_date=config['end_date'],
        fiscal_year_start_month=config['finance']['budget'].get('fiscal_year_start_month', 7)
    )
    save_dataframe(dim_date, 'DimDate', output_path, config, domain='dimensions')
    dimensions['DimDate'] = dim_date
    
    # DimCustomer
    logger.info("Generating DimCustomer...")
    dim_customer = generate_dim_customer(config['dim_customer'], seed)
    save_dataframe(dim_customer, 'DimCustomer', output_path, config, domain='dimensions')
    dimensions['DimCustomer'] = dim_customer
    
    # DimProduct
    logger.info("Generating DimProduct...")
    dim_product = generate_dim_product(config['dim_product'], seed)
    save_dataframe(dim_product, 'DimProduct', output_path, config, domain='dimensions')
    dimensions['DimProduct'] = dim_product
    
    # DimEmployee
    logger.info("Generating DimEmployee...")
    dim_employee = generate_dim_employee(config['dim_employee'], seed, config['start_date'], config['end_date'])
    save_dataframe(dim_employee, 'DimEmployee', output_path, config, domain='dimensions')
    dimensions['DimEmployee'] = dim_employee
    
    # DimGeography
    logger.info("Generating DimGeography...")
    dim_geography = generate_dim_geography(config['dim_geography'], dim_customer, seed)
    save_dataframe(dim_geography, 'DimGeography', output_path, config, domain='dimensions')
    dimensions['DimGeography'] = dim_geography
    
    # DimFacility
    logger.info("Generating DimFacility...")
    dim_facility = generate_dim_facility(config['dim_facility'], dim_geography, seed)
    save_dataframe(dim_facility, 'DimFacility', output_path, config, domain='dimensions')
    dimensions['DimFacility'] = dim_facility
    
    # DimProject
    logger.info("Generating DimProject...")
    dim_project = generate_dim_project(config['dim_project'], dim_employee, seed)
    save_dataframe(dim_project, 'DimProject', output_path, config, domain='dimensions')
    dimensions['DimProject'] = dim_project
    
    # DimAccount
    logger.info("Generating DimAccount...")
    dim_account = generate_dim_account(config['dim_account'])
    save_dataframe(dim_account, 'DimAccount', output_path, config, domain='dimensions')
    dimensions['DimAccount'] = dim_account
    
    logger.info(f"[OK] Conformed dimensions generated: {sum(len(df) for df in dimensions.values()):,} total rows")
    return dimensions


def generate_domain_data(domain_name: str, generator_func, config: Dict[str, Any], 
                        dimensions: Dict[str, pd.DataFrame], output_path: Path) -> Dict[str, pd.DataFrame]:
    """Generate data for a specific domain and save in Bronze layer structure."""
    # Create display name for logs (supply_chain → Supply Chain)
    display_name = domain_name.replace('_', ' ').title()
    logger.info(f"Generating {display_name} domain...")
    
    try:
        domain_data = generator_func(config, dimensions, config['seed'])
        
        for table_name, df in domain_data.items():
            # Use technical name (with underscores) for folder structure
            save_dataframe(df, table_name, output_path, config, domain=domain_name)
        
        total_rows = sum(len(df) for df in domain_data.values())
        logger.info(f"  [OK] {display_name}: {len(domain_data)} tables, {total_rows:,} total rows")
        return domain_data
    
    except Exception as e:
        logger.error(f"  [ERROR] Error generating {display_name}: {e}", exc_info=True)
        return {}


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description='Generate enterprise data platform synthetic data')
    parser.add_argument('--config', default='config.yml', help='Path to configuration file')
    parser.add_argument('--domains', default='all', help='Comma-separated list of domains to generate (or "all")')
    parser.add_argument('--output', help='Override output path')
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Override output path if specified
    if args.output:
        config['output']['structured_path'] = args.output
    
    # Create output directories
    structured_path, unstructured_path = create_output_directories(config)
    
    # Start timer
    start_time = datetime.now()
    logger.info("=" * 80)
    logger.info("FULL ENTERPRISE DATA PLATFORM - DATA GENERATION")
    logger.info("=" * 80)
    logger.info(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Seed: {config['seed']}")
    logger.info(f"Date Range: {config['start_date']} to {config['end_date']}")
    logger.info("=" * 80)
    
    # Generate conformed dimensions
    dimensions = generate_conformed_dimensions(config, structured_path)
    
    # Define domain generators
    domain_generators = {
        'crm': generate_crm_data,
        'sales': generate_sales_data,
        'product': generate_product_data,
        'marketing': generate_marketing_data,
        'hr': generate_hr_data,
        'supply_chain': generate_supply_chain_data,
        'manufacturing': generate_manufacturing_data,
        'finance': generate_finance_data,
        'esg': generate_esg_data,
        'call_center': generate_call_center_data,
        'itops': generate_itops_data,
        'finops': generate_finops_data,
        'risk_compliance': generate_risk_compliance_data,
        'rd': generate_rd_data,
        'quality_security': generate_quality_security_data
    }
    
    # Determine which domains to generate
    if args.domains == 'all':
        domains_to_generate = domain_generators.keys()
    else:
        domains_to_generate = [d.strip() for d in args.domains.split(',')]
    
    logger.info("")
    logger.info("=" * 80)
    logger.info("STEP 2: Generating Domain-Specific Data")
    logger.info("=" * 80)
    
    # Generate domain data
    all_data = {}
    for domain in domains_to_generate:
        if domain not in domain_generators:
            logger.warning(f"Unknown domain: {domain}")
            continue
        
        # Pass technical name with underscores (e.g., supply_chain)
        domain_data = generate_domain_data(
            domain,
            domain_generators[domain],
            config,
            dimensions,
            structured_path
        )
        all_data[domain] = domain_data
    
    # Data quality validation
    logger.info("")
    logger.info("=" * 80)
    logger.info("STEP 3: Data Quality Validation")
    logger.info("=" * 80)
    
    if config['quality']['referential_integrity']:
        logger.info("Validating referential integrity...")
        # Combine all data for validation
        all_tables = {**dimensions}
        for domain_data in all_data.values():
            all_tables.update(domain_data)
        
        integrity_results = validate_referential_integrity(all_tables)
        if integrity_results['passed']:
            logger.info("  [OK] All referential integrity checks passed")
        else:
            logger.warning(f"  [WARNING] {len(integrity_results['failures'])} integrity issues found")
            for issue in integrity_results['failures'][:5]:  # Show first 5
                logger.warning(f"    - {issue}")
    
    if config['quality']['check_business_rules']:
        logger.info("Validating business rules...")
        rules_results = validate_business_rules(all_tables)
        if rules_results['passed']:
            logger.info("  [OK] All business rule checks passed")
        else:
            logger.warning(f"  [WARNING] {len(rules_results['failures'])} rule violations found")
    
    # Generate unstructured data
    logger.info("")
    logger.info("=" * 80)
    logger.info("STEP 4: Generating Unstructured Data")
    logger.info("=" * 80)
    
    unstructured_config = config.get('unstructured', {})
    if unstructured_config:
        generate_unstructured_files(unstructured_config, unstructured_path, config['seed'], dimensions)
        logger.info("  [OK] Unstructured data files generated")
    else:
        logger.info("  [SKIP] Skipped (no unstructured data configured)")
    
    # Summary
    end_time = datetime.now()
    duration = end_time - start_time
    
    total_rows = sum(len(df) for df in dimensions.values())
    for domain_data in all_data.values():
        total_rows += sum(len(df) for df in domain_data.values())
    
    logger.info("")
    logger.info("=" * 80)
    logger.info("GENERATION COMPLETE!")
    logger.info("=" * 80)
    logger.info(f"End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Duration: {duration}")
    logger.info(f"Total Structured Records: {total_rows:,}")
    logger.info(f"Output Path: {structured_path}")
    logger.info("=" * 80)
    logger.info("")
    logger.info("Next Steps:")
    logger.info("  1. Review generated files in output/ directory")
    logger.info("  2. Upload to Microsoft Fabric Lakehouse (Bronze layer)")
    logger.info("  3. Run transformation notebooks (Bronze → Silver → Gold)")
    logger.info("  4. Create semantic model and configure Data Agent")
    logger.info("")
    logger.info("For detailed instructions, see docs/demo-script.md")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
