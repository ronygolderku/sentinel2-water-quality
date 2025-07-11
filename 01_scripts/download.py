"""
Sentinel-2 Data Download Script
Downloads Sentinel-2 L1C data from Copernicus Data Space Ecosystem
"""

import os
import sys
import argparse
import logging
from datetime import datetime
from pathlib import Path

import yaml
import requests
import pandas as pd
import geopandas as gpd
from shapely.geometry import shape

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Sentinel2Downloader:
    def __init__(self, config_file):
        """Initialize the downloader with configuration."""
        self.config = self._load_config(config_file)
        self.base_dir = Path(__file__).parent.parent
        self.download_dir = self.base_dir / self.config['directories']['raw_data']
        self.download_dir.mkdir(parents=True, exist_ok=True)
        
    def _load_config(self, config_file):
        """Load configuration from YAML file."""
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def _get_keycloak_token(self):
        """Get authentication token from Copernicus."""
        data = {
            "client_id": "cdse-public",
            "username": self.config['download']['copernicus_user'],
            "password": self.config['download']['copernicus_password'],
            "grant_type": "password",
        }
        
        try:
            response = requests.post(
                "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
                data=data,
            )
            response.raise_for_status()
            return response.json()["access_token"]
        except Exception as e:
            logger.error(f"Failed to get authentication token: {e}")
            raise
    
    def search_products(self, start_date, end_date):
        """Search for Sentinel-2 products."""
        logger.info(f"Searching for products from {start_date} to {end_date}")
        
        # Format dates
        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')
        
        # Build search query
        collection = self.config['download']['data_collection']
        geometry = self.config['study_area']['wkt_geometry']
        cloud_threshold = self.config['download']['cloud_cover_threshold']
        
        search_url = (
            f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?"
            f"$filter=Collection/Name eq '{collection}' "
            f"and OData.CSC.Intersects(area=geography'SRID=4326;{geometry}') "
            f"and Attributes/OData.CSC.DoubleAttribute/any(att:att/Name eq 'cloudCover' and att/Value lt {cloud_threshold}) "
            f"and ContentDate/Start gt {start_str}T00:00:00.000Z "
            f"and ContentDate/Start lt {end_str}T00:00:00.000Z"
            f"&$count=True&$top=1000"
        )
        
        try:
            response = requests.get(search_url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to search products: {e}")
            return None
    
    def download_products(self, start_date, end_date):
        """Download Sentinel-2 products."""
        # Search for products
        search_results = self.search_products(start_date, end_date)
        
        if not search_results or not search_results.get('value'):
            logger.warning("No products found for the specified criteria")
            return
        
        # Convert to DataFrame
        products_df = pd.DataFrame(search_results['value'])
        
        # Add geometry and convert to GeoDataFrame
        products_df['geometry'] = products_df['GeoFootprint'].apply(shape)
        products_gdf = gpd.GeoDataFrame(products_df).set_geometry('geometry')
        
        # Filter for L1C products only
        l1c_products = products_gdf[products_gdf['Name'].str.contains('L1C')]
        
        if l1c_products.empty:
            logger.warning("No L1C products found")
            return
        
        logger.info(f"Found {len(l1c_products)} L1C products")
        
        # Download products
        for idx, product in l1c_products.iterrows():
            self._download_single_product(product)
    
    def _download_single_product(self, product):
        """Download a single product."""
        try:
            # Get product identifier
            product_name = product['Name']
            product_id = product['Id']
            
            # Check if already downloaded
            output_file = self.download_dir / f"{product_name}.zip"
            if output_file.exists():
                logger.info(f"Product already exists: {product_name}")
                return
            
            logger.info(f"Downloading: {product_name}")
            
            # Create session and get token
            session = requests.Session()
            token = self._get_keycloak_token()
            session.headers.update({"Authorization": f"Bearer {token}"})
            
            # Download product
            download_url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products({product_id})/$value"
            
            response = session.get(download_url, allow_redirects=False)
            
            # Handle redirects
            while response.status_code in (301, 302, 303, 307):
                download_url = response.headers["Location"]
                response = session.get(download_url, allow_redirects=False)
            
            # Download the file
            if response.status_code == 200:
                file_response = session.get(download_url, verify=False, allow_redirects=True)
                
                with open(output_file, 'wb') as f:
                    f.write(file_response.content)
                
                logger.info(f"Successfully downloaded: {product_name}")
            else:
                logger.error(f"Failed to download {product_name}: HTTP {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error downloading {product_name}: {e}")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Download Sentinel-2 data')
    parser.add_argument('--config', required=True, help='Configuration file path')
    parser.add_argument('--start-date', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='End date (YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    # Load configuration
    config_path = Path(args.config)
    if not config_path.exists():
        logger.error(f"Configuration file not found: {config_path}")
        sys.exit(1)
    
    # Initialize downloader
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
    
    # Download products
    downloader.download_products(start_date, end_date)
    
    logger.info("Download process completed")

if __name__ == "__main__":
    main()
