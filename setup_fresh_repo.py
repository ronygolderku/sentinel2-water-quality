#!/usr/bin/env python3
"""
Clean Setup Script for Fresh Repository
This script prepares a fresh copy of the repository for first-time use
"""

import os
import shutil
from pathlib import Path

def setup_fresh_repository():
    """Setup a fresh repository for first-time use"""
    print("🚀 Setting up fresh Sentinel-2 Water Quality Processing Toolkit")
    print("=" * 70)
    
    base_path = Path(__file__).parent
    
    # Create necessary directories
    directories_to_create = [
        "03_raw_data/sentinel2_l1c",
        "04_processed_data/l2a_resampled",
        "04_processed_data/l2a_reprojected", 
        "04_processed_data/c2rcc_output",
        "04_processed_data/cdom_output",
        "05_final_products/chl",
        "05_final_products/tsm",
        "05_final_products/cdom",
        "05_final_products/true_color",
        "06_logs"
    ]
    
    print("📁 Creating directory structure...")
    for directory in directories_to_create:
        dir_path = base_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Created {directory}")
    
    # Copy template configuration if parameters.yaml doesn't exist
    config_file = base_path / "02_config" / "parameters.yaml"
    template_file = base_path / "02_config" / "parameters_template.yaml"
    
    if not config_file.exists() and template_file.exists():
        print("\n⚙️ Setting up configuration...")
        shutil.copy(template_file, config_file)
        print(f"   ✅ Copied configuration template to {config_file}")
        print(f"   ⚠️  Please edit {config_file} with your Copernicus credentials")
    elif config_file.exists():
        print("\n⚙️ Configuration file already exists")
        print(f"   ℹ️  Using existing {config_file}")
    else:
        print("\n❌ Configuration template not found")
        print("   Please check if parameters_template.yaml exists")
    
    # Create empty __init__.py files for Python packages
    init_files = [
        "01_scripts/__init__.py",
        "02_config/__init__.py"
    ]
    
    print("\n🐍 Setting up Python packages...")
    for init_file in init_files:
        init_path = base_path / init_file
        init_path.parent.mkdir(parents=True, exist_ok=True)
        init_path.touch()
        print(f"   ✅ Created {init_file}")
    
    # Create a README for users in key directories
    readme_contents = {
        "03_raw_data/README.md": "# Raw Data Directory\n\nThis directory stores downloaded Sentinel-2 L1C data.\nFiles are automatically downloaded here by the toolkit.\n",
        "04_processed_data/README.md": "# Processed Data Directory\n\nThis directory stores intermediate processing results.\nFiles are automatically created here during processing.\n",
        "05_final_products/README.md": "# Final Products Directory\n\nThis directory stores the final water quality maps and visualizations.\nFiles are automatically created here after successful processing.\n",
        "06_logs/README.md": "# Logs Directory\n\nThis directory stores processing logs and error information.\nCheck these files for debugging and monitoring processing status.\n"
    }
    
    print("\n📝 Creating directory documentation...")
    for readme_path, content in readme_contents.items():
        readme_file = base_path / readme_path
        readme_file.parent.mkdir(parents=True, exist_ok=True)
        with open(readme_file, 'w') as f:
            f.write(content)
        print(f"   ✅ Created {readme_path}")
    
    print("\n" + "=" * 70)
    print("✅ Fresh repository setup completed!")
    print("\nNext steps:")
    print("1. Edit 02_config/parameters.yaml with your Copernicus credentials")
    print("2. Run: python quick_setup.py")
    print("3. Run: python run_workflow.py --action full --start-date 2025-05-15 --end-date 2025-05-16")
    print("\nFor detailed instructions, see:")
    print("- README.md")
    print("- 07_documentation/GETTING_STARTED.md")
    print("\nHappy processing! 🛰️🌊")

if __name__ == "__main__":
    setup_fresh_repository()
