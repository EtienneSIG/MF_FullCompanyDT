"""
Cleanup duplicate domain folders created with spaces instead of underscores
"""

import os
import shutil
from pathlib import Path

def cleanup_duplicate_folders():
    """Remove duplicate domain folders with spaces in names."""
    output_path = Path('output/structured')
    
    # Folders to remove (with spaces)
    folders_to_remove = [
        'Supply Chain',
        'Call Center',
        'Quality Security',
        'Risk Compliance'
    ]
    
    print("Cleaning up duplicate folders...")
    for folder_name in folders_to_remove:
        folder_path = output_path / folder_name
        if folder_path.exists():
            print(f"  Removing: {folder_path}")
            shutil.rmtree(folder_path)
            print(f"    ✓ Deleted")
        else:
            print(f"  Skip (not found): {folder_path}")
    
    print("\n✅ Cleanup complete!")
    print("\nRemaining folders:")
    if output_path.exists():
        for item in sorted(output_path.iterdir()):
            if item.is_dir():
                print(f"  {item.name}/")

if __name__ == '__main__':
    cleanup_duplicate_folders()
