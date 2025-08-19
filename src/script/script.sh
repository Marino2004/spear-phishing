#!/bin/bash
# Analyse des arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -u|--user)
            USER="$2"
            shift 2
            ;;
        -t|--token)
            TOKEN="$2"
            shift 2
            ;;
        -e|--email)
            EMAIL="$2"
            shift 2
            ;;
        *)
            echo "Usage: $0 -u USER [-t TOKEN] [-e EMAIL]"
            exit 1
            ;;
    esac
done

###############################################
# Cas 1 : seulement email fourni (DOIT être vérifié en PREMIER)
###############################################
if [ -n "$EMAIL" ] ; then
    echo "{\"email\": \"$EMAIL\"}" > output.json
    echo "✅ Email enregistré dans output.json"
    exit 0
fi

###############################################
# Vérification si aucun argument fourni
###############################################
if [ -z "$USER" ] && [ -z "$EMAIL" ]; then
    echo "Usage: $0 -u USER [-t TOKEN] [-e EMAIL]"
    exit 1
fi

###############################################
# Cas 2 : USER fourni → vérifier output.json et email
###############################################
if [ -n "$USER" ]; then
    if [ ! -f "output.json" ]; then
        echo "❌ Erreur : output.json introuvable. Ajoutez d'abord un email avec -e"
        exit 1
    fi
    EMAIL_EXIST=$(jq -r '.email // empty' output.json)
    if [ -z "$EMAIL_EXIST" ]; then
        echo "❌ Erreur : aucun email trouvé dans output.json. Ajoutez-le avec -e"
        exit 1
    fi
fi

# Commande curl avec ou sans token
if [ -n "$TOKEN" ]; then
    CURL="curl -s -H \"Authorization: token $TOKEN\""
else
    CURL="curl -s"
fi

# Récupération des dépôts
repos=$(eval $CURL "https://api.github.com/users/$USER/repos?per_page=100" | jq -r '.[].name')

# Déclaration associative pour compter les langages
declare -A languages

# Boucle sur chaque dépôt
for repo in $repos; do
    lang_url="https://api.github.com/repos/$USER/$repo/languages"
    lang_data=$(eval $CURL "$lang_url")
    
    for lang in $(echo "$lang_data" | jq -r 'keys[]'); do
        bytes=$(echo "$lang_data" | jq ".\"$lang\"")
        ((languages[$lang]+=$bytes))
    done
done

# Langage dominant
top_lang=""
top_value=0
lang_list=()

for lang in "${!languages[@]}"; do
    lang_list+=("$lang")
    if (( languages[$lang] > top_value )); then
        top_value=${languages[$lang]}
        top_lang=$lang
    fi
done

# Infos de base de l'utilisateur
user_info=$(curl -s "https://api.github.com/users/$USER")
user_name=$(echo "$user_info" | jq -r '.name // "N/A"')
user_location=$(echo "$user_info" | jq -r '.location // "N/A"')

# Créer un fichier temporaire avec les nouvelles données
temp_file=$(mktemp)
jq \
  --arg user "$USER" \
  --arg name "$user_name" \
  --arg location "$user_location" \
  --arg langages "$(IFS=, ; echo "${lang_list[*]}")" \
  --arg top "$top_lang" \
  '. + {user: $user, name: $name, location: $location, langages: $langages, top: $top}' \
  output.json > "$temp_file"

# Remplacer l'ancien fichier par le nouveau
mv "$temp_file" output.json

echo "✅ output.json mis à jour avec les infos utilisateur"