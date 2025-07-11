#!/bin/bash

dim_folder="d:/Sentinel2_WQ/pre-process_reproject/"
output_folder="d:/Sentinel2_WQ/Final-product/True_Color/"
profile="d:/Sentinel2_WQ/SNAP_graphs//rgb_profile_s2.rgb"
output_format="png"

# Create output folder if it doesn't exist
mkdir -p "$output_folder"

for dim_file in "$dim_folder"/Subset_S2_MSIL2A_*.dim; do
    echo "🛰️  Processing $dim_file..."

    # Extract acquisition date from filename (e.g., 20190201)
    filename=$(basename "$dim_file")
    date_part=$(echo "$filename" | grep -oP '\d{8}')

    # Reformat date to desired format: YYYYMMDD
    yyyy=${date_part:0:4}
    mm=${date_part:4:2}
    dd=${date_part:6:2}
    output_name="${yyyy}${mm}${dd}.png"

    # Run pconvert to generate the PNG
    pconvert -f "$output_format" -p "$profile" -o "$output_folder" "$dim_file"

    # Rename the latest PNG to desired format
    latest_file=$(ls -t "$output_folder"/*.png | head -n1)
    mv "$latest_file" "$output_folder/$output_name"
    echo "✅ Saved: $output_name"
done

echo "🎉 All PNG images saved in YYYYMMDD format under $output_folder."
