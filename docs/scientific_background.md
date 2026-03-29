# Scientific Background & Water Quality Monitoring

## Why Monitor Water Quality?

Water quality monitoring is essential for understanding the ecological and trophic status of aquatic environments. Accurate and consistent data captures critical changes in:

- **Phytoplankton Biomass** - Indicates primary productivity and potential eutrophication
- **Total Suspended Matter (TSM)** - Reflects particulate load, turbidity, and water clarity
- **Colored Dissolved Organic Matter (CDOM)** - Represents dissolved organic compounds affecting light penetration
- **Water Transparency** - Influences light availability for photosynthesis

These parameters are vital for:
- ✅ Environmental monitoring and ecosystem health assessment
- ✅ Detecting harmful algal blooms and eutrophication
- ✅ Coastal zone management and marine spatial planning
- ✅ Climate change impact assessment
- ✅ Water resource management

---

## Sentinel-2 Satellite System

### Mission Overview

**Sentinel-2**, operated by the European Space Agency (ESA), is specifically designed for high-resolution Earth observation of land and coastal areas. It is ideal for water quality monitoring due to its:

- ✅ High spatial resolution (10-60m depending on band)
- ✅ Multispectral capabilities (13 spectral bands)
- ✅ Frequent revisit time (5-day global coverage with constellation)
- ✅ Open data policy (free/open access)
- ✅ Extended archive since 2015

### Satellite Constellation

The Sentinel-2 constellation consists of:

| Satellite | Launch Date | Status | Notes |
|-----------|------------|--------|-------|
| **S2A** | June 2015 | Operational | Original Sentinel-2 |
| **S2B** | March 2017 | Operational | Improves revisit time to 5 days |
| **S2C** | September 2024 | Operational | Replaced S2A (maintaining constellation) |

### Multispectral Instrument (MSI)

Each satellite carries the **Multi-Spectral Instrument (MSI)**, which acquires **Level-1C Top-of-Atmosphere (TOA) reflectance** data in 13 spectral bands:

#### Spectral Bands for Water Quality Monitoring

| Band | Wavelength (nm) | Resolution (m) | Application |
|------|----------------|-----------------|------------|
| **B1** | 443 (Coastal) | 60 | Aerosol detection, water properties |
| **B2** | 490 (Blue) | 10 | Water absorption, chlorophyll |
| **B3** | 560 (Green) | 10 | Vegetation & water reflectance |
| **B4** | 665 (Red) | 10 | Chlorophyll-a absorption |
| **B5-B7** | 705-783 (NIR) | 20 | Vegetation indices, atmospheric correction |
| **B8** | 842 (NIR) | 10 | Vegetation & water discrimination |
| **B8A** | 865 (NIR) | 20 | Advanced vegetation indices |
| **B9** | 940 (Water vapour) | 60 | Atmospheric correction |
| **B10** | 1375 (Cirrus) | 60 | Cloud detection |
| **B11-B12** | 1610-2190 (SWIR) | 20 | Vegetation & soil discrimination |

### Data Availability

This toolkit downloads **Level-1C products** with less than 5% cloud cover from the **Copernicus Data Space Ecosystem**, which provides:
- ✅ Open access to all Sentinel-2 data
- ✅ Data archive from 2015 to present
- ✅ Global coverage
- ✅ Regular processing and updates

---

## C2RCC Processor Workflow

### What is C2RCC?

**C2RCC** (Case-2 Regional Coast Colour) is a state-of-the-art atmospheric correction and bio-optical inversion algorithm specifically designed for **optically complex waters** such as:
- 🌊 Coastal zones
- 🌊 Estuaries
- 🌊 Inland lakes
- 🌊 Turbid/eutrophic waters

Unlike Case-1 waters (open ocean), these environments contain suspended and dissolved substances that significantly influence spectral reflectance.

### Processing Architecture

The C2RCC algorithm is implemented in this toolkit through:

1. **SNAP Integration**: Uses ESA's Sentinel Application Platform (SNAP)
2. **Graph Processing Tool (gpt)**: Command-line processing engine
3. **Neural Network Model**: C2RCC-Nets for parameter inversion
4. **XML Configuration**: User-customizable processing parameters

