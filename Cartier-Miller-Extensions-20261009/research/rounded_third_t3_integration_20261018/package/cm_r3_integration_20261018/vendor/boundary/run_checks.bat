@echo off
cd /d "%~dp0"
python cartier_miller.py check --benchmarks all
if errorlevel 1 exit /b 1
echo Full release checks passed. See the evidence ZIP in the results folder.
