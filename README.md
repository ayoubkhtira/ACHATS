# 📦 Tableau de bord Achats – Streamlit

Ce projet Streamlit affiche un tableau de bord Achats basé sur un fichier **Excel** (plusieurs feuilles, ex. `ASMENT TEMARA`, `SAFI`).

## 🚀 Démarrage local

```bash
# 1) Cloner le dépôt
git clone <VOTRE_URL_GITHUB> achats-dashboard
cd achats-dashboard

# 2) Créer un environnement (optionnel) et installer les dépendances
pip install -r requirements.txt

# 3) Placer le fichier Excel
mkdir -p data
# Copiez votre fichier ici sous le nom exact
# data/AGENT ACHATS.xlsx

# 4) Lancer
streamlit run app.py
```

## 🗂️ Structure du dépôt

```
.
├── app.py
├── requirements.txt
├── README.md
├── .streamlit/
│   └── config.toml
└── data/
    └── AGENT ACHATS.xlsx  # (à ajouter)
```

## 🌐 Déploiement sur Streamlit Cloud
1. Poussez ce dossier sur **GitHub** (public ou privé).
2. Allez sur [share.streamlit.io](https://share.streamlit.io) et connectez votre compte GitHub.
3. Créez une **nouvelle app** en sélectionnant:
   - Repository: votre dépôt
   - Branch: `main` (ou celle utilisée)
   - Main file path: `app.py`
4. Dans l’onglet **Advanced settings**, ajoutez si besoin des variables d’environnement.
5. Cliquez **Deploy**. Ensuite, dans *Settings → Secrets*, vous pouvez gérer les secrets si nécessaire.

> ⚠️ **Important**: ajoutez le fichier `AGENT ACHATS.xlsx` dans le dossier `data/` de votre dépôt. S'il est confidentiel, vous pouvez créer un dépôt privé.

## 🧩 Fonctionnalités
- Filtres par **site**, **statut**, **unité** et **recherche** (Code DA / Article / Désignation).
- KPIs (lignes, articles uniques, quantité totale, codes DA uniques).
- Graphiques **Plotly**: répartition par statut, top 10 articles par quantité.
- Export **CSV/Excel** des données filtrées.

## 🔧 Personnalisation
- Renommez le fichier Excel ou les colonnes ? Mettez à jour `DATA_PATH` et/ou les correspondances dans `COL_MAP_CANDIDATES` de `app.py`.
- Ajoutez d'autres pages dans `pages/` (ex.: `pages/02_Analyse_fournisseurs.py`).

## 🐛 Dépannage
- Erreur `FileNotFoundError`: placez bien le fichier sous `data/AGENT ACHATS.xlsx`.
- Problème de lecture: vérifiez que le fichier n'est pas protégé et que les noms de colonnes existent.

---
Fait avec ❤️ par l'équipe Achats.
