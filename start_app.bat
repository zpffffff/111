@echo off
REM Start FastAPI service
echo Starting FastAPI service...
start python main.py

REM Wait for FastAPI service to start
echo Waiting for FastAPI service to start...
timeout /t 10 >nul

REM Check if FastAPI service is running
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo FastAPI service is running.
) else (
    echo Failed to start FastAPI service!
    pause
    exit /b
)

REM Open HTML file
echo Opening HTML file...
start msedge "http://127.0.0.1:8004/your_file.html"

pause