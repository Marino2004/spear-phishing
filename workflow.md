```mermaid
---
title: Spear-Phishing
---
flowchart TD
    A[1- Lien sur le profil Linkedin/Github]
    B[2- Service de connexion SMTP]
    C["3- Génération du contenu du mail (IA)"]
    D["4- Création du fake Page Google Authentification"]
    E["5- Social Engeenering fake redirection"]
    F["6- Test de mot de passe sur sur != site (Maltego)"]

    A --> B
    B --> |"Profil data"| C
    C --> D
    D --> E
    E --> F