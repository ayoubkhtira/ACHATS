# 📦 Dashboard Achats — Demandes & Commandes

Application web développée avec **Python** et **Streamlit** pour le suivi, l’analyse et la visualisation des demandes d’achat et des commandes achats à partir de fichiers Excel.

## 🎯 Objectif du projet

Cette application permet aux utilisateurs d’importer un fichier Excel contenant des données achats afin de :

- analyser les demandes d’achat,
- analyser les commandes achats,
- suivre les articles les plus demandés,
- identifier les meilleurs fournisseurs,
- filtrer les données par période, fournisseur, division, GAc ou demandeur,
- visualiser les KPI achats,
- exporter les données filtrées.

## 🧾 Données attendues

Le fichier Excel peut contenir une ou deux feuilles :

- une feuille pour les demandes d’achat,
- une feuille pour les commandes achats.

### Colonnes attendues pour les demandes d’achat

```text
Dem.achat | Poste | Article | Désignation | GAc | Créé par | Demandeur | Quantité | UQ | Date DA | Date lanc.
