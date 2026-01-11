# Système de Gestion des Étudiants

## Introduction et objectifs du projet

Ce projet a été réalisé dans le cadre de la formation **Python**.  
L’objectif principal est de concevoir une application web permettant la **gestion des étudiants** à travers une interface simple et intuitive.

L’application permet :
- l’ajout d’étudiants,
- l’affichage de la liste des étudiants,
- la modification des informations,
- la suppression d’un étudiant.

Ce projet vise également à mettre en pratique les notions vues en cours concernant les **applications web**, les **API REST** et la **communication entre le frontend et le backend**.

---

## Technologies utilisées

### Frontend
- **HTML5** : structure des pages
- **CSS3** : mise en forme et design de l’interface
- **JavaScript (Fetch API)** : communication avec le backend

> ⚠️ **PyScript n’a pas été utilisé dans ce projet.**  
> Le frontend repose uniquement sur des technologies web classiques (HTML, CSS et JavaScript).

### Backend
- **Python**
- **Flask** : framework web pour créer l’API REST
- **Flask-CORS** : gestion des requêtes entre le frontend et le backend

### Base de données
- **MySQL** : stockage des données des étudiants
- **mysql-connector-python** : connexion entre Flask et MySQL

---

## Architecture de l’application

L’architecture du projet est basée sur une séparation claire des responsabilités :


- Le **frontend** envoie des requêtes HTTP (GET, POST, PUT, DELETE).
- Le **backend Flask** traite ces requêtes et applique la logique métier.
- La **base de données MySQL** stocke les informations des étudiants.

---

## Présentation des fonctionnalités et du code

### 1. Ajouter un étudiant
- Saisie des informations via un formulaire
- Envoi des données au backend avec une requête **POST**
- Insertion des données dans la base MySQL

### 2. Afficher les étudiants
- Récupération des données via une requête **GET**
- Affichage dynamique dans un tableau HTML

### 3. Modifier un étudiant
- Ouverture d’une fenêtre modale
- Mise à jour via une requête **PUT**
- Synchronisation automatique avec la base de données

### 4. Supprimer un étudiant
- Suppression via une requête **DELETE**
- Mise à jour immédiate de l’interface

---

## Difficultés rencontrées et solutions apportées

### 🔴 Problème de connexion à MySQL
**Erreur rencontrée :**

✅ **Solution :**
- Vérification que le serveur MySQL est bien lancé
- Correction des paramètres de connexion (host, user, password, database)

---

### 🔴 Erreur `UnboundLocalError: cursor`
**Cause :**
- Tentative de fermer le curseur alors qu’il n’était pas initialisé suite à une erreur de connexion.

✅ **Solution :**
- Initialisation correcte du curseur
- Gestion des exceptions avec `try / except / finally`

---

### 🔴 Problème de communication frontend / backend (CORS)
**Cause :**
- Le frontend et le backend fonctionnent sur des ports différents.

✅ **Solution :**
- Utilisation de **Flask-CORS** pour autoriser les requêtes HTTP

---

## Conclusion

Ce projet a permis de comprendre le fonctionnement d’une application web complète, depuis l’interface utilisateur jusqu’à la base de données.  
Il a également permis de renforcer les compétences en **Flask**, **JavaScript**, **API REST** et **bases de données relationnelles**.
