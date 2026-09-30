# AI Data Analyst

Un analyste de données conversationnel : l'utilisateur pose une question en
langage naturel, le système génère la requête **SQL**, l'exécute sur une base
**e-commerce**, analyse le résultat avec **Pandas**, produit un **graphique** et
renvoie une réponse expliquée.

```
Question (langage naturel)
        │
        ▼
   LLM (Groq)  ──►  génération SQL
        │
        ▼
  Garde-fou SQL  ──►  vérifie lecture seule + ajoute LIMIT
        │
        ▼
  PostgreSQL / SQLite  ──►  exécution
        │
        ▼
   Pandas  ──►  DataFrame + graphique (Matplotlib)
        │
        ▼
   LLM  ──►  réponse en langage naturel + source (SQL)
```

## Exemples de questions

- « Quel produit a généré le plus de chiffre d'affaires en 2025 ? »
- « Pourquoi les ventes ont diminué en mars 2025 ? »
- « Montre-moi les 5 catégories les plus rentables. »
- « Quel est le panier moyen par pays ? »

## Stack technique

- **Python**
- **FastAPI** (API + interface web légère)
- **PostgreSQL** (via Docker) ou **SQLite** (démarrage sans installation)
- **SQLAlchemy** / **Pandas**
- **Matplotlib** pour les graphiques
- **LLM via Groq API** (Llama 3.3 70B, configurable)
- **Docker / docker-compose**

## Sécurité

Le text-to-SQL est risqué par nature. Le module [src/sql_guard.py](src/sql_guard.py) :

- n'autorise **que les requêtes `SELECT`** (une seule instruction),
- **rejette** tout `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, etc.,
- ajoute automatiquement une clause `LIMIT` si elle est absente.

## Démarrage rapide (SQLite, sans Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # puis renseigne GROQ_API_KEY

python -m scripts.generate_data     # génère le dataset e-commerce
python -m scripts.seed_db           # crée et remplit la base
uvicorn app:app --reload
```

Ouvre ensuite http://localhost:8000

## Avec Docker + PostgreSQL

```bash
docker compose up --build -d
docker compose exec api python -m scripts.generate_data
docker compose exec api python -m scripts.seed_db
```

L'API est disponible sur http://localhost:8000

## Tests

```bash
pytest
```

## Structure

```
ai-data-analyst/
├── app.py                  API FastAPI + UI
├── scripts/
│   ├── generate_data.py    Génération du dataset e-commerce
│   └── seed_db.py          Création et chargement de la base
├── src/
│   ├── config.py           Paramètres
│   ├── db.py               Connexion SQLAlchemy
│   ├── schema.py           Schéma des tables + description pour le LLM
│   ├── llm.py              Client Groq
│   ├── prompts.py          Prompts text-to-SQL et synthèse
│   ├── sql_generator.py    Question -> SQL
│   ├── sql_guard.py        Validation lecture seule
│   ├── executor.py         Exécution SQL -> DataFrame
│   ├── charts.py           Génération de graphiques
│   ├── analyzer.py         Synthèse en langage naturel
│   └── pipeline.py         Orchestration
├── static/index.html       Interface web
├── docker-compose.yml
└── tests/
```
