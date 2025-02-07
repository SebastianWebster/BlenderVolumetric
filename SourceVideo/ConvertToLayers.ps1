# PowerShell script to process a 4x4 image matrix video and organize output into folders

# Ensure the input folder is provided
$inputFolder = "F:\Projects\ShadyMultCam\Jglads\MultiLayerFootage\Clip_5\src"
$outputBaseDir = "F:\Projects\ShadyMultCam\Jglads\MultiLayerFootage\Clip_5\Clip_4_Layers\out"
$frameOutputDir = "$outputBaseDir\frames"

# Dimensions for each individual image
$width = 1920  # Individual image width (7680 / 4)
$height = 1072 # Individual image height (4288 / 4)

# Create output directories if they don't exist
if (!(Test-Path -Path $outputBaseDir)) {
    New-Item -ItemType Directory -Path $outputBaseDir
}
if (!(Test-Path -Path $frameOutputDir)) {
    New-Item -ItemType Directory -Path $frameOutputDir
}

# Process each video file in the input folder
Get-ChildItem -Path $inputFolder -Filter "*.mp4" | ForEach-Object {
    $inputVideo = $_.FullName
    $videoBaseName = $_.BaseName

    # Extract frames from the video if not already done
    $existingFrames = Get-ChildItem -Path $frameOutputDir -Filter "$($videoBaseName)_frame_*.png" -ErrorAction SilentlyContinue
    if (!$existingFrames) {
        ffmpeg -i $inputVideo -q:v 2 "$frameOutputDir\$($videoBaseName)_frame_%04d.png"
    } else {
        Write-Host "Frames for $videoBaseName already exist. Skipping frame extraction."
    }

    # Process each extracted frame
    Get-ChildItem -Path $frameOutputDir -Filter "$($videoBaseName)_frame_*.png" | ForEach-Object {
        $framePath = $_.FullName
        $frameBaseName = $_.BaseName

        # Loop through the 4x4 grid
        for ($row = 0; $row -lt 4; $row++) {
            for ($col = 0; $col -lt 4; $col++) {
                # Calculate the layer index
                $index = ($row * 4) + $col

                # Calculate the crop position
                $x = $col * $width
                $y = $row * $height

                # Determine output folder
                if ($row -lt 2) {
                    $folder = "$outputBaseDir\Layer_$index"
                } else {
                    $depthIndex = $index - 8
                    $folder = "$outputBaseDir\LayerDepth_$depthIndex"
                }

                # Create the folder if it doesn't exist
                if (!(Test-Path -Path $folder)) {
                    New-Item -ItemType Directory -Path $folder
                }

                # Define output file path
                $outputFile = "$folder\_$index_$($frameBaseName).png"

                # Skip cropping if output file already exists
                if (!(Test-Path -Path $outputFile)) {
                    ffmpeg -i $framePath -vf "crop=$($width):$($height):$($x):$($y)" -q:v 2 $outputFile
                } else {
                    Write-Host "File $outputFile already exists. Skipping."
                }
            }
        }
    }

    # Optionally delete the frames after processing
    # Remove-Item -Path "$frameOutputDir\*.png" -Force
}

# Cleanup temporary frames directory (uncomment if desired)
# Remove-Item -Path $frameOutputDir -Recurse -Force

Write-Host "Processing complete."
