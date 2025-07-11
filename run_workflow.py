"""
Master script for Sentinel-2 Water Quality Processing
This script orchestrates the complete workflow from download to final products
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from datetime import datetime

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent / "01_scripts"))

import utils
from download import Sentinel2Downloader
from process_pipeline import WaterQualityProcessor
from plotting import WaterQualityPlotter

def main():
    parser = argparse.ArgumentParser(description='Sentinel-2 Water Quality Processing Master Script')
    parser.add_argument('--config', default='02_config/parameters.yaml', 
                       help='Configuration file path')
    parser.add_argument('--action', choices=['download', 'process', 'plot', 'full'], 
                       default='full', help='Action to perform')
    parser.add_argument('--start-date', help='Start date for download (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='End date for download (YYYY-MM-DD)')
    parser.add_argument('--clean', action='store_true', 
                       help='Clean processed data before processing')
    parser.add_argument('--setup', action='store_true', 
                       help='Setup directory structure')
    
    args = parser.parse_args()
    
    # Setup logging
    base_path = Path(__file__).parent
    log_dir = base_path / "06_logs"
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"master_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    utils.setup_logging(log_file, logging.INFO)
    
    logger = logging.getLogger(__name__)
    logger.info("Starting Sentinel-2 Water Quality Processing")
    
    # Setup directory structure if requested
    if args.setup:
        logger.info("Setting up directory structure")
        utils.create_directory_structure(base_path)
    
    # Validate configuration
    config_path = base_path / args.config
    if not config_path.exists():
        logger.error(f"Configuration file not found: {config_path}")
        sys.exit(1)
    
    # Clean processed data if requested
    if args.clean:
        logger.info("Cleaning processed data")
        utils.clean_processed_data(base_path)
    
    # Validate dependencies
    if not utils.validate_snap_installation():
        logger.error("SNAP installation validation failed")
        sys.exit(1)
    
    if not utils.validate_python_dependencies():
        logger.error("Python dependencies validation failed")
        logger.info("Install missing packages using: pip install -r requirements.txt")
        sys.exit(1)
    
    success = True
    
    try:
        if args.action in ['download', 'full']:
            # Download data
            logger.info("Starting data download")
            downloader = Sentinel2Downloader(config_path)
            
            # Parse dates
            if args.start_date:
                start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
            else:
                start_date = datetime.strptime(downloader.config['download']['default_start_date'], '%Y-%m-%d')
            
            if args.end_date:
                end_date = datetime.strptime(args.end_date, '%Y-%m-%d')
            else:
                end_date = datetime.strptime(downloader.config['download']['default_end_date'], '%Y-%m-%d')
            
            downloader.download_products(start_date, end_date)
            logger.info("Data download completed")
        
        if args.action in ['process', 'full']:
            # Process data
            logger.info("Starting data processing")
            processor = WaterQualityProcessor(config_path)
            success = processor.run_full_pipeline()
            
            if success:
                logger.info("Data processing completed successfully")
            else:
                logger.error("Data processing failed")
        
        if args.action in ['plot', 'full']:
            # Generate plots
            logger.info("Starting plot generation")
            plotter = WaterQualityPlotter(config_path)
            plot_success = plotter.generate_all_plots()
            
            if plot_success:
                logger.info("Plot generation completed successfully")
            else:
                logger.error("Plot generation failed")
                success = False
        
        # Print statistics
        utils.print_processing_statistics(base_path)
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        success = False
    
    if success:
        logger.info("Workflow completed successfully")
    else:
        logger.error("Workflow completed with errors")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
