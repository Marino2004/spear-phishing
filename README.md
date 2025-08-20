# 🐙 PhishHub

```
░█████████  ░██        ░██           ░██        ░██     ░██            ░██        
░██     ░██ ░██                      ░██        ░██     ░██            ░██        
░██     ░██ ░████████  ░██ ░███████  ░████████  ░██     ░██ ░██    ░██ ░████████  
░█████████  ░██    ░██ ░██░██        ░██    ░██ ░██████████ ░██    ░██ ░██    ░██ 
░██         ░██    ░██ ░██ ░███████  ░██    ░██ ░██     ░██ ░██    ░██ ░██    ░██ 
░██         ░██    ░██ ░██       ░██ ░██    ░██ ░██     ░██ ░██   ░███ ░███   ░██ 
░██         ░██    ░██ ░██ ░███████  ░██    ░██ ░██     ░██  ░█████░██ ░██░█████  
                                                                                  
```

**PhishHub** est un outil en ligne de commande (**CLI**) permettant :  
- d’analyser des comptes GitHub (utilisateurs, dépôts, langages, etc.)  
- de configurer et gérer un serveur de collecte de données  
- d’envoyer des rapports par email  
- de visualiser et réinitialiser les données collectées  

> ⚠️ **Avertissement :** Ce projet est fourni à des fins **éducatives** et **démonstratives** uniquement.  
> L’utilisation pour des activités malveillantes ou illégales est strictement interdite.

---

## 🚀 Fonctionnalités

- 📧 Configuration d’un email cible  
- 👤 Analyse d’un utilisateur GitHub (via `script.sh`)  
- 📨 Envoi automatique d’email (via `mail_sender.py`)  
- 🌐 Démarrage et arrêt du serveur d’analyse  
- 📋 Visualisation du statut détaillé et des données collectées  
- 🗑️ Réinitialisation des données (`output.json` + logs)  
- 📄 Affichage des logs du serveur  

---

## 📦 Structure du projet

```
phishhub/
│── src/
│   ├── script/
│   │   ├── script.sh
│   │   ├── server.sh
│   │   ├── kill_server.sh
│   │   └── phishing.log
│   └── service/
│       └── mail_service/
│           └── mail_sender.py
│
│── output.json
│── main.py
│── README.md
```

---

## ⚙️ Installation

### 1. Cloner le dépôt
```bash
git clone https://github.com/ton-utilisateur/phishhub.git
cd phishhub
```

### 2. Donner les permissions d’exécution
```bash
chmod +x src/script/*.sh
```

### 3. Installer les dépendances Python
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## ▶️ Utilisation

Lancer l’outil :
```bash
python3 main.py
```

Menu principal interactif :  

```
📊 STATUT ACTUEL :
   Email configuré     : ✅/❌
   Utilisateur analysé : ✅/❌
   Scripts disponibles : ✅/❌

🎯 OPTIONS DISPONIBLES :
   1) 📧 Ajouter/Modifier l'email
   2) 👤 Analyser un utilisateur GitHub
   3) 📨 Envoyer un email à la cible
   4) 🚀 Démarrer le serveur
   5) 🛑 Arrêter le serveur
   6) 📋 Afficher le statut détaillé
   7) 🗑️ Réinitialiser les données
   8) 📄 Afficher le log du serveur
   99) 🚪 Quitter
```

---

## 🗑️ Réinitialisation

Pour supprimer toutes les données utilisateur et logs :  
```bash
Option 7 du menu principal
```

---

## 📜 Licence

Ce projet est sous licence MIT – voir le fichier [LICENSE](LICENSE).  
Usage à vos risques et périls.

---

## ✨ Auteur

Développé par **MIHA Marino**  
📌 Version 1.0.0  