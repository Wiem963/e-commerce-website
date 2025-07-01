# 🛒 E-commerce Website – Django 5.2, REST API & JWT Auth

Ce projet est une plateforme **C2C (Consumer-to-Consumer)** développée avec **Django**, permettant à des utilisateurs de vendre et d’acheter des produits (voitures et pièces détachées).  
Le site inclut un système d’authentification sécurisé avec **JWT**, une API REST, et une interface frontend en **Django Templates**.

---

## 🚀 Fonctionnalités principales

### 🔐 Authentification & Gestion des rôles
- Connexion / inscription via API sécurisée avec **JWT**
- Deux rôles principaux :
  - 👤 **Customer**
  - 🧑‍💼 **Seller**
- Un même utilisateur peut être **Customer** et **Seller**

### 👥 Gestion de profil
- Mise à jour des informations personnelles
- Rôle assignable lors de l’inscription

---

### 🛍️ Produits (par le Seller)
- Ajout des produits
- Deux types :
  - 🚗 **Cars**
  - ⚙️ **Parts**
- Visualisation de la liste de ses produits

---

### 📦 Offres (Offers)
- Un **Customer** peut envoyer une offre à un **Seller** sur un produit
- Le **Seller** peut :
  - ✅ Accepter l'offre
  - ❌ Rejeter l'offre
- Consultation des offres reçues ou envoyées

---

### 🤝 Deals
- Un **Deal** est créé lorsque l'offre est envoyée
- Le **Customer** peut consulter ses deals en cours
- Suivi de l'historique des transactions

---

### 🌐 Site Web C2C
- Plateforme orientée **entre particuliers**
- Interface simple pour parcourir les produits et faire des offres

---

### 🖥️ Interface utilisateur (Django Templates)
- Page d’accueil avec les produits disponibles
- Pages dynamiques : produit, offre, deals, profil utilisateur, etc.

---

## ⚙️ Technologies utilisées

- 🐍 **Python 3.13.3**
- 🌐 **Django 5.2.2**
- 🔐 **djangorestframework** & **JWT**
- 🗄️ **MySQL**
- 🎨 **Django Templates**

---

## ⚙️ Installation rapide

### 1. Cloner le dépôt

--- bash
git clone https://github.com/Wiem963/e-commerce-website.git
cd e-commerce-website

python -m venv env
source env/bin/activate  # Linux/macOS
env\Scripts\activate     # Windows

---



### 2. Connectez-vous à MySQL et créez la base :

CREATE DATABASE carpoint_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

### 3. Appliquer les migrations

python manage.py makemigrations carpoint
python manage.py migrate

### 4. Lancer le serveur
python manage.py runserver


