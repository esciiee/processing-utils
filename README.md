# IPEDClim Yearly Analysis

A processing toolkit for converting .nc files to .tif by year.
Note: Not a generic library.

## System Requirements

### Dependencies
- **libgdal**: GDAL library
- **Python**: 3.8+ with pip
- **Google Cloud SDK**: gcloud utilities for Earth Engine data transfer
- **Earth Engine CLI**: earthengine command-line interface


### Installation
```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install libgdal-dev gdal-bin

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### DataSheet
```bash
# Download the dataset
wget "https://zenodo.org/records/16169255/files/02_IPED_Clim.zip?download=1" -O 02_IPED_Clim.zip
# Extract the data
unzip 02_IPED_Clim.zip
```

## Usage

Before running the transfer scripts, authenticate with both gcloud, earthengine

```bash
# Process yearly data, produces the .tif files
python yealy_analysis.py

# Transfer data to gcloud
./transfer_to_gcloud.sh

# Upload gcloud data to Earth Engine
./transfer_yeraly_data.sh

# Clean up Earth Engine assets
./delete_files.sh
```

## Data Structure

- Input: IPEDClim NetCDF files with bioclimatic variables
- Output: Yearly GeoTIFF files (IPEDClim_YYYY.tif)
- Format: Multi-band rasters containing bio1-bio19 variables

## Requirements

See `requirements.txt` for complete Python dependency list.
