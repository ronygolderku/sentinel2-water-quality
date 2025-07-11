"""
Utility functions for Sentinel-2 water quality processing
"""

import os
import logging
import shutil
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

def setup_logging(log_file=None, level=logging.INFO):
    """Setup logging configuration."""
    format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    if log_file:
        logging.basicConfig(
            level=level,
            format=format_str,
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
    else:
        logging.basicConfig(level=level, format=format_str)

def create_directory_structure(base_path):
    """Create the complete directory structure."""
    directories = [
        "01_scripts",
        "01_scripts/config",
        "02_config",
        "02_config/snap_graphs",
        "03_raw_data/sentinel2_l1c",
        "04_processed_data/l2a_resampled",
        "04_processed_data/l2a_reprojected",
        "04_processed_data/c2rcc_output",
        "04_processed_data/cdom_output",
        "05_final_products/chl",
        "05_final_products/tsm",
        "05_final_products/cdom",
        "05_final_products/true_color",
        "06_logs",
        "07_documentation"
    ]
    
    base_path = Path(base_path)
    
    for dir_name in directories:
        dir_path = base_path / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {dir_path}")

def clean_processed_data(base_path):
    """Clean processed data directories."""
    processed_dirs = [
        "04_processed_data/l2a_resampled",
        "04_processed_data/l2a_reprojected",
        "04_processed_data/c2rcc_output",
        "04_processed_data/cdom_output"
    ]
    
    base_path = Path(base_path)
    
    for dir_name in processed_dirs:
        dir_path = base_path / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path)
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Cleaned directory: {dir_path}")

def get_processing_statistics(base_path):
    """Get processing statistics."""
    base_path = Path(base_path)
    
    stats = {
        'raw_data': len(list((base_path / "03_raw_data/sentinel2_l1c").glob("*.zip"))),
        'l2a_resampled': len(list((base_path / "04_processed_data/l2a_resampled").glob("*.dim"))),
        'l2a_reprojected': len(list((base_path / "04_processed_data/l2a_reprojected").glob("*.dim"))),
        'c2rcc_output': len(list((base_path / "04_processed_data/c2rcc_output").glob("*.nc"))),
        'cdom_output': len(list((base_path / "04_processed_data/cdom_output").glob("*.nc"))),
        'chl_plots': len(list((base_path / "05_final_products/chl").glob("*.png"))),
        'tsm_plots': len(list((base_path / "05_final_products/tsm").glob("*.png"))),
        'cdom_plots': len(list((base_path / "05_final_products/cdom").glob("*.png"))),
        'true_color_plots': len(list((base_path / "05_final_products/true_color").glob("*.png")))
    }
    
    return stats

def print_processing_statistics(base_path):
    """Print processing statistics."""
    stats = get_processing_statistics(base_path)
    
    print("\n" + "="*50)
    print("PROCESSING STATISTICS")
    print("="*50)
    print(f"Raw data files (ZIP): {stats['raw_data']}")
    print(f"L2A resampled files: {stats['l2a_resampled']}")
    print(f"L2A reprojected files: {stats['l2a_reprojected']}")
    print(f"C2RCC output files: {stats['c2rcc_output']}")
    print(f"CDOM output files: {stats['cdom_output']}")
    print(f"Chlorophyll plots: {stats['chl_plots']}")
    print(f"TSM plots: {stats['tsm_plots']}")
    print(f"CDOM plots: {stats['cdom_plots']}")
    print(f"True color plots: {stats['true_color_plots']}")
    print("="*50)

