# LITReview

LITReview est une application web Django qui permet à une communauté d'utilisateurs de demander, rédiger et lire des critiques de livres et d'articles.

## Prérequis

Pour exécuter ce projet, vous devez avoir les outils suivants installés :
- **Python** : Version 3.8 ou supérieure.
- **pip** : Le gestionnaire de paquets de Python (généralement installé avec Python).
- **Git** : Outil de contrôle de version pour cloner le dépôt.
- **Terminal** : Un terminal comme Command Prompt (Windows), Terminal (macOS), ou un shell Linux.

## Installer et lancer LITReview

### 1. Cloner ce dépôt Github en local

Dans votre terminal, tapez :
```bash
git clone https://github.com/redaabdi/LitReview-web-application----Projet-de-Formation
cd LitReview-web-application----Projet-de-Formation
```

### 2. Créer et activer un environnement virtuel


- Sous Windows :
  ```bash
  python -m venv venv
  ```
- Sous macOS / Linux :
  ```bash
  python3 -m venv venv
  ```


Activez-le :
- Sous Windows :
  ```bash
  venv\Scripts\activate
  ```
- Sous macOS / Linux :
  ```bash
  source venv/bin/activate
  ```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Lancer le serveur

```bash
cd litreview
python manage.py runserver
```

### 5. Ouvrir l'application

Ouvrez votre navigateur internet et rendez-vous à l'adresse :
```
http://127.0.0.1:8000/homepage/
```


## Fonctionnalités principales

- S'inscrire, se connecter et se déconnecter
- "Demander une critique" pour créer un ticket
- "Créer une critique" pour créer un ticket et sa critique en une seule étape
- "Créer une critique" en réponse à un ticket
- Posts : Voir, modifier et supprimer ses propres tickets et critiques
- Suivre, se désabonner, bloquer ou débloquer d'autres utilisateurs
- Consulter un flux avec les tickets et critiques des utilisateurs suivis, ainsi que les réponses à nos tickets, classés du plus récent au plus ancien

## Crédits

Réda Abdi pour le projet « Développez une application Web en utilisant Django », dans le cadre de la formation « Développeur d'applications Python » de OpenClassrooms.
