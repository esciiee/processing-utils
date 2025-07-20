#!/usr/bin/env bash
# Ported from https://arbennett.github.io/software,/hydrology/2017/07/30/netcdfToGEE.html
bucket_path=$1
if [[ $bucket_path != gs://* ]]; then
    bucket_path="gs://$bucket_path"
fi

# Create collection
result=$(earthengine create collection users/$2)
echo $result
if test -z "$result"; then
    echo "$result"
    exit 1
fi
echo "Collection created"
# Loop through tif files
echo "bucket_path: $bucket_path"
for geotiff in $(gsutil ls gs://$1/*.tif); do
    echo $geotiff
    filename=$(basename "$geotiff")
    asset_id="${filename%.*}"
    earthengine upload image --asset_id=users/$2/$asset_id "$geotiff"
done


