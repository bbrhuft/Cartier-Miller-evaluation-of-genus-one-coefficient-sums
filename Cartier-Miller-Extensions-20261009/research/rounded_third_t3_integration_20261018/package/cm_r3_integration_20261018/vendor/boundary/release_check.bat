@echo off
cd /d "%~dp0"
python cartier_miller.py check --benchmarks smoke
if errorlevel 1 exit /b 1
echo Release checks passed. The results folder contains a shareable evidence ZIP.
