"""
Upload generated CSV files to Fabric Lakehouse via OneLake File Explorer
Prerequisites: OneLake File Explorer must be installed and lakehouse mounted

Update the ONELAKE_PATH variable below with your actual OneLake path
"""

import shutil
import os
from pathlib import Path

# ============================================================================
# CONFIGURATION - UPDATE THESE VALUES
# ============================================================================

# Path to your OneLake mounted drive (example: "O:/YourWorkspace/YourLakehouse/Files/bronze")
# or UNC path like "\\OneLake\YourWorkspace\YourLakehouse.Lakehouse\Files\bronze"
ONELAKE_PATH = r"O:\YourWorkspace\YourLakehouse\Files\bronze"

# Source path (generated data)
SOURCE_PATH = Path("output/structured")

# ============================================================================
# UPLOAD SCRIPT
# ============================================================================

def upload_to_onelake():
    """Upload all CSV files to OneLake/Fabric Lakehouse."""
    
    source = Path(SOURCE_PATH)
    destination = Path(ONELAKE_PATH)
    
    # Check if source exists
    if not source.exists():
        print(f"❌ Source path not found: {source}")
        print("   Please run generate_all.py first to generate data")
        return False
    
    # Check if destination exists (OneLake mounted)
    if not destination.exists():
        print(f"❌ OneLake path not found: {destination}")
        print("   Please:")
        print("   1. Install OneLake File Explorer")
        print("   2. Mount your Lakehouse")
        print("   3. Update ONELAKE_PATH in this script")
        return False
    
    print("="*80)
    print("UPLOADING DATA TO FABRIC LAKEHOUSE")
    print("="*80)
    print(f"Source:      {source.absolute()}")
    print(f"Destination: {destination.absolute()}")
    print()
    
    # Get list of domain folders
    domains = [d for d in source.iterdir() if d.is_dir()]
    
    copied_files = 0
    copied_domains = 0
    
    for domain_folder in sorted(domains):
        domain_name = domain_folder.name
        dest_domain = destination / domain_name
        
        print(f"📁 {domain_name}/")
        
        # Create domain folder in destination if needed
        dest_domain.mkdir(parents=True, exist_ok=True)
        
        # Copy all CSV files
        csv_files = list(domain_folder.glob("*.csv"))
        
        if not csv_files:
            print(f"   ⏭️  No CSV files found")
            continue
        
        for csv_file in csv_files:
            dest_file = dest_domain / csv_file.name
            
            try:
                shutil.copy2(csv_file, dest_file)
                file_size_mb = csv_file.stat().st_size / (1024 * 1024)
                print(f"   ✅ {csv_file.name:30s} ({file_size_mb:,.1f} MB)")
                copied_files += 1
            except Exception as e:
                print(f"   ❌ {csv_file.name}: {str(e)}")
        
        copied_domains += 1
        print()
    
    print("="*80)
    print("UPLOAD COMPLETE")
    print("="*80)
    print(f"✅ Copied {copied_files} files from {copied_domains} domains")
    print()
    print("Next steps:")
    print("  1. Go to your Fabric Lakehouse")
    print("  2. Verify files in Files/bronze/")
    print("  3. Run notebook: 01_ingest_to_bronze.ipynb")
    
    return True


if __name__ == '__main__':
    upload_to_onelake()
