# Blender Volumetric Video
Using the scripts and the blenderfile in this repo you should be able to visualise and modify a volumetric layered video in Blender

To do so you must have:
 - A Source volumetric video in grid format where half of the layers images are RGB and the other half is DEPTH+ALPHA

The ImportLayersToBlender script will:
  - Create planes and apply the image sequence of each respective layer to the plane
  - Scale, subdivide and vertically offset each plane by specified parameters
  - Using an existing materialnode setup the materials for each layer (Makes it easier to modify display of all layers at once)
 
## Steps to get running

1. Run the ConvertToLayersScript.ps1
Making sure to modify the parameters to match where your source footage input and frame outputs are
Ensure the input folder is provided
```
$inputFolder = "F:\Projects\BlenderVolumetric\SourceVideo\Clip_1\src"  
$outputBaseDir = "F:\Projects\BlenderVolumetric\SourceVideo\Clip_1\Clip_1_Layers"  
$frameOutputDir = "$outputBaseDir\frames"  
```

3. Once Layers have been converted into individual folders for each layer per grid slot. Open the Blenderfile

4. Click on the Scripting tab up the top and paste in the 'ImportLayersToBlender.py' script.

5. Make sure that the image path specified at the bottom of the script `base_folder` var is correct for your system

6.Running the script should result in a similar setup to the image below 
![image](https://github.com/user-attachments/assets/d657766a-6861-4abd-90ad-665b69fe46e6)

7. Now try messing with the layers, I found that just using a SimpleDeform Modifier on all layers at once and using a object coordinate to drive the deform produced pretty interesting results
The Material Node Group can also be modified and animated to change the depth amount of each layer or alpha channel weighting + whatever else you want to add to it
