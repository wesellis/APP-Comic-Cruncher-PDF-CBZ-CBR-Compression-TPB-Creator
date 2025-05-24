<#
.SYNOPSIS
    Converts Comic Book Archive (CBR) files to CBZ format with optional JPEG to WebP optimization.

.DESCRIPTION
    This PowerShell script automates the conversion of CBR (Comic Book RAR) files to CBZ (Comic Book ZIP) format.
    It includes optional JPEG to WebP conversion for reduced file sizes while maintaining quality.
    The script uses parallel processing for faster conversions and automatic cleanup of temporary files.

.PARAMETER ConvertToWebP
    Optional switch to enable JPEG to WebP conversion. If not specified, user will be prompted.

.PARAMETER ParallelTasks
    Number of parallel tasks for WebP conversion. Default is 12. Should not exceed CPU logical cores.

.PARAMETER TempPath
    Temporary directory for file processing. Default is "C:\Temp\Convert-temp".

.EXAMPLE
    .\ConverterPS.ps1
    Interactive mode - prompts for WebP conversion preference

.EXAMPLE
    .\ConverterPS.ps1 -ConvertToWebP -ParallelTasks 8
    Convert with WebP optimization using 8 parallel tasks

.NOTES
    Author: Wesley Ellis
    Email: wes@wesellis.com
    Website: wesellis.com
    Created: December 2024
    Updated: May 23, 2025
    Version: 1.1.0

    Prerequisites:
    - PowerShell 7.1 or later (required for parallel processing)
    - 7-Zip with 7z.exe in system PATH
    - nConvert with nconvert.exe in system PATH (for WebP conversion)
    - libwebp.dll in nConvert "Plugins" folder (for WebP conversion)

    Performance Notes:
    - Adjust ParallelTasks based on your CPU capabilities
    - Use SSD storage for TempPath for better performance
    - Ensure adequate free disk space (2-3x input file sizes)

.LINK
    https://github.com/wesellis/CBR-to-CBZ-Converter

.LINK
    https://www.7-zip.org/

.LINK
    https://www.xnview.com/en/nconvert/
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [switch]$ConvertToWebP,
    
    [Parameter(Mandatory = $false)]
    [ValidateRange(1, 32)]
    [int]$ParallelTasks = 12,
    
    [Parameter(Mandatory = $false)]
    [string]$TempPath = "C:\Temp\Convert-temp"
)

# ============================================================================
# Script Name: CBR to CBZ Converter
# Author: Wesley Ellis
# Email: wes@wesellis.com
# Website: wesellis.com
# Date: May 23, 2025
# Description: Converts CBR files to CBZ with optional JPEG to WebP optimization
# ============================================================================

# Script variables
$ErrorActionPreference = "Stop"
$VerbosePreference = "Continue"

# Clear the console for better user experience
Clear-Host

function Write-Header {
    <#
    .SYNOPSIS
        Displays the script header and information
    #>
    Write-Host "===============================================" -ForegroundColor Cyan
    Write-Host "        CBR to CBZ Converter v1.1.0" -ForegroundColor Yellow
    Write-Host "        by Wesley Ellis (wes@wesellis.com)" -ForegroundColor Gray
    Write-Host "===============================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "This script converts all .cbr files in the current directory to .cbz format." -ForegroundColor White
    Write-Host "Optional JPEG to WebP conversion is available for smaller file sizes." -ForegroundColor White
    Write-Host ""
}

