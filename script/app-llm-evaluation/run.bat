@echo off
set SCRIPT_DIR=%~dp0
set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%

if "%MLC_PYTHON_BIN_WITH_PATH%"=="" (
    set "MLC_PYTHON_BIN_WITH_PATH=python"
)

if exist "%SCRIPT_DIR%\.env" (
    echo Loading environment variables from %SCRIPT_DIR%\.env
    for /f "usebackq tokens=* delims=" %%a in ("%SCRIPT_DIR%\.env") do (
        set "line=%%a"
        echo !line! | findstr /b "#" >nul
        if errorlevel 1 (
            if not "!line!"=="" (
                for /f "tokens=1,* delims==" %%b in ("!line!") do (
                    set "%%b=%%c"
                )
            )
        )
    )
) else (
    echo No .env file found in %SCRIPT_DIR%. Skipping environment variable loading.
)

%MLC_PYTHON_BIN_WITH_PATH% "%SCRIPT_DIR%\process.py"
if errorlevel 1 exit /b 1
