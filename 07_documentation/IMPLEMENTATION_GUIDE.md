# Implementation Guide - Automatic Geometry & Multi-tile Processing

This guide explains how the Sentinel-2 Water Quality toolkit automatically handles study area configuration and multi-tile processing.

## Table of Contents

1. [Automatic Geometry Update System](#automatic-geometry-update-system)
2. [Single-tile vs Multi-tile Workflow](#single-tile-vs-multi-tile-workflow)
3. [How the Workflow Detects Tile Coverage](#how-the-workflow-detects-tile-coverage)
4. [Processing Pipeline Details](#processing-pipeline-details)
5. [Key Features & Safety Checks](#key-features--safety-checks)

---

## Automatic Geometry Update System

### Overview

The workflow is designed to require **only one configuration**: your study area WKT polygon. Everything else updates automatically.

### How It Works

```
User edits parameters.yaml
        ↓
Workflow starts (process_pipeline.py)
        ↓
Calls update_snap_geometry.py automatically
        ↓
Script reads WKT_geometry from parameters.yaml
        ↓
Extracts geographic bounds (west, east, north, south)
        ↓
Updates all SNAP XML files:
  ├── resample_subset.xml (geoRegion with WKT)
  ├── mosaic.xml (bounds + variables preserved!)
  └── Other processing files
        ↓
Processing runs with synchronized geometry
```

### What Gets Updated

#### 1. **resample_subset.xml**
```xml
<geoRegion>POLYGON ((lon1 lat1, lon2 lat2, ...))</geoRegion>
```
- Contains full WKT polygon
- Used for spatial subsetting during resampling
- Ensures data subset matches study area

#### 2. **mosaic.xml**
```xml
<westBound>value</westBound>
<northBound>value</northBound>
<eastBound>value</eastBound>
<southBound>value</southBound>
```
- Extracted from WKT bounds
- Used for mosaic geolocation processing
- **Variables section ALWAYS preserved** (not removed during updates!)

### Safety Features

✅ **Regex-based updates** - Only targets specific XML tags, leaves rest untouched
✅ **Variables preserved** - Mosaic variables section never removed
✅ **Automatic on every run** - Ensures consistency between config and XML files
✅ **Portable** - Works across Windows, Linux, macOS

---

## Single-tile vs Multi-tile Workflow

### How It's Detected

The `get_tiles_by_date()` method analyzes C2RCC output to determine coverage:

```python
# Groups C2RCC files by date
# Counts how many tiles per date
# Result: {'20250515': {'single': [...], 'multiple': [...]}}
```

**Detection logic:**
1. After C2RCC processing completes, files exist in `c2rcc_output/`
2. Filename contains tile ID (e.g., `T52LFL`, `T52LFM`)
3. For each date, count unique tile IDs
4. If 1 tile → single-tile processing
5. If 2+ tiles → multi-tile processing

### Single-Tile Processing

```
📦 Input: 1 C2RCC file per date
   └── Subset_S2_MSIL2A_20250515_T52LFL_C2RCC.nc

📊 Step 5 (Mosaic): SKIPPED
   ℹ "Single tile detected - mosaic not needed"

⚙️ Step 6 (CDOM): Uses C2RCC file directly
   └── Source: 04_processed_data/c2rcc_output/
   └── Output: 04_processed_data/cdom_output/CDOM.nc

📈 Step 7 (Plotting): Reads from c2rcc_output/
   └── Generates: 05_final_products/{chl,tsm,cdom}/*.png

💾 Benefits:
   ✅ No mosaic processing (30-50% faster)
   ✅ Saves 30-50% disk space
   ✅ Direct output to final products
```

### Multi-Tile Processing

```
📦 Input: Multiple C2RCC files per date
   ├── Subset_S2_MSIL2A_20250515_T52LFL_C2RCC.nc
   ├── Subset_S2_MSIL2A_20250515_T52LFM_C2RCC.nc
   └── Subset_S2_MSIL2A_20250515_T52LFN_C2RCC.nc

📊 Step 5 (Mosaic): CREATES MOSAIC
   ├── Reads bounds from mosaic.xml (auto-updated from WKT)
   ├── Combines all tiles for date
   └── Output: 04_processed_data/mosaic_output/
             Mosaic_S2_MSIL2A_20250515.nc

⚙️ Step 6 (CDOM): Uses mosaic file
   └── Source: 04_processed_data/mosaic_output/
   └── Output: 04_processed_data/cdom_output/CDOM.nc

📈 Step 7 (Plotting): Reads from mosaic_output/
   └── Generates: 05_final_products/{chl,tsm,cdom}/*.png

💾 Benefits:
   ✅ Seamless coverage across tiles
   ✅ Single unified product per date
   ✅ Consistent spatial coverage
```

---

## How the Workflow Detects Tile Coverage

### Step-by-Step Detection Process

#### Before Mosaic Step

The `get_tiles_by_date()` method:

```python
1. Lists all files in c2rcc_output/
2. For each file: extracts date and tile ID
3. Groups by date
4. Categorizes as 'single' or 'multiple'

Result structure:
{
  '20250515': {
    'single': [],  # Empty if multiple tiles
    'multiple': [  # Files from different tiles
      Path('.../T52LFL_C2RCC.nc'),
      Path('.../T52LFM_C2RCC.nc')
    ]
  }
}
```

#### Tile ID Extraction

Tile IDs extracted from filenames:
```
S2A_MSIL1C_20150903T014036_N0500_R031_T52LFL_20231017T130149.zip
                                      ^^^^^^
                                    Tile ID (T + 5 chars)
```

#### Processing Decision

```python
if len(multiple_files) < 2:
    # Single-tile date
    logger.info("Single tile detected - mosaic not needed")
    continue  # Skip to next date

else:
    # Multi-tile date
    Create mosaic for this date
    Add to mosaic_output/
```

---

## Processing Pipeline Details

### Full 7-Step Pipeline with Decision Logic

```
Step 1: Resample & Subset
├─ Input: Downloaded ZIP files (03_raw_data/)
├─ Process: Resample to 10m, subset to WKT bounds
├─ Output: l2a_resampled/*.dim
└─ Geometry: From resample_subset.xml (WKT auto-updated)

Step 2: Reproject to WGS84
├─ Input: l2a_resampled/*.dim
├─ Process: Reproject all bands to WGS84 (EPSG:4326)
├─ Output: l2a_reprojected/*.dim
└─ Geometry: Applied during reprojection

Step 3: Generate True Color Images
├─ Input: l2a_reprojected/*.dim
├─ Process: Create RGB true color composites
├─ Output: 05_final_products/true_color/*.png
└─ Status: Independent of tile count

Step 4: C2RCC Processing
├─ Input: l2a_reprojected/*.dim
├─ Process: Atmospheric correction & water quality retrieval
├─ Output: c2rcc_output/*_C2RCC.nc
└─ Per-tile: Each tile processed individually

Step 5: Mosaic Processing (CONDITIONAL)
├─ Decision: Check get_tiles_by_date()
├─ If single-tile per date:
│  └─ SKIP (log: "mosaic not needed")
├─ If multi-tile per date:
│  ├─ Input: All c2rcc_output files for that date
│  ├─ Bounds: From mosaic.xml (auto-updated)
│  ├─ Process: Combine tiles using SNAP Mosaic
│  └─ Output: mosaic_output/Mosaic_*.nc
└─ Result: Determines source for Step 6

Step 6: CDOM Calculation (ADAPTIVE)
├─ Detect available sources:
│  ├─ If mosaic exists for date → USE mosaic
│  └─ If only C2RCC exists → USE c2rcc
├─ Input: mosaic_output/* OR c2rcc_output/*
├─ Process: Band math calculation
├─ Output: cdom_output/*_CDOM.nc
└─ Automatic: Source selected automatically

Step 7: Generate Plots (ADAPTIVE)
├─ Input sources:
│  ├─ Check mosaic_output/ first
│  ├─ Also read c2rcc_output/
├─ Process: Create publication-ready visualizations
├─ Output: 05_final_products/{chl,tsm,cdom}/*.png
└─ Automatic: Reads from both sources as available
```

### Data Flow Diagram

```
Downloaded Data (03_raw_data/)
    ↓
    └─→ [Step 1: Resample] → l2a_resampled/
            ↓
        [Step 2: Reproject] → l2a_reprojected/
            ↓
        ┌─→ [Step 3: True Color] → true_color/
        │
        └─→ [Step 4: C2RCC] → c2rcc_output/
                ├─ Single tile per date
                │   ↓
                ├─→ [SKIP Step 5]
                │   ↓
                └─→ [Step 6: CDOM] (uses c2rcc)
                │   ↓
                └─→ [Step 7: Plots] (reads c2rcc)
                │   ↓
                └─→ Final products/

                ├─ Multiple tiles per date
                │   ↓
                ├─→ [Step 5: Mosaic] → mosaic_output/
                │   ↓
                └─→ [Step 6: CDOM] (uses mosaic)
                    ↓
                └─→ [Step 7: Plots] (reads mosaic)
                    ↓
                └─→ Final products/
```

---

## Key Features & Safety Checks

### ✅ Automatic Features

| Feature | Benefit |
|---------|---------|
| Geometry auto-update | No manual XML editing needed |
| Tile auto-detection | Single vs multi-tile determined automatically |
| Source auto-selection | CDOM uses correct source (mosaic or C2RCC) |
| Plotting auto-adaptation | Reads from both directories as needed |
| Variables preservation | Mosaic XML variables never removed |

### 🛡️ Safety Checks

```python
# Error handling
if not tiles_by_date:
    logger.info("No C2RCC files found - skipping mosaic")
    return True  # Not considered an error

# Source validation
if mosaic_file.exists():  # Multi-tile
    source = mosaic_file  # Use mosaic
elif single_files:        # Single-tile
    source = single_files[0]  # Use c2rcc
else:
    logger.warning(f"No source found for {date}")
    continue  # Skip this date

# Bounds preservation
# Regex only replaces: <westBound>VALUE</westBound>
# Never affects: <variables>...</variables>
```

### 📊 Logging

Every step includes detailed logging:
```
2026-03-29 15:50:14 - INFO - STEP 5: Mosaic Processing (if multiple tiles)
2026-03-29 15:50:14 - INFO - Creating mosaic for 20250515 from 2 tiles
2026-03-29 15:50:14 - INFO - Single-tile dates found: 1 (mosaic processing skipped)
2026-03-29 15:50:14 - INFO - STEP 6: CDOM Calculation
2026-03-29 15:50:14 - INFO - CDOM calculation for 20250515 (source: mosaic)
```

---

## Summary

This toolkit provides:
1. **Simplicity**: Update WKT once, everything else happens automatically
2. **Efficiency**: Single-tile studies run faster and use less disk space
3. **Scalability**: Multi-tile areas processed seamlessly with automatic mosaicing
4. **Reliability**: Safety checks and error handling at every step
5. **Portability**: Works across all platforms (Windows, Linux, macOS)

**The workflow is completely automated and requires no manual intervention after initial WKT configuration!**
