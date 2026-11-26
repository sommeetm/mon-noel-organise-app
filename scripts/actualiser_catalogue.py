#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur du catalogue d'idées cadeaux précis pour « Mon Noël organisé ».
Chaque article possède une référence exacte, une enseigne reconnue,
un prix indicatif en euros et une description claire.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

CATALOGUE_ARTICLES = [
    # --- Cinéma & Séries ---
    {
        "id": "CAD-001",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray Batman : L'Intégrale des 4 films (1989-1997)",
        "enseigne": "Amazon",
        "prix": 39.99,
        "devise": "EUR",
        "description": "Réunit les quatre films de Tim Burton et Joel Schumacher en haute définition."
    },
    {
        "id": "CAD-002",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray 4K Ultra HD Le Seigneur des Anneaux : La Trilogie (Versions longues)",
        "enseigne": "Fnac",
        "prix": 79.99,
        "devise": "EUR",
        "description": "Les trois volets réalisés par Peter Jackson remasterisés en 4K HDR."
    },
    {
        "id": "CAD-003",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret DVD Intégrale Kaamelott : Livres I à VI",
        "enseigne": "Cultura",
        "prix": 64.99,
        "devise": "EUR",
        "description": "L'intégralité de la série culte d'Alexandre Astier avec bonus et bêtisiers."
    },
    # --- High-Tech & Audio ---
    {
        "id": "CAD-004",
        "categorie": "High-Tech & Audio",
        "titre": "Enceinte Bluetooth portable JBL Flip 6 Noir",
        "enseigne": "Fnac",
        "prix": 119.99,
        "devise": "EUR",
        "description": "Enceinte nomade étanche IP67 avec 12 heures d'autonomie et son stéréo puissant."
    },
    {
        "id": "CAD-005",
        "categorie": "High-Tech & Audio",
        "titre": "Liseuse Kindle Paperwhite (16 Go, écran 6,8 pouces sans reflets)",
        "enseigne": "Amazon",
        "prix": 159.99,
        "devise": "EUR",
        "description": "Éclairage chaud réglable, autonomie de plusieurs semaines et résistance à l'eau."
    },
    {
        "id": "CAD-006",
        "categorie": "High-Tech & Audio",
        "titre": "Casque sans fil à réduction de bruit Sony WH-CH720N",
        "enseigne": "Boulanger",
        "prix": 99.99,
        "devise": "EUR",
        "description": "Casque circum-aural léger avec réduction active du bruit et 35 heures d'autonomie."
    },
    # --- Jeux & Société ---
    {
        "id": "CAD-007",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Les Aventuriers du Rail : Europe",
        "enseigne": "Cultura",
        "prix": 44.95,
        "devise": "EUR",
        "description": "Un classique familial accessible et stratégique pour relier les grandes villes européennes."
    },
    {
        "id": "CAD-008",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Skyjo (édition française Magilano)",
        "enseigne": "Amazon",
        "prix": 15.95,
        "devise": "EUR",
        "description": "Jeu de cartes rapide et convivial idéal pour animer les soirées en famille."
    },
    {
        "id": "CAD-009",
        "categorie": "Jeux & Société",
        "titre": "Set LEGO Icons 10311 L'Orchidée",
        "enseigne": "Fnac",
        "prix": 49.99,
        "devise": "EUR",
        "description": "Plante décorative à construire de 608 pièces avec vase cannelé inclus."
    },
    # --- Livres & BD ---
    {
        "id": "CAD-010",
        "categorie": "Livres & BD",
        "titre": "Beau livre L'Art de Filmer — Guide pratique complet de réalisation vidéo",
        "enseigne": "Fnac",
        "prix": 35.00,
        "devise": "EUR",
        "description": "Ouvrage illustré complet consacré aux techniques de cadrage, lumière et narration vidéo."
    },
    {
        "id": "CAD-011",
        "categorie": "Livres & BD",
        "titre": "Coffret BD Blacksad : Intégrale des tomes 1 à 5 (Dargaud)",
        "enseigne": "Cultura",
        "prix": 75.00,
        "devise": "EUR",
        "description": "Les cinq premières enquêtes du détective John Blacksad par Juan Díaz Canales et Juanjo Guarnido."
    },
    {
        "id": "CAD-012",
        "categorie": "Livres & BD",
        "titre": "Livre de cuisine Simplissime : Le livre de cuisine le plus facile du monde (J.-F. Mallet)",
        "enseigne": "Amazon",
        "prix": 21.95,
        "devise": "EUR",
        "description": "200 recettes illustrées réalisables avec 2 à 6 ingrédients maximum."
    },
    # --- Gastronomie ---
    {
        "id": "CAD-013",
        "categorie": "Gastronomie",
        "titre": "Coffret dégustation 6 thés grands crus Palais des Thés",
        "enseigne": "Nature & Découvertes",
        "prix": 34.00,
        "devise": "EUR",
        "description": "Assortiment de 6 boîtes métalliques de thés noirs, verts et parfumés prêts à offrir."
    },
    {
        "id": "CAD-014",
        "categorie": "Gastronomie",
        "titre": "Machine à expresso Krups Pixie Nespresso Titane",
        "enseigne": "Darty",
        "prix": 119.99,
        "devise": "EUR",
        "description": "Cafetière compacte haute pression 19 bars avec arrêt automatique et chauffe rapide."
    },
    {
        "id": "CAD-015",
        "categorie": "Gastronomie",
        "titre": "Coffret découverte 5 huiles d'olive et vinaigres balsamiques Oliviers & Co",
        "enseigne": "Galeries Lafayette",
        "prix": 49.50,
        "devise": "EUR",
        "description": "Sélection gastronomique méditerranéenne présentée dans un coffret cadeau."
    },
    # --- Maison & Déco ---
    {
        "id": "CAD-016",
        "categorie": "Maison & Déco",
        "titre": "Diffuseur d'huiles essentielles par ultrason Cera",
        "enseigne": "Nature & Découvertes",
        "prix": 54.95,
        "devise": "EUR",
        "description": "Diffuseur en céramique et bois d'hévéa avec lumière d'ambiance douce."
    },
    {
        "id": "CAD-017",
        "categorie": "Maison & Déco",
        "titre": "Lampe nomade rechargeable Fatboy Edison the Petit",
        "enseigne": "Boulanger",
        "prix": 69.00,
        "devise": "EUR",
        "description": "Lampe de table sans fil avec trois niveaux d'intensité lumineuse."
    },
    {
        "id": "CAD-018",
        "categorie": "Maison & Déco",
        "titre": "Plaid polaire sherpa double face 130x170 cm Gris anthracite",
        "enseigne": "Maisons du Monde",
        "prix": 29.99,
        "devise": "EUR",
        "description": "Plaid chaud et doux pour les soirées d'hiver au salon."
    }
]


