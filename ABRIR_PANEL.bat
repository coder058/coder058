@echo off
cd /d "%~dp0"
echo Abriendo el panel de Claude... (no cierres esta ventana)
where python >nul 2>nul
if %errorlevel%==0 (python hub\server.py) else (py hub\server.py)
echo.
echo El panel se ha cerrado. Si ves un error arriba, copialo y pegaselo a Claude.
pause
