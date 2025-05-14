# EpicEvents

Application de gestion d'événements destinée à simplifier le suivi des clients, des contrats et des évènements.

## Détails
**Auteur** : Pierre BULGARE\
**Version** : 1.0

## Fonctionnalités

- Gestion des clients : création, modification, suppression et consultation.
- Gestion des contrats : suivi des contrats associés aux clients.
- Gestion des événements : planification et suivi des événements.
- Authentification et gestion des utilisateurs.

## Prérequis

- Python 3.9 ou supérieur
- Django 4.0 ou supérieur
- PostgreSQL (ou autre base de données compatible)

## Installation et Configuration de l'application

1. Clonez le dépôt :
    ```bash
    git clone https://github.com/votre-repo/epicevents.git
    cd epicevents
    ```

2. Créez un environnement virtuel et activez-le :
    ```bash
    python -m venv venv
    
    [Linux]
    source venv/bin/activate
    [Windows]
    env\Scripts\activate
    ```

3. Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

4. Créez la base de données (PostgreSQL) :
* Téléchargez et installez PostgreSQL https://www.postgresql.org/download/
* Ouvrez PgAdmin puis connectez-vous au serveur
* Clic droit sur le serveur -> Create -> Database
* Entrez les informations et configurations souhaitées puis cliquez sur Save

5. Créez un utilisateur pour la gestion de la base de données :
* Clic droit sur le serveur -> Create -> Login/Group Roles
* Entrez les informations puis cliquez sur Save 

6. Configurez l'environnement
* Créer un fichier et nommez le .env
* Ajoutez la variable DATABASE_URL avec la valeur suivante :
  * postgresql://nom_dutilisateur:mot_de_passe@localhost/nom_de_votre_bdd
* Créez la clé secrète JWT : 
    ```bash
    openssl rand -base64 32
    ```
    * Ajoutez la variable JWT_SECRET_KEY avec en valeur la clé obtenue
* Créer un mot de passe administrateur :
  * Générez un mot de passe crypté
    ```bash
    python -c "import bcrypt; password = input('Entrez le mot de passe ADMIN : '); print('Hash bcrypt :', bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode())"
    ```
  * Ajoutez la variable ADMIN_PASSWORD avec en valeur le mot de passe crypté

## Lancement de l'application (Automatique)
 * Mode Utilisateur : Lancez le fichier `run.cmd`
 * Mode Administrateur : Lancez le fichier `run_admin.cmd`

## Lancement de l'application (Manuelle)
* Activez l'environnement python
  ```bash
  [Linux]
  source venv/bin/activate
  [Windows]
  env\Scripts\activate
  ```

* Mode Utilisateur :
  * Lancez l'application
    ```bash
    python app\app.py
    ```

* Mode Administrateur :
  * Lancez l'application
    ```bash
    python app\admin.py
    ```
