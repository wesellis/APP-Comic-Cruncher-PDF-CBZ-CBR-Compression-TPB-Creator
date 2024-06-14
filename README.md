### CBR to CBZ Converter PowerShell Script

This PowerShell script automates the conversion of Comic Book Archive (CBR) files to Comic Book Zip (CBZ) files. It also includes an option to convert JPEG images to WebP format.

#### Requirements

Before using this script, ensure you have the following:

1. **7-Zip**: Required for extracting and compressing archive files.
   - Download and install from [7-Zip.org](https://www.7-zip.org/).
   - Ensure `7z.exe` is added to your system's PATH environment variable.

2. **nConvert (Optional for WebP Conversion)**: Required if converting JPEG images to WebP format.
   - Download nConvert from [XnView.com](https://www.xnview.com/en/nconvert/).
   - Place `nconvert.exe` in your system's PATH.
   - `libwebp.dll` should be in the "Plugins" subfolder of the nConvert installation directory. Download from [XnView.com](https://www.xnview.com/en/xnconvert/).

3. **PowerShell Version**: Ensure you have PowerShell 7.1 or later installed for optimal performance, especially when using the `-Parallel` feature.

#### Setup Instructions

Follow these steps to set up and use the script:

1. **Clone or Download Repository**:
   - Clone or download the repository from [CBR-to-CBZ-Converter](https://github.com/wesellis/CBR-to-CBZ-Converter).

2. **Ensure Dependencies**:
   - Install and configure 7-Zip and nConvert as per the requirements above.

3. **Script Execution**:
   - Open PowerShell and navigate to the directory containing `ConverterPS.ps1`.

4. **Run the Script**:
   - Execute the script by running `.\ConverterPS.ps1`.
   - Follow on-screen prompts:
     - Press 'y' followed by ENTER to convert JPEGs to WebP (optional).

5. **Conversion Process**:
   - The script will:
     - Convert all `.cbr` files in the current directory to `.cbz`.
     - Optionally convert JPEG images to WebP format if selected.
     - Utilize parallel processing for faster conversions (requires PowerShell 7.1+).

6. **Cleanup**:
   - Temporary files are managed automatically by the script in the directory `C:\Temp\Convert-temp`. Ensure this directory exists and is writable.

#### Script Overview

```powershell
# Place the full contents of your PowerShell script here
# Replace the script with actual content
# For example:
# Clear host
Clear-Host

# Print info to console
Write-Host "This script will convert all .cbr files in the current directory to .cbz"
Write-Host "Converting jpg to webp (for both .cbr and .cbz) is included interactively as an option.`n"
Write-Host "NOTE 1: 7-Zip is required and the executable (7z.exe) needs to be in the windows PATH variable for this to work. `nhttps://www.7-zip.org/`n"
Write-Host "NOTE 2 (WebP only): nConvert is required for conversion to webp and the executable (nconvert.exe) needs to be in the windows PATH variable for this to work. `nhttps://www.xnview.com/en/nconvert/`n"
Write-Host "NOTE 3 (WebP only): nConvert needs 'libwebp.dll' to be located in 'Plugins' subfolder. This file is included in (for example) XnConvert`nhttps://www.xnview.com/en/xnconvert/`n"
Write-Host "Note 4 (WebP only): To speed up conversion from jpeg to webp the script is using the 'ForEach-Object -Parallel' method. `nFor this reason a recent version of PowerShell is needed. Script written with version 7.1 `nhttps://microsoft.com/PowerShell"

# Ask user if jpeg should be converted
$convwebp = Read-Host -Prompt "Press 'y' followed by ENTER to convert jpegs to webp"

# Create stopwatch to check total time used
$stopWatch = New-Object -TypeName System.Diagnostics.Stopwatch
$stopWatch.reset()
$stopWatch.start()

# Set the current directory as a variable
$basepath = Get-Location

# Set the number of tasks to do in parallel to do when converting from jpg to webp
$cores = 12

# Set the temporary directory used when unpacking/converting/packing
$temppath = "C:\Temp\Convert-temp"
if ((Test-Path $temppath) -Match "False") {
    New-Item $temppath -ItemType "Directory"
}

# Parameters for 7zip
$7xoutpath = "-o" + $temppath
$7ainpath = $temppath + "\*"

# Check if conversion of jpeg to webp is wanted
if ( $convwebp -match "[yY]" ) {
    # Find all .cbz files in current directory
    $files = Get-ChildItem -Filter *cbz

    # For all files (.cbz) found
    Foreach ($f in $files) {
        # Use 7zip to check if there are any jpgs in the .cbz file. If not go to next .cbz
        If ((7z l $f) -match "jpg") {
            # Extract to the temporary directory
            7z e $f $7xoutpath

            # Filter all jpgs in the temporary directory
            Set-Location $temppath
            Get-ChildItem -Filter *jpg -Recurse | ForEach-Object -Parallel {(nconvert -D -quiet -out webp -q 85 $_) } -ThrottleLimit 12
            Set-Location $basepath

            # Delete original .cbz
            Remove-Item $f

            # Use 7zip to create new .cbz file with all the files in the temporary directory
            $7newname = $f.BaseName + ".cbz"
            7z a $7newname $7ainpath -tzip -sdel

            # End of the if statement that checked for jpgs
        }

        # Loop back to next .cbz file
    }
    # End of if statement that checked for webp conversion
}
# Done with all .cbz files!

# Find all .cbr files in current directory
$files = Get-ChildItem -Filter *cbr

# For all files (.cbr) found:
foreach ($f in $files) {
    # Extract to the temporary directory
    7z e $f $7xoutpath

    # Check if conversion to webp is wanted
    if ( $convwebp -match "[yY]" ) {
        # Filter all jpgs in the temporary directory
        Set-Location $temppath    
        Get-ChildItem -Filter *jpg -Recurse | ForEach-Object -Parallel {(nconvert -D -quiet -out webp -q 85 $_) } -ThrottleLimit $cores
        Set-Location $basepath

        # End of if statement that checked for webp conversion
    }

    # Delete original .cbr
    Remove-Item $f

    # Use 7zip to create new .cbz file with all the files in the temporary directory
    $7newname = $f.BaseName + ".cbz"
    7z a $7newname $7ainpath -tzip -sdel

    # Loop back to next .cbr file
}

# Done! Display the stopwatch
$stopwatch
