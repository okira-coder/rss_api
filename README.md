# API de Transformation RSS

Cette API permet de transformer des flux RSS en un format JSON standardisé.

## Installation

1. Cloner le repository
2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

### Endpoint principal : `/api/articles`

**Méthode** : POST

**Format de la requête** :
```json
[
  {
    "rss": {
      "channel": {
        "title": "Nom de la source",
        "item": [
          {
            "title": "Titre de l'article",
            "description": "Description HTML",
            "link": "URL de l'article",
            "pubDate": "Date de publication",
            "author": "Nom de l'auteur"
          }
        ]
      }
    }
  }
]
```

**Réponse** :
```json
{
  "status": "success",
  "count": 1,
  "articles": [
    {
      "source": {
        "id": null,
        "name": "Nom de la source"
      },
      "author": "Nom de l'auteur",
      "title": "Titre de l'article",
      "description": "Description nettoyée",
      "url": "URL de l'article",
      "urlToImage": "URL de l'image",
      "publishedAt": "Date de publication",
      "content": "Contenu de l'article"
    }
  ]
}
```

### Endpoint de santé : `/health`

**Méthode** : GET

**Réponse** :
```json
{
  "status": "healthy",
  "timestamp": "2024-03-14T12:00:00.000Z"
}
```

## Déploiement sur Render

1. Créer un nouveau service Web sur Render
2. Connecter votre repository GitHub
3. Configurer les paramètres suivants :
   - Build Command : `pip install -r requirements.txt`
   - Start Command : `gunicorn app:app` 