def validate_snap_installation():
    """Validate SNAP installation."""
    try:
        import subprocess
        import shutil
        
        # Check if gpt is available using shutil.which first
        gpt_location = shutil.which('gpt')
        
        if gpt_location:
            logger.info(f"Found 'gpt' command at: {gpt_location}")
            
            # Try a quick test with correct parameter
            try:
                result = subprocess.run(['gpt', '-h'], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    logger.info("SNAP GPT is working correctly")
                    return True
                else:
                    logger.error(f"SNAP GPT found but not working properly (return code: {result.returncode})")
            except subprocess.TimeoutExpired:
                logger.info("SNAP GPT found but response was slow")
                return True  # If it times out, SNAP is probably there but slow
            except Exception as e:
                logger.error(f"Error testing GPT: {e}")
        
        # If which() didn't find it, try manual paths
        logger.info("Searching in common installation paths...")
        gpt_paths = [
            r'C:\Program Files\esa-snap\bin\gpt.exe',
            r'C:\Program Files\esa-snap\bin\gpt.bat',
            r'C:\Program Files\snap\bin\gpt.exe',
            r'C:\Program Files\snap\bin\gpt.bat',
            r'C:\Program Files (x86)\snap\bin\gpt.exe',
            r'C:\Program Files (x86)\esa-snap\bin\gpt.exe',
        ]
        
        for gpt_path in gpt_paths:
            if os.path.exists(gpt_path):
                logger.info(f"Found SNAP GPT at: {gpt_path}")
                snap_bin_dir = os.path.dirname(gpt_path)
                
                # Add SNAP bin directory to PATH for this session
                current_path = os.environ.get('PATH', '')
                if snap_bin_dir not in current_path:
                    os.environ['PATH'] = snap_bin_dir + os.pathsep + current_path
                    logger.info(f"Added {snap_bin_dir} to PATH for this session")
                
                try:
                    result = subprocess.run(['gpt', '-h'], capture_output=True, text=True, timeout=15)
                    if result.returncode == 0:
                        logger.info("SNAP GPT is working correctly")
                        return True
                    else:
                        logger.error(f"SNAP found but not working properly (return code: {result.returncode})")
                except Exception as e:
                    logger.error(f"Error testing SNAP: {e}")
                    continue
        
        logger.error("SNAP GPT not found. Please install SNAP and add it to PATH")
        return False
        
    except Exception as e:
        logger.error(f"Error validating SNAP installation: {e}")
        return False

def validate_python_dependencies():
    """Validate Python dependencies."""
    required_packages = [
        'numpy', 'matplotlib', 'xarray', 'cartopy', 'cmocean', 
        'geopandas', 'shapely', 'pandas', 'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"Missing Python packages: {', '.join(missing_packages)}")
        return False
    else:
        logger.info("All required Python packages are available")
        return True

def create_requirements_file(base_path):
    """Create requirements.txt file."""
    requirements = """# Sentinel-2 Water Quality Processing Requirements
numpy>=1.20.0
matplotlib>=3.3.0
xarray>=0.16.0
cartopy>=0.18.0
cmocean>=2.0.0
geopandas>=0.9.0
shapely>=1.7.0
pandas>=1.3.0
requests>=2.25.0
pyyaml>=5.4.0
netcdf4>=1.5.0
"""
    
    requirements_file = Path(base_path) / "requirements.txt"
    
    with open(requirements_file, 'w') as f:
        f.write(requirements)
    
    logger.info(f"Created requirements.txt: {requirements_file}")

def migrate_existing_data(old_base_path, new_base_path):
    """Migrate data from old structure to new structure."""
    old_path = Path(old_base_path)
    new_path = Path(new_base_path)
    
    # Migration mapping
    migration_map = {
        'dataset': '03_raw_data/sentinel2_l1c',
        'pre-process_resample_subset': '04_processed_data/l2a_resampled',
        'pre-process_reproject': '04_processed_data/l2a_reprojected',
        'process_c2rcc': '04_processed_data/c2rcc_output',
        'process_cdom': '04_processed_data/cdom_output',
        'Final-product/CHL': '05_final_products/chl',
        'Final-product/TSM': '05_final_products/tsm',
        'Final-product/CDOM': '05_final_products/cdom',
        'Final-product/True_Color': '05_final_products/true_color',
        'SNAP_graphs': '02_config/snap_graphs'
    }
    
    for old_dir, new_dir in migration_map.items():
        old_dir_path = old_path / old_dir
        new_dir_path = new_path / new_dir
        
        if old_dir_path.exists():
            # Create new directory
            new_dir_path.mkdir(parents=True, exist_ok=True)
            
            # Copy files
            if old_dir_path.is_dir():
                for file_path in old_dir_path.iterdir():
                    if file_path.is_file():
                        shutil.copy2(file_path, new_dir_path)
                        logger.info(f"Migrated: {file_path.name} -> {new_dir}")
            
            logger.info(f"Migrated directory: {old_dir} -> {new_dir}")
        else:
            logger.warning(f"Source directory not found: {old_dir}")

def archive_old_structure(base_path):
    """Archive the old directory structure."""
    base_path = Path(base_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"old_structure_backup_{timestamp}"
    
    old_dirs = [
        'dataset', 'pre-process_resample_subset', 'pre-process_reproject',
        'process_c2rcc', 'process_cdom', 'Final-product', 'SNAP_graphs'
    ]
    
    archive_path = base_path / archive_name
    archive_path.mkdir(exist_ok=True)
    
    for old_dir in old_dirs:
        old_dir_path = base_path / old_dir
        if old_dir_path.exists():
            shutil.move(str(old_dir_path), str(archive_path))
            logger.info(f"Archived: {old_dir} -> {archive_name}")
    
    logger.info(f"Old structure archived to: {archive_path}")

if __name__ == "__main__":
    # Example usage
    import argparse
    
    parser = argparse.ArgumentParser(description='Utility functions for Sentinel-2 processing')
    parser.add_argument('--action', choices=['create_dirs', 'clean', 'stats', 'validate', 'migrate'], 
                       required=True, help='Action to perform')
    parser.add_argument('--path', required=True, help='Base path for operations')
    parser.add_argument('--old-path', help='Old path for migration')
    
    args = parser.parse_args()
    
    if args.action == 'create_dirs':
        create_directory_structure(args.path)
    elif args.action == 'clean':
        clean_processed_data(args.path)
    elif args.action == 'stats':
        print_processing_statistics(args.path)
    elif args.action == 'validate':
        snap_ok = validate_snap_installation()
        python_ok = validate_python_dependencies()
        print(f"SNAP: {'OK' if snap_ok else 'FAIL'}")
        print(f"Python dependencies: {'OK' if python_ok else 'FAIL'}")
    elif args.action == 'migrate':
        if args.old_path:
            migrate_existing_data(args.old_path, args.path)
        else:
            print("--old-path required for migration")
