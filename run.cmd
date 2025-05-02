@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: Vérifier que Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python n'est pas installé sur cet ordinateur.
    echo Veuillez installer Python avant de continuer.
    start https://www.python.org/downloads/
    exit /b 1
)

:: Récupérer la version de Python
for /f "tokens=2 delims= " %%v in ('python --version') do set py_version=%%v

:: Extraire les versions majeure et mineure
for /f "tokens=1,2 delims=." %%a in ("%py_version%") do (
    set major=%%a
    set minor=%%b
)

:: Vérifier que la version est Python3 est installée
if not "!major!"=="3" (
    echo Python !py_version! n'est pas compatible avec cette application. Veuillez installer Python 3.
    start https://www.python.org/downloads/
    exit /b 1
)

:: Vérifier que la version 3.9 ou supérieure est installée
if !minor! lss 9 (
    echo Python !py_version! n'est pas compatible avec cette application. Veuillez installer Python 3.9 ou supérieur.
    start https://www.python.org/downloads/
    exit /b 1
)

:: Vérifier que pip est installé
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip n'est pas installé sur cet ordinateur.
    echo Veuillez installer pip avant de continuer.
    start https://pip.pypa.io/en/stable/installation/
    exit /b 1
)

:: Vérifier s'il existe un environnement virtuel
if not exist "venv" (
    echo Il n'y a pas d'environnement virtuel.
    echo Création de l'environnement virtuel...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Échec de la création de l'environnement virtuel.
        exit /b 1
    )
)

:: Activer l'environnement virtuel
if exist "venv\Scripts\activate.bat" (
    echo Activation de l'environnement virtuel...
    call venv\Scripts\activate
) else (
    echo Impossible d'activer l'environnement virtuel.
    echo Veuillez vérifier que le fichier activate.bat existe dans le répertoire venv\Scripts.
    exit /b 1
)

:: Vérifier si les dépendances sont installées
if not exist "requirements.txt" (
    echo Le fichier requirements.txt est introuvable.
    echo Veuillez vous assurer que le fichier requirements.txt est présent dans le répertoire courant pour installer les dépendances.
    exit /b 1
)

:: Mise à jour de pip et installation des dépendances
echo Vérification et mise à jour de pip...
python -m pip install --upgrade pip --quiet
if %errorlevel% neq 0 (
    echo Échec de la mise à jour de pip.
    exit /b 1
)
echo Vérification et installation des dépendances...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo Échec de l'installation des dépendances.
    exit /b 1
)

:: Lancer l'application
echo Lancement de l'application...
python run.py