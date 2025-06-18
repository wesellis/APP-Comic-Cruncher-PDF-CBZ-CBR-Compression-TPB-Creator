@echo on
echo =====================================================
echo COMIC CRUNCHER INSTALLATION
echo =====================================================
echo.
echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python from https://python.org
    echo.
    pause
    exit /b 1
)

echo.
echo Checking pip installation...
pip --version
if %errorlevel% neq 0 (
    echo ERROR: pip is not available!
    echo.
    pause
    exit /b 1
)

echo.
echo Current directory: %CD%
echo.
echo Installing Comic Cruncher dependencies...
echo.
echo Uninstalling any existing PyQt6 to avoid conflicts...
pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip -y
echo.
echo Installing Pillow (latest compatible version)...
pip install Pillow -v
echo.
echo Installing pdf2image...
pip install pdf2image -v
echo.
echo Installing rarfile...
pip install rarfile -v
echo.
echo Installing PyQt6 (latest stable)...
pip install PyQt6 -v

echo.
echo Verifying installations...
python -c "import PyQt6; print('PyQt6: OK')"
python -c "import PIL; print('Pillow: OK')"
python -c "import pdf2image; print('pdf2image: OK')"
python -c "import rarfile; print('rarfile: OK')"

echo.
echo =====================================================
echo INSTALLATION COMPLETE!
echo =====================================================
echo.
echo IMPORTANT: You still need to install Poppler for PDF support:
echo 1. Download from: https://github.com/oschwartz10612/poppler-windows/releases/
echo 2. Extract to a folder (e.g., C:\poppler)
echo 3. Add the 'bin' folder to your Windows PATH
echo 4. Restart your command prompt after adding to PATH
echo.
echo To test Poppler installation:
echo   pdftoppm -h
echo.
echo To run Comic Cruncher:
echo   python comic_cruncher.py
echo   OR double-click run.bat
echo.
echo Press any key to close this window...
pause >nul
