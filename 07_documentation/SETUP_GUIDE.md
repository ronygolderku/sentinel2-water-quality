# Quick Setup Guide - Study Area Configuration

## Overview

The Sentinel-2 Water Quality workflow is designed to be **study-area agnostic**. You can easily configure it for any geographic region with a simple WKT polygon update.

## Simple 3-Step Setup

### Step 1: Update Study Area Geometry

Edit `02_config/parameters.yaml` and update the WKT polygon:

```yaml
study_area:
  name: "Your Study Area Name"
  wkt_geometry: "POLYGON ((lon1 lat1, lon2 lat2, lon3 lat3, lon4 lat4, lon1 lat1))"
```

**Example - Western Australia Coast:**
```yaml
study_area:
  name: "Western Australia Coast"
  wkt_geometry: "POLYGON ((115.54 -31.93, 115.79 -31.93, 115.79 -32.26, 115.54 -32.26, 115.54 -31.93))"
```

### Step 2: Update Credentials

Also in `02_config/parameters.yaml`, update your Copernicus credentials:

```yaml
download:
  copernicus_user: "your_email@domain.com"
  copernicus_password: "your_password"
  cloud_cover_threshold: 10
  default_start_date: "2025-05-01"
  default_end_date: "2025-06-30"
```

### Step 3: Run the Workflow

The workflow will automatically:
1. Extract bounds from your WKT polygon
2. Update all SNAP processing configuration files
3. Apply the study area to all processing steps
4. Download, process, and visualize data for your area

```bash
# Full workflow
python 01_scripts/process_pipeline.py --config 02_config/parameters.yaml

# Or step-by-step
python 01_scripts/download.py --config 02_config/parameters.yaml
python 01_scripts/process_pipeline.py --config 02_config/parameters.yaml
python 01_scripts/plotting.py --config 02_config/parameters.yaml
```

## Getting Your WKT Polygon

### Option 1: Draw Online
Use [WKT geometry builder](https://arthur-e.github.io/Wicket/demo/) to draw your study area and get WKT

### Option 2: QGIS
1. Open QGIS
2. Draw a rectangle or polygon for your study area
3. Right-click → Copy as WKT
4. Paste into parameters.yaml

### Option 3: Manually
Identify corner coordinates (longitude, latitude) of your study area and format as:
```
POLYGON ((west north, east north, east south, west south, west north))
```

## Format Requirements

- **Coordinate Order**: Longitude first, then latitude (X, Y)
- **Closure**: First and last coordinates must be identical
- **Projection**: WGS84 (EPSG:4326)
- **Geometry**: Must be a closed polygon

## Verification

After updating parameters.yaml, you can verify geometry update:

```bash
python 01_scripts/update_snap_geometry.py --config 02_config/parameters.yaml
```

Output will show:
```
Study Area WKT: POLYGON ((115.54 -31.93, ...
✓ Extracted bounds:
  Latitude:  -32.260000 to -31.930000
  Longitude: 115.540000 to 115.790000

✓ Updated resample_subset.xml with new geometry
✓ Updated mosaic.xml with bounding box
✓ All SNAP geometry files updated successfully!
```

## Example Study Areas

### Great Barrier Reef, Australia
```
POLYGON ((142.0 -10.0, 156.0 -10.0, 156.0 -24.0, 142.0 -24.0, 142.0 -10.0))
```

### Baltic Sea, Europe
```
POLYGON ((9.0 53.0, 30.0 53.0, 30.0 66.0, 9.0 66.0, 9.0 53.0))
```

### Caribbean
```
POLYGON ((-85.0 10.0, -60.0 10.0, -60.0 25.0, -85.0 25.0, -85.0 10.0))
```

## Troubleshooting

### "Invalid WKT format"
- Check that coordinates are in (longitude, latitude) order
- Ensure polygon is closed (first and last coordinate are identical)
- Verify numbers are properly formatted

### Bounds don't match study area
- Check that all 4 corner coordinates are included
- Ensure westmost longitude is actually west (smaller value)
- Ensure northmost latitude is actually north (less negative for Southern Hemisphere)

## Automatic Updates

The workflow automatically updates all configuration files when you run it:
- `resample_subset.xml` - Study area for resampling and subsetting
- `mosaic.xml` - Bounds for mosaic operation and reprojection
- All other SNAP processing files use the updated geometry

No manual XML editing required!