def valider_article(article: dict) -> None:
    """Vérifie qu'aucun article n'utilise de libellé générique ou multi-enseignes."""
    champs_requis = {"id", "categorie", "titre", "enseigne", "prix", "devise", "description"}
    manquants = champs_requis - set(article.keys())
    if manquants:
        raise ValueError(f"Champs manquants pour {article.get('id')}: {manquants}")

    if " / " in article["enseigne"]:
        raise ValueError(
            f"Enseigne multiple interdite sur {article['id']}: {article['enseigne']}"
        )

    if not isinstance(article["prix"], (int, float)) or article["prix"] <= 0:
        raise ValueError(f"Prix invalide sur {article['id']}: {article['prix']}")


def generer_catalogue(chemin_sortie: Path) -> dict:
    for article in CATALOGUE_ARTICLES:
        valider_article(article)

    payload = {
        "meta": {
            "projet": "Mon Noël organisé",
            "date_mise_a_jour": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "nombre_articles": len(CATALOGUE_ARTICLES),
            "devise": "EUR"
        },
        "articles": CATALOGUE_ARTICLES
    }

    chemin_sortie.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "
",
        encoding="utf-8"
    )
    return payload


if __name__ == "__main__":
    racine = Path(__file__).resolve().parent.parent
    fichier_json = racine / "catalogue.json"
    resultat = generer_catalogue(fichier_json)
    print(f"Catalogue généré : {resultat['meta']['nombre_articles']} articles précis dans {fichier_json}")
