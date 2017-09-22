# Import needed modules
import us
import arcpy
import os
import requests
import zipfile
import io
import datetime

# Set general variables
workspace = r"C:\Users\albe9057\Documents\ANieto_SolutionEngineering\Projects\DOT\FHWA\HPMS_Download\Work"
outputs_dir = r"C:\Users\albe9057\Documents\ANieto_SolutionEngineering\Projects\DOT\FHWA\HPMS_Download\Outputs"

states_list = [state.name.lower().replace(" ", "") for state in us.states.STATES]
states_list

# Create a state data crosswalk dictionary
state_crosswalk_dict = {
    "districtofcolumbia": 'district'
}

# Perform state corrections for download urls
for state in state_crosswalk_dict:
    if state in states_list:
        states_list.remove(state)
        states_list.append(state_crosswalk_dict[state])

# Get the baseline part of the download url
baseline_download_url = r"https://www.fhwa.dot.gov/policyinformation/hpms/shapefiles/"
year = "2015"

# Create a list of download URLs
download_urls = ["{0}/{1}{2}.zip".format(baseline_download_url, state, year) for state in states_list]
download_urls   

# Create the workspace file geodatabase
workspace_gdb = arcpy.CreateFileGDB_management(workspace, "hpms_workspace").getOutput(0)

# Download iteration loop
for download_url in download_urls:
    state_name = download_url.split("//")[-1].split(".")[0]
    print("Downloading {0}...".format(state_name))
    response = requests.get(download_url)
    zipDocument = zipfile.ZipFile(io.BytesIO(response.content))
    shapefile_folder = os.makedirs(os.path.join(workspace, state_name))
    zipDocument.extractall(path=shapefile_folder)

