from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import json
from datetime import datetime
import logging
import os

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def extract_image_url(description):
    """Extrait l'URL de la première image d'une description HTML"""
    if not description:
        return None
    try:
        soup = BeautifulSoup(description, 'html.parser')
        img_tag = soup.find('img')
        return img_tag['src'] if img_tag else None
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction de l'image: {str(e)}")
        return None

def validate_feed_data(data):
    """Valide la structure des données d'entrée"""
    if not isinstance(data, dict):
        raise ValueError("Les données doivent être un objet")
    if 'body' not in data:
        raise ValueError("Les données doivent contenir une section 'body'")
    if 'data' not in data['body']:
        raise ValueError("Les données doivent contenir une section 'data' dans 'body'")
    if 'channel' not in data['body']['data']:
        raise ValueError("Les données doivent contenir une section 'channel' dans 'data'")

@app.route('/api/articles', methods=['POST'])
def process_feeds():
    try:
        if not request.is_json:
            return jsonify({"error": "Le contenu doit être au format JSON"}), 400

        data = request.json
        validate_feed_data(data)
        result = []

        # Accéder aux données via la structure body > data > channel
        channel = data['body']['data']['channel']
        source_name = channel.get('title', 'Unknown Source')

        items = channel.get('item', [])
        if isinstance(items, dict):
            items = [items]

        for item in items:
            try:
                author = item.get('dc:creator') or item.get('author') or None
                description = item.get('description', '')

                # Nettoyage du texte de description
                clean_description = BeautifulSoup(description, 'html.parser').get_text().strip()

                article = {
                    "source": {
                        "id": None,
                        "name": source_name
                    },
                    "author": author,
                    "title": item.get('title', '').strip(),
                    "description": clean_description,
                    "url": item.get('link', ''),
                    "urlToImage": extract_image_url(description),
                    "publishedAt": item.get('pubDate', ''),
                    "content": clean_description
                }
                result.append(article)
            except Exception as e:
                logger.error(f"Erreur lors du traitement d'un article: {str(e)}")
                continue

        return jsonify(result)

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.error(f"Erreur serveur: {str(e)}")
        return jsonify({"error": "Une erreur interne est survenue"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint pour vérifier l'état de l'API"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8900))) 
