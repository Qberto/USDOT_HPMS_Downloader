
# coding: utf-8

# ### Pseudocode
# 
# Goal: Scripted process to download HPMS shapefiles from FHWA website, compile into a single feature class, and provide output as a single zipped file geodatabase. A second goal is to publish this data as a service using the ArcGIS API for Python.
# 
# ### Process
# 
# 1. Create list of download urls
# 
# 2. Iterate on the list, download zip, and execute main zip->shapefile->feature class conversion loop
# 
# 3. Merge all feature classes into a single feature class for nation-wide HPMS
# 
# 4. Provide output as zipped file geodatabase. 
# 
# 
# ### Dependencies
# 
# - 'us' module. To install, run "pip install us"
# - 'arcpy' module

# In[ ]:


# Import needed modules
import us
import arcpy
import os
import requests
import zipfile
import shutil
import io
import datetime


# In[6]:


# Set general variables
workspace = r"C:\Users\albe9057\Documents\ANieto_SolutionEngineering\Projects\DOT\FHWA\HPMS_Download\Work"


# ### 1. Create list of download urls

# In[7]:


states_list = [state.name.lower().replace(" ", "") for state in us.states.STATES]
states_list


# In[11]:


# Create a state data crosswalk dictionary
state_crosswalk_dict = {
    "districtofcolumbia": 'district'
}


# In[22]:


# Create a URL crosswalk dictionary
url_crosswalk_dict = {
    'https://www.fhwa.dot.gov/policyinformation/hpms/shapefiles//missouri2015.zip': 'https://www.fhwa.dot.gov/policyinformation/hpms/shapefiles//missouri2015t.zip'
}


# In[36]:


# Create a shapefile name crosswalk dictionary
shapefile_crosswalk_dict = {
    "Missouri_Sections.shp": "Missouri_Sectionst.shp"
}


# In[13]:


# Perform state corrections for download urls
for state in state_crosswalk_dict:
    if state in states_list:
        states_list.remove(state)
        states_list.append(state_crosswalk_dict[state])


# Download Access URL: https://www.fhwa.dot.gov/policyinformation/hpms/shapefiles.cfm

# In[14]:


# Get the baseline part of the download url
baseline_download_url = r"https://www.fhwa.dot.gov/policyinformation/hpms/shapefiles/"
year = "2015"


# In[24]:


# Create a list of download URLs, checking against the URL crosswalk to make sure we account for exceptions
download_urls = []
for state in states_list:
    if "{0}/{1}{2}.zip".format(baseline_download_url, state, year) not in url_crosswalk_dict:
        download_urls.append("{0}/{1}{2}.zip".format(baseline_download_url, state, year))
    else:
        download_urls.append(url_crosswalk_dict["{0}/{1}{2}.zip".format(baseline_download_url, state, year)])
download_urls        


# In[25]:


# Create a list of download URLs
# download_urls = ["{0}/{1}{2}.zip".format(baseline_download_url, state, year) for state in states_list]
# download_urls   


# ### 2. Iterate on states to download and convert

# In[33]:


# Create the workspace file geodatabase
workspace_gdb = arcpy.CreateFileGDB_management(workspace, "hpms_workspace").getOutput(0) if not arcpy.Exists(os.path.join(workspace, "hpms_workspace.gdb")) else os.path.join(workspace, "hpms_workspace.gdb")
workspace_gdb


# In[66]:


# Create containers for shapefile paths and folder paths for the merge operation after the loop
shapefiles_list = []
folders_list = []

# Download iteration loop
for download_url in download_urls:   
    
    # Get the state+year string by slicing the download URL
    stateyear_name = download_url.split("//")[-1].split(".")[0]
    shapefile_folder = os.path.join(workspace, stateyear_name)
    
    # Handle the "lovely" Missouri naming exception
    shapefile_name_string = "_Sectionst.shp" if stateyear_name == "missouri2015t" else "_Sections.shp"

    # Establish the shapefile path
    shapefile_path = os.path.join(shapefile_folder, "{0}{1}".format(stateyear_name.split("2")[0].capitalize(), shapefile_name_string))
    
    # Determine if the shapefile already exists, and skip the download if that's the case
    if os.path.exists(shapefile_path):
        print("Shapefile for {0} already exists. Skipping...".format(stateyear_name))
        shapefiles_list.append(shapefile_path)
        continue
    
    # Send a request to the url, download the shapefile, and unzip to the work folder for the state
    print("Downloading {0}...".format(stateyear_name))
    response = requests.get(download_url)
    # Unzip our request content to a specified folder (making it along the way)
    zipDocument = zipfile.ZipFile(io.BytesIO(response.content))
    os.makedirs(shapefile_folder)
    os.chdir(shapefile_folder)
    zipDocument.extractall(path=shapefile_folder)
    # Append the shapefile path to the shapefiles_list variable
    shapefiles_list.append(shapefile_path)


# In[67]:


# Create a log file containing output information
## Pending


# In[68]:


# QC shapefiles for valid geometry and shape type before merging. Remove any shapefiles without Polyline shape types.
print("Pre-QC shapefile count: {0}".format(len(shapefiles_list)))
for shapefile in shapefiles_list:
    desc = arcpy.Describe(shapefile)
    if desc.shapeType != "Polyline":
        print(shapefile, desc.shapeType)
        shapefiles_list.remove(shapefile)
print("Post-QC shapefile count: {0}".format(len(shapefiles_list)))


# In[ ]:


# Perform an arcpy merge using the shapefiles list from the iteration above
output_fc_path = os.path.join(workspace_gdb, "HPMS_National_{0}".format(year))
output_hpms_fc = arcpy.Merge_management(inputs=shapefiles_list, output=output_fc_path).getOutput(0)
output_hpms_fc


# In[ ]:


# Zip up the HPMS file geodatabase and provide as an output
out_zipped_fgdb = os.path.join(workspace, "HPMS_National_{0}.zip".format(year))
shutil.make_archive(out_zipped_fgdb, "zip", workspace_gdb)

