@echo on
echo =====================================================
echo COMIC CRUNCHER LAUNCHER
echo =====================================================
echo.
echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please run install.bat first
    echo.
    goto :error
)

echo.
echo Checking dependencies...
python -c "import PyQt6" 2>nul
if %errorlevel% neq 0 (
    echo ERROR: PyQt6 not installed!
    echo Please run install.bat first
    echo.
    goto :error
)

python -c "import PIL" 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Pillow not installed!
    echo Please run install.bat first
    echo.
    goto :error
)

echo Dependencies check: OK
echo.
echo Current directory: %CD%
echo Looking for comic_cruncher.py...
if not exist "comic_cruncher.py" (
    echo ERROR: comic_cruncher.py not found in current directory!
    echo Please make sure you're running this from the correct folder
    echo.
    goto :error
)

echo Found comic_cruncher.py
echo.
echo =====================================================
echo STARTING COMIC CRUNCHER
echo =====================================================
echo.
echo Launching application...
python comic_cruncher.py

echo.
echo =====================================================
echo APPLICATION CLOSED
echo =====================================================
echo.
if %errorlevel% neq 0 (
    echo Application exited with error code: %errorlevel%
    echo.
)
echo Press any key to close this window...
pause >nul
exit /b 0

:error
echo Press any key to close this window...
pause >nul
exit /b 1
