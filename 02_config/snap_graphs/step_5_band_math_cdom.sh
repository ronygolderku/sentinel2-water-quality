#!/bin/bash

output_folder="d:/Sentinel2_WQ/process_cdom/"
nameStart="Subset_S2_MSIL2A_"
nameEnd=".nc"

for i in "d:/Sentinel2_WQ/process_c2rcc"/*.nc
do
    product_basename=$(basename "$i")
    ac_date=$(echo "$product_basename" | cut -d '_' -f 4)
    output_pathname="${output_folder}${nameStart}${ac_date}${nameEnd}"
    echo "Processing file: $i"
    echo "Output file will be: $output_pathname"
    gpt "d:/Sentinel2_WQ/SNAP_graphs/cdom_band_math.xml" -PInput="$i" -POutput="$output_pathname"
done