"""
Sentinel-2 Water Quality Plotting Script
Generate visualization plots for water quality parameters
"""

import os
import sys
import argparse
import logging
import re
from pathlib import Path
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import xarray as xr
import cartopy.crs as ccrs
import cmocean

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WaterQualityPlotter:
    def __init__(self, config_file):
        """Initialize the plotter with configuration."""
        self.config_file = Path(config_file)
        self.base_dir = Path(__file__).parent.parent
        self.setup_directories()
        self.setup_colormaps()
        
    def setup_directories(self):
        """Setup working directories."""
        self.dirs = {
            'c2rcc_output': self.base_dir / "04_processed_data/c2rcc_output",
            'mosaic_output': self.base_dir / "04_processed_data/mosaic_output",
            'cdom_output': self.base_dir / "04_processed_data/cdom_output",
            'final_products': self.base_dir / "05_final_products"
        }

        # Create output directories
        for param in ['chl', 'tsm', 'cdom']:
            output_dir = self.dirs['final_products'] / param
            output_dir.mkdir(parents=True, exist_ok=True)
    
    def setup_colormaps(self):
        """Setup custom colormaps."""
        # Chlorophyll-a colormap
        color_values = [
            [147,0,108], [111,0,144], [72,0,183], [33,0,222], [0,10,255], [0,74,255],
            [0,144,255], [0,213,255], [0,255,215], [0,255,119], [0,255,15], [96,255,0],
            [200,255,0], [255,235,0], [255,183,0], [255,131,0], [255,79,0], [255,31,0],
            [230,0,0], [165,0,0], [105,0,0]
        ]
        
        sample_values = [
            0.0105927390978, 0.01511153517746066, 0.02218493234759939,
            0.03259381777070279, 0.047886418593687446, 0.06831451603621097,
            0.10029112852033921, 0.1473464383750438, 0.2164794954661175,
            0.30882852380362497, 0.4533847704508146, 0.6661070836975002,
            0.9786359751581525, 1.3961169989723918, 2.049610500045872,
            3.011261431529367, 4.424106633340013, 6.311407543621453,
            9.265646919990738, 13.612969492356, 20.0
        ]
        
        self.chl_cmap = colors.ListedColormap(np.array(color_values)/255.0)
        self.chl_norm = colors.BoundaryNorm(sample_values, len(sample_values))
        
        # TSM colormap
        self.tsm_cmap = cmocean.cm.turbid
        self.tsm_cmap.set_bad(color="black")
        
        # CDOM colormap  
        self.cdom_cmap = plt.cm.YlOrBr
        self.cdom_cmap.set_bad(color="black")
    
    def extract_date_from_filename(self, filename):
        """Extract date from filename."""
        match = re.search(r"\d{8}", filename)
        if match:
            try:
                parsed_date = datetime.strptime(match.group(), "%Y%m%d")
                return parsed_date.strftime("%Y%m%d")
            except ValueError:
                return "Unknown_Date"
        return "Unknown_Date"
    
    def create_base_plot(self, data, lat, lon, title="", figsize=(10, 6)):
        """Create base plot with cartopy projection."""
        fig, ax = plt.subplots(figsize=figsize, subplot_kw={"projection": ccrs.PlateCarree()})
        
        # Set extent
        extent = [lon.min(), lon.max(), lat.min(), lat.max()]
        ax.set_extent(extent, crs=ccrs.PlateCarree())
        ax.set_axis_off()
        
        return fig, ax, extent
    
    def save_plot(self, fig, output_path, dpi=300):
        """Save plot to file."""
        fig.savefig(output_path, dpi=dpi, transparent=True, pad_inches=0, bbox_inches="tight")
        plt.close(fig)
        logger.info(f"Saved: {output_path}")
    
    def plot_chlorophyll(self):
        """Generate chlorophyll-a plots from C2RCC and mosaic outputs."""
        logger.info("Generating Chlorophyll-a plots")

        output_dir = self.dirs['final_products'] / 'chl'
        success_count = 0

        # Process files from both c2rcc and mosaic outputs
        input_dirs = []

        # Add mosaic files if they exist (multiple tiles)
        mosaic_files = list(self.dirs['mosaic_output'].glob("*.nc"))
        if mosaic_files:
            input_dirs.append(("mosaic", mosaic_files))
            logger.info(f"Found {len(mosaic_files)} mosaic files")

        # Add c2rcc files (single tiles)
        c2rcc_files = list(self.dirs['c2rcc_output'].glob("*.nc"))
        if c2rcc_files:
            input_dirs.append(("c2rcc", c2rcc_files))
            logger.info(f"Found {len(c2rcc_files)} C2RCC files")

        if not input_dirs:
            logger.warning("No input files found for chlorophyll plotting")
            return success_count

        for source_type, files in input_dirs:
            for nc_file in files:
                try:
                    # Extract date from filename
                    formatted_date = self.extract_date_from_filename(nc_file.name)
                    output_file = output_dir / f"{formatted_date}.png"

                    if output_file.exists():
                        logger.info(f"Chlorophyll plot already exists: {output_file.name}")
                        success_count += 1
                        continue

                    # Open dataset
                    ds = xr.open_dataset(nc_file)

                    # Extract chlorophyll data
                    chl_data = ds["conc_chl"].where(ds["conc_chl"] != 0, np.nan).values
                    lat = ds["lat"].values
                    lon = ds["lon"].values

                    # Create plot
                    fig, ax, extent = self.create_base_plot(chl_data, lat, lon)

                    # Set colormap
                    self.chl_cmap.set_bad(color="black")

                    # Plot data
                    img = ax.imshow(
                        chl_data,
                        extent=extent,
                        cmap=self.chl_cmap,
                        transform=ccrs.PlateCarree(),
                        origin="upper",
                        norm=self.chl_norm
                    )

                    # Save plot
                    self.save_plot(fig, output_file)
                    success_count += 1

                    ds.close()

                except Exception as e:
                    logger.error(f"Error processing {nc_file.name}: {e}")

        logger.info(f"Chlorophyll plots: {success_count} files processed")
        return success_count
    
    def plot_tsm(self):
        """Generate TSM plots from C2RCC and mosaic outputs."""
        logger.info("Generating TSM plots")

        output_dir = self.dirs['final_products'] / 'tsm'
        success_count = 0

        # Process files from both c2rcc and mosaic outputs
        input_dirs = []

        # Add mosaic files if they exist (multiple tiles)
        mosaic_files = list(self.dirs['mosaic_output'].glob("*.nc"))
        if mosaic_files:
            input_dirs.append(("mosaic", mosaic_files))
            logger.info(f"Found {len(mosaic_files)} mosaic files")

        # Add c2rcc files (single tiles)
        c2rcc_files = list(self.dirs['c2rcc_output'].glob("*.nc"))
        if c2rcc_files:
            input_dirs.append(("c2rcc", c2rcc_files))
            logger.info(f"Found {len(c2rcc_files)} C2RCC files")

        if not input_dirs:
            logger.warning("No input files found for TSM plotting")
            return success_count

        for source_type, files in input_dirs:
            for nc_file in files:
                try:
                    # Extract date from filename
                    formatted_date = self.extract_date_from_filename(nc_file.name)
                    output_file = output_dir / f"{formatted_date}.png"

                    if output_file.exists():
                        logger.info(f"TSM plot already exists: {output_file.name}")
                        success_count += 1
                        continue

                    # Open dataset
                    ds = xr.open_dataset(nc_file)

                    # Check if TSM variable exists
                    if "conc_tsm" not in ds.variables:
                        logger.warning(f"Variable 'conc_tsm' not found in {nc_file.name}")
                        continue

                    # Extract TSM data
                    tsm_data = ds["conc_tsm"].where(ds["conc_tsm"] != 0, np.nan).values
                    lat = ds["lat"].values
                    lon = ds["lon"].values

                    # Create plot
                    fig, ax, extent = self.create_base_plot(tsm_data, lat, lon)

                    # Plot data
                    img = ax.imshow(
                        tsm_data,
                        extent=extent,
                        cmap=self.tsm_cmap,
                        transform=ccrs.PlateCarree(),
                        origin="upper",
                        vmin=0,
                        vmax=4
                    )

                    # Save plot
                    self.save_plot(fig, output_file)
                    success_count += 1

                    ds.close()

                except Exception as e:
                    logger.error(f"Error processing {nc_file.name}: {e}")

        logger.info(f"TSM plots: {success_count} files processed")
        return success_count
    
    def plot_cdom(self):
        """Generate CDOM plots."""
        logger.info("Generating CDOM plots")
        
        input_dir = self.dirs['cdom_output']
        output_dir = self.dirs['final_products'] / 'cdom'
        
        success_count = 0
        
        for nc_file in input_dir.glob("*.nc"):
            try:
                # Extract date from filename
                formatted_date = self.extract_date_from_filename(nc_file.name)
                output_file = output_dir / f"{formatted_date}.png"
                
                if output_file.exists():
                    logger.info(f"CDOM plot already exists: {output_file.name}")
                    success_count += 1
                    continue
                
                # Open dataset
                ds = xr.open_dataset(nc_file)
                
                # Extract CDOM data
                cdom_data = ds["CDOM"].where(ds["CDOM"] != 0, np.nan).values
                lat = ds["lat"].values
                lon = ds["lon"].values
                
                # Create plot
                fig, ax, extent = self.create_base_plot(cdom_data, lat, lon)
                
                # Plot data
                img = ax.imshow(
                    cdom_data,
                    extent=extent,
                    cmap=self.cdom_cmap,
                    transform=ccrs.PlateCarree(),
                    origin="upper",
                    vmin=0,
                    vmax=4
                )
                
                # Save plot
                self.save_plot(fig, output_file)
                success_count += 1
                
                ds.close()
                
            except Exception as e:
                logger.error(f"Error processing {nc_file.name}: {e}")
        
        logger.info(f"CDOM plots: {success_count} files processed")
        return success_count
    
    def generate_all_plots(self):
        """Generate all water quality plots."""
        logger.info("Starting plot generation for all water quality parameters")
        
        results = {}
        
        # Generate plots for each parameter
        results['chlorophyll'] = self.plot_chlorophyll()
        results['tsm'] = self.plot_tsm()
        results['cdom'] = self.plot_cdom()
        
        # Summary
        logger.info("Plot generation summary:")
        for param, count in results.items():
            logger.info(f"{param}: {count} plots generated")
        
        total_plots = sum(results.values())
        logger.info(f"Total plots generated: {total_plots}")
        
        return total_plots > 0

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Generate water quality plots')
    parser.add_argument('--config', required=True, help='Configuration file path')
    parser.add_argument('--parameter', choices=['chl', 'tsm', 'cdom', 'all'], 
                       default='all', help='Parameter to plot')
    
    args = parser.parse_args()
    
    # Check configuration file
    config_path = Path(args.config)
    if not config_path.exists():
        logger.error(f"Configuration file not found: {config_path}")
        sys.exit(1)
    
    # Initialize plotter
    plotter = WaterQualityPlotter(config_path)
    
    # Generate plots
    if args.parameter == 'all':
        success = plotter.generate_all_plots()
    elif args.parameter == 'chl':
        success = plotter.plot_chlorophyll() > 0
    elif args.parameter == 'tsm':
        success = plotter.plot_tsm() > 0
    elif args.parameter == 'cdom':
        success = plotter.plot_cdom() > 0
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()