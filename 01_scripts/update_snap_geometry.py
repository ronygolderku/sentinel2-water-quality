"""
Utility to update SNAP XML graph files with geometry from parameters.yaml

This script reads the WKT study area geometry from parameters.yaml
and automatically updates all relevant SNAP XML graph files with the
correct geographic region. This ensures all processing uses consistent
study area boundaries.
"""

import re
import yaml
from pathlib import Path
from xml.dom import minidom


def extract_coordinates_from_wkt(wkt_geometry):
    """Extract coordinates from WKT POLYGON geometry.

    Args:
        wkt_geometry: WKT POLYGON string

    Returns:
        List of (lon, lat) tuples
    """
    # Extract coordinates from POLYGON ((lon1 lat1, lon2 lat2, ...))
    match = re.search(r'POLYGON\s*\(\s*\((.*?)\)', wkt_geometry)
    if not match:
        raise ValueError(f"Invalid WKT format: {wkt_geometry}")

    coords_str = match.group(1)
    coordinates = []

    for coord in coords_str.split(','):
        coord = coord.strip()
        parts = coord.split()
        if len(parts) >= 2:
            lon, lat = float(parts[0]), float(parts[1])
            coordinates.append((lon, lat))

    return coordinates


def get_bounding_box_from_coords(coordinates):
    """Calculate bounding box from coordinates.

    Args:
        coordinates: List of (lon, lat) tuples

    Returns:
        dict with west, east, north, south bounds
    """
    lons = [coord[0] for coord in coordinates]
    lats = [coord[1] for coord in coordinates]

    return {
        'west': min(lons),
        'east': max(lons),
        'north': max(lats),
        'south': min(lats)
    }


def coords_to_wkt_polygon(coordinates):
    """Convert coordinates to WKT POLYGON string.

    Args:
        coordinates: List of (lon, lat) tuples

    Returns:
        WKT POLYGON string
    """
    coords_str = ', '.join([f"{lon} {lat}" for lon, lat in coordinates])
    return f"POLYGON (({coords_str}))"


def update_resample_subset_xml(xml_path, wkt_geometry):
    """Update resample_subset.xml with new geoRegion.

    Args:
        xml_path: Path to resample_subset.xml
        wkt_geometry: WKT POLYGON string
    """
    with open(xml_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace geoRegion value
    pattern = r'<geoRegion>POLYGON\s*\(\s*\([^)]*\)\s*\)</geoRegion>'
    replacement = f'<geoRegion>{wkt_geometry}</geoRegion>'

    content = re.sub(pattern, replacement, content)

    with open(xml_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Updated {xml_path.name} with new geometry")


def update_cdom_xml(xml_path, bounds):
    """Update CDOM XML with new geographic bounds.

    Args:
        xml_path: Path to CDOM XML file
        bounds: dict with west, east, north, south bounds
    """
    with open(xml_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update bounds if they exist
    if '<westBound>' in content:
        content = re.sub(
            r'<westBound>[^<]*</westBound>',
            f'<westBound>{bounds["west"]}</westBound>',
            content
        )
    if '<eastBound>' in content:
        content = re.sub(
            r'<eastBound>[^<]*</eastBound>',
            f'<eastBound>{bounds["east"]}</eastBound>',
            content
        )
    if '<northBound>' in content:
        content = re.sub(
            r'<northBound>[^<]*</northBound>',
            f'<northBound>{bounds["north"]}</northBound>',
            content
        )
    if '<southBound>' in content:
        content = re.sub(
            r'<southBound>[^<]*</southBound>',
            f'<southBound>{bounds["south"]}</southBound>',
            content
        )

    with open(xml_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Updated {xml_path.name} with bounding box:")
    print(f"  West: {bounds['west']}, East: {bounds['east']}")
    print(f"  North: {bounds['north']}, South: {bounds['south']}")


def update_all_snap_geometries(config_file):
    """Update all SNAP XML files with geometry from parameters.yaml.

    Args:
        config_file: Path to parameters.yaml

    Returns:
        bool: True if successful
    """
    config_path = Path(config_file)

    if not config_path.exists():
        print(f"✗ Configuration file not found: {config_path}")
        return False

    # Read configuration
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"✗ Error reading configuration: {e}")
        return False

    # Extract WKT geometry
    try:
        wkt_geometry = config['study_area']['wkt_geometry']
        print(f"Study Area WKT: {wkt_geometry[:50]}...")
    except KeyError:
        print("✗ study_area.wkt_geometry not found in configuration")
        return False

    # Extract coordinates and bounds
    try:
        coordinates = extract_coordinates_from_wkt(wkt_geometry)
        bounds = get_bounding_box_from_coords(coordinates)
        print(f"\n✓ Extracted bounds:")
        print(f"  Latitude:  {bounds['south']:.6f} to {bounds['north']:.6f}")
        print(f"  Longitude: {bounds['west']:.6f} to {bounds['east']:.6f}\n")
    except Exception as e:
        print(f"✗ Error extracting coordinates: {e}")
        return False

    # Find SNAP graphs directory
    snap_graphs_dir = config_path.parent / "snap_graphs"
    if not snap_graphs_dir.exists():
        print(f"✗ SNAP graphs directory not found: {snap_graphs_dir}")
        return False

    # Update resample_subset.xml
    resample_file = snap_graphs_dir / "resample_subset.xml"
    if resample_file.exists():
        try:
            update_resample_subset_xml(resample_file, wkt_geometry)
        except Exception as e:
            print(f"✗ Error updating {resample_file.name}: {e}")
            return False
    else:
        print(f"⚠ {resample_file.name} not found")

    # Update mosaic.xml with bounds
    mosaic_file = snap_graphs_dir / "mosaic.xml"
    if mosaic_file.exists():
        try:
            # Check if file has bounds to update
            with open(mosaic_file, 'r') as f:
                content = f.read()
                if '<westBound>' in content:
                    update_cdom_xml(mosaic_file, bounds)
                    print(f"✓ Updated {mosaic_file.name} with new bounds")
                else:
                    print(f"ℹ {mosaic_file.name} has no bounds to update")
        except Exception as e:
            print(f"✗ Error updating {mosaic_file.name}: {e}")

    # Update CDOM XML if it has bounds
    cdom_file = snap_graphs_dir / "cdom_band_math.xml"
    if cdom_file.exists():
        try:
            # Check if file has bounds to update
            with open(cdom_file, 'r') as f:
                content = f.read()
                if '<westBound>' in content or '<southBound>' in content:
                    update_cdom_xml(cdom_file, bounds)
                else:
                    print(f"ℹ {cdom_file.name} has no bounds to update")
        except Exception as e:
            print(f"✗ Error updating {cdom_file.name}: {e}")

    print("\n✓ All SNAP geometry files updated successfully!")
    return True


def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Update SNAP XML graph files with study area geometry'
    )
    parser.add_argument(
        '--config',
        required=True,
        help='Path to parameters.yaml configuration file'
    )

    args = parser.parse_args()

    success = update_all_snap_geometries(args.config)
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