### Processing Steps

```
Level-1C TOA Reflectance
    ↓
[Atmospheric Correction]
    - Aerosol optical depth estimation
    - Rayleigh scattering correction
    - Atmospheric water vapor estimation
    - Ozone correction
    ↓
[Bio-optical Inversion]
    - Water-leaving reflectance calculation
    - Phytoplankton-specific absorption
    - CDOM absorption modeling
    - TSM backscatter estimation
    ↓
[Quality Flags & Masks]
    - Valid pixel identification
    - Cloud/shadow masking
    - Land masking
    ↓
Water Quality Parameters (NetCDF output)
```

### Configuration Parameters

Key settings for C2RCC processing are defined in `02_config/snap_graphs/c2rcc_param.xml`:

```yaml
Atmospheric Model:  Maritime/Coastal/Desert
Salinity:           35.0 (default for coastal seawater)
Temperature:        30.0°C (regional average)
CHL Factor:         21.0 (empirical scaling)
TSM Factor:         1.06 (empirical scaling)
Valid Pixel Expr:   B8 > 0 && B8 < 0.1 (NIR thresholds)
```

---

## Bio-geophysical Parameter Extraction

### 1. Chlorophyll-a Concentration (Chl-a)

**Definition**: Proxy for phytoplankton biomass and primary productivity

**Physical Basis**:
- Chlorophyll-a absorbs strongly in the blue (B2: 490 nm) and red (B4: 665 nm) regions
- Reflectance minimum at 665 nm indicates high Chl-a concentration
- C2RCC uses neural network inversion of spectral reflectance

**Units**: mg/m³

**Typical Ranges**:
- **Oligotrophic waters**: 0.1 - 0.5 mg/m³
- **Mesotrophic waters**: 0.5 - 2.0 mg/m³
- **Eutrophic waters**: 2.0 - 20.0+ mg/m³

**Interpretation**:
- 🟢 Low values: Clear, nutrient-poor waters
- 🟡 Medium values: Productive coastal waters
- 🔴 High values: Potential eutrophication, harmful algal blooms

**Quality Flag**: Flagged as invalid if outside physical range or affected by atmospheric correction uncertainty

---

### 2. Total Suspended Matter (TSM)

**Definition**: Mass concentration of particulates suspended in water column

**Physical Basis**:
- Particles scatter light across visible and near-infrared wavelengths
- TSM concentration inversely related to water transparency
- C2RCC estimates from red (B4) and NIR (B8) reflectance ratio

**Units**: g/m³

**Typical Ranges**:
- **Clear waters**: 0.5 - 2.0 g/m³
- **Moderate turbidity**: 2.0 - 5.0 g/m³
- **High turbidity (rivers/estuaries)**: 5.0 - 50.0+ g/m³

**Sources**:
- ✅ Plankton and phytoplankton
- ✅ Terrigenous sediment (river plumes, erosion)
- ✅ Anthropogenic particles (pollution)
- ✅ Resuspended bottom material

**Interpretation**:
- 🟢 Low TSM: Good water transparency, healthy ecosystem
- 🔴 High TSM: Turbid water, potential stress, sediment plume detection

---

### 3. Colored Dissolved Organic Matter (CDOM)

**Definition**: Dissolved organic carbon with ability to absorb light (chromophoric DOM)

**Physical Basis**:
- Originates from terrestrial and aquatic sources
- Absorbs strongly in blue wavelengths (B1: 443 nm)
- Custom band-math expression applied to C2RCC water-leaving reflectance

**CDOM Algorithm**:

The CDOM absorption coefficient (a_CDOM at 443 nm) is calculated using:

```
CDOM = exp(0.544⋅log(rhown_B1) − 0.571⋅log(rhown_B2)
           − 2.181⋅log(rhown_B3) + 1.398⋅log(rhown_B4) − 1.406)
```

