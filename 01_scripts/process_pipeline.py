"""
Sentinel-2 Water Quality Processing Pipeline
Main processing script that orchestrates the entire workflow
"""

import os
import sys
import argparse
import logging
import subprocess
import re
from pathlib import Path
from datetime import datetime
import json

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WaterQualityProcessor:
    def __init__(self, config_file):
        """Initialize the processor with configuration."""
        self.config_file = Path(config_file)
        self.base_dir = Path(__file__).parent.parent
        self.setup_directories()
        self.setup_logging()
        
    def setup_directories(self):
        """Setup working directories."""
        self.dirs = {
            'raw_data': self.base_dir / "03_raw_data/sentinel2_l1c",
            'l2a_resampled': self.base_dir / "04_processed_data/l2a_resampled",
            'l2a_reprojected': self.base_dir / "04_processed_data/l2a_reprojected", 
            'c2rcc_output': self.base_dir / "04_processed_data/c2rcc_output",
            'cdom_output': self.base_dir / "04_processed_data/cdom_output",
            'final_products': self.base_dir / "05_final_products",
            'logs': self.base_dir / "06_logs",
            'config': self.base_dir / "02_config"
        }
        
        # Create directories if they don't exist
        for dir_path in self.dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def setup_logging(self):
        """Setup logging to file."""
        log_file = self.dirs['logs'] / f"processing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        logger.info(f"Processing started. Log file: {log_file}")
    
    def run_gpt_command(self, command, description):
        """Run a SNAP GPT command."""
        logger.info(f"Starting: {description}")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"Completed: {description}")
                return True
            else:
                logger.error(f"Failed: {description}")
                logger.error(f"Error output: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Exception in {description}: {e}")
            return False
    
    def extract_date_from_filename(self, filename):
        """Extract date from filename in various formats."""
        # Handle different filename formats
        parts = filename.split('_')
        
        # Look for date in format YYYYMMDDTHHMMSS
        for part in parts:
            if 'T' in part and len(part) == 15:  # YYYYMMDDTHHMMSS format
                return part[:8]  # Extract YYYYMMDD
        
        # Look for date in format YYYYMMDD
        for part in parts:
            if len(part) == 8 and part.isdigit():  # YYYYMMDD format
                return part
        
        # Try to find date pattern in the whole filename
        match = re.search(r'(\d{8})T\d{6}', filename)
        if match:
            return match.group(1)
        
        match = re.search(r'(\d{8})', filename)
        if match:
            return match.group(1)
        
        logger.warning(f"Could not extract date from filename: {filename}")
        return None

    def step_1_resample_subset(self):
        """Step 1: Resample and subset the data."""
        logger.info("=" * 50)
        logger.info("STEP 1: Resample and Subset")
        logger.info("=" * 50)
        
        graph_file = self.dirs['config'] / "snap_graphs/resample_subset.xml"
        
        if not graph_file.exists():
            logger.error(f"Graph file not found: {graph_file}")
            return False
        
        success_count = 0
        total_count = 0
        
        # Process each zip file
        for zip_file in self.dirs['raw_data'].glob("*.zip"):
            total_count += 1
            
            # Extract date from filename
            filename = zip_file.stem
            date_part = filename.split('_')[2]  # Extract date part
            
            output_file = self.dirs['l2a_resampled'] / f"Subset_S2_MSIL2A_{date_part}.dim"
            
            if output_file.exists():
                logger.info(f"Output already exists: {output_file.name}")
                success_count += 1
                continue
            
            command = f'gpt "{graph_file}" -PInput="{zip_file}" -POutput="{output_file}"'
            
            if self.run_gpt_command(command, f"Resample and subset {zip_file.name}"):
                success_count += 1
        
        logger.info(f"Step 1 completed: {success_count}/{total_count} files processed successfully")
        return success_count == total_count
    
    def step_2_reproject(self):
        """Step 2: Reproject to WGS84."""
        logger.info("=" * 50)
        logger.info("STEP 2: Reproject to WGS84")
        logger.info("=" * 50)
        
        param_file = self.dirs['config'] / "snap_graphs/reproject.xml"
        
        if not param_file.exists():
            logger.error(f"Parameter file not found: {param_file}")
            return False
        
        success_count = 0
        total_count = 0
        
        # Process each DIM file
        for dim_file in self.dirs['l2a_resampled'].glob("*.dim"):
            total_count += 1
            
            # Create output filename
            output_file = self.dirs['l2a_reprojected'] / f"{dim_file.stem}_reprojected.dim"
            
            if output_file.exists():
                logger.info(f"Output already exists: {output_file.name}")
                success_count += 1
                continue
            
            command = f'gpt Reproject -SsourceProduct="{dim_file}" -p "{param_file}" -t "{output_file}"'
            
            if self.run_gpt_command(command, f"Reproject {dim_file.name}"):
                success_count += 1
        
        logger.info(f"Step 2 completed: {success_count}/{total_count} files processed successfully")
        return success_count == total_count
    
    def step_3_true_color(self):
        """Step 3: Generate true color images."""
        logger.info("=" * 50)
        logger.info("STEP 3: Generate True Color Images")
        logger.info("=" * 50)
        
        rgb_profile = self.dirs['config'] / "snap_graphs/rgb_profile_s2.rgb"
        output_dir = self.dirs['final_products'] / "true_color"
        output_dir.mkdir(exist_ok=True)
        
        if not rgb_profile.exists():
            logger.error(f"RGB profile not found: {rgb_profile}")
            return False
        
        success_count = 0
        total_count = 0
        
        # Process each reprojected DIM file
        for dim_file in self.dirs['l2a_reprojected'].glob("*.dim"):
            total_count += 1
            
            # Extract date from filename
            filename = dim_file.stem
            date_part = self.extract_date_from_filename(filename)
            
            if not date_part:
                continue
            
            # Format date as YYYYMMDD
            output_name = f"{date_part}.png"
            output_file = output_dir / output_name
            
            if output_file.exists():
                logger.info(f"Output already exists: {output_name}")
                success_count += 1
                continue
            
            command = f'pconvert -f png -p "{rgb_profile}" -o "{output_dir}" "{dim_file}"'
            
            if self.run_gpt_command(command, f"Generate true color for {dim_file.name}"):
                # Rename the generated file to the desired format
                generated_files = list(output_dir.glob("*.png"))
                if generated_files:
                    latest_file = max(generated_files, key=lambda p: p.stat().st_mtime)
                    if latest_file.name != output_name:
                        latest_file.rename(output_file)
                    success_count += 1
        
        logger.info(f"Step 3 completed: {success_count}/{total_count} files processed successfully")
        return success_count == total_count
    
    def step_4_c2rcc(self):
        """Step 4: Apply C2RCC processing."""
        logger.info("=" * 50)
        logger.info("STEP 4: C2RCC Processing")
        logger.info("=" * 50)
        
        param_file = self.dirs['config'] / "snap_graphs/c2rcc_param.xml"
        
        if not param_file.exists():
            logger.error(f"Parameter file not found: {param_file}")
            return False
        
        success_count = 0
        total_count = 0
        
        # Process each reprojected DIM file
        for dim_file in self.dirs['l2a_reprojected'].glob("*.dim"):
            total_count += 1
            
            # Extract date from filename
            filename = dim_file.stem
            date_part = self.extract_date_from_filename(filename)
            
            if not date_part:
                continue
            
            # Create output filename with date
            output_file = self.dirs['c2rcc_output'] / f"Subset_S2_MSIL2A_{date_part}_C2RCC.nc"
            
            if output_file.exists():
                logger.info(f"Output already exists: {output_file.name}")
                success_count += 1
                continue
            
            command = f'gpt c2rcc.msi -SsourceProduct="{dim_file}" -p "{param_file}" -t "{output_file}" -f NetCDF4-BEAM'
            
            if self.run_gpt_command(command, f"C2RCC processing {dim_file.name}"):
                success_count += 1
        
        logger.info(f"Step 4 completed: {success_count}/{total_count} files processed successfully")
        return success_count == total_count
    
    def step_5_cdom_calculation(self):
        """Step 5: Calculate CDOM."""
        logger.info("=" * 50)
        logger.info("STEP 5: CDOM Calculation")
        logger.info("=" * 50)
        
        graph_file = self.dirs['config'] / "snap_graphs/cdom_band_math.xml"
        
        if not graph_file.exists():
            logger.error(f"Graph file not found: {graph_file}")
            return False
        
        success_count = 0
        total_count = 0
        
        # Process each C2RCC output file
        for nc_file in self.dirs['c2rcc_output'].glob("*.nc"):
            total_count += 1
            
            # Extract date from filename
            filename = nc_file.stem
            date_part = self.extract_date_from_filename(filename)
            
            if not date_part:
                continue
            
            output_file = self.dirs['cdom_output'] / f"Subset_S2_MSIL2A_{date_part}_CDOM.nc"
            
            if output_file.exists():
                logger.info(f"Output already exists: {output_file.name}")
                success_count += 1
                continue
            
            command = f'gpt "{graph_file}" -PInput="{nc_file}" -POutput="{output_file}"'
            
            if self.run_gpt_command(command, f"CDOM calculation {nc_file.name}"):
                success_count += 1
        
        logger.info(f"Step 5 completed: {success_count}/{total_count} files processed successfully")
        return success_count == total_count
    
    def step_6_generate_plots(self):
        """Step 6: Generate final plots."""
        logger.info("=" * 50)
        logger.info("STEP 6: Generate Final Plots")
        logger.info("=" * 50)
        
        # Run the plotting script
        plotting_script = self.base_dir / "01_scripts/plotting.py"
        
        if not plotting_script.exists():
            logger.error(f"Plotting script not found: {plotting_script}")
            return False
        
        try:
            result = subprocess.run([
                sys.executable, 
                str(plotting_script), 
                "--config", str(self.config_file)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("Plotting completed successfully")
                return True
            else:
                logger.error(f"Plotting failed: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Exception in plotting: {e}")
            return False
    
    def run_full_pipeline(self):
        """Run the complete processing pipeline."""
        logger.info("Starting complete Sentinel-2 water quality processing pipeline")
        start_time = datetime.now()
        
        steps = [
            ("Resample and Subset", self.step_1_resample_subset),
            ("Reproject to WGS84", self.step_2_reproject),
            ("Generate True Color", self.step_3_true_color),
            ("C2RCC Processing", self.step_4_c2rcc),
            ("CDOM Calculation", self.step_5_cdom_calculation),
            ("Generate Plots", self.step_6_generate_plots)
        ]
        
        results = {}
        
        for step_name, step_func in steps:
            logger.info(f"Starting step: {step_name}")
            success = step_func()
            results[step_name] = success
            
            if not success:
                logger.error(f"Step failed: {step_name}")
                logger.error("Pipeline stopped due to failure")
                break
            
            logger.info(f"Step completed successfully: {step_name}")
        
        # Summary
        end_time = datetime.now()
        duration = end_time - start_time
        
        logger.info("=" * 50)
        logger.info("PROCESSING SUMMARY")
        logger.info("=" * 50)
        logger.info(f"Start time: {start_time}")
        logger.info(f"End time: {end_time}")
        logger.info(f"Duration: {duration}")
        logger.info("")
        
        for step_name, success in results.items():
            status = "SUCCESS" if success else "FAILED"
            logger.info(f"{step_name}: {status}")
        
        all_success = all(results.values())
        logger.info(f"Overall status: {'SUCCESS' if all_success else 'FAILED'}")
        
        return all_success

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Process Sentinel-2 water quality data')
    parser.add_argument('--config', required=True, help='Configuration file path')
    parser.add_argument('--step', help='Run specific step only (1-6)')
    
    args = parser.parse_args()
    
    # Check configuration file
    config_path = Path(args.config)
    if not config_path.exists():
        logger.error(f"Configuration file not found: {config_path}")
        sys.exit(1)
    
    # Initialize processor
    processor = WaterQualityProcessor(config_path)
    
    # Run specific step or full pipeline
    if args.step:
        step_map = {
            '1': processor.step_1_resample_subset,
            '2': processor.step_2_reproject,
            '3': processor.step_3_true_color,
            '4': processor.step_4_c2rcc,
            '5': processor.step_5_cdom_calculation,
            '6': processor.step_6_generate_plots
        }
        
        if args.step in step_map:
            success = step_map[args.step]()
            sys.exit(0 if success else 1)
        else:
            logger.error(f"Invalid step: {args.step}")
            sys.exit(1)
    else:
        # Run full pipeline
        success = processor.run_full_pipeline()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
