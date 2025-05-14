@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: VÇrifier que Python est installÇ
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python n'est pas installÇ sur cet ordinateur.
    echo Veuillez installer Python avant de continuer.
    start https://www.python.org/downloads/
    exit /b 1
)

:: RÇcupÇrer la version de Python
for /f "tokens=2 delims= " %%v in ('python --version') do set py_version=%%v

:: Extraire les versions majeure et mineure
for /f "tokens=1,2 delims=." %%a in ("%py_version%") do (
    set major=%%a
    set minor=%%b
)

:: VÇrifier que la version est Python3 est installÇe
if not "!major!"=="3" (
    echo Python !py_version! n'est pas compatible avec cette application. Veuillez installer Python 3.
    start https://www.python.org/downloads/
    exit /b 1
)

:: VÇrifier que la version 3.9 ou supÇrieure est installÇe
if !minor! lss 9 (
    echo Python !py_version! n'est pas compatible avec cette application. Veuillez installer Python 3.9 ou supÇrieur.
    start https://www.python.org/downloads/
    exit /b 1
)

:: VÇrifier que pip est installÇ
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip n'est pas installÇ sur cet ordinateur.
    echo Veuillez installer pip avant de continuer.
    start https://pip.pypa.io/en/stable/installation/
    exit /b 1
)

:: VÇrifier s'il existe un environnement virtuel
if not exist "venv" (
    echo Il n'y a pas d'environnement virtuel.
    echo CrÇation de l'environnement virtuel...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo êchec de la crÇation de l'environnement virtuel.
        exit /b 1
    )
)

:: Activer l'environnement virtuel
if exist "venv\Scripts\activate.bat" (
    echo Activation de l'environnement virtuel...
    call venv\Scripts\activate
) else (
    echo Impossible d'activer l'environnement virtuel.
    echo Veuillez vÇrifier que le fichier activate.bat existe dans le rÇpertoire venv\Scripts.
    exit /b 1
)

:: VÇrifier si les dÇpendances sont installÇes
if not exist "requirements.txt" (
    echo Le fichier requirements.txt est introuvable.
    echo Veuillez vous assurer que le fichier requirements.txt est prÇsent dans le rÇpertoire courant pour installer les dÇpendances.
    exit /b 1
)

:: Mise Ö jour de pip et installation des dÇpendances
echo VÇrification et mise Ö jour de pip...
python -m pip install --upgrade pip --quiet
if %errorlevel% neq 0 (
    echo êchec de la mise Ö jour de pip.
    exit /b 1
)
echo VÇrification et installation des dÇpendances...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo êchec de l'installation des dÇpendances.
    exit /b 1
)

:: Lancer l'application
echo Lancement de l'application...
python run.py
if %errorlevel% neq 0 (
    echo êchec du lancement de l'application.
    exit /b 1
)