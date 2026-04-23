# Code for "Assessing the Impact of Sea Surface Temperature Biases in CMIP6 Coupled Models on the North Pacific Westerly Jet"

This directory contains the scripts used to generate AGCM boundary data, read CMIP6 and observational datasets, and produce the main and supplementary figures.

## Directory Structure

.
├── boundary/
│   ├── boundary/
│   │   └── woaNxN2amip.py
│   ├── pcmdi2mrigrd.py
│   ├── sst_glb_ano.py
│   ├── sst_msk.py
│   ├── sst_rgn_an
│   └── sstice_linearinterp10.rb
├── cmip/
│   ├── cmip/
│   │   ├── cmip_data.py
│   │   └── cmip_varnames.py
│   └── cmip_mm.py
├── config/
│   ├── config.py
│   └── fig_module.py
├── io_interface/
│   └── io_interface/
│       └── nc_write.py
├── map/
│   └── map_cartopy.py
├── mriagcm3/
│   ├── grid/
│   │   ├── TL159_lat.txt
│   │   └── mriagcm.py
│   └── read_clm.py
├── obs/
│   ├── read_sst_module.py
│   └── read_wind_module.py
├── make_boundary.py
├── plots.py
└── plots_SI.py

## Main Workflow

The basic workflow is:

1. Prepare downloaded observational and CMIP6 datasets under `Data/`
2. Generate AGCM boundary data
3. Generate the main figures
4. Generate the supplementary figures

## Requirements

The code uses the following Python packages:

- numpy
- scipy
- netCDF4
- matplotlib
- cartopy
- cmocean
- seaborn
- pygrib

In addition, the following are used:

- Ruby
- NumRu/GPhys (optional; see below)

## Notes on Ruby / GPhys

`make_boundary.py` first attempts to use the Ruby script:

boundary/sstice_linearinterp10.rb

This script requires:

- Ruby
- NumRu/GPhys

If Ruby or the required Ruby libraries are not available, `make_boundary.py` automatically falls back to a Python implementation (`boundary/pcmdi2mrigrd.py`).

According to the script message, the Python fallback may produce slightly different values.

## Running the Code

### 1. Generate AGCM boundary data

Run:

python make_boundary.py

This script generates AGCM boundary and forcing data under `Data/AGCM/` using:

- observational SST data
- CMIP6-based SST bias data

It also generates:

- SST data interpolated onto the MRI-AGCM3.5 grid
- SST mask data

### 2. Generate the main figures

Run:

python plots.py

This script generates the main figures used in the paper.

### 3. Generate the supplementary figures

Run:

python plots_SI.py

This script generates the supplementary figures.

## Output

Figure output directories are controlled by:

config/config.py

By default, figures are written under a directory such as:

fig/20260423/ORG/

The output path is determined by the function `figdir()` in `config/config.py`.

## File Descriptions

### Top-level scripts

- `make_boundary.py`  
  Main preprocessing script for AGCM boundary generation.  
  It creates AGCM SST forcing data, regional SST anomaly forcing, and SST mask data.

- `plots.py`  
  Main plotting script for the manuscript figures.

- `plots_SI.py`  
  Plotting script for supplementary figures.

---

### boundary/

Scripts for generating SST boundary conditions and anomaly forcing for AGCM sensitivity experiments.

- `boundary/pcmdi2mrigrd.py`  
  Converts input4MIPs SST data to the MRI-AGCM3.5 model grid.

- `boundary/sst_glb_ano.py`  
  Generates the global annual-mean SST bias forcing used for the GLB experiment.

- `boundary/sst_rgn_ano.py`  
  Generates regionally masked SST anomaly forcing for PAC, GLB-PAC, WNP, EQ, and ENP experiments.

- `boundary/sst_msk.py`  
  Generates an SST/ocean mask file for the AGCM grid.

- `boundary/sstice_linearinterp10.rb`  
  Ruby script for interpolation of SST/sea-ice forcing data.  
  Used when Ruby + NumRu/GPhys are available.

- `boundary/boundary/woaNxN2amip.py`  
  Utility for horizontal remapping to the AGCM grid.

---

### cmip/

Scripts for reading, averaging, and processing CMIP6 data.

- `cmip/cmip_mm.py`  
  Main CMIP6 processing module.  
  Includes functions for:
  - reading multi-model SST
  - reading zonal wind and related variables
  - computing multi-model means
  - estimating jet latitude
  - generating climatological diagnostics

- `cmip/cmip/cmip_data.py`  
  Low-level file/path handling and data readers for CMIP6 NetCDF files.

- `cmip/cmip/cmip_varnames.py`  
  Variable-name utilities.

---

### config/

Configuration and plotting setup.

- `config/config.py`  
  Defines the base data directory and figure output directory.

- `config/fig_module.py`  
  Figure-generation utilities used by `plots.py` and `plots_SI.py`.

---

### io_interface/

Utilities for writing NetCDF output.

- `io_interface/io_interface/nc_write.py`  
  Functions for writing 1D, 3D, and 4D NetCDF files.

---

### map/

Plotting helpers based on cartopy.

- `map/map_cartopy.py`  
  Utilities for map projection setup, contours, and shading.

---

### mriagcm3/

MRI-AGCM3 grid and model-output readers.

- `mriagcm3/read_clm.py`  
  Reads climatological AGCM output stored under `Data/TSE-C/`.

- `mriagcm3/grid/mriagcm.py`  
  Grid utilities for MRI-AGCM3.

- `mriagcm3/grid/TL159_lat.txt`  
  Latitude definition for the TL159 model grid.

---

### obs/

Readers for observational datasets.

- `obs/read_sst_module.py`  
  Reads input4MIPs SST data and MRI-AGCM-formatted SST files.

- `obs/read_wind_module.py`  
  Reads JRA-55 zonal wind data from GRIB files and optionally stores climatologies in NetCDF format.

## Reproducibility Notes

- The scripts assume the directory structure described in `Data/README.md`
- External datasets must be downloaded and placed in the correct paths before running the scripts
- Some intermediate datasets are generated automatically during execution
- The code uses local path assumptions defined in `config/config.py`

## Recommended Order

1. Prepare `Data/obs/` and `Data/CMIP/`
2. Run `make_boundary.py`
3. Run `plots.py`
4. Run `plots_SI.py`
