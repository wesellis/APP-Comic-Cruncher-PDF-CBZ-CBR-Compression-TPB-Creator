# Create web-safe image copies

# Copy the original images with web-safe names
Copy-Item "assets\2025-06-18 17_02_51-Comic Cruncher.png" "assets\comic-cruncher-mode.png"
Copy-Item "assets\2025-06-19 06_43_51-Comic Cruncher.png" "assets\comic-combiner-mode.png"  
Copy-Item "assets\2025-06-19 06_44_01-Claude.png" "assets\batch-processing.png"

Write-Host "✅ Created web-safe image copies:"
Write-Host "   comic-cruncher-mode.png"
Write-Host "   comic-combiner-mode.png"
Write-Host "   batch-processing.png"
Write-Host ""
Write-Host "🚀 Ready for GitHub Pages deployment!"