Where:
- `rhown_B1, B2, B3, B4` = water-leaving reflectance from C2RCC (Bands 1-4)
- Coefficients derived from regional calibration dataset
- Regional applicability: Australian coastal waters

**Units**: m⁻¹

**Typical Ranges**:
- **Clear offshore**: 0.01 - 0.05 m⁻¹
- **Coastal waters**: 0.05 - 0.5 m⁻¹
- **River plumes/estuaries**: 0.5 - 4.0+ m⁻¹

**Interpretation**:
- 🟢 Low CDOM: Clear offshore waters, minimal organic matter
- 🟡 Moderate CDOM: Coastal waters with natural organic loading
- 🔴 High CDOM: River plume, terrestrial discharge, potential pollution

**Light Penetration**:
- CDOM reduces underwater light availability (affects photosynthesis)
- High CDOM + high TSM = severely reduced light penetration
- Important for phytoplankton productivity assessment

---

## Single vs Multi-Tile Processing

### Why Tiles Matter?

Sentinel-2 divides Earth into a global reference grid of **~101,300 tiles** (100 km × 100 km each). Study areas can fall within:

- **Single Tile**: Research area entirely within one S2 tile
- **Multiple Tiles**: Research area spans 2 or more adjacent tiles (requiring mosaic)

### Processing Implications

#### 🟢 Single-Tile Scenarios
```
Typical Study Areas:
- Small lakes (<50 km²)
- Coastal bays and inlets
- Urban water bodies
- Localized monitoring zones

Workflow: C2RCC → CDOM Calculation → Plotting
Benefits:
  ✅ 30-50% faster processing (no mosaic)
  ✅ 30-50% less disk space required
  ✅ Direct output to final products
  ✅ Lower computational overhead
```

#### 🟠 Multi-Tile Scenarios
```
Typical Study Areas:
- Large lakes (>100 km²)
- Entire estuaries
- Archipelagos
- Regional coastal zones
- Global tile-spanning areas

Workflow: C2RCC → Mosaic → CDOM Calculation → Plotting
Benefits:
  ✅ Seamless coverage across tile boundaries
  ✅ Single unified product per date
  ✅ Automatic tile stitching
  ✅ Continuous spatial analysis
```

### Automatic Detection

This toolkit **automatically detects** which scenario applies by:
1. Analyzing C2RCC output filenames
2. Counting tiles per acquisition date
3. Creating mosaic if multiple tiles found
4. Adapting downstream processing accordingly

**Result**: No manual configuration needed - just focus on your science! 🚀

---

## True-Color Visualization

### Purpose

True-color RGB composites provide natural-looking visual assessments and support reporting/publication.

### Band Selection

```
Red Channel:   Band 4 (665 nm) - Chlorophyll absorption
Green Channel: Band 3 (560 nm) - Vegetation/water reflectance
Blue Channel:  Band 2 (490 nm) - Water absorption
```

### Output Format

- **Format**: PNG (lossless)
- **Resolution**: 300 DPI (publication-ready)
- **Location**: `05_final_products/true_color/`
- **Use**: Visual validation, reporting, presentations

### Interpreting True-Color Images

| Color | Interpretation |
|-------|----------------|
| 🔵 **Dark Blue** | Deep, clear water (low TSM, low CDOM) |
| 🟦 **Light Blue** | Shallow or turbid water (high TSM) |
| 🟩 **Green/Brown** | High CDOM, river plume, or algal bloom |
| 🟨 **Yellow/Tan** | Very high TSM, suspended sediment plume |
| ⚪ **White** | Clouds, foam, or extreme turbidity |

---

## Quality Control & Data Validation

### Cloud Cover Filtering

The toolkit automatically excludes scenes with:
- ❌ > 5% cloud cover (configurable)
- ❌ Persistent cloud shadows
- ❌ Cloud-affected coastal zones

### Valid Pixel Filtering

C2RCC outputs quality flags for each pixel based on:
- ✅ Atmospheric correction confidence
- ✅ Water/land discrimination
- ✅ Parameter inversion convergence
- ✅ Physical plausibility ranges

**Default Expression**: `B8 > 0 && B8 < 0.1` (NIR thresholds)

