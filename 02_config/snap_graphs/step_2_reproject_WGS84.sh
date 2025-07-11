#!/bin/bash
input_folder="d:/Sentinel2_WQ/pre-process_resample_subset/"
output_folder="d:/Sentinel2_WQ/pre-process_reproject/"
paramFile="d:/Sentinel2_WQ/SNAP_graphs/reproject.xml"

oldEnd=".dim"
newEnd="_reprojected.dim"

for i in "$input_folder"*.dim
do
    name=$(basename "$i")
    output_file="${output_folder}${name/$oldEnd/$newEnd}"

    echo "Processing file: $i"
    echo "Output file will be: $output_file"

    gpt Reproject -SsourceProduct="$i" -p "$paramFile" -t "$output_file"
done