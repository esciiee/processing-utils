#!/usr/bin/env bash
# Ported from https://arbennett.github.io/software,/hydrology/2017/07/30/netcdfToGEE.html
# Uploads some files from google cloud storage to gee
# Usage:
#   ./transfer_to_gee.sh src_bucket dest_asset

result=`earthengine create collection users/$2`

if `test -z "$result"`; then
    echo $result
	exit 1
fi

for geotiff in $(gsutil ls gs://$1/bio*.tif); do
    filename=$(basename "$geotiff")
    asset_id="${filename%.*}"
    earthengine upload image --asset_id=users/$2/$asset_id "$geotiff"
done

