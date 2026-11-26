#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur du catalogue d'idées cadeaux précis pour « Mon Noël organisé ».
Contient 336 références nommées, chacune rattachée à une enseigne
reconnue, un prix indicatif en euros, une description claire et une
recherche automatique d'image via APIs publiques gratuites (sans clé API).
"""

import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.parse import quote
from urllib.request import Request, urlopen

USER_AGENT = "MonNoelOrganiseBot/1.0 (https://github.com; contact@example.org)"
TIMEOUT_SECONDS = 8
REQUEST_PAUSE = 0.25

CATALOGUE_ARTICLES = [
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
    {
        "id": "CAD-004",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray Retour vers le Futur : La Trilogie (35e Anniversaire)",
        "enseigne": "Fnac",
        "prix": 29.99,
        "devise": "EUR",
        "description": "Les trois aventures de Marty McFly et Doc Brown avec disque bonus."
    },
    {
        "id": "CAD-005",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray Indiana Jones : L'Intégrale des 4 premiers films",
        "enseigne": "Amazon",
        "prix": 34.99,
        "devise": "EUR",
        "description": "Les aventures d'Indiana Jones en version restaurée haute définition."
    },
    {
        "id": "CAD-006",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray 4K Dune : Première et Deuxième Parties",
        "enseigne": "Fnac",
        "prix": 44.99,
        "devise": "EUR",
        "description": "Le diptyque de science-fiction de Denis Villeneuve en 4K Ultra HD."
    },
    {
        "id": "CAD-007",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret DVD Intégrale Friends : Saisons 1 à 10",
        "enseigne": "Cultura",
        "prix": 59.99,
        "devise": "EUR",
        "description": "Les 236 épisodes de la sitcom culte réunis dans un coffret intégral."
    },
    {
        "id": "CAD-008",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray Harry Potter : L'Intégrale des 8 films",
        "enseigne": "Amazon",
        "prix": 49.99,
        "devise": "EUR",
        "description": "Toute la saga cinématographique Poudlard en Blu-ray."
    },
    {
        "id": "CAD-009",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray Star Wars : La Saga Skywalker (9 films)",
        "enseigne": "Fnac",
        "prix": 89.99,
        "devise": "EUR",
        "description": "Les neuf épisodes de la saga réunis dans un coffret collector."
    },
    {
        "id": "CAD-010",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret DVD Le Gendarme de Saint-Tropez : L'Intégrale des 6 films",
        "enseigne": "Cultura",
        "prix": 24.99,
        "devise": "EUR",
        "description": "Les six comédies avec Louis de Funès remasterisées."
    },
    {
        "id": "CAD-011",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray Jurassic Park : La Trilogie originale",
        "enseigne": "Amazon",
        "prix": 22.99,
        "devise": "EUR",
        "description": "Les trois films de dinosaures de Steven Spielberg et Joe Johnston."
    },
    {
        "id": "CAD-012",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray 4K Matrix : La Trilogie",
        "enseigne": "Fnac",
        "prix": 49.99,
        "devise": "EUR",
        "description": "La trilogie des sœurs Wachowski en 4K Ultra HD."
    },
    {
        "id": "CAD-013",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret DVD Breaking Bad : L'Intégrale de la série",
        "enseigne": "Amazon",
        "prix": 54.99,
        "devise": "EUR",
        "description": "Les cinq saisons complètes de la série primée."
    },
    {
        "id": "CAD-014",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray Le Parrain : La Trilogie (50e Anniversaire)",
        "enseigne": "Fnac",
        "prix": 44.99,
        "devise": "EUR",
        "description": "Les trois chefs-d'œuvre de Francis Ford Coppola restaurés."
    },
    {
        "id": "CAD-015",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret DVD Intégrale Les Bronzés (Les 3 films)",
        "enseigne": "Cultura",
        "prix": 19.99,
        "devise": "EUR",
        "description": "Les trois comédies cultes de la troupe du Splendid."
    },
    {
        "id": "CAD-016",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray Studio Ghibli : Coffret Hayao Miyazaki (10 films)",
        "enseigne": "Fnac",
        "prix": 119.99,
        "devise": "EUR",
        "description": "Dix chefs-d'œuvre de l'animation japonaise en haute définition."
    },
    {
        "id": "CAD-017",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray James Bond : Intégrale Daniel Craig (5 films)",
        "enseigne": "Amazon",
        "prix": 39.99,
        "devise": "EUR",
        "description": "De Casino Royale à Mourir peut attendre en Blu-ray."
    },
    {
        "id": "CAD-018",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret DVD Sherlock (BBC) : Saisons 1 à 4",
        "enseigne": "Cultura",
        "prix": 29.99,
        "devise": "EUR",
        "description": "Les enquêtes modernes avec Benedict Cumberbatch et Martin Freeman."
    },
    {
        "id": "CAD-019",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray 4K Interstellar + Inception + Dunkerque (Christopher Nolan)",
        "enseigne": "Fnac",
        "prix": 39.99,
        "devise": "EUR",
        "description": "Trois films majeurs de Christopher Nolan en 4K Ultra HD."
    },
    {
        "id": "CAD-020",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret DVD Marcel Pagnol : Jean de Florette et Manon des Sources",
        "enseigne": "Cultura",
        "prix": 19.99,
        "devise": "EUR",
        "description": "Le diptyque provençal réalisé par Claude Berri."
    },
    {
        "id": "CAD-021",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray Alien : Quadrilogie",
        "enseigne": "Amazon",
        "prix": 29.99,
        "devise": "EUR",
        "description": "Les quatre premiers volets de la saga de science-fiction."
    },
    {
        "id": "CAD-022",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret DVD Downton Abbey : L'Intégrale de la série (Saisons 1 à 6)",
        "enseigne": "Fnac",
        "prix": 49.99,
        "devise": "EUR",
        "description": "La chronique historique de la famille Crawley."
    },
    {
        "id": "CAD-023",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray Spider-Man : Trilogie Sam Raimi",
        "enseigne": "Amazon",
        "prix": 24.99,
        "devise": "EUR",
        "description": "Les trois films avec Tobey Maguire en Blu-ray."
    },
    {
        "id": "CAD-024",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret DVD Astérix : Les 4 films cultes (Clavier / Cornillac)",
        "enseigne": "Cultura",
        "prix": 22.99,
        "devise": "EUR",
        "description": "Quatre adaptations live des aventures d'Astérix et Obélix."
    },
    {
        "id": "CAD-025",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray 4K Blade Runner + Blade Runner 2049",
        "enseigne": "Fnac",
        "prix": 34.99,
        "devise": "EUR",
        "description": "Les deux films de science-fiction en 4K Ultra HD."
    },
    {
        "id": "CAD-026",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret DVD Intégrale Columbo : Saisons 1 à 10",
        "enseigne": "Amazon",
        "prix": 69.99,
        "devise": "EUR",
        "description": "Toutes les enquêtes du lieutenant Columbo avec Peter Falk."
    },
    {
        "id": "CAD-027",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray Pirates des Caraïbes : Intégrale des 5 films",
        "enseigne": "Fnac",
        "prix": 39.99,
        "devise": "EUR",
        "description": "Les cinq aventures du capitaine Jack Sparrow."
    },
    {
        "id": "CAD-028",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret DVD La Grande Vadrouille + Le Corniaud (Édition Collector)",
        "enseigne": "Cultura",
        "prix": 19.99,
        "devise": "EUR",
        "description": "Deux classiques de Gérard Oury avec Bourvil et Louis de Funès."
    },
    {
        "id": "CAD-029",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray Game of Thrones : L'Intégrale des Saisons 1 à 8",
        "enseigne": "Amazon",
        "prix": 99.99,
        "devise": "EUR",
        "description": "Les huit saisons complètes de la série fantastique."
    },
    {
        "id": "CAD-030",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray Clint Eastwood : Coffret Westerns (3 films)",
        "enseigne": "Fnac",
        "prix": 27.99,
        "devise": "EUR",
        "description": "Trois grands westerns classiques en haute définition."
    },
    {
        "id": "CAD-031",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret DVD Peaky Blinders : Saisons 1 à 6",
        "enseigne": "Cultura",
        "prix": 44.99,
        "devise": "EUR",
        "description": "L'intégrale de la série britannique sur le clan Shelby."
    },
    {
        "id": "CAD-032",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray Mission Impossible : Coffret 6 films",
        "enseigne": "Amazon",
        "prix": 34.99,
        "devise": "EUR",
        "description": "Six volets d'action portés par Tom Cruise."
    },
    {
        "id": "CAD-033",
        "categorie": "High-Tech & Audio",
        "titre": "Enceinte Bluetooth portable JBL Flip 6 Noir",
        "enseigne": "Fnac",
        "prix": 119.99,
        "devise": "EUR",
        "description": "Enceinte nomade étanche IP67 avec 12 heures d'autonomie et son stéréo puissant."
    },
    {
        "id": "CAD-034",
        "categorie": "High-Tech & Audio",
        "titre": "Liseuse Kindle Paperwhite (16 Go, écran 6,8 pouces sans reflets)",
        "enseigne": "Amazon",
        "prix": 159.99,
        "devise": "EUR",
        "description": "Éclairage chaud réglable, autonomie de plusieurs semaines et résistance à l'eau."
    },
    {
        "id": "CAD-035",
        "categorie": "High-Tech & Audio",
        "titre": "Casque sans fil à réduction de bruit Sony WH-CH720N",
        "enseigne": "Boulanger",
        "prix": 99.99,
        "devise": "EUR",
        "description": "Casque circum-aural léger avec réduction active du bruit et 35 heures d'autonomie."
    },
    {
        "id": "CAD-036",
        "categorie": "High-Tech & Audio",
        "titre": "Écouteurs sans fil Apple AirPods (3e génération) avec boîtier Lightning",
        "enseigne": "Darty",
        "prix": 179.0,
        "devise": "EUR",
        "description": "Audio spatial personnalisé et résistance à la transpiration et à l'eau."
    },
    {
        "id": "CAD-037",
        "categorie": "High-Tech & Audio",
        "titre": "Enceinte connectée Amazon Echo Dot (5e génération) Anthracite",
        "enseigne": "Amazon",
        "prix": 64.99,
        "devise": "EUR",
        "description": "Enceinte compacte avec assistant vocal Alexa et son amélioré."
    },
    {
        "id": "CAD-038",
        "categorie": "High-Tech & Audio",
        "titre": "Montre connectée Garmin Forerunner 55 Noire",
        "enseigne": "Boulanger",
        "prix": 169.99,
        "devise": "EUR",
        "description": "Montre GPS de course
