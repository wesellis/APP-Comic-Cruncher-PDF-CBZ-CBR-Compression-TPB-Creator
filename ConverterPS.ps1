# Clear host
Clear-Host

# Print info to console
Write-Host "This script will convert all .cbr files in the current directory to .cbz"
Write-Host "Converting jpg to webp (for both .cbr and .cbz) is included interactively as an option.`n"
Write-Host "NOTE 1: 7-Zip is required and the executable (7z.exe) needs to be in the windows PATH variable for this to work. `nhttps://www.7-zip.org/`n"
Write-Host "NOTE 2 (WebP only): nConvert is required for converion to webp and the executable (nconvert.exe) needs to be in the windows PATH variable for this to work. `nhttps://www.xnview.com/en/nconvert/`n"
Write-Host "NOTE 3 (WebP only): nConvert needs 'libwebp.dll' to be located in 'Plugins' subfolder. This file is included in (for example) XnConvert`nhttps://www.xnview.com/en/xnconvert/`n"
Write-Host "Note 4 (WebP only): To speed up conversion from jpeg to webp the script is using the 'ForEach-Object -Parallel' method. `nFor this reason a recent version of PowerShell is needed. Script written with version 7.1 `nhttps://microsoft.com/PowerShell"

# Ask user if jpeg should be converted
$convwebp = Read-Host -Prompt "Press 'y' followed by ENTER to convert jpegs to webp"

# Create stopwatch to check total time used
# $stopWatch.reset() is most likely not needed, but it won't hurt and better safe than sorry...
$stopWatch = New-Object -TypeName System.Diagnostics.Stopwatch
$stopWatch.reset()
$stopWatch.start()

# Set the current directory as a variable
$basepath = Get-Location

# Set the number of tasks to do in parallel to do when converting from jpg to webp
# Should not exceed the number of logical cores in the CPU
# Example: Ryzen 5 3600X has 6 cores with two threads per core = max 12
# I found that setting the value higher made the conversion go slower
$cores = 12

# Set the temporary directory used when unpacking/converting/packing
# Directory will be created if it doesn't exists
# Directory will be cleaned by the script with no temporary files remaining.
# Directory itself will remain however.
# Change to whatever you like!
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
            # '-Parallel' tells Powershell to run several conversion in parallel
            # Use nConvert for the conversion to webp
            # '-D' in the nconvert command is used to delete the jpgs after conversion      
            Set-Location $temppath
            Get-ChildItem -Filter *jpg -Recurse | ForEach-Object -Parallel {(nconvert -D -quiet -out webp -q 85 $_) } -ThrottleLimit 12
            Set-Location $basepath

            # Delete original .cbz
            Remove-Item $f

            # Use 7zip to create new .cbz file with all the files in the temporary directory
            # '-sdel' tells 7zip to delete the files in the temporary directory afterwards
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
        # '-Parallel' tells Powershell to run several conversion in parallel
        # Use nConvert for the conversion to webp
        # '-D' in the nconvert command is used to delete the jpgs after conversion
        Set-Location $temppath    
        Get-ChildItem -Filter *jpg -Recurse | ForEach-Object -Parallel {(nconvert -D -quiet -out webp -q 85 $_) } -ThrottleLimit $cores
        Set-Location $basepath

        # End of if statement that checked for webp conversion
    }

    # Delete original .cbr
    Remove-Item $f

    # Use 7zip to create new .cbz file with all the files in the temporary directory
    # '-sdel' tells 7zip to delete the files in the temporary directory afterwards
    $7newname = $f.BaseName + ".cbz"
    7z a $7newname $7ainpath -tzip -sdel

    # Loop back to next .cbr file
}

# Done! Display the stopwatch
$stopwatch
