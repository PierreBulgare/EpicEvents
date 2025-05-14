@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: V�rifier que Python est install�
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python n'est pas install� sur cet ordinateur.
    echo Veuillez installer Python avant de continuer.
    start https://www.python.org/downloads/
    exit /b 1
)

:: R�cup�rer la version de Python
for /f "tokens=2 delims= " %%v in ('python --version') do set py_version=%%v

:: Extraire les versions majeure et mineure
for /f "tokens=1,2 delims=." %%a in ("%py_version%") do (
    set major=%%a
    set minor=%%b
)

:: V�rifier que la version est Python3 est install�e
if not "!major!"=="3" (
    echo Python !py_version! n'est pas compatible avec cette application. Veuillez installer Python 3.
    start https://www.python.org/downloads/
    exit /b 1
)

:: V�rifier que la version 3.9 ou sup�rieure est install�e
if !minor! lss 9 (
    echo Python !py_version! n'est pas compatible avec cette application. Veuillez installer Python 3.9 ou sup�rieur.
    start https://www.python.org/downloads/
    exit /b 1
)

:: V�rifier que pip est install�
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip n'est pas install� sur cet ordinateur.
    echo Veuillez installer pip avant de continuer.
    start https://pip.pypa.io/en/stable/installation/
    exit /b 1
)

:: V�rifier s'il existe un environnement virtuel
if not exist "venv" (
    echo Il n'y a pas d'environnement virtuel.
    echo Cr�ation de l'environnement virtuel...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo �chec de la cr�ation de l'environnement virtuel.
        exit /b 1
    )
)

:: Activer l'environnement virtuel
if exist "venv\Scripts\activate.bat" (
    echo Activation de l'environnement virtuel...
    call venv\Scripts\activate
) else (
    echo Impossible d'activer l'environnement virtuel.
    echo Veuillez v�rifier que le fichier activate.bat existe dans le r�pertoire venv\Scripts.
    exit /b 1
)

:: V�rifier si les d�pendances sont install�es
if not exist "requirements.txt" (
    echo Le fichier requirements.txt est introuvable.
    echo Veuillez vous assurer que le fichier requirements.txt est pr�sent dans le r�pertoire courant pour installer les d�pendances.
    exit /b 1
)

:: Mise � jour de pip et installation des d�pendances
echo V�rification et mise � jour de pip...
python -m pip install --upgrade pip --quiet
if %errorlevel% neq 0 (
    echo �chec de la mise � jour de pip.
    exit /b 1
)
echo V�rification et installation des d�pendances...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo �chec de l'installation des d�pendances.
    exit /b 1
)

:: Lancer l'application
echo Lancement de l'application...
python run.py
if %errorlevel% neq 0 (
    echo �chec du lancement de l'application.
    exit /b 1
)