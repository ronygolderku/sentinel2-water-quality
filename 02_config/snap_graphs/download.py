from datetime import date, timedelta
import requests
import pandas as pd
import geopandas as gpd
from shapely.geometry import shape
import os
from datetime import datetime
copernicus_user = "ronygolderku@gmail.com" # copernicus User
copernicus_password = "G@DVH26uGtb3BBq" # copernicus Password
ft = "POLYGON ((115.53949386146294 -31.925260296569277, 115.78672226811288 -31.92786249897796, 115.78223830220871 -32.26641419173019, 115.53409693090781 -32.2637777945036, 115.53949386146294 -31.925260296569277))"  # WKT Representation of BBOX
data_collection = "SENTINEL-2" # Sentinel satellite

# Define the start and end dates
start_date = datetime(2025, 5, 1)  # Start from May 1, 2025
end_date = datetime(2025, 6, 30)  # End on June 30, 2025

# Format as YYYY-MM-DD
start_string = start_date.strftime('%Y-%m-%d')
end_string = end_date.strftime('%Y-%m-%d')

print("Start Date:", start_string)  # Output: 2015-01-01
print("End Date:", end_string)      # Output: 2018-12-31
def get_keycloak(username: str, password: str) -> str:
    data = {
        "client_id": "cdse-public",
        "username": username,
        "password": password,
        "grant_type": "password",
    }
    try:
        r = requests.post(
            "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
            data=data,
        )
        r.raise_for_status()
    except Exception as e:
        raise Exception(
            f"Keycloak token creation failed. Response from the server was: {r.json()}"
        )
    return r.json()["access_token"]

json_ = requests.get(
    f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name eq '{data_collection}' "
    f"and OData.CSC.Intersects(area=geography'SRID=4326;{ft}') "
    f"and Attributes/OData.CSC.DoubleAttribute/any(att:att/Name eq 'cloudCover' and att/Value lt 10) "
    f"and ContentDate/Start gt {start_string}T00:00:00.000Z "
    f"and ContentDate/Start lt {end_string}T00:00:00.000Z&$count=True&$top=1000"
).json() 

p = pd.DataFrame.from_dict(json_["value"]) # Fetch available dataset
if p.shape[0] > 0 : # If we get data back
    p["geometry"] = p["GeoFootprint"].apply(shape)
    # Convert pandas dataframe to Geopandas dataframe by setting up geometry
    productDF = gpd.GeoDataFrame(p).set_geometry("geometry") 
    # Keep only L1C dataset (remove L2A if present)
    productDF = productDF[productDF["Name"].str.contains("L1C")]
    print(f" total L1C tiles found {len(productDF)}")
    productDF["identifier"] = productDF["Name"].str.split(".").str[0]
    allfeat = len(productDF) 
    
    if allfeat == 0: # If L1C tiles are not available in current query
        print(f"No L1C tiles found for the specified date range: {start_string} to {end_string}")
    else: # If L1C tiles are available in current query
        # download all tiles from server
        for index,feat in enumerate(productDF.iterfeatures()):
            try:
                # Create requests session 
                session = requests.Session()
                # Get access token based on username and password
                keycloak_token = get_keycloak(copernicus_user,copernicus_password)
                
                session.headers.update({"Authorization": f"Bearer {keycloak_token}"})
                url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products({feat['properties']['Id']})/$value"
                response = session.get(url, allow_redirects=False)
                while response.status_code in (301, 302, 303, 307):
                    url = response.headers["Location"]
                    response = session.get(url, allow_redirects=False)
                print(feat["properties"]["Id"])
                file = session.get(url, verify=False, allow_redirects=True)

                # Create download directory if it doesn't exist
                download_dir = "dataset"
                os.makedirs(download_dir, exist_ok=True)
                
                with open(
                    os.path.join(download_dir, f"{feat['properties']['identifier']}.zip"), #location to save zip from copernicus 
                    "wb",
                ) as zip_file:
                    print(feat["properties"]["Name"])
                    zip_file.write(file.content)
            except:
                print("problem with server")
else : # If no tiles found for given date range and AOI
    print('no data found')