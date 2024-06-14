This PowerShell script automates the conversion of Comic Book Archive (CBR) files to Comic Book Zip (CBZ) files. It also includes an option to convert JPEG images to WebP format.
Requirements

Before using this script, ensure you have the following:

    7-Zip: Required for extracting and compressing archive files.
        Download and install from 7-Zip.org.
        Ensure 7z.exe is added to your system's PATH environment variable.

    nConvert (Optional for WebP Conversion): Required if converting JPEG images to WebP format.
        Download nConvert from XnView.com.
        Place nconvert.exe in your system's PATH.
        libwebp.dll should be in the "Plugins" subfolder of the nConvert installation directory. Download from XnView.com.

    PowerShell Version: Ensure you have PowerShell 7.1 or later installed for optimal performance, especially when using the -Parallel feature.

Setup Instructions

Follow these steps to set up and use the script:

    Clone or Download Repository:
        Clone or download the repository from CBR-to-CBZ-Converter.

    Ensure Dependencies:
        Install and configure 7-Zip and nConvert as per the requirements above.

    Script Execution:
        Open PowerShell and navigate to the directory containing ConverterPS.ps1.

    Run the Script:
        Execute the script by running .\ConverterPS.ps1.
        Follow on-screen prompts:
            Press 'y' followed by ENTER to convert JPEGs to WebP (optional).

    Conversion Process:
        The script will:
            Convert all .cbr files in the current directory to .cbz.
            Optionally convert JPEG images to WebP format if selected.
            Utilize parallel processing for faster conversions (requires PowerShell 7.1+).

    Cleanup:
        Temporary files are managed automatically by the script in the directory C:\Temp\Convert-temp. Ensure this directory exists and is writable.
