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
        self.update_snap_geometry()

    def update_snap_geometry(self):
        """Update SNAP XML files with geometry from configuration."""
        try:
            from update_snap_geometry import update_all_snap_geometries
            logger.info("Updating SNAP geometry files from study area configuration...")
            if update_all_snap_geometries(self.config_file):
                logger.info("SNAP geometry files updated successfully")
            else:
                logger.warning("Failed to update SNAP geometry files")
        except Exception as e:
            logger.warning(f"Could not update SNAP geometry files: {e}")
        
    def setup_directories(self):
        """Setup working directories."""
        self.dirs = {
            'raw_data': self.base_dir / "03_raw_data/sentinel2_l1c",
            'l2a_resampled': self.base_dir / "04_processed_data/l2a_resampled",
            'l2a_reprojected': self.base_dir / "04_processed_data/l2a_reprojected", 
            'c2rcc_output': self.base_dir / "04_processed_data/c2rcc_output",
            'mosaic_output': self.base_dir / "04_processed_data/mosaic_output",
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
    
    def extract_block_name_from_filename(self, filename):
        """Extract block name (tile ID) from filename.
        
        Example: S2A_MSIL1C_20150903T014036_N0500_R031_T52LFL_20231017T130149.zip
        Extracts: T52LFL
        """
        parts = filename.split('_')
        
        # Look for tile ID pattern (T followed by 5 characters)
        for part in parts:
            if part.startswith('T') and len(part) == 6:
                return part
        
        logger.warning(f"Could not extract block name from filename: {filename}")
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
            
            # Extract date and block name from filename
            filename = zip_file.stem
            date_part = self.extract_date_from_filename(filename)
            block_name = self.extract_block_name_from_filename(filename)
            
            if not date_part or not block_name:
                logger.warning(f"Could not extract date or block name from {zip_file.name}, skipping")
                continue
            
            output_file = self.dirs['l2a_resampled'] / f"Subset_S2_MSIL2A_{date_part}_{block_name}.dim"
            
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
        """Step 3: Generate true color images from reprojected data."""
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
            
            # Extract date and block name from filename
            filename = dim_file.stem
            date_part = self.extract_date_from_filename(filename)
            block_name = self.extract_block_name_from_filename(filename)
            
            if not date_part or not block_name:
                logger.warning(f"Could not extract date or block name from {dim_file.name}, skipping")
                continue
            
            # Create output filename with date and block name
            output_file = self.dirs['c2rcc_output'] / f"Subset_S2_MSIL2A_{date_part}_{block_name}_C2RCC.nc"
            
            if output_file.exists():
                logger.info(f"Output already exists: {output_file.name}")
                success_count += 1
                continue
            
            command = f'gpt c2rcc.msi -SsourceProduct="{dim_file}" -p "{param_file}" -t "{output_file}" -f NetCDF4-BEAM'
            
            if self.run_gpt_command(command, f"C2RCC processing {dim_file.name}"):
                success_count += 1
        
        logger.info(f"Step 4 completed: {success_count}/{total_count} files processed successfully")
        return success_count == total_count


    def get_tiles_by_date(self):
        """Group C2RCC files by date and count tiles per date.

        Returns a dict with structure:
        {
            'date': {
                'single': [list of files for single tile],
                'multiple': [list of files for multiple tiles]
            }
        }
        """
        from collections import defaultdict
        c2rcc_files = list(self.dirs['c2rcc_output'].glob("*.nc"))

        if not c2rcc_files:
            logger.warning("No C2RCC files found")
            return {}

        files_by_date = defaultdict(list)

        for nc_file in c2rcc_files:
            filename = nc_file.stem
            date_part = self.extract_date_from_filename(filename)

            if date_part:
                files_by_date[date_part].append(nc_file)

        # Categorize by single vs multiple tiles
        result = {}
        for date_part, files in files_by_date.items():
            result[date_part] = {
                'single': files if len(files) == 1 else [],
                'multiple': files if len(files) > 1 else []
            }

        return result

    def step_5_mosaic(self):
        """Step 5: Create mosaic from multiple tiles (if needed)."""
        logger.info("=" * 50)
        logger.info("STEP 5: Mosaic Processing (if multiple tiles)")
        logger.info("=" * 50)

        param_file = self.dirs['config'] / "snap_graphs/mosaic.xml"

        if not param_file.exists():
            logger.error(f"Parameter file not found: {param_file}")
            return False

        tiles_by_date = self.get_tiles_by_date()

        if not tiles_by_date:
            logger.info("No C2RCC files found for processing - skipping mosaic step")
            return True  # Not an error, just no data to process

        success_count = 0
        total_count = 0
        single_tile_count = 0

        # Process each date
        for date_part, tile_info in tiles_by_date.items():
            multiple_files = tile_info['multiple']
            single_files = tile_info['single']

            # Count single tile dates
            if single_files:
                single_tile_count += 1
                logger.info(f"{date_part}: Single tile detected - mosaic not needed")
                continue

            # Process only dates with multiple tiles
            if len(multiple_files) < 2:
                continue

            total_count += 1

            # Sort files for consistent ordering
            multiple_files.sort()

            # Create mosaic output directory if needed
            mosaic_output_file = self.dirs['mosaic_output'] / f"Mosaic_S2_MSIL2A_{date_part}.nc"

            if mosaic_output_file.exists():
                logger.info(f"Mosaic already exists: {mosaic_output_file.name}")
                success_count += 1
                continue

            # Build source files string for gpt command
            source_files = " ".join([f'"{str(f)}"' for f in multiple_files])

            # Build mosaic command using XML parameter file
            command = f'gpt Mosaic {source_files} -p "{param_file}" -t "{mosaic_output_file}" -f NetCDF4-BEAM'

            logger.info(f"Creating mosaic for {date_part} from {len(multiple_files)} tiles")
            logger.info(f"Input files: {[f.name for f in multiple_files]}")

            if self.run_gpt_command(command, f"Mosaic processing for {date_part}"):
                success_count += 1

        if single_tile_count > 0:
            logger.info(f"Single-tile dates found: {single_tile_count} (mosaic processing skipped)")

        if total_count == 0:
            logger.info("No dates with multiple tiles found for mosaicking")
            return True  # Not an error, single tiles only

        logger.info(f"Step 5 completed: {success_count}/{total_count} mosaics created successfully")
        return success_count == total_count
    
    def step_6_cdom_calculation(self):
        """Step 6: Calculate CDOM from both single-tile and mosaicked data."""
        logger.info("=" * 50)
        logger.info("STEP 6: CDOM Calculation")
        logger.info("=" * 50)

        graph_file = self.dirs['config'] / "snap_graphs/cdom_band_math.xml"

        if not graph_file.exists():
            logger.error(f"Graph file not found: {graph_file}")
            return False

        success_count = 0
        total_count = 0

        # Get tile information to know which source to use
        tiles_by_date = self.get_tiles_by_date()

        if not tiles_by_date:
            logger.info("No C2RCC files found for CDOM calculation - skipping step")
            return True  # Not an error, just no data to process

        # Process each date
        for date_part, tile_info in tiles_by_date.items():
            single_files = tile_info['single']
            multiple_files = tile_info['multiple']

            # Determine source file (mosaic for multiple tiles, c2rcc for single tile)
            if multiple_files:
                # Use mosaic output
                mosaic_file = self.dirs['mosaic_output'] / f"Mosaic_S2_MSIL2A_{date_part}.nc"
                if not mosaic_file.exists():
                    logger.warning(f"Mosaic file not found for {date_part}, skipping CDOM")
                    continue
                source_file = mosaic_file
                source_type = "mosaic"
            elif single_files:
                # Use c2rcc output (single tile)
                source_file = single_files[0]
                source_type = "c2rcc"
            else:
                logger.warning(f"No source files found for {date_part}")
                continue

            total_count += 1

            output_file = self.dirs['cdom_output'] / f"Subset_S2_MSIL2A_{date_part}_CDOM.nc"

            if output_file.exists():
                logger.info(f"Output already exists: {output_file.name}")
                success_count += 1
                continue

            logger.info(f"CDOM calculation for {date_part} (source: {source_type})")
            command = f'gpt "{graph_file}" -PInput="{source_file}" -POutput="{output_file}"'

            if self.run_gpt_command(command, f"CDOM calculation {source_file.name}"):
                success_count += 1

        if total_count == 0:
            logger.info("No files found for CDOM calculation")
            return True  # Not an error

        logger.info(f"Step 6 completed: {success_count}/{total_count} files processed successfully")
        return success_count == total_count
    
    def step_7_generate_plots(self):
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
            ("Mosaic (if multiple tiles)", self.step_5_mosaic),
            ("CDOM Calculation", self.step_6_cdom_calculation),
            ("Generate Plots", self.step_7_generate_plots)
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
    parser.add_argument('--step', help='Run specific step only (1-7)')

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
            '5': processor.step_5_mosaic,
            '6': processor.step_6_cdom_calculation,
            '7': processor.step_7_generate_plots
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
