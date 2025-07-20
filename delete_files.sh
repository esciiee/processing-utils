#!/bin/bash

# Script to delete bio*.tif files from Google Earth Engine
# Usage: ./delete_files.sh

echo "Searching for bio*.tif files in users/starters/..."

# Get list of assets matching the pattern
echo "Getting list of assets..."
result=$(earthengine ls users/starters/)
echo $result
assets=$(earthengine ls users/starters/ | grep "bio")

if [ -z "$assets" ]; then
    echo "No bio*.tif files found in users/starters/"
    exit 0
fi

echo "Found the following bio*.tif files:"
echo "$assets"
echo ""

# Ask for confirmation
read -p "Do you want to delete these files? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Operation cancelled."
    exit 0
fi

echo "Deleting files..."

# Delete each file
while IFS= read -r asset; do
    if [ ! -z "$asset" ]; then
        echo "Deleting: $asset"
        earthengine rm --verbose "$asset"
        
        # Check if the command was successful
        if [ $? -eq 0 ]; then
            echo "✓ Successfully deleted: $asset"
        else
            echo "✗ Failed to delete: $asset"
        fi
        echo ""
    fi
done <<< "$assets"

echo "Deletion process completed."
