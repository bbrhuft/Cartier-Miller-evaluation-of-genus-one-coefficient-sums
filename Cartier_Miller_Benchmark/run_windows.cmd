@echo off
setlocal
cd /d "%~dp0"
if not defined MSYS2_ROOT set "MSYS2_ROOT=C:\msys64"
set "PATH=%MSYS2_ROOT%\ucrt64\bin;%PATH%"
if not exist "%MSYS2_ROOT%\ucrt64\bin\python.exe" (
  echo MSYS2 UCRT64 Python was not found. Follow README.md first.
  echo For another installation folder, set MSYS2_ROOT to that folder.
  pause
  exit /b 2
)
"%MSYS2_ROOT%\ucrt64\bin\python.exe" "%~dp0run_windows.py" %*
set "BENCHMARK_EXIT=%ERRORLEVEL%"
if not "%BENCHMARK_EXIT%"=="0" echo Benchmark failed. Please retain the error text above.
pause
exit /b %BENCHMARK_EXIT%
