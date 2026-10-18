@echo off
cd /d "%~dp0"
python cartier_miller.py calibrate --bound 20000 --family rounded_third --collection streaming --profile laptop_dispatch.json
if errorlevel 1 exit /b 1
python cartier_miller.py many --bound 20000 --family rounded_third --engine auto --profile laptop_dispatch.json --out rounded_thirds.csv
if errorlevel 1 exit /b 1
echo Calibration and measured evaluation completed. See rounded_thirds.csv.
