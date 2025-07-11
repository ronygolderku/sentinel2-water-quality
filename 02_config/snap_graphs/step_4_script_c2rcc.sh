#!/bin/bash

output_folder="d:/Sentinel2_WQ/process_c2rcc/"
paramFile="d:/Sentinel2_WQ/SNAP_graphs/c2rcc_param.xml"
oldEnd=".dim"
newEnd="_C2RCC.nc"

for i in d:/Sentinel2_WQ/pre-process_reproject/*.dim
do
    name=$(basename "$i")
    output_file="${output_folder}${name/$oldEnd/$newEnd}"
    
    echo "Processing file: $i"
    echo "Output file will be: $output_file"
    
    #gpt c2rcc.msi -SsourceProduct="$i" -p "$paramFile" -t "$output_file"
    gpt c2rcc.msi -SsourceProduct="$i" -p "$paramFile" -t "$output_file" -f NetCDF4-BEAM
done