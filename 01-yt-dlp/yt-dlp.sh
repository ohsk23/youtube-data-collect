#!/bin/bash

# Create data directory with today's date
DATE=$(date +%Y%m%d)
DATA_DIR="./data/$DATE/json"
mkdir -p "$DATA_DIR"

# Read channels.txt and process each channel
while IFS=$'\t' read -r url title || [ -n "$url" ]; do
    # Skip empty lines
    [ -z "$url" ] && continue
    
    # Replace spaces with underscores in the filename
    filename=$(echo "$title" | tr ' ' '_')
    
    yt-dlp --ignore-errors --flat-playlist -J "$url" > "$DATA_DIR/${filename}.json" &
done < ./01-yt-dlp/channels.txt

# Wait for all background processes to complete
wait 