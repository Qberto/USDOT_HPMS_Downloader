# USDOT_HPMS_Downloader
Repository containing download utilities for the Highway Performance Monitoring System (https://www.fhwa.dot.gov/policyinformation/hpms/fieldmanual/)

This repository contains a jupyter notebook and python file that allows automated download of HPMS shapefiles from the Federal Highway Administration. The output is a zipped File Geodatabase containing a merged national-level HPMS feature class. 

The download process is quick, but the merging operation

# Requirements

The system running this operation must have ArcGIS Desktop or ArcGIS Pro installed, with access to the arcpy library. All additional libraries used come from the Python standard library.

# Executing

Clone or download this repository. You may choose to execute one of the following two files:

HPMS_Downloader_v1.py - Python executable
HPMS_Downloader_v1.ipynb - Jupyter Notebook

Change the following variables to point to your directories:

"workspace" - This location will contain the temporary shapefiles that are downloaded from the FHWA server and the output zipped file geodatabase

(This is found in line 42 of the Python executable, or the second cell of the Jupyter Notebook.)

# Reference

All data is provided by the U.S. Department of Transportation's Federal Highway Administration. 

A manual access point for download of shapefile data is available [HERE] (https://www.fhwa.dot.gov/policyinformation/hpms/shapefiles.cfm)

# Caveats

This is a prototype utility and will be integrated into other USDOT utilities into a Python library. Feedback and questions are welcome, but please consider this product in a testing phase and not production-ready. 

