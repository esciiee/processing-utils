#!/usr/bin/env bash
# Ported from https://arbennett.github.io/software,/hydrology/2017/07/30/netcdfToGEE.html
# Uploads some files to google cloud storage
#
# -----------------------------------------
# WARNING: This will make everything in the
#           output bucket public!!!
# -----------------------------------------
#
# Usage:
#   ./transfer_to_gcs.sh src_dir dest_bucket

gsutil cp $1/* gs://$2
gsutil -m acl set -R -a public-read gs://$2