function Test-Prerequisites {
    <#
    .SYNOPSIS
        Verifies that required tools are available
    #>
    Write-Verbose "Checking prerequisites..."
    
    # Test 7-Zip
    try {
        $null = & 7z 2>&1
        Write-Host "✓ 7-Zip found" -ForegroundColor Green
    }
    catch {
        Write-Error "7-Zip not found in PATH. Please install 7-Zip and add 7z.exe to your PATH."
        Write-Host "Download from: https://www.7-zip.org/" -ForegroundColor Yellow
        return $false
    }
    
    # Test nConvert (if WebP conversion requested)
    if ($ConvertToWebP -or $convwebp -match "[yY]") {
        try {
            $null = & nconvert 2>&1
            Write-Host "✓ nConvert found" -ForegroundColor Green
        }
        catch {
            Write-Warning "nConvert not found in PATH. WebP conversion will be disabled."
            Write-Host "Download from: https://www.xnview.com/en/nconvert/" -ForegroundColor Yellow
            return $false
        }
    }
    
    # Test PowerShell version
    if ($PSVersionTable.PSVersion.Major -lt 7) {
        Write-Warning "PowerShell 7.1+ recommended for optimal performance."
        Write-Host "Download from: https://microsoft.com/PowerShell" -ForegroundColor Yellow
    } else {
        Write-Host "✓ PowerShell version $($PSVersionTable.PSVersion) detected" -ForegroundColor Green
    }
    
    return $true
}

function Initialize-Environment {
    <#
    .SYNOPSIS
        Sets up the working environment and variables
    #>
    Write-Verbose "Initializing environment..."
    
    # Create temporary directory if it doesn't exist
    if (-not (Test-Path $TempPath)) {
        Write-Verbose "Creating temporary directory: $TempPath"
        New-Item -Path $TempPath -ItemType Directory -Force | Out-Null
    }
    
    # Set up 7-Zip parameters
    $script:7zExtractParams = "-o$TempPath"
    $script:7zSourcePath = "$TempPath\*"
    
    Write-Host "Temporary directory: $TempPath" -ForegroundColor Gray
    Write-Host "Parallel tasks: $ParallelTasks" -ForegroundColor Gray
    Write-Host ""
}

function Convert-CBZFiles {
    <#
    .SYNOPSIS
        Processes existing CBZ files for WebP conversion
    #>
    param([bool]$EnableWebP)
    
    if (-not $EnableWebP) { return }
    
    $cbzFiles = Get-ChildItem -Filter "*.cbz" -File
    if ($cbzFiles.Count -eq 0) {
        Write-Host "No CBZ files found for processing." -ForegroundColor Gray
        return
    }
    
    Write-Host "Processing $($cbzFiles.Count) CBZ file(s) for WebP conversion..." -ForegroundColor Yellow
    
    foreach ($file in $cbzFiles) {
        Write-Verbose "Processing CBZ: $($file.Name)"
        
        # Check if CBZ contains JPEG files
        $listOutput = & 7z l $file.FullName 2>&1
        if ($listOutput -match "\.jpg|\.jpeg") {
            Write-Host "  Converting: $($file.Name)" -ForegroundColor Cyan
            
            # Extract files
            & 7z e $file.FullName $script:7zExtractParams | Out-Null
            
            # Convert JPEG to WebP
            Push-Location $TempPath
            Get-ChildItem -Filter "*.jpg" -Recurse | ForEach-Object -Parallel {
                & nconvert -D -quiet -out webp -q 85 $_.FullName
            } -ThrottleLimit $ParallelTasks
            Pop-Location
            
            # Remove original CBZ and create new one
            Remove-Item $file.FullName -Force
            $newName = $file.BaseName + ".cbz"
            & 7z a $newName $script:7zSourcePath -tzip -sdel | Out-Null
            
            Write-Host "  ✓ Completed: $newName" -ForegroundColor Green
        }
    }
}

