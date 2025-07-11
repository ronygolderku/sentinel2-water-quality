#!/bin/bash

output_folder="d:/Sentinel2_WQ/pre-process_resample_subset/"
nameStart="Subset_S2_MSIL2A_"
nameEnd=".dim"

for i in "d:\Sentinel2_WQ\dataset"/*.zip
do
    product_basename=$(basename "$i")
    ac_date=$(echo "$product_basename" | cut -d '_' -f 3)
    output_pathname="${output_folder}${nameStart}${ac_date}${nameEnd}"
    gpt "d:/Sentinel2_WQ/SNAP_graphs/resample_subset.xml" -PInput="$i" -POutput="$output_pathname"
done
