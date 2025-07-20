import os
import sys
from osgeo import gdal, osr
import xarray as xr
import numpy as np
import glob

def main():
    """
    Convert IPEDClim NetCDF files to yearly multi-variable GeoTIFFs.
    Each GeoTIFF contains all bio variables (bio1-bio19) for one year.
    """
    input_dir = "./02_IPED_Clim"
    output_dir = "./02_IPED_Clim_yearly"
    
    # Create output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    elif os.path.isfile(output_dir):
        exit("Output path exists and is a regular file!")
    
    # Get all NetCDF files
    nc_files = glob.glob(os.path.join(input_dir, "IPEDClim_BIO*.nc"))
    nc_files.sort()
    
    print(f"Found {len(nc_files)} NetCDF files")
    
    # Load all datasets
    datasets = {}
    years = None
    geospatial_info = None
    
    for nc_file in nc_files:
        filename = os.path.basename(nc_file)
        bio_num = filename.split('_')[1].replace('BIO', '').lstrip('0').split('.')[0]
        varname = f"bio{bio_num}"
        
        print(f"Loading {varname} from {filename}")
        
        ds = xr.open_dataset(nc_file)
        ds = ds.sortby('lat', ascending=False)
        
        if varname in ds.data_vars:
            datasets[varname] = ds[varname]
            
            # Get years and geospatial info from first file
            if years is None:
                years = ds['year'].values
                lat = ds['lat'].values
                lon = ds['lon'].values
                geospatial_info = get_netcdf_info_from_coords(lat, lon)
                print(f"Years: {years.min()}-{years.max()} ({len(years)} years)")
    
    # Create one GeoTIFF per year with all bio variables
    ndv, geot, proj = geospatial_info
    
    for i, year in enumerate(years):
        print(f"\nProcessing year {int(year)}")
        
        # Collect all bio variables for this year
        year_data = {}
        for varname, data_var in datasets.items():
            year_data[varname] = data_var.isel(year=i).values
        
        # Create multi-variable GeoTIFF
        outfile = os.path.join(output_dir, f"IPEDClim_{int(year)}.tif")
        create_multivariable_geotiff(outfile, year_data, ndv, geot, proj)

def create_multivariable_geotiff(filename, var_data_dict, ndv, geot, proj):
    """
    Create multi-band GeoTIFF with all bio variables for one year.
    """
    # Sort variables by bio number for consistent band order
    sorted_vars = sorted(var_data_dict.keys(), key=lambda x: int(x.replace('bio', '')))
    n_bands = len(sorted_vars)
    
    # Get dimensions from first variable
    first_data = var_data_dict[sorted_vars[0]]
    ysize, xsize = first_data.shape
    
    print(f"  Creating {filename} with {n_bands} bands")
    
    # Create GeoTIFF
    driver = gdal.GetDriverByName('GTiff')
    ds = driver.Create(filename, xsize, ysize, n_bands, gdal.GDT_Float32,
                      ['COMPRESS=DEFLATE', 'PREDICTOR=2', 'TILED=YES'])
    
    # Set georeference
    ds.SetGeoTransform(geot)
    ds.SetProjection(proj.ExportToWkt())
    
    # Write each bio variable as a band
    for i, varname in enumerate(sorted_vars, 1):
        data = var_data_dict[varname]
        data = np.where(np.isnan(data), ndv, data)
        
        band = ds.GetRasterBand(i)
        band.WriteArray(data)
        band.SetNoDataValue(ndv)
        band.SetDescription(varname)
        
        print(f"    Band {i}: {varname}")
    
    ds.FlushCache()
    ds = None
    print(f"  Created: {os.path.basename(filename)}")

def get_netcdf_info_from_coords(lat, lon):
    """Create geotransform and projection from coordinates."""
    # Sort coordinates
    lat_sorted = np.sort(lat)[::-1]  # Descending
    lon_sorted = np.sort(lon)        # Ascending
    
    # Calculate pixel sizes
    pixel_width = (lon_sorted.max() - lon_sorted.min()) / (len(lon) - 1) if len(lon) > 1 else 0.1
    pixel_height = (lat_sorted.max() - lat_sorted.min()) / (len(lat) - 1) if len(lat) > 1 else 0.1
    
    # Top-left corner
    top_left_x = lon_sorted.min() - pixel_width/2
    top_left_y = lat_sorted.max() + pixel_height/2
    
    geot = (top_left_x, pixel_width, 0, top_left_y, 0, -pixel_height)
    
    # WGS84 projection
    proj = osr.SpatialReference()
    proj.ImportFromEPSG(4326)
    
    ndv = -9999.0
    return ndv, geot, proj

def list_output_files():
    """List created files for reference."""
    output_dir = "./02_IPED_Clim_yearly"
    if os.path.exists(output_dir):
        files = sorted([f for f in os.listdir(output_dir) if f.endswith('.tif')])
        print(f"\nCreated {len(files)} yearly GeoTIFF files:")
        for f in files:
            print(f"  {f}")
        print("\nUpload these files to Google Earth Engine as Image assets.")
    else:
        print("No output directory found.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        list_output_files()
    else:
        main()
        list_output_files()