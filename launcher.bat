@echo off
REM P2P File Sharing Application Launcher for Windows
REM This script helps you start the server and clients easily

:menu
cls
echo ==========================================
echo   P2P File Sharing - Launcher
echo ==========================================
echo.
echo 1. Start Server
echo 2. Start Client (GUI)
echo 3. Run Test Suite
echo 4. View Documentation
echo 5. Clean Repository Files
echo 6. Exit
echo.
set /p choice="Choose an option [1-6]: "

if "%choice%"=="1" goto start_server
if "%choice%"=="2" goto start_client
if "%choice%"=="3" goto run_tests
if "%choice%"=="4" goto view_docs
if "%choice%"=="5" goto clean_repos
if "%choice%"=="6" goto exit_app
goto invalid_choice

:start_server
echo.
echo Starting server...
echo Press Ctrl+C to stop
echo.
python server.py
goto menu

:start_client
echo.
echo Starting client GUI...
echo Make sure to:
echo   1. Use a unique hostname (e.g., client1, client2, ...)
echo   2. Use a unique port (e.g., 6000, 6001, 6002, ...)
echo.
start python client_gui.py
goto menu

:run_tests
echo.
echo Running test suite...
echo Make sure the server is running first!
echo.
set /p answer="Is the server running? (y/n): "
if /i "%answer%"=="y" (
    python test_suite.py
) else (
    echo Please start the server first (option 1)
)
echo.
pause
goto menu

:view_docs
cls
echo ==========================================
echo   Documentation Files
echo ==========================================
echo.
echo 1. README.md - Main documentation
echo 2. QUICK_START.md - Quick start guide
echo 3. PROTOCOL_SPECIFICATION.md - Protocol details
echo.
echo You can view these files with any text editor or markdown viewer
echo.
pause
goto menu

:clean_repos
echo.
echo This will delete all client repository directories
echo   (client_repo_*)
echo.
set /p answer="Are you sure? (y/n): "
if /i "%answer%"=="y" (
    for /d %%i in (client_repo_*) do rd /s /q "%%i"
    echo Repository directories cleaned
) else (
    echo Cancelled
)
echo.
pause
goto menu

:invalid_choice
echo.
echo Invalid option. Please try again.
timeout /t 2 >nul
goto menu

:exit_app
echo.
echo Goodbye!
exit /b 0