function Convert-CBRFiles {
    <#
    .SYNOPSIS
        Converts CBR files to CBZ format
    #>
    param([bool]$EnableWebP)
    
    $cbrFiles = Get-ChildItem -Filter "*.cbr" -File
    if ($cbrFiles.Count -eq 0) {
        Write-Host "No CBR files found for conversion." -ForegroundColor Gray
        return
    }
    
    Write-Host "Converting $($cbrFiles.Count) CBR file(s) to CBZ format..." -ForegroundColor Yellow
    
    foreach ($file in $cbrFiles) {
        Write-Host "  Converting: $($file.Name)" -ForegroundColor Cyan
        
        # Extract CBR file
        & 7z e $file.FullName $script:7zExtractParams | Out-Null
        
        # Convert JPEG to WebP if requested
        if ($EnableWebP) {
            Push-Location $TempPath
            Get-ChildItem -Filter "*.jpg" -Recurse | ForEach-Object -Parallel {
                & nconvert -D -quiet -out webp -q 85 $_.FullName
            } -ThrottleLimit $ParallelTasks
            Pop-Location
        }
        
        # Remove original CBR and create CBZ
        Remove-Item $file.FullName -Force
        $newName = $file.BaseName + ".cbz"
        & 7z a $newName $script:7zSourcePath -tzip -sdel | Out-Null
        
        Write-Host "  ✓ Completed: $newName" -ForegroundColor Green
    }
}

function Show-CompletionSummary {
    <#
    .SYNOPSIS
        Displays conversion completion summary
    #>
    param([System.Diagnostics.Stopwatch]$Timer)
    
    $Timer.Stop()
    
    Write-Host ""
    Write-Host "===============================================" -ForegroundColor Cyan
    Write-Host "           CONVERSION COMPLETED" -ForegroundColor Green
    Write-Host "===============================================" -ForegroundColor Cyan
    Write-Host "Total time: $($Timer.Elapsed.ToString('mm\:ss'))" -ForegroundColor Yellow
    
    # Count final files
    $finalCBZ = (Get-ChildItem -Filter "*.cbz" -File).Count
    $remainingCBR = (Get-ChildItem -Filter "*.cbr" -File).Count
    
    Write-Host "CBZ files: $finalCBZ" -ForegroundColor Green
    if ($remainingCBR -gt 0) {
        Write-Host "Remaining CBR files: $remainingCBR" -ForegroundColor Yellow
    }
    Write-Host ""
}

# Main script execution
try {
    # Display header
    Write-Header
    
    # Check prerequisites
    if (-not (Test-Prerequisites)) {
        Write-Error "Prerequisites not met. Please install required tools."
        exit 1
    }
    
    # Initialize environment
    Initialize-Environment
    
    # Get WebP conversion preference if not specified as parameter
    $enableWebPConversion = $ConvertToWebP
    if (-not $ConvertToWebP) {
        Write-Host "WebP Conversion Options:" -ForegroundColor Yellow
        Write-Host "- Reduces file size by 20-30%" -ForegroundColor Gray
        Write-Host "- Maintains visual quality" -ForegroundColor Gray
        Write-Host "- Requires nConvert with libwebp.dll" -ForegroundColor Gray
        Write-Host ""
        $webpChoice = Read-Host "Convert JPEG images to WebP? (y/N)"
        $enableWebPConversion = $webpChoice -match "[yY]"
    }
    
    if ($enableWebPConversion) {
        Write-Host "WebP conversion enabled with quality setting: 85%" -ForegroundColor Green
    } else {
        Write-Host "WebP conversion disabled - keeping original JPEG format" -ForegroundColor Gray
    }
    Write-Host ""
    
    # Start timing
    $stopWatch = [System.Diagnostics.Stopwatch]::StartNew()
    
    # Process existing CBZ files (if WebP conversion enabled)
    Convert-CBZFiles -EnableWebP $enableWebPConversion
    
    # Convert CBR files to CBZ
    Convert-CBRFiles -EnableWebP $enableWebPConversion
    
    # Show completion summary
    Show-CompletionSummary -Timer $stopWatch
    
}
catch {
    Write-Error "Script execution failed: $($_.Exception.Message)"
    Write-Host "Stack trace: $($_.ScriptStackTrace)" -ForegroundColor Red
    exit 1
}
finally {
    # Cleanup: Ensure we're back in the original directory
    if ($pwd.Path -ne $PSScriptRoot -and $PSScriptRoot) {
        Set-Location $PSScriptRoot
    }
    Write-Verbose "Script execution completed."
}