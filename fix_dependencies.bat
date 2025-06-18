@echo on
echo =====================================================
echo COMIC CRUNCHER - QUICK FIX
echo =====================================================
echo.
echo This will fix the PyQt6 DLL and Pillow version issues
echo.

echo Uninstalling problematic packages...
pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip Pillow -y

echo.
echo Installing fresh compatible versions...
pip install --upgrade pip
pip install Pillow
pip install PyQt6
pip install pdf2image
pip install rarfile

echo.
echo Testing imports...
python -c "import PyQt6.QtWidgets; print('PyQt6: OK')"
python -c "import PIL; print('Pillow: OK')"
python -c "import pdf2image; print('pdf2image: OK')"
python -c "import rarfile; print('rarfile: OK')"

echo.
echo =====================================================
echo FIX COMPLETE! 
echo =====================================================
echo.
echo Try running the app now with: python comic_cruncher.py
echo.
echo Press any key to close this window...
pause >nul
