@echo off
echo ================================
echo  Activating venv...
echo ================================

call venv\Scripts\activate

echo ================================
echo  Running PyInstaller...
echo ================================

pyinstaller ^
  --noconfirm ^
  --clean ^
  --paths . ^
  --hidden-import pydantic_settings ^
  --hidden-import pydantic_settings.main ^
  --add-data "dist;dist" ^
  --add-data "app;app" ^
  --add-data "..\db;db" ^
  --onefile app/main.py

echo ================================
echo  Build Finished!
echo ================================
pause
