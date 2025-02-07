
Using the scripts and the blenderfile in this repo you should be able to visualise and modify a volumetric layered video in Blender

To do so you must have:
 - A Source volumetric video in grid format where half of the layers images are RGB and the other half is DEPTH+ALPHA
 
 
##Steps to get running

1. Run the ConvertToLayers Script
Making sure to modify the parameters to match where your source footage input and frame outputs are
# Ensure the input folder is provided
$inputFolder = "F:\Projects\BlenderVolumetric\SourceVideo\Clip_1\src"
$outputBaseDir = "F:\Projects\BlenderVolumetric\SourceVideo\Clip_1\Clip_1_Layers"
$frameOutputDir = "$outputBaseDir\frames"


2. Once Layers have been converted into individual folders for each layer per grid slot. Open the Blenderfile

3. Click on the Scripting tab up the top and paste in the 'ImportLayersToBlender.py' script.

4. Make sure that the image path specified at the bottom of the script `base_folder` var is correct for your system