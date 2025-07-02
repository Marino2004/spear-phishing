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
        *)
            echo "Usage: $0 -u USER [-t TOKEN]"
            exit 1
            ;;
    esac
done

# Vérifie si USER est défini
if [ -z "$USER" ]; then
    echo "Erreur : utilisateur non spécifié. Utilisez -u USER"
    exit 1
fi

# Commande curl avec ou sans token
if [ -n "$TOKEN" ]; then
    CURL="curl -s -H \"Authorization: token $TOKEN\""
else
    CURL="curl -s"
fi

# Récupération des noms de dépôts
repos=$(eval $CURL "https://api.github.com/users/$USER/repos?per_page=100" | jq -r '.[].name')

# Déclaration associative pour compter les langages
declare -A languages

# Boucle sur chaque dépôt
for repo in $repos; do
    lang_url="https://api.github.com/repos/$USER/$repo/languages"
    lang_data=$(eval $CURL "$lang_url")

    # Ajout des octets de chaque langage dans la table associative
    for lang in $(echo "$lang_data" | jq -r 'keys[]'); do
        bytes=$(echo "$lang_data" | jq ".\"$lang\"")
        ((languages[$lang]+=$bytes))
    done
done

# Récupération du langage dominant
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

# Récupérer les infos de base de l'utilisateur
user_info=$(curl -s "https://api.github.com/users/$USER")

# Extraire le nom et la localisation avec jq
user_name=$(echo "$user_info" | jq -r '.name // "N/A"')
user_location=$(echo "$user_info" | jq -r '.location // "N/A"')

# Génération du JSON
json_output=$(cat <<EOF
{
  "user": "$USER",
  "name": "$user_name",
  "location": "$user_location",
  "langages": "$(IFS=, ; echo "${lang_list[*]}")",
  "top": "$top_lang"
}
EOF
)

# Affichage à l'écran
echo "$json_output"

# Sauvegarde dans le fichier output.json
echo "$json_output" > output.json