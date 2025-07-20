# Processing .nc to .tif

A processing toolkit for converting .nc files to .tif by year.
Note: Not a generic library.

# Algorithm

The `yealy_analysis.py` script performs temporal data reorganization of IPEDClim variables. It reads 19 individual NetCDF files (IPEDClim_BIO01.nc through IPEDClim_BIO19.nc), each containing multi-year time series for a specific variable (bio1-bio19). The algorithm pivots this variable-centric structure into year-centric multi-band GeoTIFF files, where each output file (IPEDClim_YYYY.tif) contains all 19 variables as separate bands for a single year(This is one Image). The collection of images all such years is used to create the ImageCollection.

## Input and Output

### Input Structure
- **Format**: 19 individual NetCDF files (`IPEDClim_BIO{i}.nc` where i = 1 to 19)
- For each file
    **Dimensions**: 
        - `year`: 29 (1991-2019)
        - `lat`: 304 (6.8° to 37.1°N)
        - `lon`: 293 (68.2° to 97.4°E)
    - **Resolution**: 0.1° × 0.1° (dx=0.1, dy=0.1)
    - **Data Variables**: Each file contains one bioclimatic variable (bio1, bio2, ..., bio19)
    - **Data Type**: float32 with temporal, spatial coordinates

### Output Structure
- **Format**: 29 multi-band GeoTIFF files (`IPEDClim_YYYY.tif` where YYYY = 1991 to 2019)
- **Bands**: 19 bands per file (bio1-bio19 as separate bands)
- **Projection**: WGS84 (EPSG:4326)
- **Compression**: DEFLATE with tiling for optimal storage
- **Google Earth Engine Ready**: Each yearly GeoTIFF can be uploaded as an **Image** asset, and the collection of all years forms an **ImageCollection** for temporal analysis



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