### Physical Range Validation

| Parameter | Min | Max | Default Flags |
|-----------|-----|-----|---------------|
| **Chl-a** | 0.01 | 20.0 mg/m³ | Low SSC alert |
| **TSM** | 0.5 | 50.0 g/m³ | High turbidity |
| **CDOM** | 0.01 | 4.0 m⁻¹ | River plume |

---

## Processing Workflow Summary

```
┌─────────────────────────────────────────────────────────────┐
│         Level-1C TOA Reflectance (12-bit DN)               │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ↓
        ┌──────────────────────────────┐
        │  Step 1: Resample & Subset    │ (10m resolution)
        └──────────────────────────────┘
                       │
                       ↓
        ┌──────────────────────────────┐
        │  Step 2: Reproject to WGS84   │ (EPSG:4326)
        └──────────────────────────────┘
                       │
                       ↓
        ┌──────────────────────────────┐
        │  Step 3: True Color Composite │ (RGB PNG)
        └──────────────────────────────┘
                       │
                       ↓
        ┌──────────────────────────────────────┐
        │  Step 4: C2RCC Atmospheric Correction │
        │          (Per-tile processing)       │
        └──────────────────────────────────────┘
                       │
                ┌──────┴──────┐
                │             │
         Single-Tile    Multi-Tile
              │             │
              │             ↓
              │    ┌──────────────────────┐
              │    │  Step 5: Mosaic      │
              │    │  (Tile Stitching)    │
              │    └──────────────────────┘
              │             │
              └──────┬──────┘
                     ↓
        ┌──────────────────────────────────────┐
        │  Step 6: CDOM Calculation            │
        │  (Adaptive source selection)         │
        └──────────────────────────────────────┘
                     │
                     ↓
        ┌──────────────────────────────────────┐
        │  Step 7: Water Quality Plots         │
        │  (CHL, TSM, CDOM visualization)     │
        └──────────────────────────────────────┘
                     │
                     ↓
        ┌──────────────────────────────────────┐
        │  Publication-Ready Products          │
        │  05_final_products/                  │
        └──────────────────────────────────────┘
```

---

## References & Further Reading

### Key Publications

1. **C2RCC Algorithm**: Brockmann et al. (2016) - Remote Sensing of Environment
2. **Sentinel-2 Mission**: Drusch et al. (2012) - Remote Sensing of Environment
3. **Water Colour Remote Sensing**: Gege et al. (2020) - Optical Remote Sensing of Inland Waters
4. **Coastal Water Quality**: Moore et al. (2009) - Remote Sensing of Environment

### Data Sources

- 🛰️ **Sentinel-2 Data**: https://dataspace.copernicus.eu/
- 📚 **ESA Documentation**: https://sentinel.esa.int/web/sentinel/missions/sentinel-2
- 🔧 **SNAP Software**: https://step.esa.int/main/download/snap-download/

### Related Tools

- **seadas**: Ocean color processing (NASA)
- **ACOLITE**: Atmospheric correction for coastal waters
- **L2gen**: OBDAAC Level-2 processing

---

## Glossary

| Term | Definition |
|------|-----------|
| **TOA** | Top-of-Atmosphere reflectance (L1C product level) |
| **C2RCC** | Case-2 Regional Coast Colour atmospheric correction algorithm |
| **MSI** | Multispectral Instrument aboard Sentinel-2 satellites |
| **CDOM** | Colored Dissolved Organic Matter (chromophoric DOM) |
| **TSM** | Total Suspended Matter (particulate concentration) |
| **Chl-a** | Chlorophyll-a pigment concentration (phytoplankton proxy) |
| **Eutrophication** | Excessive nutrient enrichment and algal growth |
| **Neural Network Inversion** | ML-based retrieval of geophysical parameters from reflectance |
| **Mosaic** | Seamless combination of adjacent satellite tiles |
| **Quality Flag** | Metadata indicating pixel validity and confidence |

---

**Last Updated**: 2026-03-29
**Version**: 1.0
**Contact**: mdrony.golder@uwa.edu.au
