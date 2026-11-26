#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur du catalogue d'idées cadeaux précis pour « Mon Noël organisé ».
Contient 336 références nommées, chacune rattachée à une enseigne
reconnue, un prix indicatif en euros, une description claire et une
recherche automatique d'image produit via l'API Serper (Google Images).
"""

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.request import Request, urlopen

USER_AGENT = "MonNoelOrganiseBot/1.0 (https://github.com; contact@example.org)"
TIMEOUT_SECONDS = 10
REQUEST_PAUSE = 0.1
SERPER_IMAGES_URL = "https://google.serper.dev/images"

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
        "description": "Montre GPS de course à pied avec suivi quotidien de la santé et autonomie de 2 semaines."
    },
    {
        "id": "CAD-039",
        "categorie": "High-Tech & Audio",
        "titre": "Liseuse Kobo Clara BW (16 Go, écran E Ink Carta 1300 6 pouces)",
        "enseigne": "Fnac",
        "prix": 139.99,
        "devise": "EUR",
        "description": "Liseuse compacte étanche avec éclairage ComfortLight PRO."
    },
    {
        "id": "CAD-040",
        "categorie": "High-Tech & Audio",
        "titre": "Casque Bluetooth Marshall Major IV Noir",
        "enseigne": "Darty",
        "prix": 119.99,
        "devise": "EUR",
        "description": "Casque supra-auriculaire au design iconique offrant plus de 80 heures d'autonomie."
    },
    {
        "id": "CAD-041",
        "categorie": "High-Tech & Audio",
        "titre": "Batterie externe Anker PowerCore 20000 mAh USB-C",
        "enseigne": "Amazon",
        "prix": 45.99,
        "devise": "EUR",
        "description": "Batterie haute capacité pour recharger smartphones et tablettes plusieurs fois."
    },
    {
        "id": "CAD-042",
        "categorie": "High-Tech & Audio",
        "titre": "Platine vinyle Audio-Technica AT-LP60XUSB Noir",
        "enseigne": "Fnac",
        "prix": 159.0,
        "devise": "EUR",
        "description": "Platine tourne-disque entièrement automatique avec préampli phono intégré."
    },
    {
        "id": "CAD-043",
        "categorie": "High-Tech & Audio",
        "titre": "Enceinte Bluetooth Bose SoundLink Flex Noir",
        "enseigne": "Boulanger",
        "prix": 149.99,
        "devise": "EUR",
        "description": "Enceinte portable robuste avec technologie PositionIQ."
    },
    {
        "id": "CAD-044",
        "categorie": "High-Tech & Audio",
        "titre": "Caméra instantanée Fujifilm Instax Mini 12 Lilas",
        "enseigne": "Fnac",
        "prix": 89.99,
        "devise": "EUR",
        "description": "Appareil photo instantané avec mode gros plan et miroir selfie intégré."
    },
    {
        "id": "CAD-045",
        "categorie": "High-Tech & Audio",
        "titre": "Bracelet connecté Xiaomi Smart Band 8 Noir",
        "enseigne": "Amazon",
        "prix": 39.99,
        "devise": "EUR",
        "description": "Écran AMOLED 1,62 pouce, suivi sportif complet et 16 jours d'autonomie."
    },
    {
        "id": "CAD-046",
        "categorie": "High-Tech & Audio",
        "titre": "Station météo connectée Netatmo avec capteur extérieur",
        "enseigne": "Darty",
        "prix": 149.99,
        "devise": "EUR",
        "description": "Mesure température, humidité, qualité de l'air intérieur et pression atmosphérique."
    },
    {
        "id": "CAD-047",
        "categorie": "High-Tech & Audio",
        "titre": "Écouteurs sans fil JBL Tune Beam Noir",
        "enseigne": "Boulanger",
        "prix": 69.99,
        "devise": "EUR",
        "description": "Écouteurs intra-auriculaires avec réduction de bruit active."
    },
    {
        "id": "CAD-048",
        "categorie": "High-Tech & Audio",
        "titre": "Tablette tactile Samsung Galaxy Tab A9+ (64 Go, Wi-Fi)",
        "enseigne": "Darty",
        "prix": 219.0,
        "devise": "EUR",
        "description": "Écran 11 pouces 90 Hz et quatre haut-parleurs Dolby Atmos."
    },
    {
        "id": "CAD-049",
        "categorie": "High-Tech & Audio",
        "titre": "Radio réveil simulateur d'aube Philips Somneo HF3506/05",
        "enseigne": "Boulanger",
        "prix": 89.99,
        "devise": "EUR",
        "description": "Réveil progressif par lumière naturelle et sons apaisants."
    },
    {
        "id": "CAD-050",
        "categorie": "High-Tech & Audio",
        "titre": "Localisateur d'objets Apple AirTag (Lot de 1)",
        "enseigne": "Fnac",
        "prix": 39.0,
        "devise": "EUR",
        "description": "Balise Bluetooth pour retrouver clés, sac ou bagage via l'application Localiser."
    },
    {
        "id": "CAD-051",
        "categorie": "High-Tech & Audio",
        "titre": "Enceinte portable Ultimate Ears Wonderboom 3 Bleu",
        "enseigne": "Amazon",
        "prix": 79.99,
        "devise": "EUR",
        "description": "Son à 360 degrés, flottante et résistante aux chutes."
    },
    {
        "id": "CAD-052",
        "categorie": "High-Tech & Audio",
        "titre": "Souris sans fil ergonomique Logitech MX Master 3S",
        "enseigne": "Boulanger",
        "prix": 99.99,
        "devise": "EUR",
        "description": "Souris haute précision silencieuse avec défilement électromagnétique MagSpeed."
    },
    {
        "id": "CAD-053",
        "categorie": "High-Tech & Audio",
        "titre": "Clavier sans fil Logitech K380 Multi-Device Gris",
        "enseigne": "Fnac",
        "prix": 44.99,
        "devise": "EUR",
        "description": "Clavier compact Bluetooth compatible ordinateur, tablette et smartphone."
    },
    {
        "id": "CAD-054",
        "categorie": "High-Tech & Audio",
        "titre": "Cadre photo numérique connecté Frameo 10,1 pouces Wi-Fi",
        "enseigne": "Amazon",
        "prix": 89.99,
        "devise": "EUR",
        "description": "Permet d'envoyer des photos à distance directement depuis son smartphone."
    },
    {
        "id": "CAD-055",
        "categorie": "High-Tech & Audio",
        "titre": "Mini projecteur portable Anker Nebula Capsule",
        "enseigne": "Amazon",
        "prix": 299.99,
        "devise": "EUR",
        "description": "Picoprojecteur format canette avec haut-parleur 360° intégré."
    },
    {
        "id": "CAD-056",
        "categorie": "High-Tech & Audio",
        "titre": "Casque gaming filaire HyperX Cloud II Rouge/Noir",
        "enseigne": "Fnac",
        "prix": 79.99,
        "devise": "EUR",
        "description": "Casque confortable avec coussinets à mémoire de forme et son surround 7.1."
    },
    {
        "id": "CAD-057",
        "categorie": "High-Tech & Audio",
        "titre": "Chargeur sans fil induction Belkin BoostCharge 15W",
        "enseigne": "Darty",
        "prix": 34.99,
        "devise": "EUR",
        "description": "Socle de charge rapide compatible Qi pour smartphone."
    },
    {
        "id": "CAD-058",
        "categorie": "High-Tech & Audio",
        "titre": "Réveil numérique avec station de charge USB Lexon Flip Classic",
        "enseigne": "Fnac",
        "prix": 39.9,
        "devise": "EUR",
        "description": "Réveil réversible design ON/OFF par simple retournement."
    },
    {
        "id": "CAD-059",
        "categorie": "High-Tech & Audio",
        "titre": "Enceinte Bluetooth JBL Go 4 Rouge",
        "enseigne": "Boulanger",
        "prix": 49.99,
        "devise": "EUR",
        "description": "Ultra-compacte avec dragonne intégrée et étanchéité IP67."
    },
    {
        "id": "CAD-060",
        "categorie": "High-Tech & Audio",
        "titre": "Webcam Full HD 1080p Logitech C920 HD Pro",
        "enseigne": "Amazon",
        "prix": 74.99,
        "devise": "EUR",
        "description": "Caméra USB avec mise au point automatique et double micro stéréo."
    },
    {
        "id": "CAD-061",
        "categorie": "High-Tech & Audio",
        "titre": "Liseuse Vivlio Light HD Color (16 Go, écran couleur 6 pouces)",
        "enseigne": "Cultura",
        "prix": 159.99,
        "devise": "EUR",
        "description": "Idéale pour lire romans, BD et albums illustrés en couleur."
    },
    {
        "id": "CAD-062",
        "categorie": "High-Tech & Audio",
        "titre": "Montre connectée Huawei Watch Fit 2 Noire",
        "enseigne": "Darty",
        "prix": 119.99,
        "devise": "EUR",
        "description": "Écran AMOLED rectangulaire 1,74 pouce et appels Bluetooth."
    },
    {
        "id": "CAD-063",
        "categorie": "High-Tech & Audio",
        "titre": "Écouteurs à conduction osseuse Shokz OpenRun Noir",
        "enseigne": "Boulanger",
        "prix": 139.99,
        "devise": "EUR",
        "description": "Écouteurs sport à oreilles libres légers et résistants à la sueur."
    },
    {
        "id": "CAD-064",
        "categorie": "High-Tech & Audio",
        "titre": "Dictaphone numérique Sony ICD-PX470",
        "enseigne": "Fnac",
        "prix": 69.99,
        "devise": "EUR",
        "description": "Enregistreur vocal stéréo avec connecteur USB direct intégré."
    },
    {
        "id": "CAD-065",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Les Aventuriers du Rail : Europe",
        "enseigne": "Cultura",
        "prix": 44.95,
        "devise": "EUR",
        "description": "Un classique familial accessible et stratégique pour relier les grandes villes européennes."
    },
    {
        "id": "CAD-066",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Skyjo (édition française Magilano)",
        "enseigne": "Amazon",
        "prix": 15.95,
        "devise": "EUR",
        "description": "Jeu de cartes rapide et convivial idéal pour animer les soirées en famille."
    },
    {
        "id": "CAD-067",
        "categorie": "Jeux & Société",
        "titre": "Set LEGO Icons 10311 L'Orchidée",
        "enseigne": "Fnac",
        "prix": 49.99,
        "devise": "EUR",
        "description": "Plante décorative à construire de 608 pièces avec vase cannelé inclus."
    },
    {
        "id": "CAD-068",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Dixit (édition française Libellud)",
        "enseigne": "Cultura",
        "prix": 29.99,
        "devise": "EUR",
        "description": "Jeu d'imagination et de poésie autour de cartes magnifiquement illustrées."
    },
    {
        "id": "CAD-069",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Catan (Les Colons de Catane - édition Kosmos)",
        "enseigne": "Fnac",
        "prix": 39.99,
        "devise": "EUR",
        "description": "Jeu de gestion de ressources, de commerce et de développement sur une île."
    },
    {
        "id": "CAD-070",
        "categorie": "Jeux & Société",
        "titre": "Jeu d'ambiance Code Names (édition française Iello)",
        "enseigne": "Cultura",
        "prix": 21.99,
        "devise": "EUR",
        "description": "Jeu d'association d'idées en équipe pour 2 à 8 joueurs."
    },
    {
        "id": "CAD-071",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Azul (édition française Next Move)",
        "enseigne": "Amazon",
        "prix": 39.9,
        "devise": "EUR",
        "description": "Jeu de placement de tuiles inspiré des azulejos portugais."
    },
    {
        "id": "CAD-072",
        "categorie": "Jeux & Société",
        "titre": "Set LEGO Technic 42151 La Bugatti Bolide",
        "enseigne": "Amazon",
        "prix": 44.99,
        "devise": "EUR",
        "description": "Maquette détaillée avec moteur W16 fonctionnel et direction."
    },
    {
        "id": "CAD-073",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société 7 Wonders (Nouvelle Édition - Repos Production)",
        "enseigne": "Fnac",
        "prix": 44.95,
        "devise": "EUR",
        "description": "Jeu de draft de cartes où chaque joueur développe une cité antique."
    },
    {
        "id": "CAD-074",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Trio (édition française Cocktail Games)",
        "enseigne": "Cultura",
        "prix": 12.99,
        "devise": "EUR",
        "description": "Petit jeu de déduction et de mémoire rapide et malin."
    },
    {
        "id": "CAD-075",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Carcassonne (édition française Z-Man Games)",
        "enseigne": "Amazon",
        "prix": 29.99,
        "devise": "EUR",
        "description": "Jeu de pose de tuiles médiéval simple à apprendre et très rejouable."
    },
    {
        "id": "CAD-076",
        "categorie": "Jeux & Société",
        "titre": "Set LEGO Botanicals 10280 Le Bouquet de Fleurs",
        "enseigne": "Fnac",
        "prix": 54.99,
        "devise": "EUR",
        "description": "Bouquet de 756 pièces à composer avec tiges ajustables."
    },
    {
        "id": "CAD-077",
        "categorie": "Jeux & Société",
        "titre": "Jeu d'ambiance Blanc-Manger Coco : Le Jeu de base",
        "enseigne": "Cultura",
        "prix": 24.99,
        "devise": "EUR",
        "description": "Jeu d'humour décalé pour soirées entre adultes."
    },
    {
        "id": "CAD-078",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Splendor (édition française Space Cowboys)",
        "enseigne": "Fnac",
        "prix": 32.99,
        "devise": "EUR",
        "description": "Jeu de collection de gemmes et de développement à la Renaissance."
    },
    {
        "id": "CAD-079",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Unlock! Game Adventures (3 scénarios)",
        "enseigne": "Cultura",
        "prix": 34.99,
        "devise": "EUR",
        "description": "Escape game coopératif sur table inspiré de jeux de plateau célèbres."
    },
    {
        "id": "CAD-080",
        "categorie": "Jeux & Société",
        "titre": "Puzzle Ravensburger 1000 pièces : Le Château de Neuschwanstein",
        "enseigne": "Amazon",
        "prix": 16.99,
        "devise": "EUR",
        "description": "Puzzle de qualité supérieure avec pièces découpées avec précision."
    },
    {
        "id": "CAD-081",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Mysterium (édition française Libellud)",
        "enseigne": "Fnac",
        "prix": 39.99,
        "devise": "EUR",
        "description": "Jeu d'enquête coopératif asymétrique dans un manoir hanté."
    },
    {
        "id": "CAD-082",
        "categorie": "Jeux & Société",
        "titre": "Set LEGO Star Wars 75304 Le Casque de Dark Vador",
        "enseigne": "Amazon",
        "prix": 69.99,
        "devise": "EUR",
        "description": "Modèle d'exposition collector de 834 pièces avec socle."
    },
    {
        "id": "CAD-083",
        "categorie": "Jeux & Société",
        "titre": "Jeu de cartes The Mind (édition française Oya)",
        "enseigne": "Cultura",
        "prix": 13.5,
        "devise": "EUR",
        "description": "Défi coopératif silencieux où il faut poser ses cartes dans l'ordre croissant."
    },
    {
        "id": "CAD-084",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Concept (édition française Repos Production)",
        "enseigne": "Fnac",
        "prix": 31.99,
        "devise": "EUR",
        "description": "Faites deviner des mots en combinant des icônes universelles."
    },
    {
        "id": "CAD-085",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Pandemic (édition française Z-Man Games)",
        "enseigne": "Amazon",
        "prix": 36.99,
        "devise": "EUR",
        "description": "Jeu coopératif où les joueurs incarnent une équipe de spécialistes."
    },
    {
        "id": "CAD-086",
        "categorie": "Jeux & Société",
        "titre": "Coffret Échecs et Dames en bois pliable 35x35 cm",
        "enseigne": "Nature & Découvertes",
        "prix": 39.95,
        "devise": "EUR",
        "description": "Plateau marqueté avec rangement intérieur pour les pièces en bois."
    },
    {
        "id": "CAD-087",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Dobble Classic (édition Zygomatic)",
        "enseigne": "Cultura",
        "prix": 14.99,
        "devise": "EUR",
        "description": "Jeu d'observation et de rapidité dans sa boîte métallique ronde."
    },
    {
        "id": "CAD-088",
        "categorie": "Jeux & Société",
        "titre": "Set LEGO Creator 3-en-1 31129 Le Tigre Majestueux",
        "enseigne": "Fnac",
        "prix": 44.99,
        "devise": "EUR",
        "description": "Permet de construire au choix un tigre, un panda roux ou une carpe koï."
    },
    {
        "id": "CAD-089",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société MicroMacro : Crime City (édition Blackrock)",
        "enseigne": "Cultura",
        "prix": 26.99,
        "devise": "EUR",
        "description": "Jeu d'enquête coopératif sur une immense carte de ville illustrée."
    },
    {
        "id": "CAD-090",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société 6 qui prend! (édition Gigamic)",
        "enseigne": "Amazon",
        "prix": 12.99,
        "devise": "EUR",
        "description": "Jeu de cartes tactique incontournable jusqu'à 10 joueurs."
    },
    {
        "id": "CAD-091",
        "categorie": "Jeux & Société",
        "titre": "Puzzle Djeco 1000 pièces Gallery : La Jungle",
        "enseigne": "Cultura",
        "prix": 18.95,
        "devise": "EUR",
        "description": "Puzzle panoramique grand format au style graphique contemporain."
    },
    {
        "id": "CAD-092",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Harmonies (édition Libellud)",
        "enseigne": "Fnac",
        "prix": 32.99,
        "devise": "EUR",
        "description": "Créez des paysages en 3D pour accueillir la faune sauvage."
    },
    {
        "id": "CAD-093",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Time's Up! Family 1",
        "enseigne": "Amazon",
        "prix": 21.99,
        "devise": "EUR",
        "description": "Faites deviner des mots en trois manches : description, un mot, mime."
    },
    {
        "id": "CAD-094",
        "categorie": "Jeux & Société",
        "titre": "Set LEGO Harry Potter 76419 Le Château et le Domaine de Poudlard",
        "enseigne": "Fnac",
        "prix": 149.99,
        "devise": "EUR",
        "description": "Maquette architecturale détaillée de 2660 pièces."
    },
    {
        "id": "CAD-095",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Azul : Pavillon d'Été",
        "enseigne": "Cultura",
        "prix": 39.9,
        "devise": "EUR",
        "description": "Variante stratégique autour des tuiles en forme de losange."
    },
    {
        "id": "CAD-096",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Exploding Kittens (édition française)",
        "enseigne": "Amazon",
        "prix": 19.99,
        "devise": "EUR",
        "description": "Jeu de cartes explosif et humoristique aux parties rapides."
    },
    {
        "id": "CAD-097",
        "categorie": "Livres & BD",
        "titre": "Beau livre L'Art de Filmer — Guide pratique complet de réalisation vidéo",
        "enseigne": "Fnac",
        "prix": 35.0,
        "devise": "EUR",
        "description": "Ouvrage illustré complet consacré aux techniques de cadrage, lumière et narration vidéo."
    },
    {
        "id": "CAD-098",
        "categorie": "Livres & BD",
        "titre": "Coffret BD Blacksad : Intégrale des tomes 1 à 5 (Dargaud)",
        "enseigne": "Cultura",
        "prix": 75.0,
        "devise": "EUR",
        "description": "Les cinq premières enquêtes du détective John Blacksad par Juan Díaz Canales et Juanjo Guarnido."
    },
    {
        "id": "CAD-099",
        "categorie": "Livres & BD",
        "titre": "Livre de cuisine Simplissime : Le livre de cuisine le plus facile du monde (J.-F. Mallet)",
        "enseigne": "Amazon",
        "prix": 21.95,
        "devise": "EUR",
        "description": "200 recettes illustrées réalisables avec 2 à 6 ingrédients maximum."
    },
    {
        "id": "CAD-100",
        "categorie": "Livres & BD",
        "titre": "Roman Le Comte de Monte-Cristo — Alexandre Dumas (Édition reliée collector)",
        "enseigne": "Fnac",
        "prix": 24.9,
        "devise": "EUR",
        "description": "Le chef-d'œuvre d'aventures et de vengeance dans une belle édition reliée."
    },
    {
        "id": "CAD-101",
        "categorie": "Livres & BD",
        "titre": "BD Astérix : L'Iris blanc — Album n°40 (Éditions Albert René)",
        "enseigne": "Cultura",
        "prix": 10.95,
        "devise": "EUR",
        "description": "Le quarantième album des aventures d'Astérix signé Fabcaro et Didier Conrad."
    },
    {
        "id": "CAD-102",
        "categorie": "Livres & BD",
        "titre": "Beau livre La Terre vue du Ciel — Yann Arthus-Bertrand (Éditions de La Martinière)",
        "enseigne": "Fnac",
        "prix": 39.9,
        "devise": "EUR",
        "description": "Les plus célèbres photographies aériennes de la planète."
    },
    {
        "id": "CAD-103",
        "categorie": "Livres & BD",
        "titre": "Coffret Manga Demon Slayer : Coffret Intégrale Saison 1 (Tomes 1 à 7 - Panini)",
        "enseigne": "Cultura",
        "prix": 51.03,
        "devise": "EUR",
        "description": "Les sept premiers volumes du célèbre manga de Koyoharu Gotouge."
    },
    {
        "id": "CAD-104",
        "categorie": "Livres & BD",
        "titre": "Roman L'Anomalie — Hervé Le Tellier (Gallimard Folio)",
        "enseigne": "Amazon",
        "prix": 9.2,
        "devise": "EUR",
        "description": "Prix Goncourt captivant mêlant suspense, humour et vertige scientifique."
    },
    {
        "id": "CAD-105",
        "categorie": "Livres & BD",
        "titre": "Livre de pâtisserie Le Grand Cours de Pâtisserie — Ferrandi Paris (Flammarion)",
        "enseigne": "Fnac",
        "prix": 49.95,
        "devise": "EUR",
        "description": "Techniques de base, recettes illustrées pas à pas et créations de chefs."
    },
    {
        "id": "CAD-106",
        "categorie": "Livres & BD",
        "titre": "BD L'Arabe du futur : Tome 1 (1978-1984) — Riad Sattouf (Allary Éditions)",
        "enseigne": "Cultura",
        "prix": 22.9,
        "devise": "EUR",
        "description": "Le premier volet de la série autobiographique maintes fois primée."
    },
    {
        "id": "CAD-107",
        "categorie": "Livres & BD",
        "titre": "Atlas Le Grand Atlas du Monde — National Geographic",
        "enseigne": "Fnac",
        "prix": 45.0,
        "devise": "EUR",
        "description": "Cartographie détaillée, données géographiques et photographies."
    },
    {
        "id": "CAD-108",
        "categorie": "Livres & BD",
        "titre": "Roman Kilomètre zéro — Maud Ankaoua (Eyrolles)",
        "enseigne": "Amazon",
        "prix": 9.9,
        "devise": "EUR",
        "description": "Roman initiatique best-seller autour du développement personnel et du voyage."
    },
    {
        "id": "CAD-109",
        "categorie": "Livres & BD",
        "titre": "BD Blake et Mortimer : La Marque Jaune (Éditions Blake et Mortimer)",
        "enseigne": "Cultura",
        "prix": 16.5,
        "devise": "EUR",
        "description": "L'aventure londonienne culte signée Edgar P. Jacobs."
    },
    {
        "id": "CAD-110",
        "categorie": "Livres & BD",
        "titre": "Beau livre Histoire de France en 100 cartes (Éditions Autrement)",
        "enseigne": "Fnac",
        "prix": 29.9,
        "devise": "EUR",
        "description": "Les grandes étapes de l'histoire française expliquées par la cartographie."
    },
    {
        "id": "CAD-111",
        "categorie": "Livres & BD",
        "titre": "Livre de cuisine On va déguster la France — François-Régis Gaudry (Marabout)",
        "enseigne": "Amazon",
        "prix": 42.0,
        "devise": "EUR",
        "description": "Encyclopédie gourmande des spécialités, produits et recettes des régions françaises."
    },
    {
        "id": "CAD-112",
        "categorie": "Livres & BD",
        "titre": "BD Tintin : Objectif Lune + On a marché sur la Lune (Casterman)",
        "enseigne": "Cultura",
        "prix": 25.0,
        "devise": "EUR",
        "description": "Le diptyque spatial incontournable d'Hergé."
    },
    {
        "id": "CAD-113",
        "categorie": "Livres & BD",
        "titre": "Roman Changer l'eau des fleurs — Valérie Perrin (Le Livre de Poche)",
        "enseigne": "Fnac",
        "prix": 9.4,
        "devise": "EUR",
        "description": "Roman émouvant salué par de nombreux prix des lecteurs."
    },
    {
        "id": "CAD-114",
        "categorie": "Livres & BD",
        "titre": "Beau livre Le Petit Prince — Antoine de Saint-Exupéry (Édition grand format Gallimard)",
        "enseigne": "Cultura",
        "prix": 22.0,
        "devise": "EUR",
        "description": "Le conte philosophique illustré des aquarelles originales de l'auteur."
    },
    {
        "id": "CAD-115",
        "categorie": "Livres & BD",
        "titre": "Coffret BD Gaston Lagaffe : Coffret 5 albums classiques (Dupuis)",
        "enseigne": "Fnac",
        "prix": 59.0,
        "devise": "EUR",
        "description": "Les gaffes légendaires créées par André Franquin."
    },
    {
        "id": "CAD-116",
        "categorie": "Livres & BD",
        "titre": "Livre jardinage Le Guide Clause du Jardinage (Éditions Ulmer)",
        "enseigne": "Amazon",
        "prix": 34.9,
        "devise": "EUR",
        "description": "La référence complète pour entretenir potager, verger et plantes d'ornement."
    },
    {
        "id": "CAD-117",
        "categorie": "Livres & BD",
        "titre": "Roman Les Sept Sœurs : Tome 1 — Lucinda Riley (Le Livre de Poche)",
        "enseigne": "Cultura",
        "prix": 9.7,
        "devise": "EUR",
        "description": "Premier tome de la saga familiale internationale."
    },
    {
        "id": "CAD-118",
        "categorie": "Livres & BD",
        "titre": "Beau livre Cinéma : Les 1001 films qu'il faut avoir vus dans sa vie (Omnibus)",
        "enseigne": "Fnac",
        "prix": 36.0,
        "devise": "EUR",
        "description": "Panorama chronologique des chefs-d'œuvre du septième art."
    },
    {
        "id": "CAD-119",
        "categorie": "Livres & BD",
        "titre": "BD Corto Maltese : La Ballade de la mer salée (Casterman)",
        "enseigne": "Cultura",
        "prix": 29.0,
        "devise": "EUR",
        "description": "L'œuvre fondatrice d'Hugo Pratt en grand format."
    },
    {
        "id": "CAD-120",
        "categorie": "Livres & BD",
        "titre": "Livre bien-être Les Quatre Accords Toltèques — Don Miguel Ruiz (Jouvence)",
        "enseigne": "Amazon",
        "prix": 11.9,
        "devise": "EUR",
        "description": "Guide pratique de liberté personnelle vendu à des millions d'exemplaires."
    },
    {
        "id": "CAD-121",
        "categorie": "Livres & BD",
        "titre": "Roman Dune : Tome 1 — Frank Herbert (Édition Collector Robert Laffont)",
        "enseigne": "Fnac",
        "prix": 26.9,
        "devise": "EUR",
        "description": "Le monument de la science-fiction dans une édition reliée soignée."
    },
    {
        "id": "CAD-122",
        "categorie": "Livres & BD",
        "titre": "Beau livre Le Louvre : Toutes les peintures (Éditions Place des Victoires)",
        "enseigne": "Cultura",
        "prix": 39.95,
        "devise": "EUR",
        "description": "Catalogue illustré des chefs-d'œuvre picturaux du musée du Louvre."
    },
    {
        "id": "CAD-123",
        "categorie": "Livres & BD",
        "titre": "BD Mortelle Adèle : Tome 1 — Tout ça finira mal (Bayard)",
        "enseigne": "Amazon",
        "prix": 11.95,
        "devise": "EUR",
        "description": "Le premier tome de la série jeunesse humoristique plébiscitée par les enfants."
    },
    {
        "id": "CAD-124",
        "categorie": "Livres & BD",
        "titre": "Livre photo Composer ses photos — Michael Freeman (Eyrolles)",
        "enseigne": "Fnac",
        "prix": 26.0,
        "devise": "EUR",
        "description": "Les règles et astuces de cadrage pour réussir ses photographies."
    },
    {
        "id": "CAD-125",
        "categorie": "Livres & BD",
        "titre": "Roman La Vie secrète des écrivains — Guillaume Musso (Le Livre de Poche)",
        "enseigne": "Cultura",
        "prix": 8.9,
        "devise": "EUR",
        "description": "Thriller littéraire se déroulant sur une île méditerranéenne."
    },
    {
        "id": "CAD-126",
        "categorie": "Livres & BD",
        "titre": "Coffret Manga Spy x Family : Coffret Tomes 1 à 3 (Kurokawa)",
        "enseigne": "Fnac",
        "prix": 22.5,
        "devise": "EUR",
        "description": "Les débuts de la famille Forger mêlant espionnage et comédie."
    },
    {
        "id": "CAD-127",
        "categorie": "Gastronomie",
        "titre": "Coffret dégustation 6 thés grands crus Palais des Thés",
        "enseigne": "Nature & Découvertes",
        "prix": 34.0,
        "devise": "EUR",
        "description": "Assortiment de 6 boîtes métalliques de thés noirs, verts et parfumés prêts à offrir."
    },
    {
        "id": "CAD-128",
        "categorie": "Gastronomie",
        "titre": "Machine à expresso Krups Pixie Nespresso Titane",
        "enseigne": "Darty",
        "prix": 119.99,
        "devise": "EUR",
        "description": "Cafetière compacte haute pression 19 bars avec arrêt automatique et chauffe rapide."
    },
    {
        "id": "CAD-129",
        "categorie": "Gastronomie",
        "titre": "Coffret découverte 5 huiles d'olive et vinaigres balsamiques Oliviers & Co",
        "enseigne": "Galeries Lafayette",
        "prix": 49.5,
        "devise": "EUR",
        "description": "Sélection gastronomique méditerranéenne présentée dans un coffret cadeau."
    },
    {
        "id": "CAD-130",
        "categorie": "Gastronomie",
        "titre": "Ballotin de chocolats assortis Leonidas 500 g",
        "enseigne": "Amazon",
        "prix": 29.9,
        "devise": "EUR",
        "description": "Assortiment de pralinés, ganaches et caramels belges."
    },
    {
        "id": "CAD-131",
        "categorie": "Gastronomie",
        "titre": "Coffret 24 sachets de thés et infusions bio Kusmi Tea Les Essentiels",
        "enseigne": "Nature & Découvertes",
        "prix": 26.9,
        "devise": "EUR",
        "description": "Sélection des recettes emblématiques Anastasia, Prince Vladimir et AquaRosa."
    },
    {
        "id": "CAD-132",
        "categorie": "Gastronomie",
        "titre": "Appareil à raclette Tefal Colormania 6 personnes",
        "enseigne": "Boulanger",
        "prix": 49.99,
        "devise": "EUR",
        "description": "Appareil convivial avec 6 coupelles antiadhésives et indicateur Thermo-Spot."
    },
    {
        "id": "CAD-133",
        "categorie": "Gastronomie",
        "titre": "Coffret dégustation 4 miels de France Famille Mary",
        "enseigne": "Nature & Découvertes",
        "prix": 24.95,
        "devise": "EUR",
        "description": "Miels d'acacia, de lavande, de forêt et de montagne récoltés en France."
    },
    {
        "id": "CAD-134",
        "categorie": "Gastronomie",
        "titre": "Machine à café à grain De'Longhi Magnifica S ECAM 22.110.B",
        "enseigne": "Darty",
        "prix": 329.99,
        "devise": "EUR",
        "description": "Expresso broyeur avec buse vapeur cappuccino et réglage de mouture."
    },
    {
        "id": "CAD-135",
        "categorie": "Gastronomie",
        "titre": "Coffret gourmand Terroir du Sud-Ouest (Foie gras, confit et douceurs)",
        "enseigne": "Galeries Lafayette",
        "prix": 59.0,
        "devise": "EUR",
        "description": "Panier gastronomique festif pour les repas de fin d'année."
    },
    {
        "id": "CAD-136",
        "categorie": "Gastronomie",
        "titre": "Coffret 12 tablettes de chocolat grand cru Valrhona",
        "enseigne": "Galeries Lafayette",
        "prix": 46.0,
        "devise": "EUR",
        "description": "Dégustation de chocolats noirs et au lait d'origines variées."
    },
    {
        "id": "CAD-137",
        "categorie": "Gastronomie",
        "titre": "Théière en fonte noire avec infuseur inox Bredemeijer Jang 1,1 L",
        "enseigne": "Boulanger",
        "prix": 69.95,
        "devise": "EUR",
        "description": "Théière traditionnelle conservant la chaleur durablement."
    },
    {
        "id": "CAD-138",
        "categorie": "Gastronomie",
        "titre": "Coffret préparation Rhum arrangé bio (3 bouteilles et épices)",
        "enseigne": "Nature & Découvertes",
        "prix": 36.95,
        "devise": "EUR",
        "description": "Mélanges d'épices, vanille et fruits séchés à faire macérer."
    },
    {
        "id": "CAD-139",
        "categorie": "Gastronomie",
        "titre": "Moulin à café électrique Bosch TSM6A013B Noir",
        "enseigne": "Darty",
        "prix": 24.99,
        "devise": "EUR",
        "description": "Lames en acier inoxydable pour moudre fraîchement les grains de café."
    },
    {
        "id": "CAD-140",
        "categorie": "Gastronomie",
        "titre": "Coffret calissons d'Aix-en-Provence Le Roy René (32 pièces)",
        "enseigne": "Galeries Lafayette",
        "prix": 34.5,
        "devise": "EUR",
        "description": "Confiserie provençale traditionnelle aux amandes et melons confits."
    },
    {
        "id": "CAD-141",
        "categorie": "Gastronomie",
        "titre": "Mousseur à lait électrique Severin SM 3586 Inox",
        "enseigne": "Amazon",
        "prix": 44.99,
        "devise": "EUR",
        "description": "Réalise une mousse de lait chaude ou froide pour cappuccinos et chocolats."
    },
    {
        "id": "CAD-142",
        "categorie": "Gastronomie",
        "titre": "Coffret dégustation 5 moutardes fines Edmond Fallot (Beaune)",
        "enseigne": "Galeries Lafayette",
        "prix": 22.9,
        "devise": "EUR",
        "description": "Moutardes artisanales au cassis, pain d'épices, noix, estragon et Bourgogne."
    },
    {
        "id": "CAD-143",
        "categorie": "Gastronomie",
        "titre": "Crêpière électrique Krampouz Billig 33 cm",
        "enseigne": "Boulanger",
        "prix": 169.99,
        "devise": "EUR",
        "description": "Plaque en fonte usinée de fabrication française avec spatule et râteau."
    },
    {
        "id": "CAD-144",
        "categorie": "Gastronomie",
        "titre": "Coffret 9 mini-confitures artisanales Bonne Maman Édition Noël",
        "enseigne": "Amazon",
        "prix": 19.9,
        "devise": "EUR",
        "description": "Saveurs festives exclusives dans un coffret illustré."
    },
    {
        "id": "CAD-145",
        "categorie": "Gastronomie",
        "titre": "Carafe filtrante Brita Marella XL Blanche + 3 cartouches Maxtra Pro",
        "enseigne": "Darty",
        "prix": 34.99,
        "devise": "EUR",
        "description": "Capacité 3,5 L pour filtrer l'eau du robinet au quotidien."
    },
    {
        "id": "CAD-146",
        "categorie": "Gastronomie",
        "titre": "Coffret épices du monde Terre Exotique (6 boîtes métal)",
        "enseigne": "Nature & Découvertes",
        "prix": 38.0,
        "devise": "EUR",
        "description": "Poivres rares, currys et mélanges aromatiques pour sublimer la cuisine."
    },
    {
        "id": "CAD-147",
        "categorie": "Gastronomie",
        "titre": "Machine à eau pétillante SodaStream Terra Noire",
        "enseigne": "Boulanger",
        "prix": 79.99,
        "devise": "EUR",
        "description": "Livrée avec cylindre de CO2 Quick Connect et bouteille réutilisable 1 L."
    },
    {
        "id": "CAD-148",
        "categorie": "Gastronomie",
        "titre": "Coffret macarons assortis Maison Ladurée (12 pièces)",
        "enseigne": "Galeries Lafayette",
        "prix": 35.0,
        "devise": "EUR",
        "description": "Coffret iconique garni des parfums classiques de la maison parisienne."
    },
    {
        "id": "CAD-149",
        "categorie": "Gastronomie",
        "titre": "Bouilloire électrique à température réglable Russell Hobbs Precision",
        "enseigne": "Darty",
        "prix": 59.99,
        "devise": "EUR",
        "description": "Sélection précise de 60°C à 100°C pour chaque variété de thé."
    },
    {
        "id": "CAD-150",
        "categorie": "Gastronomie",
        "titre": "Coffret bistrot Sauces et condiments Maille (4 pots grès)",
        "enseigne": "Galeries Lafayette",
        "prix": 29.0,
        "devise": "EUR",
        "description": "Assortiment de spécialités gastronomiques en pots de grès."
    },
    {
        "id": "CAD-151",
        "categorie": "Gastronomie",
        "titre": "Gaufrier électrique Lagrange Super 2 Plaques Gaufres",
        "enseigne": "Boulanger",
        "prix": 99.99,
        "devise": "EUR",
        "description": "Plaques massives en fonte d'aluminium fabriquées en France."
    },
    {
        "id": "CAD-152",
        "categorie": "Gastronomie",
        "titre": "Coffret biscuits bretons pur beurre La Trinitaine (Boîte métal collector)",
        "enseigne": "Amazon",
        "prix": 21.5,
        "devise": "EUR",
        "description": "Palets et galettes bretonnes dans une boîte décorée réutilisable."
    },
    {
        "id": "CAD-153",
        "categorie": "Gastronomie",
        "titre": "Service à fondue électrique Tefal Inox & Design 8 personnes",
        "enseigne": "Darty",
        "prix": 64.99,
        "devise": "EUR",
        "description": "Caquelon antiadhésif et 8 fourchettes incluses."
    },
    {
        "id": "CAD-154",
        "categorie": "Gastronomie",
        "titre": "Coffret café en grains de spécialité Cafés Lugat (4 x 250 g)",
        "enseigne": "Amazon",
        "prix": 36.0,
        "devise": "EUR",
        "description": "Quatre origines fraîchement torréfiées en France."
    },
    {
        "id": "CAD-155",
        "categorie": "Gastronomie",
        "titre": "Pierre à pizza en cordiérite Weber avec pelle en aluminium",
        "enseigne": "Boulanger",
        "prix": 49.99,
        "devise": "EUR",
        "description": "Permet de cuire des pizzas croustillantes au four ou au barbecue."
    },
    {
        "id": "CAD-156",
        "categorie": "Gastronomie",
        "titre": "Coffret nougats de Montélimar Chabert & Guillot (400 g)",
        "enseigne": "Galeries Lafayette",
        "prix": 23.5,
        "devise": "EUR",
        "description": "Nougat tendre aux amandes et miel de lavande."
    },
    {
        "id": "CAD-157",
        "categorie": "Maison & Déco",
        "titre": "Diffuseur d'huiles essentielles par ultrason Cera",
        "enseigne": "Nature & Découvertes",
        "prix": 54.95,
        "devise": "EUR",
        "description": "Diffuseur en céramique et bois d'hévéa avec lumière d'ambiance douce."
    },
    {
        "id": "CAD-158",
        "categorie": "Maison & Déco",
        "titre": "Lampe nomade rechargeable Fatboy Edison the Petit",
        "enseigne": "Boulanger",
        "prix": 69.0,
        "devise": "EUR",
        "description": "Lampe de table sans fil avec trois niveaux d'intensité lumineuse."
    },
    {
        "id": "CAD-159",
        "categorie": "Maison & Déco",
        "titre": "Plaid polaire sherpa double face 130x170 cm Gris anthracite",
        "enseigne": "Maisons du Monde",
        "prix": 29.99,
        "devise": "EUR",
        "description": "Plaid chaud et doux pour les soirées d'hiver au salon."
    },
    {
        "id": "CAD-160",
        "categorie": "Maison & Déco",
        "titre": "Bougie parfumée Yankee Candle Grande Jarre Feu de Bois (623 g)",
        "enseigne": "Amazon",
        "prix": 29.9,
        "devise": "EUR",
        "description": "Jusqu'à 150 heures de combustion avec parfum boisé chaleureux."
    },
    {
        "id": "CAD-161",
        "categorie": "Maison & Déco",
        "titre": "Horloge murale silencieuse en bois et métal 40 cm",
        "enseigne": "Maisons du Monde",
        "prix": 39.99,
        "devise": "EUR",
        "description": "Design industriel épuré sans tic-tac audible."
    },
    {
        "id": "CAD-162",
        "categorie": "Maison & Déco",
        "titre": "Lampe de sel de l'Himalaya naturelle sur socle bois",
        "enseigne": "Nature & Découvertes",
        "prix": 24.95,
        "devise": "EUR",
        "description": "Diffuse une lumière ambrée apaisante dans le salon ou la chambre."
    },
    {
        "id": "CAD-163",
        "categorie": "Maison & Déco",
        "titre": "Vase en céramique texturée blanc cassé hauteur 28 cm",
        "enseigne": "Maisons du Monde",
        "prix": 27.99,
        "devise": "EUR",
        "description": "Vase décoratif minimaliste pour bouquets secs ou frais."
    },
    {
        "id": "CAD-164",
        "categorie": "Maison & Déco",
        "titre": "Guirlande lumineuse boules coton La Case de Cousin Paul (20 boules)",
        "enseigne": "Nature & Découvertes",
        "prix": 29.9,
        "devise": "EUR",
        "description": "Guirlande LED tissée à la main aux teintes chaleureuses."
    },
    {
        "id": "CAD-165",
        "categorie": "Maison & Déco",
        "titre": "Miroir verrière en métal noir 60x90 cm",
        "enseigne": "Maisons du Monde",
        "prix": 69.99,
        "devise": "EUR",
        "description": "Agrandit visuellement l'espace avec un style atelier."
    },
    {
        "id": "CAD-166",
        "categorie": "Maison & Déco",
        "titre": "Couverture lestée relaxante 6 kg 135x200 cm",
        "enseigne": "Amazon",
        "prix": 59.99,
        "devise": "EUR",
        "description": "Favorise la détente et un sommeil réparateur."
    },
    {
        "id": "CAD-167",
        "categorie": "Maison & Déco",
        "titre": "Terrarium végétal autonome sous cloche en verre",
        "enseigne": "Nature & Découvertes",
        "prix": 49.95,
        "devise": "EUR",
        "description": "Mini-écosystème d'intérieur facile d'entretien."
    },
    {
        "id": "CAD-168",
        "categorie": "Maison & Déco",
        "titre": "Set de 2 coussins en velours côtelé 45x45 cm Terracotta",
        "enseigne": "Maisons du Monde",
        "prix": 25.98,
        "devise": "EUR",
        "description": "Housses déhoussables douces pour réchauffer un canapé."
    },
    {
        "id": "CAD-169",
        "categorie": "Maison & Déco",
        "titre": "Bougie parfumée Diptyque Baies 190 g",
        "enseigne": "Galeries Lafayette",
        "prix": 62.0,
        "devise": "EUR",
        "description": "Bougie iconique aux notes de feuilles de cassis et de roses."
    },
    {
        "id": "CAD-170",
        "categorie": "Maison & Déco",
        "titre": "Baromètre à cristaux Fitzroy en forme de goutte sur socle bois",
        "enseigne": "Nature & Découvertes",
        "prix": 29.95,
        "devise": "EUR",
        "description": "Objet décoratif scientifique réagissant aux variations atmosphériques."
    },
    {
        "id": "CAD-171",
        "categorie": "Maison & Déco",
        "titre": "Plateau de service en bois d'acacia avec poignées métal",
        "enseigne": "Maisons du Monde",
        "prix": 24.99,
        "devise": "EUR",
        "description": "Idéal pour le petit-déjeuner au lit ou l'apéritif."
    },
    {
        "id": "CAD-172",
        "categorie": "Maison & Déco",
        "titre": "Lampadaire trépied en bois naturel et abat-jour lin blanc",
        "enseigne": "Maisons du Monde",
        "prix": 89.99,
        "devise": "EUR",
        "description": "Luminaire chaleureux d'inspiration scandinave."
    },
    {
        "id": "CAD-173",
        "categorie": "Maison & Déco",
        "titre": "Diffuseur à bâtonnets Esteban Paris Teck & Tonka 250 ml",
        "enseigne": "Nature & Découvertes",
        "prix": 34.0,
        "devise": "EUR",
        "description": "Parfum d'intérieur boisé et épicé rechargeable."
    },
    {
        "id": "CAD-174",
        "categorie": "Maison & Déco",
        "titre": "Panier de rangement tressé en jonc de mer avec poignées",
        "enseigne": "Maisons du Monde",
        "prix": 22.99,
        "devise": "EUR",
        "description": "Corbeille décorative pour plaids, revues ou plantes."
    },
    {
        "id": "CAD-175",
        "categorie": "Maison & Déco",
        "titre": "Réveil bois LED avec affichage température et heure",
        "enseigne": "Amazon",
        "prix": 22.99,
        "devise": "EUR",
        "description": "Cube décoratif minimaliste à intensité lumineuse réglable."
    },
    {
        "id": "CAD-176",
        "categorie": "Maison & Déco",
        "titre": "Carafe à décanter le vin en verre cristallin Peugeot Ibis 75 cl",
        "enseigne": "Galeries Lafayette",
        "prix": 49.0,
        "devise": "EUR",
        "description": "Forme évasée conçue pour aérer les vins rouges jeunes."
    },
    {
        "id": "CAD-177",
        "categorie": "Maison & Déco",
        "titre": "Tapis berbère à motifs géométriques crème et noir 120x170 cm",
        "enseigne": "Maisons du Monde",
        "prix": 79.99,
        "devise": "EUR",
        "description": "Tapis doux à poils courts pour salon ou chambre."
    },
    {
        "id": "CAD-178",
        "categorie": "Maison & Déco",
        "titre": "Photophore lanterne en métal doré et verre",
        "enseigne": "Maisons du Monde",
        "prix": 19.99,
        "devise": "EUR",
        "description": "Crée des jeux de lumière chaleureux sur une table de fête."
    },
    {
        "id": "CAD-179",
        "categorie": "Maison & Déco",
        "titre": "Set de 4 mugs en grès émaillé artisanal",
        "enseigne": "Maisons du Monde",
        "prix": 26.99,
        "devise": "EUR",
        "description": "Tasses de 320 ml aux nuances naturelles compatibles lave-vaisselle."
    },
    {
        "id": "CAD-180",
        "categorie": "Maison & Déco",
        "titre": "Sablier magnétique en verre sur socle en bois",
        "enseigne": "Nature & Découvertes",
        "prix": 24.95,
        "devise": "EUR",
        "description": "La limaille de fer forme des sculptures magnétiques au fil de l'écoulement."
    },
    {
        "id": "CAD-181",
        "categorie": "Maison & Déco",
        "titre": "Parure de lit percale de coton 240x220 cm Vert sauge",
        "enseigne": "Galeries Lafayette",
        "prix": 79.0,
        "devise": "EUR",
        "description": "Housse de couette et 2 taies d'oreiller au toucher doux."
    },
    {
        "id": "CAD-182",
        "categorie": "Maison & Déco",
        "titre": "Cadre pêle-mêle mural 9 photos en bois naturel",
        "enseigne": "Maisons du Monde",
        "prix": 24.99,
        "devise": "EUR",
        "description": "Permet d'exposer ses souvenirs de famille."
    },
    {
        "id": "CAD-183",
        "categorie": "Maison & Déco",
        "titre": "Bouillotte peluche micro-ondable aux graines de lin et lavande",
        "enseigne": "Nature & Découvertes",
        "prix": 26.95,
        "devise": "EUR",
        "description": "Diffuse une chaleur douce et apaisante en quelques instants."
    },
    {
        "id": "CAD-184",
        "categorie": "Maison & Déco",
        "titre": "Plante artificielle Monstera Deliciosa en pot 90 cm",
        "enseigne": "Maisons du Monde",
        "prix": 49.99,
        "devise": "EUR",
        "description": "Touche végétale réaliste sans aucun entretien."
    },
    {
        "id": "CAD-185",
        "categorie": "Maison & Déco",
        "titre": "Boîte à bijoux en bois et velours avec miroir intégré",
        "enseigne": "Maisons du Monde",
        "prix": 32.99,
        "devise": "EUR",
        "description": "Compartiments dédiés pour bagues, colliers et bracelets."
    },
    {
        "id": "CAD-186",
        "categorie": "Maison & Déco",
        "titre": "Lampe de chevet tactile Dimmable Aukey",
        "enseigne": "Amazon",
        "prix": 29.99,
        "devise": "EUR",
        "description": "Éclairage blanc chaud réglable et modes couleurs doux."
    },
    {
        "id": "CAD-187",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret Eau de Parfum Lancôme La Vie Est Belle (50 ml + Lait corps)",
        "enseigne": "Sephora",
        "prix": 98.0,
        "devise": "EUR",
        "description": "Le parfum iconique aux notes d'iris, jasmin et fleur d'oranger en coffret."
    },
    {
        "id": "CAD-188",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret Eau de Toilette Dior Sauvage (60 ml + Gel douche)",
        "enseigne": "Sephora",
        "prix": 92.0,
        "devise": "EUR",
        "description": "Fragrance fraîche et boisée présentée dans un écrin cadeau."
    },
    {
        "id": "CAD-189",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret Soins Mains Karité L'Occitane en Provence (4 crèmes 30 ml)",
        "enseigne": "Sephora",
        "prix": 34.0,
        "devise": "EUR",
        "description": "Quatre crèmes mains iconiques enrichies en beurre de karité."
    },
    {
        "id": "CAD-190",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret Parfum Yves Saint Laurent Black Opium (50 ml + Mascara miniature)",
        "enseigne": "Marionnaud",
        "prix": 99.0,
        "devise": "EUR",
        "description": "Eau de parfum café floral dans un coffret festif."
    },
    {
        "id": "CAD-191",
        "categorie": "Beauté & Parfums",
        "titre": "Sèche-cheveux ionique Dyson Supersonic Gris/Fuchsia",
        "enseigne": "Darty",
        "prix": 399.0,
        "devise": "EUR",
        "description": "Séchage rapide sans chaleur extrême avec embouts magnétiques."
    },
    {
        "id": "CAD-192",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret Rituel Spa The Ritual of Sakura (Mousse de douche, gommage, crème)",
        "enseigne": "Sephora",
        "prix": 39.9,
        "devise": "EUR",
        "description": "Coffret bien-être parfumé à la fleur de cerisier et au lait de riz."
    },
    {
        "id": "CAD-193",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret Eau de Parfum Paco Rabanne 1 Million (50 ml + Gel douche)",
        "enseigne": "Marionnaud",
        "prix": 84.0,
        "devise": "EUR",
        "description": "Parfum masculin épicé et cuiré en coffret cadeau."
    },
    {
        "id": "CAD-194",
        "categorie": "Beauté & Parfums",
        "titre": "Brosse soufflante rotative Revlon One-Step Volumiser",
        "enseigne": "Boulanger",
        "prix": 49.99,
        "devise": "EUR",
        "description": "Sèche et coiffe en un seul passage avec revêtement céramique."
    },
    {
        "id": "CAD-195",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret Huile Prodigieuse Nuxe (Flacon 100 ml + Bougie + Crème)",
        "enseigne": "Marionnaud",
        "prix": 39.9,
        "devise": "EUR",
        "description": "Le soin multi-fonctions culte pour visage, corps et cheveux."
    },
    {
        "id": "CAD-196",
        "categorie": "Beauté & Parfums",
        "titre": "Tondeuse barbe et cheveux Philips OneBlade Pro 360",
        "enseigne": "Darty",
        "prix": 59.99,
        "devise": "EUR",
        "description": "Taille, définit les contours et rase toutes longueurs de poils."
    },
    {
        "id": "CAD-197",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret Eau de Parfum Guerlain Mon Guerlain (50 ml + Vaporisateur sac)",
        "enseigne": "Sephora",
        "prix": 96.0,
        "devise": "EUR",
        "description": "Composition associant lavande, jasmin sambac et vanille."
    },
    {
        "id": "CAD-198",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret Découverte 5 miniatures de parfums Maison Francis Kurkdjian",
        "enseigne": "Galeries Lafayette",
        "prix": 45.0,
        "devise": "EUR",
        "description": "Assortiment de créations de haute parfumerie française."
    },
    {
        "id": "CAD-199",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret Masques Visage Garnier SkinActive (5 masques tissus hydratants)",
        "enseigne": "Amazon",
        "prix": 14.9,
        "devise": "EUR",
        "description": "Soin hydratant et apaisant prêt à offrir."
    },
    {
        "id": "CAD-200",
        "categorie": "Beauté & Parfums",
        "titre": "Épilateur à lumière pulsée Philips Lumea Série 8000",
        "enseigne": "Boulanger",
        "prix": 349.99,
        "devise": "EUR",
        "description": "Réduction durable de la pilosité avec capteur SmartSkin."
    },
    {
        "id": "CAD-201",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret Barbe Le Baigneur (Huile à barbe, savon surgras et peigne bois)",
        "enseigne": "Nature & Découvertes",
        "prix": 42.0,
        "devise": "EUR",
        "description": "Soins bio fabriqués artisanalement en France."
    },
    {
        "id": "CAD-202",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret Eau de Toilette Hermès Terre d'Hermès (50 ml + Gel douche)",
        "enseigne": "Sephora",
        "prix": 89.0,
        "devise": "EUR",
        "description": "Fragrance boisée et minérale emblématique."
    },
    {
        "id": "CAD-203",
        "categorie": "Beauté & Parfums",
        "titre": "Brosse nettoyante visage Foreo Luna Play Smart 2",
        "enseigne": "Sephora",
        "prix": 79.0,
        "devise": "EUR",
        "description": "Nettoyage en profondeur par pulsations T-Sonic."
    },
    {
        "id": "CAD-204",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret Maquillage Benefit Cosmetics : Trio Best-Sellers (Mascara, Blush, Sourcils)",
        "enseigne": "Sephora",
        "prix": 44.0,
        "devise": "EUR",
        "description": "Les trois indispensables teint et regard en format cadeau."
    },
    {
        "id": "CAD-205",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret Savons parfumés Roger & Gallet (4 savons ronds 100 g)",
        "enseigne": "Marionnaud",
        "prix": 24.5,
        "devise": "EUR",
        "description": "Savons parfumés à cœur fabriqués au chaudron."
    },
    {
        "id": "CAD-206",
        "categorie": "Beauté & Parfums",
        "titre": "Lisseur cheveux ghd Gold Styler Noir",
        "enseigne": "Darty",
        "prix": 189.0,
        "devise": "EUR",
        "description": "Température optimale constante de 185°C pour des cheveux brillants."
    },
    {
        "id": "CAD-207",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret Eau de Parfum Giorgio Armani Sì (50 ml + Lait parfumé)",
        "enseigne": "Marionnaud",
        "prix": 94.0,
        "devise": "EUR",
        "description": "Chypre moderne et lumineux aux notes de nectar de cassis."
    },
    {
        "id": "CAD-208",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret Soins Homme ClarinsMen (Nettoyant visage, baume hydratant, huile)",
        "enseigne": "Sephora",
        "prix": 56.0,
        "devise": "EUR",
        "description": "Routine complète hydratante et énergisante."
    },
    {
        "id": "CAD-209",
        "categorie": "Beauté & Parfums",
        "titre": "Miroir de maquillage lumineux LED tactile grossissant x5",
        "enseigne": "Amazon",
        "prix": 29.99,
        "devise": "EUR",
        "description": "Éclairage réglable 3 températures de couleur sur pied."
    },
    {
        "id": "CAD-210",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret Bain et Douche Caudalie Thé des Vignes",
        "enseigne": "Marionnaud",
        "prix": 26.9,
        "devise": "EUR",
        "description": "Eau fraîche, gel douche et soin corps aux notes de musc blanc et néroli."
    },
    {
        "id": "CAD-211",
        "categorie": "Beauté & Parfums",
        "titre": "Brosse à dents électrique Oral-B iO Series 4 Noire",
        "enseigne": "Boulanger",
        "prix": 89.99,
        "devise": "EUR",
        "description": "Capteur de pression intelligent et 4 modes de brossage."
    },
    {
        "id": "CAD-212",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret Eau de Toilette Jean Paul Gaultier Le Male (75 ml + Gel douche)",
        "enseigne": "Sephora",
        "prix": 85.0,
        "devise": "EUR",
        "description": "Le flacon marinière iconique aux notes de menthe, lavande et vanille."
    },
    {
        "id": "CAD-213",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret Vernis à ongles Manucurist Green (3 teintes + Base & Top Coat)",
        "enseigne": "Galeries Lafayette",
        "prix": 49.0,
        "devise": "EUR",
        "description": "Vernis biosourcés haute tenue fabriqués en France."
    },
    {
        "id": "CAD-214",
        "categorie": "Beauté & Parfums",
        "titre": "Trousse de toilette voyage en cuir synthétique grainé",
        "enseigne": "Galeries Lafayette",
        "prix": 35.0,
        "devise": "EUR",
        "description": "Grande capacité avec compartiments zippés."
    },
    {
        "id": "CAD-215",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret Soins Visage Kiehl's : Hydratation Essentielle",
        "enseigne": "Sephora",
        "prix": 49.0,
        "devise": "EUR",
        "description": "Ultra Facial Cream, nettoyant et contour des yeux à l'avocat."
    },
    {
        "id": "CAD-216",
        "categorie": "Beauté & Parfums",
        "titre": "Rasoir électrique Philips Série 5000 Wet & Dry",
        "enseigne": "Darty",
        "prix": 89.99,
        "devise": "EUR",
        "description": "Têtes flexibles 360° utilisables sous la douche."
    },
    {
        "id": "CAD-217",
        "categorie": "Sport & Bien-être",
        "titre": "Tapis de yoga antidérapant en liège naturel et caoutchouc 4 mm",
        "enseigne": "Nature & Découvertes",
        "prix": 49.95,
        "devise": "EUR",
        "description": "Adhérence optimale et confort articulaire pour le yoga et le Pilates."
    },
    {
        "id": "CAD-218",
        "categorie": "Sport & Bien-être",
        "titre": "Pistolet de massage musculaire Theragun Relief",
        "enseigne": "Boulanger",
        "prix": 149.0,
        "devise": "EUR",
        "description": "Massage par percussion silencieux avec 3 embouts de précision."
    },
    {
        "id": "CAD-219",
        "categorie": "Sport & Bien-être",
        "titre": "Gourde isotherme Chilly's Série 2 500 ml Bleu Marine",
        "enseigne": "Nature & Découvertes",
        "prix": 29.95,
        "devise": "EUR",
        "description": "Conserve les boissons fraîches 24h et chaudes 12h sans condensation."
    },
    {
        "id": "CAD-220",
        "categorie": "Sport & Bien-être",
        "titre": "Balance impédancemètre connectée Withings Body Smart Noire",
        "enseigne": "Darty",
        "prix": 99.95,
        "devise": "EUR",
        "description": "Suivi précis du poids, de la masse grasse et de la fréquence cardiaque."
    },
    {
        "id": "CAD-221",
        "categorie": "Sport & Bien-être",
        "titre": "Sac à dos de randonnée Quechua NH Arpenaz 500 20 L",
        "enseigne": "Decathlon",
        "prix": 24.99,
        "devise": "EUR",
        "description": "Dos ventilé, housse de pluie intégrée et compartiment isotherme."
    },
    {
        "id": "CAD-222",
        "categorie": "Sport & Bien-être",
        "titre": "Coussin de massage shiatsu chauffant pour nuque et dos",
        "enseigne": "Amazon",
        "prix": 44.99,
        "devise": "EUR",
        "description": "Têtes rotatives bidirectionnelles avec fonction chaleur apaisante."
    },
    {
        "id": "CAD-223",
        "categorie": "Sport & Bien-être",
        "titre": "Paire d'haltères hexagonaux caoutchouc 2 x 5 kg",
        "enseigne": "Decathlon",
        "prix": 34.99,
        "devise": "EUR",
        "description": "Prise en main ergonomique antidérapante pour le renforcement musculaire."
    },
    {
        "id": "CAD-224",
        "categorie": "Sport & Bien-être",
        "titre": "Montre GPS multisport Coros Pace 3 Blanche",
        "enseigne": "Fnac",
        "prix": 249.0,
        "devise": "EUR",
        "description": "Ultra-légère (30 g) avec GPS double fréquence et 17 jours d'autonomie."
    },
    {
        "id": "CAD-225",
        "categorie": "Sport & Bien-être",
        "titre": "Coffret Bol chantant tibétain martelé à la main avec maillet",
        "enseigne": "Nature & Découvertes",
        "prix": 39.95,
        "devise": "EUR",
        "description": "Instrument traditionnel de relaxation et méditation."
    },
    {
        "id": "CAD-226",
        "categorie": "Sport & Bien-être",
        "titre": "Bouteille infuseur à thé en verre borosilicate double paroi",
        "enseigne": "Nature & Découvertes",
        "prix": 22.95,
        "devise": "EUR",
        "description": "Filtre inox intégré pour préparer thés et infusions nomades."
    },
    {
        "id": "CAD-227",
        "categorie": "Sport & Bien-être",
        "titre": "Tapis d'acupression et coussin cervical en lin naturel",
        "enseigne": "Nature & Découvertes",
        "prix": 59.95,
        "devise": "EUR",
        "description": "Stimule la circulation et soulage les tensions dorsales."
    },
    {
        "id": "CAD-228",
        "categorie": "Sport & Bien-être",
        "titre": "Corde à sauter rapide à roulements à billes Domyos",
        "enseigne": "Decathlon",
        "prix": 12.99,
        "devise": "EUR",
        "description": "Câble acier gainé réglable pour le cardio-training."
    },
    {
        "id": "CAD-229",
        "categorie": "Sport & Bien-être",
        "titre": "Sac de sport convertible Kipsta 40 L Noir",
        "enseigne": "Decathlon",
        "prix": 24.99,
        "devise": "EUR",
        "description": "Compartiment séparé pour chaussures et portage sac à dos."
    },
    {
        "id": "CAD-230",
        "categorie": "Sport & Bien-être",
        "titre": "Electrostimulateur musculaire Compex Fit 1.0",
        "enseigne": "Boulanger",
        "prix": 169.99,
        "devise": "EUR",
        "description": "10 programmes de tonification, récupération et soulagement."
    },
    {
        "id": "CAD-231",
        "categorie": "Sport & Bien-être",
        "titre": "Coussin de méditation Zafu en coton bio garni d'épeautre",
        "enseigne": "Nature & Découvertes",
        "prix": 39.95,
        "devise": "EUR",
        "description": "Assise ergonomique stable pour la méditation."
    },
    {
        "id": "CAD-232",
        "categorie": "Sport & Bien-être",
        "titre": "Paire de jumelles compactes Nikon Aculon A30 10x25",
        "enseigne": "Fnac",
        "prix": 79.99,
        "devise": "EUR",
        "description": "Optiques multicouches lumineuses pour randonnée et observation."
    },
    {
        "id": "CAD-233",
        "categorie": "Sport & Bien-être",
        "titre": "Kit de 3 bandes élastiques de résistance en tissu",
        "enseigne": "Decathlon",
        "prix": 14.99,
        "devise": "EUR",
        "description": "Trois niveaux de résistance pour le fitness à domicile."
    },
    {
        "id": "CAD-234",
        "categorie": "Sport & Bien-être",
        "titre": "Lampe de luminothérapie Beurer TL 30 (10 000 lux)",
        "enseigne": "Darty",
        "prix": 49.99,
        "devise": "EUR",
        "description": "Compense le manque de lumière naturelle en hiver."
    },
    {
        "id": "CAD-235",
        "categorie": "Sport & Bien-être",
        "titre": "Hamac de voyage ultraléger Ticket To The Moon Original",
        "enseigne": "Nature & Découvertes",
        "prix": 44.95,
        "devise": "EUR",
        "description": "Toile parachute respirante avec crochets de fixation."
    },
    {
        "id": "CAD-236",
        "categorie": "Sport & Bien-être",
        "titre": "Rouleau de massage en mousse haute densité Foam Roller",
        "enseigne": "Decathlon",
        "prix": 17.99,
        "devise": "EUR",
        "description": "Auto-massage profond après le sport."
    },
    {
        "id": "CAD-237",
        "categorie": "Sport & Bien-être",
        "titre": "Ceinture lombaire chauffante nomade sur batterie",
        "enseigne": "Amazon",
        "prix": 39.99,
        "devise": "EUR",
        "description": "Trois niveaux de chaleur pour détendre le bas du dos."
    },
    {
        "id": "CAD-238",
        "categorie": "Sport & Bien-être",
        "titre": "Bâtons de randonnée télescopiques Forclaz MT100 (La paire)",
        "enseigne": "Decathlon",
        "prix": 29.99,
        "devise": "EUR",
        "description": "Réglage rapide par clip et poignées mousse confortables."
    },
    {
        "id": "CAD-239",
        "categorie": "Sport & Bien-être",
        "titre": "Masque de sommeil occultant en soie naturelle 100%",
        "enseigne": "Galeries Lafayette",
        "prix": 35.0,
        "devise": "EUR",
        "description": "Doux pour la peau et bloque totalement la lumière."
    },
    {
        "id": "CAD-240",
        "categorie": "Sport & Bien-être",
        "titre": "Pèse-bagage électronique numérique Samsonite",
        "enseigne": "Fnac",
        "prix": 24.99,
        "devise": "EUR",
        "description": "Évite les suppléments bagages en voyage jusqu'à 50 kg."
    },
    {
        "id": "CAD-241",
        "categorie": "Sport & Bien-être",
        "titre": "Ballon de gymnastique Swiss Ball anti-éclatement 65 cm",
        "enseigne": "Decathlon",
        "prix": 16.99,
        "devise": "EUR",
        "description": "Livré avec pompe pour le gainage et les étirements."
    },
    {
        "id": "CAD-242",
        "categorie": "Sport & Bien-être",
        "titre": "Sac isotherme repas Lunch Bag avec boîtes hermétiques",
        "enseigne": "Amazon",
        "prix": 26.99,
        "devise": "EUR",
        "description": "Conserve le déjeuner au frais pour le bureau ou les sorties."
    },
    {
        "id": "CAD-243",
        "categorie": "Sport & Bien-être",
        "titre": "Podomètre de marche simple avec clip ceinture Omron Walking Style IV",
        "enseigne": "Amazon",
        "prix": 29.99,
        "devise": "EUR",
        "description": "Compteur de pas précis sans smartphone requis."
    },
    {
        "id": "CAD-244",
        "categorie": "Sport & Bien-être",
        "titre": "Boussole de randonnée à plaquette transparente Silva Ranger",
        "enseigne": "Decathlon",
        "prix": 34.99,
        "devise": "EUR",
        "description": "Graduation précise et loupe intégrée pour lecture de carte."
    },
    {
        "id": "CAD-245",
        "categorie": "Sport & Bien-être",
        "titre": "Coussin ergonomique à mémoire de forme pour chaise de bureau",
        "enseigne": "Amazon",
        "prix": 34.99,
        "devise": "EUR",
        "description": "Soulage la pression sur le coccyx lors des longues sessions assises."
    },
    {
        "id": "CAD-246",
        "categorie": "Sport & Bien-être",
        "titre": "Ensemble pétanque 3 boules acier inoxydable Obut Match 115",
        "enseigne": "Decathlon",
        "prix": 79.99,
        "devise": "EUR",
        "description": "Triplette de compétition fabriquée en France avec but et housse."
    },
    {
        "id": "CAD-247",
        "categorie": "Mode & Accessoires",
        "titre": "Écharpe 100% cachemire uni Gris perle 180x30 cm",
        "enseigne": "Galeries Lafayette",
        "prix": 79.0,
        "devise": "EUR",
        "description": "Douceur et chaleur naturelle dans un format classique intemporel."
    },
    {
        "id": "CAD-248",
        "categorie": "Mode & Accessoires",
        "titre": "Portefeuille en cuir véritable porte-cartes RFID Fossil Derrick",
        "enseigne": "Amazon",
        "prix": 49.99,
        "devise": "EUR",
        "description": "Cuir souple avec protection contre le piratage sans contact."
    },
    {
        "id": "CAD-249",
        "categorie": "Mode & Accessoires",
        "titre": "Parapluie pliant automatique coupe-vent Isotoner X-Tra Solide",
        "enseigne": "Galeries Lafayette",
        "prix": 34.9,
        "devise": "EUR",
        "description": "Structure renforcée résistant aux rafales avec ouverture automatique."
    },
    {
        "id": "CAD-250",
        "categorie": "Mode & Accessoires",
        "titre": "Sac à dos urbain Fjällräven Kånken Classic Bleu Marine",
        "enseigne": "Galeries Lafayette",
        "prix": 95.0,
        "devise": "EUR",
        "description": "Sac iconique en tissu Vinylon F déperlant avec coussin d'assise."
    },
    {
        "id": "CAD-251",
        "categorie": "Mode & Accessoires",
        "titre": "Montre analogique bracelet cuir marron Casio Collection MTP-1302",
        "enseigne": "Amazon",
        "prix": 49.9,
        "devise": "EUR",
        "description": "Cadran épuré et étanchéité 5 bars pour un style quotidien."
    },
    {
        "id": "CAD-252",
        "categorie": "Mode & Accessoires",
        "titre": "Coffret 3 paires de chaussettes fantaisie Happy Socks",
        "enseigne": "Galeries Lafayette",
        "prix": 29.95,
        "devise": "EUR",
        "description": "Chaussettes en coton peigné présentées dans un coffret cadeau."
    },
    {
        "id": "CAD-253",
        "categorie": "Mode & Accessoires",
        "titre": "Gants tactiles en cuir doublés laine Mérinos",
        "enseigne": "Galeries Lafayette",
        "prix": 49.0,
        "devise": "EUR",
        "description": "Permettent d'utiliser un smartphone tout en gardant les mains au chaud."
    },
    {
        "id": "CAD-254",
        "categorie": "Mode & Accessoires",
        "titre": "Ceinture réversible en cuir noir et marron avec boucle métal",
        "enseigne": "Galeries Lafayette",
        "prix": 45.0,
        "devise": "EUR",
        "description": "Deux coloris en un seul accessoire polyvalent."
    },
    {
        "id": "CAD-255",
        "categorie": "Mode & Accessoires",
        "titre": "Bonnet en laine mérinos côtelée Carhartt WIP Watch Hat",
        "enseigne": "Citadium",
        "prix": 29.0,
        "devise": "EUR",
        "description": "Bonnet chaud et résistant au style urbain intemporel."
    },
    {
        "id": "CAD-256",
        "categorie": "Mode & Accessoires",
        "titre": "Sac banane velours côtelé grand format Kaki",
        "enseigne": "Galeries Lafayette",
        "prix": 32.0,
        "devise": "EUR",
        "description": "Bandoulière réglable et double compartiment zippé."
    },
    {
        "id": "CAD-257",
        "categorie": "Mode & Accessoires",
        "titre": "Lunettes de soleil polarisées Polaroid PLD 2053/S",
        "enseigne": "Amazon",
        "prix": 44.9,
        "devise": "EUR",
        "description": "Monture légère avec verres antireflets UV400."
    },
    {
        "id": "CAD-258",
        "categorie": "Mode & Accessoires",
        "titre": "Porte-cartes métallique compact Secrid Miniwallet Cuir Noir",
        "enseigne": "Galeries Lafayette",
        "prix": 69.0,
        "devise": "EUR",
        "description": "Éjection rapide des cartes par levier avec boîtier aluminium RFID."
    },
    {
        "id": "CAD-259",
        "categorie": "Mode & Accessoires",
        "titre": "Foulard carré en soie imprimée 70x70 cm",
        "enseigne": "Galeries Lafayette",
        "prix": 55.0,
        "devise": "EUR",
        "description": "Accessoire élégant aux motifs graphiques."
    },
    {
        "id": "CAD-260",
        "categorie": "Mode & Accessoires",
        "titre": "Charentaises traditionnelles fourrées pure laine fabriquées en France",
        "enseigne": "Nature & Découvertes",
        "prix": 44.95,
        "devise": "EUR",
        "description": "Chaussons chauds au confort authentique avec semelle feutre."
    },
    {
        "id": "CAD-261",
        "categorie": "Mode & Accessoires",
        "titre": "Sac cabas en toile épaisse bio avec poches intérieures",
        "enseigne": "Nature & Découvertes",
        "prix": 24.95,
        "devise": "EUR",
        "description": "Grand cabas solide pour les courses, livres ou week-ends."
    },
    {
        "id": "CAD-262",
        "categorie": "Mode & Accessoires",
        "titre": "Boutons de manchette en acier brossé présentés en écrin",
        "enseigne": "Galeries Lafayette",
        "prix": 39.0,
        "devise": "EUR",
        "description": "Finition soignée pour chemise habillée."
    },
    {
        "id": "CAD-263",
        "categorie": "Mode & Accessoires",
        "titre": "Sac de voyage week-end cabine en toile et cuir 45 L",
        "enseigne": "Galeries Lafayette",
        "prix": 89.0,
        "devise": "EUR",
        "description": "Format accepté en cabine avec bandoulière amovible."
    },
    {
        "id": "CAD-264",
        "categorie": "Mode & Accessoires",
        "titre": "Casquette baseball en coton brossé Ralph Lauren Bleu Marine",
        "enseigne": "Galeries Lafayette",
        "prix": 55.0,
        "devise": "EUR",
        "description": "Modèle classique brodé avec patte de réglage arrière."
    },
    {
        "id": "CAD-265",
        "categorie": "Mode & Accessoires",
        "titre": "Étole grand format en laine mélangée motifs carreaux",
        "enseigne": "Galeries Lafayette",
        "prix": 39.0,
        "devise": "EUR",
        "description": "Châle enveloppant chaud pour l'hiver."
    },
    {
        "id": "CAD-266",
        "categorie": "Mode & Accessoires",
        "titre": "Étui à lunettes rigide en cuir grainé avec chiffon microfibre",
        "enseigne": "Amazon",
        "prix": 19.99,
        "devise": "EUR",
        "description": "Protège efficacement lunettes de vue ou de soleil."
    },
    {
        "id": "CAD-267",
        "categorie": "Mode & Accessoires",
        "titre": "Peignoir de bain éponge 100% coton 450 g/m² Blanc",
        "enseigne": "Galeries Lafayette",
        "prix": 65.0,
        "devise": "EUR",
        "description": "Col châle moelleux et très absorbant."
    },
    {
        "id": "CAD-268",
        "categorie": "Mode & Accessoires",
        "titre": "Montre chronographe Seiko Conceptual Quartz Acier",
        "enseigne": "Fnac",
        "prix": 179.0,
        "devise": "EUR",
        "description": "Boîtier acier inoxydable, verre Hardlex et mouvement quartz précis."
    },
    {
        "id": "CAD-269",
        "categorie": "Mode & Accessoires",
        "titre": "Porte-passeport et étiquette bagage assortis en cuir",
        "enseigne": "Galeries Lafayette",
        "prix": 35.0,
        "devise": "EUR",
        "description": "Duo pratique pour organiser ses documents de voyage."
    },
    {
        "id": "CAD-270",
        "categorie": "Mode & Accessoires",
        "titre": "Gourde porte-clés mousqueton et étui cuir",
        "enseigne": "Nature & Découvertes",
        "prix": 18.95,
        "devise": "EUR",
        "description": "Accessoire pratique pour ne plus égarer ses clés."
    },
    {
        "id": "CAD-271",
        "categorie": "Mode & Accessoires",
        "titre": "Chaussons chaussettes antidérapants fourrés polaire",
        "enseigne": "Amazon",
        "prix": 16.99,
        "devise": "EUR",
        "description": "Doublure intérieure ultra-douce pour la maison."
    },
    {
        "id": "CAD-272",
        "categorie": "Mode & Accessoires",
        "titre": "Sacoche ordinateur portable 15,6 pouces Samsonite Guardit",
        "enseigne": "Fnac",
        "prix": 49.99,
        "devise": "EUR",
        "description": "Compartiment rembourré et passant pour valise trolley."
    },
    {
        "id": "CAD-273",
        "categorie": "Mode & Accessoires",
        "titre": "Broche décorative dorée motif végétal",
        "enseigne": "Galeries Lafayette",
        "prix": 25.0,
        "devise": "EUR",
        "description": "Bijou fantaisie délicat pour manteau ou pull."
    },
    {
        "id": "CAD-274",
        "categorie": "Mode & Accessoires",
        "titre": "Coffret cirage et entretien chaussures en boîte bois",
        "enseigne": "Nature & Découvertes",
        "prix": 34.95,
        "devise": "EUR",
        "description": "Brosses en crin de cheval, cirages noir et incolore et chiffon."
    },
    {
        "id": "CAD-275",
        "categorie": "Mode & Accessoires",
        "titre": "Parapluie canne transparent cloche Isotoner",
        "enseigne": "Galeries Lafayette",
        "prix": 29.9,
        "devise": "EUR",
        "description": "Couverture large protégeant les épaules de la pluie."
    },
    {
        "id": "CAD-276",
        "categorie": "Mode & Accessoires",
        "titre": "Trousse de manucure voyage 7 pièces acier inoxydable Zwilling",
        "enseigne": "Galeries Lafayette",
        "prix": 49.0,
        "devise": "EUR",
        "description": "Étui en cuir avec coupe-ongles, ciseaux et pince à épiler."
    },
    {
        "id": "CAD-277",
        "categorie": "Loisirs & Créatifs",
        "titre": "Coffret de 36 crayons de couleur aquarellables Faber-Castell Albrecht Dürer",
        "enseigne": "Cultura",
        "prix": 69.99,
        "devise": "EUR",
        "description": "Mines riches en pigments entièrement solubles à l'eau dans un coffret métal."
    },
    {
        "id": "CAD-278",
        "categorie": "Loisirs & Créatifs",
        "titre": "Kit de broderie complet débutant motif floral avec tambour bois",
        "enseigne": "Cultura",
        "prix": 19.99,
        "devise": "EUR",
        "description": "Comprend toile imprimée, fils coton mouliné, aiguilles et guide."
    },
    {
        "id": "CAD-279",
        "categorie": "Loisirs & Créatifs",
        "titre": "Coffret peinture aquarelle Winsor & Newton Cotman (24 demi-godets)",
        "enseigne": "Cultura",
        "prix": 34.99,
        "devise": "EUR",
        "description": "Palette nomade avec pinceau et godets de couleurs lumineuses."
    },
    {
        "id": "CAD-280",
        "categorie": "Loisirs & Créatifs",
        "titre": "Maquette bois à assembler Ugears Locomotive à vapeur mécanique",
        "enseigne": "Nature & Découvertes",
        "prix": 59.95,
        "devise": "EUR",
        "description": "Puzzle mécanique 3D en bois découpé au laser fonctionnant sans colle."
    },
    {
        "id": "CAD-281",
        "categorie": "Loisirs & Créatifs",
        "titre": "Carnet de croquis Moleskine Art Plus A4 papier épais 165 g/m²",
        "enseigne": "Fnac",
        "prix": 24.9,
        "devise": "EUR",
        "description": "Papier sans acide idéal pour crayon, fusain, pastel et encre."
    },
    {
        "id": "CAD-282",
        "categorie": "Loisirs & Créatifs",
        "titre": "Kit de fabrication de bougies parfumées maison (Cire soja, mèches et huiles)",
        "enseigne": "Nature & Découvertes",
        "prix": 34.95,
        "devise": "EUR",
        "description": "Tout le nécessaire pour couler 4 bougies artisanales."
    },
    {
        "id": "CAD-283",
        "categorie": "Loisirs & Créatifs",
        "titre": "Coffret calligraphie et lettrage Tombow (Feutres pinceaux et guide)",
        "enseigne": "Cultura",
        "prix": 29.99,
        "devise": "EUR",
        "description": "Idéal pour s'initier au hand lettering et à la création de cartes."
    },
    {
        "id": "CAD-284",
        "categorie": "Loisirs & Créatifs",
        "titre": "Machine de découpe créative Cricut Joy",
        "enseigne": "Cultura",
        "prix": 149.99,
        "devise": "EUR",
        "description": "Découpe et écrit sur vinyle, papier cartonné et thermocollant."
    },
    {
        "id": "CAD-285",
        "categorie": "Loisirs & Créatifs",
        "titre": "Kit poterie sans cuisson argile autodurcissante et outils de modelage",
        "enseigne": "Cultura",
        "prix": 27.99,
        "devise": "EUR",
        "description": "Permet de sculpter vases, coupelles et objets déco à la maison."
    },
    {
        "id": "CAD-286",
        "categorie": "Loisirs & Créatifs",
        "titre": "Coffret 24 feutres à alcool double pointe Graph'it",
        "enseigne": "Cultura",
        "prix": 44.99,
        "devise": "EUR",
        "description": "Encre à base d'alcool pour illustration, manga et design."
    },
    {
        "id": "CAD-287",
        "categorie": "Loisirs & Créatifs",
        "titre": "Kit de brassage de bière artisanale maison 5 L Blonde",
        "enseigne": "Nature & Découvertes",
        "prix": 49.95,
        "devise": "EUR",
        "description": "Dame-jeanne en verre, malt, houblon, levure et matériel inclus."
    },
    {
        "id": "CAD-288",
        "categorie": "Loisirs & Créatifs",
        "titre": "Chevalet de table en bois de hêtre réglable",
        "enseigne": "Cultura",
        "prix": 29.99,
        "devise": "EUR",
        "description": "Support stable pour toiles jusqu'à 50 cm de hauteur."
    },
    {
        "id": "CAD-289",
        "categorie": "Loisirs & Créatifs",
        "titre": "Coffret origami 200 feuilles papier japonais motifs traditionnels",
        "enseigne": "Nature & Découvertes",
        "prix": 16.95,
        "devise": "EUR",
        "description": "Livret d'instructions inclus pour réaliser 20 modèles."
    },
    {
        "id": "CAD-290",
        "categorie": "Loisirs & Créatifs",
        "titre": "Pyrograveur sur bois avec 20 pointes interchangeables",
        "enseigne": "Amazon",
        "prix": 28.99,
        "devise": "EUR",
        "description": "Permet de graver et décorer bois, cuir et liège."
    },
    {
        "id": "CAD-291",
        "categorie": "Loisirs & Créatifs",
        "titre": "Kit tricot écharpe grosse maille laine mérinos et aiguilles bambou",
        "enseigne": "Cultura",
        "prix": 34.99,
        "devise": "EUR",
        "description": "Projet accessible aux débutants avec tutoriel pas à pas."
    },
    {
        "id": "CAD-292",
        "categorie": "Loisirs & Créatifs",
        "titre": "Globe terrestre lumineux interactif Politique et Physique 30 cm",
        "enseigne": "Nature & Découvertes",
        "prix": 44.95,
        "devise": "EUR",
        "description": "Double cartographie selon que la lampe est allumée ou éteinte."
    },
    {
        "id": "CAD-293",
        "categorie": "Loisirs & Créatifs",
        "titre": "Coffret peinture par numéros adulte : Paysage de Provence 40x50 cm",
        "enseigne": "Cultura",
        "prix": 22.99,
        "devise": "EUR",
        "description": "Toile sur châssis bois, peintures acryliques et 3 pinceaux."
    },
    {
        "id": "CAD-294",
        "categorie": "Loisirs & Créatifs",
        "titre": "Kit cyanotype : Tirages photographiques bleus au soleil",
        "enseigne": "Nature & Découvertes",
        "prix": 29.95,
        "devise": "EUR",
        "description": "Technique photographique ancienne sur papier et tissu."
    },
    {
        "id": "CAD-295",
        "categorie": "Loisirs & Créatifs",
        "titre": "Stylo 3D avec écran LCD et 12 filaments PLA colorés",
        "enseigne": "Amazon",
        "prix": 39.99,
        "devise": "EUR",
        "description": "Permet de dessiner des objets en relief à main levée."
    },
    {
        "id": "CAD-296",
        "categorie": "Loisirs & Créatifs",
        "titre": "Coffret linogravure Essdee (Gouges, rouleau, encre et plaques)",
        "enseigne": "Cultura",
        "prix": 26.99,
        "devise": "EUR",
        "description": "Initiation complète à la gravure et à l'impression artisanale."
    },
    {
        "id": "CAD-297",
        "categorie": "Loisirs & Créatifs",
        "titre": "Puzzle 3D Ravensburger Monument : La Tour Eiffel Édition Nuit 216 pièces",
        "enseigne": "Fnac",
        "prix": 29.99,
        "devise": "EUR",
        "description": "Maquette lumineuse LED sans colle."
    },
    {
        "id": "CAD-298",
        "categorie": "Loisirs & Créatifs",
        "titre": "Kit macramé suspension plante en corde coton naturel",
        "enseigne": "Cultura",
        "prix": 18.99,
        "devise": "EUR",
        "description": "Anneau bois, corde et notice illustrée."
    },
    {
        "id": "CAD-299",
        "categorie": "Loisirs & Créatifs",
        "titre": "Microscope binoculaire éducatif Bresser Junior 40x-1024x avec mallette",
        "enseigne": "Nature & Découvertes",
        "prix": 79.95,
        "devise": "EUR",
        "description": "Livré avec lames préparées et adaptateur smartphone."
    },
    {
        "id": "CAD-300",
        "categorie": "Loisirs & Créatifs",
        "titre": "Télescope d'initiation Celestron AstroMaster 70AZ",
        "enseigne": "Nature & Découvertes",
        "prix": 149.95,
        "devise": "EUR",
        "description": "Lunette astronomique sur monture azimutale pour observer la Lune et les planètes."
    },
    {
        "id": "CAD-301",
        "categorie": "Loisirs & Créatifs",
        "titre": "Coffret couture : Trousse et accessoires (Ciseaux, fils, aiguilles, mètre)",
        "enseigne": "Cultura",
        "prix": 24.99,
        "devise": "EUR",
        "description": "Nécessaire complet rangé dans un coffret rigide."
    },
    {
        "id": "CAD-302",
        "categorie": "Loisirs & Créatifs",
        "titre": "Album photo scrapbooking 60 pages noires épaisses avec stylos métalliques",
        "enseigne": "Cultura",
        "prix": 21.99,
        "devise": "EUR",
        "description": "Idéal pour créer un album souvenirs personnalisé."
    },
    {
        "id": "CAD-303",
        "categorie": "Loisirs & Créatifs",
        "titre": "Kit jardinage d'intérieur : 5 plantes aromatiques bio à semer",
        "enseigne": "Nature & Découvertes",
        "prix": 22.95,
        "devise": "EUR",
        "description": "Pots en fibre de coco, pastilles de terreau et graines bio."
    },
    {
        "id": "CAD-304",
        "categorie": "Loisirs & Créatifs",
        "titre": "Piano numérique portable Casio CT-S1 61 touches Noir",
        "enseigne": "Fnac",
        "prix": 219.0,
        "devise": "EUR",
        "description": "Clavier compact au toucher dynamique avec haut-parleurs intégrés."
    },
    {
        "id": "CAD-305",
        "categorie": "Loisirs & Créatifs",
        "titre": "Ukulélé soprano en acajou Kala KA-15S avec housse",
        "enseigne": "Cultura",
        "prix": 69.0,
        "devise": "EUR",
        "description": "Instrument chaleureux et facile à prendre en main."
    },
    {
        "id": "CAD-306",
        "categorie": "Loisirs & Créatifs",
        "titre": "Kit fabrication de fromage frais maison (Faisselles, présure et thermomètre)",
        "enseigne": "Nature & Découvertes",
        "prix": 29.95,
        "devise": "EUR",
        "description": "Réalisez faisselle, fromage blanc et fromage frais en 24h."
    },
    {
        "id": "CAD-307",
        "categorie": "Enfants & Ados",
        "titre": "Console Nintendo Switch Modèle OLED Blanche",
        "enseigne": "Fnac",
        "prix": 319.99,
        "devise": "EUR",
        "description": "Écran OLED 7 pouces aux couleurs éclatantes avec station d'accueil."
    },
    {
        "id": "CAD-308",
        "categorie": "Enfants & Ados",
        "titre": "Trotinette évolutive Globber Go Up Deluxe Bleu",
        "enseigne": "Decathlon",
        "prix": 89.99,
        "devise": "EUR",
        "description": "Se transforme de porteur en draisienne puis trottinette 3 roues."
    },
    {
        "id": "CAD-309",
        "categorie": "Enfants & Ados",
        "titre": "Coffret Playmobil 71327 Grand Château des Chevaliers",
        "enseigne": "Cultura",
        "prix": 89.99,
        "devise": "EUR",
        "description": "Forteresse complète avec pont-levis, personnages et accessoires."
    },
    {
        "id": "CAD-310",
        "categorie": "Enfants & Ados",
        "titre": "Globe terrestre interactif parlant Clementoni Exploraglobe",
        "enseigne": "Fnac",
        "prix": 59.99,
        "devise": "EUR",
        "description": "Stylo optique sans fil avec quiz et informations sur tous les pays."
    },
    {
        "id": "CAD-311",
        "categorie": "Enfants & Ados",
        "titre": "Appareil photo numérique enfant Kidizoom Duo FX Bleu VTech",
        "enseigne": "Amazon",
        "prix": 64.99,
        "devise": "EUR",
        "description": "Double objectif, effets spéciaux, jeux intégrés et boîtier antichoc."
    },
    {
        "id": "CAD-312",
        "categorie": "Enfants & Ados",
        "titre": "Peluche géante Ours brun tout doux 80 cm",
        "enseigne": "Cultura",
        "prix": 39.99,
        "devise": "EUR",
        "description": "Peluche moelleuse conforme aux normes de sécurité dès la naissance."
    },
    {
        "id": "CAD-313",
        "categorie": "Enfants & Ados",
        "titre": "Circuit de train en bois Brio World Grand Circuit Voyageurs (42 pièces)",
        "enseigne": "Nature & Découvertes",
        "prix": 79.95,
        "devise": "EUR",
        "description": "Rails en hêtre massif, trains magnétiques et gare."
    },
    {
        "id": "CAD-314",
        "categorie": "Enfants & Ados",
        "titre": "Set LEGO Minecraft 21249 La Boîte de Construction 4.0",
        "enseigne": "Amazon",
        "prix": 64.99,
        "devise": "EUR",
        "description": "Deux configurations de construction modulables avec figurines."
    },
    {
        "id": "CAD-315",
        "categorie": "Enfants & Ados",
        "titre": "Boîte à histoires Lunii Ma Fabrique à Histoires",
        "enseigne": "Fnac",
        "prix": 64.9,
        "devise": "EUR",
        "description": "Conteuse interactive sans écran ni ondes où l'enfant choisit son récit."
    },
    {
        "id": "CAD-316",
        "categorie": "Enfants & Ados",
        "titre": "Tableau d'activités magnétique et craie double face sur pied en bois",
        "enseigne": "Cultura",
        "prix": 49.99,
        "devise": "EUR",
        "description": "Évolutif en hauteur avec rouleau de papier et accessoires."
    },
    {
        "id": "CAD-317",
        "categorie": "Enfants & Ados",
        "titre": "Robot éducatif programmable Clementoni Mio le Robot",
        "enseigne": "Amazon",
        "prix": 34.99,
        "devise": "EUR",
        "description": "Initiation ludique à la robotique et au codage dès 8 ans."
    },
    {
        "id": "CAD-318",
        "categorie": "Enfants & Ados",
        "titre": "Draisienne en métal léger Btwin Runride 500 10 pouces",
        "enseigne": "Decathlon",
        "prix": 49.99,
        "devise": "EUR",
        "description": "Apprentissage de l'équilibre dès 2 ans avec frein adapté."
    },
    {
        "id": "CAD-319",
        "categorie": "Enfants & Ados",
        "titre": "Mallette de magie 100 tours avec accessoires et DVD explicatif",
        "enseigne": "Cultura",
        "prix": 29.99,
        "devise": "EUR",
        "description": "Tours de cartes, gobelets et disparitions pour jeunes magiciens."
    },
    {
        "id": "CAD-320",
        "categorie": "Enfants & Ados",
        "titre": "Casque audio enfant filaire volume limité JBL JR310 Bleu/Rouge",
        "enseigne": "Boulanger",
        "prix": 24.99,
        "devise": "EUR",
        "description": "Limitation sonore à 85 dB pour protéger l'audition des plus jeunes."
    },
    {
        "id": "CAD-321",
        "categorie": "Enfants & Ados",
        "titre": "Jeu de construction magnétique Magna-Tiles Clear Colors (32 pièces)",
        "enseigne": "Nature & Découvertes",
        "prix": 49.95,
        "devise": "EUR",
        "description": "Tuiles géométriques translucides aimantées pour constructions en 3D."
    },
    {
        "id": "CAD-322",
        "categorie": "Enfants & Ados",
        "titre": "Station d'observation des fourmis Fourmilière transparente éducative",
        "enseigne": "Nature & Découvertes",
        "prix": 29.95,
        "devise": "EUR",
        "description": "Permet d'observer le creusement des galeries."
    },
    {
        "id": "CAD-323",
        "categorie": "Enfants & Ados",
        "titre": "Veilleuse projecteur d'étoiles musicale Pabobo",
        "enseigne": "Fnac",
        "prix": 34.99,
        "devise": "EUR",
        "description": "Projette un ciel étoilé apaisant au plafond avec minuterie."
    },
    {
        "id": "CAD-324",
        "categorie": "Enfants & Ados",
        "titre": "Tente tipi enfant en toile coton avec tapis matelassé",
        "enseigne": "Maisons du Monde",
        "prix": 59.99,
        "devise": "EUR",
        "description": "Cabane de lecture et de jeu pour la chambre."
    },
    {
        "id": "CAD-325",
        "categorie": "Enfants & Ados",
        "titre": "Skateboard complet Oxelo Mid 500",
        "enseigne": "Decathlon",
        "prix": 44.99,
        "devise": "EUR",
        "description": "Plateau érable 7 plis adapté aux débutants et ados."
    },
    {
        "id": "CAD-326",
        "categorie": "Enfants & Ados",
        "titre": "Coffret expériences scientifiques Chimie Sans Danger Buki",
        "enseigne": "Cultura",
        "prix": 32.99,
        "devise": "EUR",
        "description": "150 expériences illustrées réalisables avec des produits courants."
    },
    {
        "id": "CAD-327",
        "categorie": "Enfants & Ados",
        "titre": "Trottinette freestyle Oxelo MF1.8",
        "enseigne": "Decathlon",
        "prix": 69.99,
        "devise": "EUR",
        "description": "Deck aluminium renforcé et roues 100 mm pour le skatepark."
    },
    {
        "id": "CAD-328",
        "categorie": "Enfants & Ados",
        "titre": "Jeu électronique Simon Classic Hasbro",
        "enseigne": "Amazon",
        "prix": 24.99,
        "devise": "EUR",
        "description": "Mémorisez et reproduisez des séquences lumineuses et sonores."
    },
    {
        "id": "CAD-329",
        "categorie": "Enfants & Ados",
        "titre": "Poupée Corolle Mon Grand Poupon Camille 36 cm",
        "enseigne": "Fnac",
        "prix": 44.99,
        "devise": "EUR",
        "description": "Corps souple délicatement parfumé à la vanille avec yeux dormeurs."
    },
    {
        "id": "CAD-330",
        "categorie": "Enfants & Ados",
        "titre": "Circuit de billes en bois modulable Haba Kullerbü",
        "enseigne": "Nature & Découvertes",
        "prix": 59.95,
        "devise": "EUR",
        "description": "Système d'assemblage stable avec rampes et clochette."
    },
    {
        "id": "CAD-331",
        "categorie": "Enfants & Ados",
        "titre": "Sac à dos scolaire Eastpak Padded Pak'r Noir",
        "enseigne": "Galeries Lafayette",
        "prix": 55.0,
        "devise": "EUR",
        "description": "Le sac à dos indémodable garanti 30 ans."
    },
    {
        "id": "CAD-332",
        "categorie": "Enfants & Ados",
        "titre": "Tablette graphique d'écriture LCD 12 pouces effaçable",
        "enseigne": "Amazon",
        "prix": 16.99,
        "devise": "EUR",
        "description": "Ardoise numérique légère sans papier pour dessiner partout."
    },
    {
        "id": "CAD-333",
        "categorie": "Enfants & Ados",
        "titre": "Set LEGO Technic 42160 Audi RS Q e-tron télécommandé",
        "enseigne": "Fnac",
        "prix": 149.99,
        "devise": "EUR",
        "description": "Voiture de rallye pilotable via l'application Control+."
    },
    {
        "id": "CAD-334",
        "categorie": "Enfants & Ados",
        "titre": "Coffret Kapla 200 planchettes en pin des Landes",
        "enseigne": "Cultura",
        "prix": 49.99,
        "devise": "EUR",
        "description": "Jeu de construction en bois naturel avec livret de modèles."
    },
    {
        "id": "CAD-335",
        "categorie": "Enfants & Ados",
        "titre": "Talkies-walkies enfant portée 3 km Buki (La paire)",
        "enseigne": "Nature & Découvertes",
        "prix": 29.95,
        "devise": "EUR",
        "description": "8 canaux, lampe torche intégrée et clip ceinture."
    },
    {
        "id": "CAD-336",
        "categorie": "Enfants & Ados",
        "titre": "Panier de basket mural réglable enfant avec ballon",
        "enseigne": "Decathlon",
        "prix": 24.99,
        "devise": "EUR",
        "description": "Se fixe facilement sur une porte ou un mur."
    },
        {
        "id": "CAD-337",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray 4K Oppenheimer Édition Collector",
        "enseigne": "Fnac",
        "prix": 34.99,
        "devise": "EUR",
        "description": "Le film de Christopher Nolan en Ultra HD avec contenus bonus."
    },
    {
        "id": "CAD-338",
        "categorie": "High-Tech & Audio",
        "titre": "Casque Bluetooth Sony WH-1000XM5 Noir",
        "enseigne": "Boulanger",
        "prix": 299.99,
        "devise": "EUR",
        "description": "Casque sans fil premium avec réduction de bruit active et audio haute résolution."
    },
    {
        "id": "CAD-339",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société 7 Wonders Duel Nouvelle Édition",
        "enseigne": "Cultura",
        "prix": 26.99,
        "devise": "EUR",
        "description": "Jeu stratégique pour deux joueurs consacré au développement de civilisations antiques."
    },
    {
        "id": "CAD-340",
        "categorie": "Livres & BD",
        "titre": "BD Le Monde sans fin Christophe Blain et Jean-Marc Jancovici Dargaud",
        "enseigne": "Fnac",
        "prix": 27.0,
        "devise": "EUR",
        "description": "Bande dessinée documentaire consacrée aux enjeux énergétiques et climatiques."
    },
    {
        "id": "CAD-341",
        "categorie": "Gastronomie",
        "titre": "Machine à café Nespresso Vertuo Pop ENV90.B Noir",
        "enseigne": "Darty",
        "prix": 89.99,
        "devise": "EUR",
        "description": "Machine à café compacte utilisant la technologie d'extraction Vertuo."
    },
    {
        "id": "CAD-342",
        "categorie": "Maison & Déco",
        "titre": "Lampe de table LED Fatboy Edison the Petit",
        "enseigne": "Nature & Découvertes",
        "prix": 75.0,
        "devise": "EUR",
        "description": "Lampe portable rechargeable à lumière douce pour intérieur et extérieur."
    },
    {
        "id": "CAD-343",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret Yves Saint Laurent Libre Eau de Parfum 50 ml",
        "enseigne": "Sephora",
        "prix": 119.0,
        "devise": "EUR",
        "description": "Coffret parfumé associant lavande, fleur d'oranger et vanille."
    },
    {
        "id": "CAD-344",
        "categorie": "Sport & Bien-être",
        "titre": "Tapis de yoga Manduka PRO 6 mm Midnight",
        "enseigne": "Decathlon",
        "prix": 135.0,
        "devise": "EUR",
        "description": "Tapis professionnel offrant un excellent amorti et une grande stabilité."
    },
    {
        "id": "CAD-345",
        "categorie": "Mode & Accessoires",
        "titre": "Sac à dos Eastpak Padded Pak'r Black",
        "enseigne": "Galeries Lafayette",
        "prix": 55.0,
        "devise": "EUR",
        "description": "Sac à dos emblématique avec compartiment principal et poche frontale zippée."
    },
    {
        "id": "CAD-346",
        "categorie": "Loisirs & Créatifs",
        "titre": "Coffret LEGO Ideas 21325 Le Forgeron Médiéval",
        "enseigne": "Fnac",
        "prix": 179.99,
        "devise": "EUR",
        "description": "Maquette détaillée d'une forge médiévale avec personnages et accessoires."
    },
    {
        "id": "CAD-347",
        "categorie": "Enfants & Ados",
        "titre": "LEGO Disney 43222 Le Château Disney",
        "enseigne": "Cultura",
        "prix": 399.99,
        "devise": "EUR",
        "description": "Grand château de construction LEGO inspiré des univers Disney."
    },
    {
        "id": "CAD-348",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray 4K Gladiator Édition Collector",
        "enseigne": "Amazon",
        "prix": 29.99,
        "devise": "EUR",
        "description": "Le péplum de Ridley Scott en haute définition avec bonus."
    },
    {
        "id": "CAD-349",
        "categorie": "High-Tech & Audio",
        "titre": "Enceinte Bluetooth Marshall Emberton II Black and Brass",
        "enseigne": "Fnac",
        "prix": 169.99,
        "devise": "EUR",
        "description": "Enceinte compacte offrant un son à 360 degrés et une autonomie prolongée."
    },
    {
        "id": "CAD-350",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Wingspan Édition Française Stonemaier Games",
        "enseigne": "Cultura",
        "prix": 59.99,
        "devise": "EUR",
        "description": "Jeu de stratégie et de collection consacré à l'observation des oiseaux."
    },
    {
        "id": "CAD-351",
        "categorie": "Livres & BD",
        "titre": "Roman La Horde du Contrevent Alain Damasio Éditions La Volte",
        "enseigne": "Fnac",
        "prix": 12.0,
        "devise": "EUR",
        "description": "Roman de science-fiction français récompensé par le Grand Prix de l'Imaginaire."
    },
    {
        "id": "CAD-352",
        "categorie": "Gastronomie",
        "titre": "Robot pâtissier KitchenAid Artisan 5KSM125 Rouge Empire",
        "enseigne": "Darty",
        "prix": 499.0,
        "devise": "EUR",
        "description": "Robot pâtissier à tête inclinable avec bol inox de 4,8 litres."
    },
    {
        "id": "CAD-353",
        "categorie": "Maison & Déco",
        "titre": "Diffuseur de parfum d'ambiance Rituals The Ritual of Sakura",
        "enseigne": "Sephora",
        "prix": 35.9,
        "devise": "EUR",
        "description": "Diffuseur de parfum aux notes de fleur de cerisier et de lait de riz."
    },
    {
        "id": "CAD-354",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret Lancôme La Vie Est Belle Eau de Parfum 50 ml",
        "enseigne": "Marionnaud",
        "prix": 105.0,
        "devise": "EUR",
        "description": "Coffret féminin autour d'un parfum gourmand aux notes d'iris et de vanille."
    },
    {
        "id": "CAD-355",
        "categorie": "Sport & Bien-être",
        "titre": "Montre GPS Garmin Forerunner 265 Noire",
        "enseigne": "Decathlon",
        "prix": 449.99,
        "devise": "EUR",
        "description": "Montre sportive AMOLED avec GPS intégré et suivi avancé des entraînements."
    },
    {
        "id": "CAD-356",
        "categorie": "Mode & Accessoires",
        "titre": "Portefeuille homme Le Tanneur Charles Cuir Grainé Noir",
        "enseigne": "Galeries Lafayette",
        "prix": 95.0,
        "devise": "EUR",
        "description": "Portefeuille en cuir grainé avec rangements pour cartes et billets."
    },
    {
        "id": "CAD-357",
        "categorie": "Loisirs & Créatifs",
        "titre": "Coffret LEGO Architecture 21060 Le Château de Himeji",
        "enseigne": "Fnac",
        "prix": 159.99,
        "devise": "EUR",
        "description": "Reproduction architecturale du célèbre château japonais en briques LEGO."
    },
    {
        "id": "CAD-358",
        "categorie": "Enfants & Ados",
        "titre": "Poupée Barbie Dreamhouse Maison de Rêve Mattel",
        "enseigne": "Cultura",
        "prix": 299.99,
        "devise": "EUR",
        "description": "Grande maison de jeu avec plusieurs espaces aménagés et accessoires."
    },
    {
        "id": "CAD-359",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray 4K Blade Runner 2049 Édition Collector",
        "enseigne": "Fnac",
        "prix": 34.99,
        "devise": "EUR",
        "description": "Film de science-fiction de Denis Villeneuve en édition haute définition."
    },
    {
        "id": "CAD-360",
        "categorie": "High-Tech & Audio",
        "titre": "Tablette Apple iPad Air 11 pouces M2 128 Go Wi-Fi Bleu",
        "enseigne": "Darty",
        "prix": 719.0,
        "devise": "EUR",
        "description": "Tablette équipée de la puce Apple M2 et d'un écran Liquid Retina."
    },
    {
        "id": "CAD-361",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Terraforming Mars Édition Française Intrafin",
        "enseigne": "Cultura",
        "prix": 59.99,
        "devise": "EUR",
        "description": "Jeu de stratégie dans lequel les joueurs participent à la colonisation de Mars."
    },
    {
        "id": "CAD-362",
        "categorie": "Livres & BD",
        "titre": "Manga One Piece Tome 1 Eiichiro Oda Éditions Glénat",
        "enseigne": "Fnac",
        "prix": 7.2,
        "devise": "EUR",
        "description": "Premier volume de la célèbre aventure de pirates imaginée par Eiichiro Oda."
    },
    {
        "id": "CAD-363",
        "categorie": "Gastronomie",
        "titre": "Cave à vin de service Haier HWS42GDAU1 42 bouteilles",
        "enseigne": "Boulanger",
        "prix": 599.0,
        "devise": "EUR",
        "description": "Cave de conservation et de service avec contrôle électronique de température."
    },
    {
        "id": "CAD-364",
        "categorie": "Maison & Déco",
        "titre": "Lampe de table Artemide Tolomeo Micro Aluminium",
        "enseigne": "Galeries Lafayette",
        "prix": 265.0,
        "devise": "EUR",
        "description": "Lampe articulée de bureau au design italien avec structure en aluminium."
    },
    {
        "id": "CAD-365",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret Dior Sauvage Eau de Toilette 100 ml",
        "enseigne": "Sephora",
        "prix": 139.0,
        "devise": "EUR",
        "description": "Coffret parfum masculin aux notes fraîches et boisées."
    },
    {
        "id": "CAD-366",
        "categorie": "Sport & Bien-être",
        "titre": "Pistolet de massage Therabody Theragun Mini 2e génération",
        "enseigne": "Decathlon",
        "prix": 199.0,
        "devise": "EUR",
        "description": "Appareil compact de massage par percussion destiné à la récupération musculaire."
    },
    {
        "id": "CAD-367",
        "categorie": "Mode & Accessoires",
        "titre": "Montre Casio G-Shock GA-2100-1AER Noir",
        "enseigne": "Galeries Lafayette",
        "prix": 99.0,
        "devise": "EUR",
        "description": "Montre analogique et numérique résistante aux chocs avec éclairage LED."
    },
    {
        "id": "CAD-368",
        "categorie": "Loisirs & Créatifs",
        "titre": "Coffret de calligraphie Pilot Parallel Pen Set 6 couleurs",
        "enseigne": "Cultura",
        "prix": 39.99,
        "devise": "EUR",
        "description": "Ensemble de stylos à plume parallèles pour la calligraphie et le lettrage créatif."
    },
    {
        "id": "CAD-369",
        "categorie": "Enfants & Ados",
        "titre": "LEGO Technic 42171 Mercedes-AMG F1 W14 E Performance",
        "enseigne": "Fnac",
        "prix": 219.99,
        "devise": "EUR",
        "description": "Maquette de Formule 1 à construire avec direction et moteur détaillés."
    },
    {
        "id": "CAD-370",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray 4K Le Cinquième Élément Édition Collector",
        "enseigne": "Amazon",
        "prix": 29.99,
        "devise": "EUR",
        "description": "Film de science-fiction de Luc Besson proposé en édition Ultra HD."
    },
    {
        "id": "CAD-371",
        "categorie": "High-Tech & Audio",
        "titre": "Appareil photo hybride Canon EOS R50 avec objectif RF-S 18-45mm",
        "enseigne": "Fnac",
        "prix": 899.0,
        "devise": "EUR",
        "description": "Appareil hybride APS-C avec autofocus intelligent et vidéo 4K."
    },
    {
        "id": "CAD-372",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Dune Imperium Édition Française",
        "enseigne": "Cultura",
        "prix": 54.99,
        "devise": "EUR",
        "description": "Jeu de stratégie mêlant placement d'ouvriers et construction de deck."
    },
    {
        "id": "CAD-373",
        "categorie": "Livres & BD",
        "titre": "Roman Les Fourmis Bernard Werber Éditions Le Livre de Poche",
        "enseigne": "Fnac",
        "prix": 8.9,
        "devise": "EUR",
        "description": "Roman mêlant science-fiction et découverte de l'univers des fourmis."
    },
    {
        "id": "CAD-374",
        "categorie": "Gastronomie",
        "titre": "Machine à pâtes Philips Pasta Maker HR2382/15",
        "enseigne": "Darty",
        "prix": 249.99,
        "devise": "EUR",
        "description": "Machine automatique permettant de préparer des pâtes fraîches maison."
    },
    {
        "id": "CAD-375",
        "categorie": "Maison & Déco",
        "titre": "Réveil lumineux Philips SmartSleep HF3651/01",
        "enseigne": "Boulanger",
        "prix": 179.99,
        "devise": "EUR",
        "description": "Réveil simulateur d'aube avec lumière progressive et sons naturels."
    },
    {
        "id": "CAD-376",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret Clarins Double Serum et Crème Multi-Intensive",
        "enseigne": "Marionnaud",
        "prix": 119.0,
        "devise": "EUR",
        "description": "Coffret de soins visage associant sérum et crème de jour."
    },
    {
        "id": "CAD-377",
        "categorie": "Sport & Bien-être",
        "titre": "Vélo d'appartement Domyos EB 520 B",
        "enseigne": "Decathlon",
        "prix": 299.99,
        "devise": "EUR",
        "description": "Vélo de fitness avec résistance réglable et console de suivi des séances."
    },
    {
        "id": "CAD-378",
        "categorie": "Mode & Accessoires",
        "titre": "Écharpe Lacoste Unisexe Laine et Cachemire",
        "enseigne": "Galeries Lafayette",
        "prix": 95.0,
        "devise": "EUR",
        "description": "Écharpe douce en mélange de laine et cachemire avec logo crocodile."
    },
    {
        "id": "CAD-379",
        "categorie": "Loisirs & Créatifs",
        "titre": "Kit de peinture par numéros Ravensburger CreArt Van Gogh Nuit étoilée",
        "enseigne": "Cultura",
        "prix": 29.99,
        "devise": "EUR",
        "description": "Kit créatif permettant de reproduire le tableau La Nuit étoilée."
    },
    {
        "id": "CAD-380",
        "categorie": "Enfants & Ados",
        "titre": "Jeu de construction GraviTrax Starter Set Ravensburger",
        "enseigne": "Cultura",
        "prix": 49.99,
        "devise": "EUR",
        "description": "Circuit de billes modulable pour expérimenter les principes de la gravité."
    },
    {
        "id": "CAD-381",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray 4K Le Roi Lion Édition 30e Anniversaire",
        "enseigne": "Fnac",
        "prix": 39.99,
        "devise": "EUR",
        "description": "Le classique Disney d'animation dans une édition haute définition."
    },
    {
        "id": "CAD-382",
        "categorie": "High-Tech & Audio",
        "titre": "Écran PC Samsung Odyssey G5 27 pouces LS27CG552EUXEN",
        "enseigne": "Boulanger",
        "prix": 249.99,
        "devise": "EUR",
        "description": "Moniteur gaming incurvé QHD avec fréquence de rafraîchissement de 165 Hz."
    },
    {
        "id": "CAD-383",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Ark Nova Édition Française Super Meeple",
        "enseigne": "Cultura",
        "prix": 69.99,
        "devise": "EUR",
        "description": "Jeu de gestion stratégique consacré à la création d'un parc zoologique."
    },
    {
        "id": "CAD-384",
        "categorie": "Livres & BD",
        "titre": "BD Les Vieux Fourneaux Tome 1 Ceux qui restent Dargaud",
        "enseigne": "Fnac",
        "prix": 14.5,
        "devise": "EUR",
        "description": "Premier album de la série humoristique créée par Wilfrid Lupano et Paul Cauuet."
    },
    {
        "id": "CAD-385",
        "categorie": "Gastronomie",
        "titre": "Coffret Le Creuset Set de 3 Mini Cocottes en Fonte Émaillée",
        "enseigne": "Galeries Lafayette",
        "prix": 99.0,
        "devise": "EUR",
        "description": "Trois petites cocottes en fonte émaillée pour préparer et servir des portions individuelles."
    },
    {
        "id": "CAD-386",
        "categorie": "Maison & Déco",
        "titre": "Horloge murale Karlsson Little Big Time Black",
        "enseigne": "Nature & Découvertes",
        "prix": 39.95,
        "devise": "EUR",
        "description": "Horloge murale minimaliste composée de grandes aiguilles décoratives."
    },
        {
        "id": "CAD-387",
        "categorie": "Cinéma & Séries",
        "titre": "Blu-ray 4K Ultra HD Le Grand Bleu – Version longue",
        "enseigne": "Fnac",
        "prix": 24.99,
        "devise": "EUR",
        "description": "Le film de Luc Besson dans une édition haute définition avec version longue."
    },
    {
        "id": "CAD-388",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray Twin Peaks – L'Intégrale de la série",
        "enseigne": "Amazon",
        "prix": 69.99,
        "devise": "EUR",
        "description": "Retrouve les mystères de la ville imaginée par David Lynch dans ce coffret intégral."
    },
    {
        "id": "CAD-389",
        "categorie": "Cinéma & Séries",
        "titre": "Blu-ray 4K Ultra HD The Batman – Édition Steelbook",
        "enseigne": "Cultura",
        "prix": 34.99,
        "devise": "EUR",
        "description": "Le film de Matt Reeves dans un boîtier métal collector avec image 4K."
    },
    {
        "id": "CAD-390",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray 4K Le Château ambulant – Studio Ghibli",
        "enseigne": "Fnac",
        "prix": 29.99,
        "devise": "EUR",
        "description": "Le film d'animation de Hayao Miyazaki en haute définition."
    },
    {
        "id": "CAD-391",
        "categorie": "High-Tech & Audio",
        "titre": "Liseuse Kobo Libra Colour 32 Go Noire",
        "enseigne": "Fnac",
        "prix": 229.99,
        "devise": "EUR",
        "description": "Liseuse à écran couleur avec boutons physiques et prise en charge du stylet compatible."
    },
    {
        "id": "CAD-392",
        "categorie": "High-Tech & Audio",
        "titre": "Kit de démarrage Philips Hue White and Color Ambiance E27",
        "enseigne": "Boulanger",
        "prix": 89.99,
        "devise": "EUR",
        "description": "Kit connecté pour piloter l'éclairage et créer des ambiances lumineuses personnalisées."
    },
    {
        "id": "CAD-393",
        "categorie": "High-Tech & Audio",
        "titre": "Webcam Logitech Brio 4K Ultra HD",
        "enseigne": "Darty",
        "prix": 139.99,
        "devise": "EUR",
        "description": "Webcam haute définition avec cadrage automatique et correction de l'éclairage."
    },
    {
        "id": "CAD-394",
        "categorie": "High-Tech & Audio",
        "titre": "Routeur Wi-Fi maillé TP-Link Deco X50 Pack de 2",
        "enseigne": "Amazon",
        "prix": 149.99,
        "devise": "EUR",
        "description": "Système Wi-Fi 6 maillé destiné à améliorer la couverture réseau du logement."
    },
    {
        "id": "CAD-395",
        "categorie": "High-Tech & Audio",
        "titre": "Clavier mécanique sans fil Keychron K2 Pro RGB",
        "enseigne": "Fnac",
        "prix": 119.99,
        "devise": "EUR",
        "description": "Clavier compact mécanique avec rétroéclairage RGB et connexion sans fil."
    },
    {
        "id": "CAD-396",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Cascadia – Édition française",
        "enseigne": "Cultura",
        "prix": 34.90,
        "devise": "EUR",
        "description": "Jeu de placement de tuiles et d'animaux consacré aux écosystèmes du nord-ouest américain."
    },
    {
        "id": "CAD-397",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Heat – Pédale au métal",
        "enseigne": "Philibert",
        "prix": 69.90,
        "devise": "EUR",
        "description": "Jeu de course automobile tactique avec gestion de vitesse et de chaleur moteur."
    },
    {
        "id": "CAD-398",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Faraway – Édition française Catch Up Games",
        "enseigne": "Cultura",
        "prix": 19.90,
        "devise": "EUR",
        "description": "Jeu de cartes stratégique où les régions explorées se décomptent dans l'ordre inverse."
    },
    {
        "id": "CAD-399",
        "categorie": "Jeux & Société",
        "titre": "Jeu coopératif Sky Team – Édition française",
        "enseigne": "Fnac",
        "prix": 24.90,
        "devise": "EUR",
        "description": "Jeu coopératif à deux joueurs consacré au pilotage et à l'atterrissage d'un avion."
    },
    {
        "id": "CAD-400",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Patchwork – Édition française",
        "enseigne": "Cultura",
        "prix": 24.99,
        "devise": "EUR",
        "description": "Jeu de stratégie à deux joueurs autour de la création d'une couverture en pièces de tissu."
    },
    {
        "id": "CAD-401",
        "categorie": "Livres & BD",
        "titre": "Roman La Passe-miroir – Tome 1 : Les Fiancés de l'hiver, Christelle Dabos",
        "enseigne": "Fnac",
        "prix": 9.90,
        "devise": "EUR",
        "description": "Premier volume d'une saga fantastique française dans un univers foisonnant."
    },
    {
        "id": "CAD-402",
        "categorie": "Livres & BD",
        "titre": "Essai Sapiens – Une brève histoire de l'humanité, Yuval Noah Harari",
        "enseigne": "Cultura",
        "prix": 12.90,
        "devise": "EUR",
        "description": "Une synthèse accessible de l'évolution des sociétés humaines."
    },
    {
        "id": "CAD-403",
        "categorie": "Livres & BD",
        "titre": "BD Carbone et Silicium – Mathieu Bablet, Éditions Ankama",
        "enseigne": "Fnac",
        "prix": 22.90,
        "devise": "EUR",
        "description": "Roman graphique de science-fiction sur l'intelligence artificielle et le devenir de l'humanité."
    },
    {
        "id": "CAD-404",
        "categorie": "Livres & BD",
        "titre": "Roman La Vérité sur l'affaire Harry Quebert – Joël Dicker",
        "enseigne": "Cultura",
        "prix": 10.90,
        "devise": "EUR",
        "description": "Thriller littéraire autour d'une enquête et d'un écrivain américain."
    },
    {
        "id": "CAD-405",
        "categorie": "Livres & BD",
        "titre": "Manga Frieren – Tome 1, Kanehito Yamada et Tsukasa Abe",
        "enseigne": "Fnac",
        "prix": 7.95,
        "devise": "EUR",
        "description": "Début d'un manga fantastique qui suit une elfe après la fin de la grande quête."
    },
    {
        "id": "CAD-406",
        "categorie": "Gastronomie",
        "titre": "Friteuse sans huile Ninja Foodi Dual Zone AF300EU",
        "enseigne": "Boulanger",
        "prix": 179.99,
        "devise": "EUR",
        "description": "Air fryer à deux tiroirs indépendants pour préparer simultanément deux recettes."
    },
    {
        "id": "CAD-407",
        "categorie": "Gastronomie",
        "titre": "Cocotte en fonte Staub La Cocotte Ronde 24 cm Rouge Cerise",
        "enseigne": "Galeries Lafayette",
        "prix": 279.00,
        "devise": "EUR",
        "description": "Cocotte en fonte émaillée adaptée aux mijotés, braisés et cuissons au four."
    },
    {
        "id": "CAD-408",
        "categorie": "Gastronomie",
        "titre": "Robot cuiseur Moulinex Companion XL HF80C800",
        "enseigne": "Darty",
        "prix": 699.99,
        "devise": "EUR",
        "description": "Robot multifonction chauffant avec grande capacité pour préparer des repas complets."
    },
    {
        "id": "CAD-409",
        "categorie": "Gastronomie",
        "titre": "Coffret de dégustation de cafés de spécialité Terres de Café",
        "enseigne": "Terres de Café",
        "prix": 32.00,
        "devise": "EUR",
        "description": "Sélection de cafés de spécialité pour découvrir plusieurs origines et profils aromatiques."
    },
    {
        "id": "CAD-410",
        "categorie": "Maison & Déco",
        "titre": "Purificateur d'air connecté Levoit Core 300S",
        "enseigne": "Amazon",
        "prix": 149.99,
        "devise": "EUR",
        "description": "Purificateur compact avec filtration multicouche et pilotage connecté."
    },
    {
        "id": "CAD-411",
        "categorie": "Maison & Déco",
        "titre": "Lampe de bureau Anglepoise Type 75 Margaret Howell Edition",
        "enseigne": "Made In Design",
        "prix": 295.00,
        "devise": "EUR",
        "description": "Lampe articulée au design contemporain pour éclairer un bureau ou un espace de lecture."
    },
    {
        "id": "CAD-412",
        "categorie": "Maison & Déco",
        "titre": "Coussin chauffant électrique Beurer HK 125 XXL",
        "enseigne": "Darty",
        "prix": 69.99,
        "devise": "EUR",
        "description": "Grand coussin chauffant textile avec plusieurs niveaux de température."
    },
    {
        "id": "CAD-413",
        "categorie": "Maison & Déco",
        "titre": "Ensemble de casseroles Cristel Mutine amovible 3 pièces",
        "enseigne": "Mathon",
        "prix": 249.90,
        "devise": "EUR",
        "description": "Batterie de casseroles en inox à poignées amovibles pour optimiser le rangement."
    },
    {
        "id": "CAD-414",
        "categorie": "Maison & Déco",
        "titre": "Vase Hay Splash Large en verre coloré",
        "enseigne": "Made In Design",
        "prix": 79.00,
        "devise": "EUR",
        "description": "Vase décoratif en verre soufflé aux formes organiques et aux couleurs contrastées."
    },
    {
        "id": "CAD-415",
        "categorie": "Beauté & Parfums",
        "titre": "Eau de Parfum Maison Margiela Replica By the Fireplace 100 ml",
        "enseigne": "Sephora",
        "prix": 145.00,
        "devise": "EUR",
        "description": "Parfum aux notes boisées et fumées évoquant un feu de cheminée."
    },
    {
        "id": "CAD-416",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret soins visage Estée Lauder Advanced Night Repair",
        "enseigne": "Sephora",
        "prix": 98.00,
        "devise": "EUR",
        "description": "Coffret découverte autour du sérum Advanced Night Repair et de soins complémentaires."
    },
    {
        "id": "CAD-417",
        "categorie": "Beauté & Parfums",
        "titre": "Palette de fards à paupières Natasha Denona Mini Glam",
        "enseigne": "Sephora",
        "prix": 29.90,
        "devise": "EUR",
        "description": "Petite palette de teintes neutres et lumineuses pour réaliser différents maquillages."
    },
    {
        "id": "CAD-418",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret parfum Acqua di Parma Colonia Eau de Cologne 100 ml",
        "enseigne": "Galeries Lafayette",
        "prix": 135.00,
        "devise": "EUR",
        "description": "Eau de Cologne aux agrumes présentée dans un coffret cadeau élégant."
    },
    {
        "id": "CAD-419",
        "categorie": "Sport & Bien-être",
        "titre": "Raquette de tennis Babolat Boost Drive Bleu",
        "enseigne": "Decathlon",
        "prix": 89.99,
        "devise": "EUR",
        "description": "Raquette légère et tolérante conçue pour les joueurs débutants et occasionnels."
    },
    {
        "id": "CAD-420",
        "categorie": "Sport & Bien-être",
        "titre": "Tapis de course pliable Domyos T520B",
        "enseigne": "Decathlon",
        "prix": 499.99,
        "devise": "EUR",
        "description": "Tapis de course motorisé pour l'entraînement à domicile avec rangement pliable."
    },
    {
        "id": "CAD-421",
        "categorie": "Sport & Bien-être",
        "titre": "Sac de couchage randonnée Forclaz MT500 15 °C",
        "enseigne": "Decathlon",
        "prix": 69.99,
        "devise": "EUR",
        "description": "Sac de couchage compact destiné aux nuits en bivouac par températures douces."
    },
    {
        "id": "CAD-422",
        "categorie": "Sport & Bien-être",
        "titre": "Montre GPS de running Polar Pacer Pro Noire",
        "enseigne": "i-Run",
        "prix": 299.90,
        "devise": "EUR",
        "description": "Montre sportive avec suivi GPS, mesure de l'entraînement et analyse de récupération."
    },
    {
        "id": "CAD-423",
        "categorie": "Sport & Bien-être",
        "titre": "Vélo d'appartement connecté Schwinn 510U",
        "enseigne": "FitnessBoutique",
        "prix": 599.00,
        "devise": "EUR",
        "description": "Vélo d'intérieur avec résistance réglable et console de suivi des séances."
    },
    {
        "id": "CAD-424",
        "categorie": "Mode & Accessoires",
        "titre": "Baskets Adidas Samba OG Blanc et Noir",
        "enseigne": "Courir",
        "prix": 120.00,
        "devise": "EUR",
        "description": "Sneakers emblématiques en cuir avec semelle extérieure en gomme."
    },
    {
        "id": "CAD-425",
        "categorie": "Mode & Accessoires",
        "titre": "Montre Swatch Clearly Gent SO28K100",
        "enseigne": "Swatch",
        "prix": 90.00,
        "devise": "EUR",
        "description": "Montre transparente au style minimaliste avec mouvement à quartz."
    },
    {
        "id": "CAD-426",
        "categorie": "Mode & Accessoires",
        "titre": "Sac à main Longchamp Le Pliage Original Taille M Noir",
        "enseigne": "Longchamp",
        "prix": 125.00,
        "devise": "EUR",
        "description": "Sac pliable léger en toile avec rabat et poignées en cuir."
    },
    {
        "id": "CAD-427",
        "categorie": "Mode & Accessoires",
        "titre": "Bottines Dr. Martens 1460 Smooth Cuir Noir",
        "enseigne": "Galeries Lafayette",
        "prix": 200.00,
        "devise": "EUR",
        "description": "Bottines à huit œillets avec surpiqûre jaune et semelle emblématique."
    },
    {
        "id": "CAD-428",
        "categorie": "Loisirs & Créatifs",
        "titre": "Machine de découpe Silhouette Portrait 4",
        "enseigne": "Cultura",
        "prix": 179.99,
        "devise": "EUR",
        "description": "Machine compacte pour découper papier, vinyle et matériaux créatifs compatibles."
    },
    {
        "id": "CAD-429",
        "categorie": "Loisirs & Créatifs",
        "titre": "Coffret de peinture acrylique Liquitex Basics 24 tubes",
        "enseigne": "Rougier & Plé",
        "prix": 39.90,
        "devise": "EUR",
        "description": "Assortiment de couleurs acryliques pour peinture sur toile et supports adaptés."
    },
    {
        "id": "CAD-430",
        "categorie": "Loisirs & Créatifs",
        "titre": "Kit de gravure linoléum Speedball Deluxe",
        "enseigne": "Rougier & Plé",
        "prix": 54.90,
        "devise": "EUR",
        "description": "Ensemble d'outils et de matériel pour découvrir la gravure et l'impression artisanale."
    },
    {
        "id": "CAD-431",
        "categorie": "Loisirs & Créatifs",
        "titre": "Coffret LEGO Art 31208 Hokusai – La Grande Vague",
        "enseigne": "LEGO",
        "prix": 99.99,
        "devise": "EUR",
        "description": "Set décoratif à assembler inspiré de l'estampe japonaise de Hokusai."
    },
    {
        "id": "CAD-432",
        "categorie": "Enfants & Ados",
        "titre": "Maison de poupée en bois KidKraft Chelsea",
        "enseigne": "Oxybul",
        "prix": 119.99,
        "devise": "EUR",
        "description": "Maison de poupée à plusieurs niveaux avec mobilier pour inventer des histoires."
    },
    {
        "id": "CAD-433",
        "categorie": "Enfants & Ados",
        "titre": "Boîte à histoires Tonies Starter Set avec Toniebox 2",
        "enseigne": "Fnac",
        "prix": 109.99,
        "devise": "EUR",
        "description": "Lecteur audio pour enfants fonctionnant avec des figurines d'histoires et de chansons."
    },
    {
        "id": "CAD-434",
        "categorie": "Enfants & Ados",
        "titre": "Jeu de construction Plus-Plus BIG Basic 100 pièces",
        "enseigne": "Oxybul",
        "prix": 29.99,
        "devise": "EUR",
        "description": "Grandes pièces de construction faciles à manipuler pour créer formes et personnages."
    },
    {
        "id": "CAD-435",
        "categorie": "Enfants & Ados",
        "titre": "Coffret Playmobil 71418 Château de Princesse",
        "enseigne": "King Jouet",
        "prix": 89.99,
        "devise": "EUR",
        "description": "Univers de jeu avec château et personnages pour inventer des aventures royales."
    },
    {
        "id": "CAD-436",
        "categorie": "Enfants & Ados",
        "titre": "Jeu éducatif Osmo Genius Starter Kit pour iPad",
        "enseigne": "Fnac",
        "prix": 79.99,
        "devise": "EUR",
        "description": "Kit d'activités interactives mêlant pièces physiques et apprentissages sur tablette compatible."
    },
        {
        "id": "CAD-437",
        "categorie": "Cinéma & Séries",
        "titre": "Blu-ray 4K Ultra HD 2001 : L'Odyssée de l'espace – Édition collector",
        "enseigne": "Fnac",
        "prix": 29.99,
        "devise": "EUR",
        "description": "Le chef-d'œuvre de Stanley Kubrick dans une édition restaurée en ultra haute définition."
    },
    {
        "id": "CAD-438",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray Twin Peaks: The Return – Saison 3",
        "enseigne": "Amazon",
        "prix": 39.99,
        "devise": "EUR",
        "description": "La troisième saison de la série de David Lynch en haute définition."
    },
    {
        "id": "CAD-439",
        "categorie": "Cinéma & Séries",
        "titre": "Blu-ray 4K Ultra HD Apocalypse Now – Final Cut",
        "enseigne": "Cultura",
        "prix": 27.99,
        "devise": "EUR",
        "description": "Le film de Francis Ford Coppola dans sa version Final Cut restaurée en 4K."
    },
    {
        "id": "CAD-440",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray Le Bureau des légendes – Intégrale des saisons",
        "enseigne": "Fnac",
        "prix": 59.99,
        "devise": "EUR",
        "description": "Retrouvez la série française d'espionnage dans un coffret réunissant ses saisons."
    },
    {
        "id": "CAD-441",
        "categorie": "Cinéma & Séries",
        "titre": "Blu-ray 4K Ultra HD Les Dents de la mer – Édition anniversaire",
        "enseigne": "Cultura",
        "prix": 24.99,
        "devise": "EUR",
        "description": "Le thriller de Steven Spielberg dans une restauration haute définition."
    },
    {
        "id": "CAD-442",
        "categorie": "High-Tech & Audio",
        "titre": "Casque audio Bose QuietComfort Ultra Headphones Noir",
        "enseigne": "Boulanger",
        "prix": 449.00,
        "devise": "EUR",
        "description": "Casque sans fil avec réduction de bruit active et audio immersif."
    },
    {
        "id": "CAD-443",
        "categorie": "High-Tech & Audio",
        "titre": "Enceinte connectée Sonos Era 100 Noire",
        "enseigne": "Fnac",
        "prix": 279.00,
        "devise": "EUR",
        "description": "Enceinte Wi-Fi compacte avec commandes vocales et diffusion multiroom."
    },
    {
        "id": "CAD-444",
        "categorie": "High-Tech & Audio",
        "titre": "Disque SSD externe Samsung T7 Shield 2 To Bleu",
        "enseigne": "Darty",
        "prix": 179.99,
        "devise": "EUR",
        "description": "Stockage portable rapide avec boîtier renforcé résistant aux chocs et aux projections."
    },
    {
        "id": "CAD-445",
        "categorie": "High-Tech & Audio",
        "titre": "Appareil photo hybride Fujifilm X-S20 avec objectif XC 15-45 mm",
        "enseigne": "Miss Numérique",
        "prix": 1499.00,
        "devise": "EUR",
        "description": "Appareil hybride polyvalent avec stabilisation intégrée et fonctions vidéo avancées."
    },
    {
        "id": "CAD-446",
        "categorie": "High-Tech & Audio",
        "titre": "Écran PC Dell UltraSharp U2723QE 27 pouces 4K",
        "enseigne": "Dell",
        "prix": 599.00,
        "devise": "EUR",
        "description": "Moniteur 4K IPS Black avec connectique USB-C pour le travail et la création."
    },
    {
        "id": "CAD-447",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Sea Salt & Paper – Édition française",
        "enseigne": "Philibert",
        "prix": 12.90,
        "devise": "EUR",
        "description": "Jeu de cartes tactique aux illustrations en origami et aux parties rapides."
    },
    {
        "id": "CAD-448",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Everdell – Édition française",
        "enseigne": "Cultura",
        "prix": 69.90,
        "devise": "EUR",
        "description": "Jeu de placement d'ouvriers et de construction de cité dans un univers forestier."
    },
    {
        "id": "CAD-449",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Les Charlatans de Belcastel – Édition française",
        "enseigne": "Philibert",
        "prix": 39.90,
        "devise": "EUR",
        "description": "Jeu de prise de risque où chacun compose sa potion en piochant des ingrédients."
    },
    {
        "id": "CAD-450",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Turing Machine – Édition française",
        "enseigne": "Fnac",
        "prix": 34.90,
        "devise": "EUR",
        "description": "Jeu de déduction logique utilisant un ordinateur mécanique et des cartes perforées."
    },
    {
        "id": "CAD-451",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société La Bête – Édition française",
        "enseigne": "Philibert",
        "prix": 34.90,
        "devise": "EUR",
        "description": "Jeu asymétrique de déduction et de poursuite inspiré de la légende de la Bête du Gévaudan."
    },
    {
        "id": "CAD-452",
        "categorie": "Livres & BD",
        "titre": "Roman Le Nom du vent – Patrick Rothfuss, édition poche",
        "enseigne": "Cultura",
        "prix": 11.90,
        "devise": "EUR",
        "description": "Premier volume d'une grande saga de fantasy racontée par son mystérieux héros."
    },
    {
        "id": "CAD-453",
        "categorie": "Livres & BD",
        "titre": "BD Shangri-La – Mathieu Bablet, Éditions Ankama",
        "enseigne": "Fnac",
        "prix": 22.90,
        "devise": "EUR",
        "description": "Roman graphique de science-fiction sur une humanité réfugiée dans une station spatiale."
    },
    {
        "id": "CAD-454",
        "categorie": "Livres & BD",
        "titre": "Manga L'Atelier des sorciers – Tome 1, Kamome Shirahama",
        "enseigne": "Cultura",
        "prix": 7.95,
        "devise": "EUR",
        "description": "Début d'une série fantastique centrée sur l'apprentissage de la magie et ses secrets."
    },
    {
        "id": "CAD-455",
        "categorie": "Livres & BD",
        "titre": "Roman La Horde du Contrevent – Alain Damasio, édition poche",
        "enseigne": "Fnac",
        "prix": 10.90,
        "devise": "EUR",
        "description": "Récit de science-fiction suivant un groupe lancé à contre-courant d'un vent perpétuel."
    },
    {
        "id": "CAD-456",
        "categorie": "Livres & BD",
        "titre": "Beau livre Le Monde de la photographie de rue – Éditions Phaidon",
        "enseigne": "Fnac",
        "prix": 39.95,
        "devise": "EUR",
        "description": "Sélection de photographies urbaines accompagnées de repères historiques et artistiques."
    },
    {
        "id": "CAD-457",
        "categorie": "Gastronomie",
        "titre": "Four à pizza électrique Ooni Volt 12",
        "enseigne": "Ooni",
        "prix": 899.00,
        "devise": "EUR",
        "description": "Four électrique d'intérieur conçu pour cuire des pizzas à très haute température."
    },
    {
        "id": "CAD-458",
        "categorie": "Gastronomie",
        "titre": "Cave à fromage de service Boska Friends",
        "enseigne": "Mathon",
        "prix": 89.90,
        "devise": "EUR",
        "description": "Accessoire de présentation et de conservation pour servir différents fromages à table."
    },
    {
        "id": "CAD-459",
        "categorie": "Gastronomie",
        "titre": "Blender haute performance Vitamix Explorian E310",
        "enseigne": "Darty",
        "prix": 449.00,
        "devise": "EUR",
        "description": "Blender puissant avec plusieurs vitesses pour soupes, smoothies et préparations maison."
    },
    {
        "id": "CAD-460",
        "categorie": "Gastronomie",
        "titre": "Coffret de dégustation de thés Mariage Frères Marco Polo",
        "enseigne": "Mariage Frères",
        "prix": 42.00,
        "devise": "EUR",
        "description": "Sélection de thés parfumés autour de la recette emblématique Marco Polo."
    },
    {
        "id": "CAD-461",
        "categorie": "Gastronomie",
        "titre": "Balance de cuisine connectée Terraillon NutriTab",
        "enseigne": "Boulanger",
        "prix": 59.99,
        "devise": "EUR",
        "description": "Balance de précision avec suivi des quantités et informations nutritionnelles via application."
    },
    {
        "id": "CAD-462",
        "categorie": "Maison & Déco",
        "titre": "Fauteuil design IKEA STRANDMON à oreilles",
        "enseigne": "IKEA",
        "prix": 299.00,
        "devise": "EUR",
        "description": "Fauteuil à dossier haut et accoudoirs enveloppants pour un coin lecture confortable."
    },
    {
        "id": "CAD-463",
        "categorie": "Maison & Déco",
        "titre": "Lampe suspendue Muuto Ambit Ø 40 cm",
        "enseigne": "Made In Design",
        "prix": 399.00,
        "devise": "EUR",
        "description": "Suspension en aluminium au design scandinave épuré pour éclairer une pièce de vie."
    },
    {
        "id": "CAD-464",
        "categorie": "Maison & Déco",
        "titre": "Aspirateur robot Roborock Q8 Max+",
        "enseigne": "Boulanger",
        "prix": 599.00,
        "devise": "EUR",
        "description": "Robot aspirateur avec station de vidage automatique et navigation cartographique."
    },
    {
        "id": "CAD-465",
        "categorie": "Maison & Déco",
        "titre": "Miroir mural rond AM.PM Hémisphère en métal",
        "enseigne": "La Redoute",
        "prix": 159.00,
        "devise": "EUR",
        "description": "Miroir décoratif à contour métallique pour agrandir visuellement une entrée ou un séjour."
    },
    {
        "id": "CAD-466",
        "categorie": "Maison & Déco",
        "titre": "Parure de lit satin de coton Bonsoirs – modèle Ginkgo",
        "enseigne": "Bonsoirs",
        "prix": 189.00,
        "devise": "EUR",
        "description": "Linge de lit en satin de coton avec motif végétal pour une chambre élégante."
    },
    {
        "id": "CAD-467",
        "categorie": "Beauté & Parfums",
        "titre": "Eau de Parfum Diptyque Orphéon 75 ml",
        "enseigne": "Diptyque",
        "prix": 190.00,
        "devise": "EUR",
        "description": "Parfum boisé et poudré inspiré de l'atmosphère d'un club parisien."
    },
    {
        "id": "CAD-468",
        "categorie": "Beauté & Parfums",
        "titre": "Sérum visage La Roche-Posay Hyalu B5 30 ml",
        "enseigne": "Nocibé",
        "prix": 39.90,
        "devise": "EUR",
        "description": "Sérum hydratant formulé avec de l'acide hyaluronique et de la vitamine B5."
    },
    {
        "id": "CAD-469",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret parfum Juliette Has a Gun Not a Perfume 50 ml",
        "enseigne": "Sephora",
        "prix": 105.00,
        "devise": "EUR",
        "description": "Parfum minimaliste construit autour d'une note unique de Cetalox."
    },
    {
        "id": "CAD-470",
        "categorie": "Beauté & Parfums",
        "titre": "Sèche-cheveux professionnel Parlux Alyon Noir",
        "enseigne": "Bleu Libellule",
        "prix": 179.00,
        "devise": "EUR",
        "description": "Sèche-cheveux professionnel léger avec moteur puissant et technologie ionique."
    },
    {
        "id": "CAD-471",
        "categorie": "Sport & Bien-être",
        "titre": "Chaussures de trail Salomon Speedcross 6 Homme",
        "enseigne": "i-Run",
        "prix": 140.00,
        "devise": "EUR",
        "description": "Chaussures de trail avec crampons profonds pour les terrains meubles et boueux."
    },
    {
        "id": "CAD-472",
        "categorie": "Sport & Bien-être",
        "titre": "Vélo gravel Triban GRVL 520 Subcompact",
        "enseigne": "Decathlon",
        "prix": 1199.00,
        "devise": "EUR",
        "description": "Vélo polyvalent conçu pour alterner routes, chemins et longues sorties."
    },
    {
        "id": "CAD-473",
        "categorie": "Sport & Bien-être",
        "titre": "Tente de randonnée MSR Hubba Hubba NX 2 personnes",
        "enseigne": "Au Vieux Campeur",
        "prix": 599.00,
        "devise": "EUR",
        "description": "Tente autoportante deux places destinée au trekking et aux nuits en itinérance."
    },
    {
        "id": "CAD-474",
        "categorie": "Sport & Bien-être",
        "titre": "Rameur magnétique Concept2 RowErg avec écran PM5",
        "enseigne": "FitnessBoutique",
        "prix": 1190.00,
        "devise": "EUR",
        "description": "Rameur d'entraînement avec résistance à air et moniteur de performance PM5."
    },
    {
        "id": "CAD-475",
        "categorie": "Mode & Accessoires",
        "titre": "Baskets New Balance 990v6 Made in USA",
        "enseigne": "Courir",
        "prix": 250.00,
        "devise": "EUR",
        "description": "Sneakers premium associant amorti moderne et silhouette classique de la marque."
    },
    {
        "id": "CAD-476",
        "categorie": "Mode & Accessoires",
        "titre": "Sac bandoulière Coccinelle Beat Soft Mini",
        "enseigne": "Galeries Lafayette",
        "prix": 295.00,
        "devise": "EUR",
        "description": "Petit sac en cuir avec bandoulière réglable et fermoir métallique emblématique."
    },
    {
        "id": "CAD-477",
        "categorie": "Mode & Accessoires",
        "titre": "Lunettes de soleil Ray-Ban Clubmaster Classic RB3016",
        "enseigne": "Ray-Ban",
        "prix": 155.00,
        "devise": "EUR",
        "description": "Monture iconique combinant une partie supérieure en acétate et une structure métallique."
    },
    {
        "id": "CAD-478",
        "categorie": "Mode & Accessoires",
        "titre": "Bottines Timberland Premium 6-Inch Waterproof Wheat",
        "enseigne": "Timberland",
        "prix": 220.00,
        "devise": "EUR",
        "description": "Bottines montantes imperméables en cuir nubuck avec semelle robuste."
    },
    {
        "id": "CAD-479",
        "categorie": "Loisirs & Créatifs",
        "titre": "Set LEGO Ideas 21335 Phare motorisé",
        "enseigne": "LEGO",
        "prix": 299.99,
        "devise": "EUR",
        "description": "Maquette détaillée à construire avec éclairage et mécanisme de phare rotatif."
    },
    {
        "id": "CAD-480",
        "categorie": "Loisirs & Créatifs",
        "titre": "Coffret de calligraphie Pilot Parallel Pen Premium",
        "enseigne": "Cultura",
        "prix": 49.90,
        "devise": "EUR",
        "description": "Ensemble de stylos à plume plate et accessoires pour pratiquer la calligraphie."
    },
    {
        "id": "CAD-481",
        "categorie": "Loisirs & Créatifs",
        "titre": "Kit de peinture à l'huile Sennelier Rive Gauche 10 tubes",
        "enseigne": "Rougier & Plé",
        "prix": 59.90,
        "devise": "EUR",
        "description": "Coffret de couleurs à l'huile pour peinture artistique et étude des mélanges."
    },
    {
        "id": "CAD-482",
        "categorie": "Loisirs & Créatifs",
        "titre": "Maquette Revell Volkswagen T1 Samba Bus échelle 1:24",
        "enseigne": "JouéClub",
        "prix": 39.99,
        "devise": "EUR",
        "description": "Maquette à assembler et peindre reproduisant le célèbre minibus Volkswagen."
    },
    {
        "id": "CAD-483",
        "categorie": "Enfants & Ados",
        "titre": "LEGO Friends 41757 Jardin botanique",
        "enseigne": "LEGO",
        "prix": 84.99,
        "devise": "EUR",
        "description": "Set de construction représentant une serre avec plantes et espaces d'exploration."
    },
    {
        "id": "CAD-484",
        "categorie": "Enfants & Ados",
        "titre": "Poupée Barbie Signature Looks modèle n° 20",
        "enseigne": "King Jouet",
        "prix": 34.99,
        "devise": "EUR",
        "description": "Poupée de collection articulée avec une tenue contemporaine et des accessoires."
    },
    {
        "id": "CAD-485",
        "categorie": "Enfants & Ados",
        "titre": "Jeu éducatif SmartGames IQ Puzzler Pro",
        "enseigne": "Oxybul",
        "prix": 14.99,
        "devise": "EUR",
        "description": "Casse-tête compact proposant des défis de logique en deux et trois dimensions."
    },
    {
        "id": "CAD-486",
        "categorie": "Enfants & Ados",
        "titre": "Circuit de voitures Hot Wheels City Ultimate Garage",
        "enseigne": "JouéClub",
        "prix": 119.99,
        "devise": "EUR",
        "description": "Grand garage de jeu avec plusieurs niveaux, pistes et espaces de rangement pour voitures."
    },
        {
        "id": "CAD-487",
        "categorie": "Cinéma & Séries",
        "titre": "Blu-ray 4K Ultra HD Shining – Édition collector",
        "enseigne": "Fnac",
        "prix": 29.99,
        "devise": "EUR",
        "description": "Le film de Stanley Kubrick dans une édition restaurée en ultra haute définition."
    },
    {
        "id": "CAD-488",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray The Wire – L'Intégrale de la série",
        "enseigne": "Amazon",
        "prix": 59.99,
        "devise": "EUR",
        "description": "Les cinq saisons de la série policière réunies dans un coffret."
    },
    {
        "id": "CAD-489",
        "categorie": "Cinéma & Séries",
        "titre": "Blu-ray 4K Ultra HD Lawrence d'Arabie – Édition anniversaire",
        "enseigne": "Cultura",
        "prix": 34.99,
        "devise": "EUR",
        "description": "L'épopée de David Lean proposée dans une restauration haute définition."
    },
    {
        "id": "CAD-490",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray Les Soprano – Intégrale des saisons",
        "enseigne": "Fnac",
        "prix": 69.99,
        "devise": "EUR",
        "description": "Retrouvez l'ensemble des saisons de la série dramatique créée par David Chase."
    },
    {
        "id": "CAD-491",
        "categorie": "Cinéma & Séries",
        "titre": "Blu-ray 4K Ultra HD Le Silence des agneaux",
        "enseigne": "Cultura",
        "prix": 24.99,
        "devise": "EUR",
        "description": "Le thriller de Jonathan Demme dans une édition en ultra haute définition."
    },
    {
        "id": "CAD-492",
        "categorie": "High-Tech & Audio",
        "titre": "Écouteurs sans fil Sennheiser Momentum True Wireless 4 Graphite",
        "enseigne": "Son-Vidéo",
        "prix": 299.00,
        "devise": "EUR",
        "description": "Écouteurs Bluetooth avec réduction de bruit adaptative et restitution audio haute fidélité."
    },
    {
        "id": "CAD-493",
        "categorie": "High-Tech & Audio",
        "titre": "Clavier sans fil Logitech MX Keys S Graphite",
        "enseigne": "Boulanger",
        "prix": 119.99,
        "devise": "EUR",
        "description": "Clavier de bureau rétroéclairé avec touches confortables et connexion multi-appareils."
    },
    {
        "id": "CAD-494",
        "categorie": "High-Tech & Audio",
        "titre": "Disque dur externe Western Digital My Passport 5 To Noir",
        "enseigne": "Darty",
        "prix": 149.99,
        "devise": "EUR",
        "description": "Solution de stockage portable de grande capacité pour sauvegarder documents et médias."
    },
    {
        "id": "CAD-495",
        "categorie": "High-Tech & Audio",
        "titre": "Microphone USB Shure MV7X Podcast",
        "enseigne": "Thomann",
        "prix": 179.00,
        "devise": "EUR",
        "description": "Microphone dynamique destiné à l'enregistrement de voix, podcasts et contenus parlés."
    },
    {
        "id": "CAD-496",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Dune: La Guerre pour Arrakis – Édition française",
        "enseigne": "Philibert",
        "prix": 129.90,
        "devise": "EUR",
        "description": "Jeu stratégique asymétrique inspiré de l'univers de Dune et de ses grandes factions."
    },
    {
        "id": "CAD-497",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Akropolis – Édition française Gigamic",
        "enseigne": "Cultura",
        "prix": 29.90,
        "devise": "EUR",
        "description": "Jeu de construction de cité antique avec placement de tuiles en plusieurs niveaux."
    },
    {
        "id": "CAD-498",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Le Château Blanc – Édition française",
        "enseigne": "Philibert",
        "prix": 34.90,
        "devise": "EUR",
        "description": "Jeu de stratégie et de placement de dés dans le Japon féodal."
    },
    {
        "id": "CAD-499",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Living Forest – Édition française",
        "enseigne": "Fnac",
        "prix": 34.90,
        "devise": "EUR",
        "description": "Jeu de stratégie mêlant construction de paquet, prise de risque et protection de la forêt."
    },
    {
        "id": "CAD-500",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Welcome To… – Édition française",
        "enseigne": "Cultura",
        "prix": 19.90,
        "devise": "EUR",
        "description": "Jeu de type flip-and-write où les joueurs aménagent leur propre quartier résidentiel."
    },
    {
        "id": "CAD-501",
        "categorie": "Livres & BD",
        "titre": "Roman Fondation – Tome 1, Isaac Asimov, édition Folio SF",
        "enseigne": "Fnac",
        "prix": 9.50,
        "devise": "EUR",
        "description": "Premier volume du cycle de science-fiction consacré à la chute et à la renaissance d'un empire galactique."
    },
    {
        "id": "CAD-502",
        "categorie": "Livres & BD",
        "titre": "BD Le Chat du rabbin – Tome 1, Joann Sfar",
        "enseigne": "Cultura",
        "prix": 17.50,
        "devise": "EUR",
        "description": "Premier album de la série mettant en scène un chat philosophe dans l'Algérie des années 1930."
    },
    {
        "id": "CAD-503",
        "categorie": "Livres & BD",
        "titre": "Manga Vinland Saga – Tome 1, Makoto Yukimura",
        "enseigne": "Fnac",
        "prix": 7.95,
        "devise": "EUR",
        "description": "Début d'une fresque historique consacrée aux Vikings et à leurs expéditions."
    },
    {
        "id": "CAD-504",
        "categorie": "Livres & BD",
        "titre": "Roman Le Problème à trois corps – Liu Cixin, collection Babel",
        "enseigne": "Cultura",
        "prix": 12.90,
        "devise": "EUR",
        "description": "Roman de science-fiction mêlant premier contact extraterrestre, physique et histoire chinoise."
    },
    {
        "id": "CAD-505",
        "categorie": "Livres & BD",
        "titre": "Beau livre Atlas des lieux mystérieux – Éditions Arthaud",
        "enseigne": "Fnac",
        "prix": 29.90,
        "devise": "EUR",
        "description": "Voyage illustré à travers des sites insolites, légendes et lieux méconnus du monde."
    },
    {
        "id": "CAD-506",
        "categorie": "Gastronomie",
        "titre": "Machine à espresso Sage Barista Express Impress",
        "enseigne": "Boulanger",
        "prix": 799.99,
        "devise": "EUR",
        "description": "Machine espresso avec moulin intégré et assistance au tassage du café."
    },
    {
        "id": "CAD-507",
        "categorie": "Gastronomie",
        "titre": "Cocotte en fonte Le Creuset Signature 26 cm Bleu Marseille",
        "enseigne": "Le Creuset",
        "prix": 399.00,
        "devise": "EUR",
        "description": "Cocotte en fonte émaillée pour mijoter, braiser et cuire au four."
    },
    {
        "id": "CAD-508",
        "categorie": "Gastronomie",
        "titre": "Machine à glaçons compacte H.Koenig KB14",
        "enseigne": "Darty",
        "prix": 129.99,
        "devise": "EUR",
        "description": "Appareil de comptoir produisant des glaçons pour les boissons et réceptions."
    },
    {
        "id": "CAD-509",
        "categorie": "Gastronomie",
        "titre": "Coffret découverte chocolats grands crus Michel Cluizel",
        "enseigne": "Michel Cluizel",
        "prix": 45.00,
        "devise": "EUR",
        "description": "Assortiment de chocolats fins permettant de découvrir plusieurs origines de cacao."
    },
    {
        "id": "CAD-510",
        "categorie": "Maison & Déco",
        "titre": "Fauteuil à bascule IKEA POÄNG avec coussin",
        "enseigne": "IKEA",
        "prix": 169.00,
        "devise": "EUR",
        "description": "Fauteuil à structure cintrée conçu pour offrir une assise souple et relaxante."
    },
    {
        "id": "CAD-511",
        "categorie": "Maison & Déco",
        "titre": "Suspension design Flos IC Lights S2",
        "enseigne": "Made In Design",
        "prix": 690.00,
        "devise": "EUR",
        "description": "Luminaire suspendu associant une sphère en verre soufflé à une structure métallique."
    },
    {
        "id": "CAD-512",
        "categorie": "Maison & Déco",
        "titre": "Aspirateur balai sans fil Samsung Bespoke Jet Plus",
        "enseigne": "Boulanger",
        "prix": 799.00,
        "devise": "EUR",
        "description": "Aspirateur sans fil avec station de vidage et accessoires pour différents types de sols."
    },
    {
        "id": "CAD-513",
        "categorie": "Maison & Déco",
        "titre": "Table d'appoint Ferm Living Plant Box Small",
        "enseigne": "The Cool Republic",
        "prix": 199.00,
        "devise": "EUR",
        "description": "Petit meuble polyvalent en métal pouvant accueillir plantes, livres ou objets décoratifs."
    },
    {
        "id": "CAD-514",
        "categorie": "Maison & Déco",
        "titre": "Ensemble de verres à eau La Rochère Abeille – Lot de 6",
        "enseigne": "La Rochère",
        "prix": 39.90,
        "devise": "EUR",
        "description": "Verres en verre pressé décorés du motif abeille emblématique de la verrerie française."
    },
    {
        "id": "CAD-515",
        "categorie": "Beauté & Parfums",
        "titre": "Eau de Parfum Guerlain Aqua Allegoria Mandarine Basilic 75 ml",
        "enseigne": "Guerlain",
        "prix": 125.00,
        "devise": "EUR",
        "description": "Parfum frais et lumineux associant des notes d'agrumes et de basilic."
    },
    {
        "id": "CAD-516",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret soin visage Clarins Double Serum Collection",
        "enseigne": "Clarins",
        "prix": 118.00,
        "devise": "EUR",
        "description": "Coffret de soins autour du sérum emblématique de la marque et de produits complémentaires."
    },
    {
        "id": "CAD-517",
        "categorie": "Beauté & Parfums",
        "titre": "Palette maquillage Dior Backstage Face & Body Glow",
        "enseigne": "Sephora",
        "prix": 52.00,
        "devise": "EUR",
        "description": "Palette illuminatrice pour apporter des reflets lumineux au visage et au corps."
    },
    {
        "id": "CAD-518",
        "categorie": "Beauté & Parfums",
        "titre": "Eau de Parfum Narciso Rodriguez For Her Musc Noir Rose 50 ml",
        "enseigne": "Nocibé",
        "prix": 112.00,
        "devise": "EUR",
        "description": "Composition florale et musquée aux accents fruités et sensuels."
    },
    {
        "id": "CAD-519",
        "categorie": "Sport & Bien-être",
        "titre": "Chaussures de randonnée Merrell Moab 3 GTX Homme",
        "enseigne": "Au Vieux Campeur",
        "prix": 160.00,
        "devise": "EUR",
        "description": "Chaussures de marche imperméables avec membrane Gore-Tex et semelle adhérente."
    },
    {
        "id": "CAD-520",
        "categorie": "Sport & Bien-être",
        "titre": "Vélo elliptique NordicTrack AirGlide 14i",
        "enseigne": "FitnessBoutique",
        "prix": 1999.00,
        "devise": "EUR",
        "description": "Appareil de cardio-training avec inclinaison réglable et console interactive."
    },
    {
        "id": "CAD-521",
        "categorie": "Sport & Bien-être",
        "titre": "Sac de randonnée Osprey Talon 22 litres",
        "enseigne": "Au Vieux Campeur",
        "prix": 150.00,
        "devise": "EUR",
        "description": "Sac léger pour randonnée à la journée avec dos ventilé et rangements accessibles."
    },
    {
        "id": "CAD-522",
        "categorie": "Sport & Bien-être",
        "titre": "Raquette de badminton Yonex Astrox 88D Play",
        "enseigne": "Badmania",
        "prix": 79.90,
        "devise": "EUR",
        "description": "Raquette orientée vers le jeu offensif et les frappes puissantes depuis le fond du court."
    },
    {
        "id": "CAD-523",
        "categorie": "Mode & Accessoires",
        "titre": "Sac à dos Rains Backpack Mini W3 Noir",
        "enseigne": "Rains",
        "prix": 80.00,
        "devise": "EUR",
        "description": "Sac urbain compact en matière imperméable avec fermeture à rabat."
    },
    {
        "id": "CAD-524",
        "categorie": "Mode & Accessoires",
        "titre": "Montre Tissot PRX Quartz 35 mm cadran bleu",
        "enseigne": "Tissot",
        "prix": 395.00,
        "devise": "EUR",
        "description": "Montre suisse à quartz avec bracelet intégré et boîtier au design rétro."
    },
    {
        "id": "CAD-525",
        "categorie": "Mode & Accessoires",
        "titre": "Ceinture en cuir grainé A.P.C. Betty",
        "enseigne": "A.P.C.",
        "prix": 150.00,
        "devise": "EUR",
        "description": "Ceinture en cuir à boucle métallique pour compléter une tenue quotidienne."
    },
    {
        "id": "CAD-526",
        "categorie": "Mode & Accessoires",
        "titre": "Sac cabas Marc Jacobs The Tote Bag Canvas Medium",
        "enseigne": "Galeries Lafayette",
        "prix": 195.00,
        "devise": "EUR",
        "description": "Cabas en toile épaisse avec poignées et bandoulière amovible."
    },
    {
        "id": "CAD-527",
        "categorie": "Mode & Accessoires",
        "titre": "Baskets Veja Campo Chromefree Leather Extra White",
        "enseigne": "Veja",
        "prix": 150.00,
        "devise": "EUR",
        "description": "Sneakers en cuir avec logo latéral contrasté et semelle en caoutchouc."
    },
    {
        "id": "CAD-528",
        "categorie": "Loisirs & Créatifs",
        "titre": "Coffret de dessin Derwent Academy 48 pièces",
        "enseigne": "Rougier & Plé",
        "prix": 49.90,
        "devise": "EUR",
        "description": "Assortiment de crayons et accessoires pour le dessin et les travaux d'illustration."
    },
    {
        "id": "CAD-529",
        "categorie": "Loisirs & Créatifs",
        "titre": "Kit de fabrication de bijoux Miyuki Delica assortiment de perles",
        "enseigne": "Perles & Co",
        "prix": 34.90,
        "devise": "EUR",
        "description": "Ensemble de perles cylindriques et accessoires pour créer bracelets et bijoux tissés."
    },
    {
        "id": "CAD-530",
        "categorie": "Loisirs & Créatifs",
        "titre": "Machine à coudre Brother CS10s",
        "enseigne": "Cultura",
        "prix": 199.99,
        "devise": "EUR",
        "description": "Machine électronique proposant plusieurs points pour les travaux de couture domestique."
    },
    {
        "id": "CAD-531",
        "categorie": "Loisirs & Créatifs",
        "titre": "Coffret de peinture aquarelle Daniel Smith Extra Fine 12 couleurs",
        "enseigne": "Rougier & Plé",
        "prix": 89.90,
        "devise": "EUR",
        "description": "Sélection de pigments aquarelle extra-fins pour les techniques humides et les lavis."
    },
    {
        "id": "CAD-532",
        "categorie": "Loisirs & Créatifs",
        "titre": "Kit de modelage Fimo Soft 24 pains de pâte polymère",
        "enseigne": "Cultura",
        "prix": 29.99,
        "devise": "EUR",
        "description": "Assortiment de pâtes polymères colorées pour fabriquer figurines, bijoux et petits objets."
    },
    {
        "id": "CAD-533",
        "categorie": "Enfants & Ados",
        "titre": "LEGO Creator 3-en-1 31150 Animaux sauvages en safari",
        "enseigne": "LEGO",
        "prix": 64.99,
        "devise": "EUR",
        "description": "Set de construction permettant de réaliser plusieurs modèles d'animaux sauvages."
    },
    {
        "id": "CAD-534",
        "categorie": "Enfants & Ados",
        "titre": "Jeu éducatif Osmo Coding Starter Kit pour iPad",
        "enseigne": "Fnac",
        "prix": 59.99,
        "devise": "EUR",
        "description": "Kit ludique d'initiation à la programmation à l'aide de blocs physiques et d'une tablette compatible."
    },
    {
        "id": "CAD-535",
        "categorie": "Enfants & Ados",
        "titre": "Circuit de voitures Carrera GO!!! Speed Champions",
        "enseigne": "JouéClub",
        "prix": 69.99,
        "devise": "EUR",
        "description": "Circuit électrique de course avec voitures miniatures et commandes manuelles."
    },
    {
        "id": "CAD-536",
        "categorie": "Enfants & Ados",
        "titre": "Coffret scientifique Buki Microscope 30 expériences",
        "enseigne": "Oxybul",
        "prix": 49.99,
        "devise": "EUR",
        "description": "Kit d'observation pour découvrir le monde microscopique avec accessoires et activités guidées."
    },
        {
        "id": "CAD-537",
        "categorie": "Cinéma & Séries",
        "titre": "Blu-ray 4K Ultra HD Interstellar – Édition collector",
        "enseigne": "Fnac",
        "prix": 29.99,
        "devise": "EUR",
        "description": "Le film de Christopher Nolan dans une édition en ultra haute définition."
    },
    {
        "id": "CAD-538",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray Six Feet Under – Intégrale de la série",
        "enseigne": "Amazon",
        "prix": 54.99,
        "devise": "EUR",
        "description": "Les cinq saisons de la série dramatique réunies dans un coffret."
    },
    {
        "id": "CAD-539",
        "categorie": "Cinéma & Séries",
        "titre": "Blu-ray 4K Ultra HD E.T. l'extra-terrestre – Édition spéciale",
        "enseigne": "Cultura",
        "prix": 24.99,
        "devise": "EUR",
        "description": "Le classique de Steven Spielberg dans une édition restaurée en 4K."
    },
    {
        "id": "CAD-540",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray Downton Abbey – Le film et sa suite",
        "enseigne": "Fnac",
        "prix": 34.99,
        "devise": "EUR",
        "description": "Deux longs métrages prolongeant l'histoire de la famille Crawley."
    },
    {
        "id": "CAD-541",
        "categorie": "Cinéma & Séries",
        "titre": "Blu-ray 4K Ultra HD Les Affranchis – Édition collector",
        "enseigne": "Cultura",
        "prix": 27.99,
        "devise": "EUR",
        "description": "Le film de Martin Scorsese proposé en ultra haute définition."
    },
    {
        "id": "CAD-542",
        "categorie": "High-Tech & Audio",
        "titre": "Enceinte connectée Wi-Fi Audio Pro C10 MKII",
        "enseigne": "Son-Vidéo",
        "prix": 399.00,
        "devise": "EUR",
        "description": "Enceinte multiroom compacte avec diffusion sans fil et entrée auxiliaire."
    },
    {
        "id": "CAD-543",
        "categorie": "High-Tech & Audio",
        "titre": "Tablette graphique Wacom Intuos Pro Medium",
        "enseigne": "LDLC",
        "prix": 349.99,
        "devise": "EUR",
        "description": "Tablette de création numérique avec stylet sensible à la pression."
    },
    {
        "id": "CAD-544",
        "categorie": "High-Tech & Audio",
        "titre": "Casque de réalité virtuelle Meta Quest 3 512 Go",
        "enseigne": "Boulanger",
        "prix": 549.99,
        "devise": "EUR",
        "description": "Casque autonome de réalité mixte pour jeux, applications et expériences immersives."
    },
    {
        "id": "CAD-545",
        "categorie": "High-Tech & Audio",
        "titre": "Objectif photo Sigma 18-50 mm f/2.8 DC DN Contemporary Sony E",
        "enseigne": "Miss Numérique",
        "prix": 549.00,
        "devise": "EUR",
        "description": "Zoom standard lumineux et compact conçu pour les appareils hybrides Sony à monture E."
    },
    {
        "id": "CAD-546",
        "categorie": "High-Tech & Audio",
        "titre": "Enregistreur audio portable Zoom H6essential",
        "enseigne": "Thomann",
        "prix": 369.00,
        "devise": "EUR",
        "description": "Enregistreur multipiste 32 bits à virgule flottante destiné aux prises de son mobiles."
    },
    {
        "id": "CAD-547",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Tzolk'in – Le Calendrier Maya",
        "enseigne": "Philibert",
        "prix": 44.90,
        "devise": "EUR",
        "description": "Jeu de stratégie avec roues dentées pour planifier les actions d'une civilisation maya."
    },
    {
        "id": "CAD-548",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Jaipur – Nouvelle édition",
        "enseigne": "Cultura",
        "prix": 19.90,
        "devise": "EUR",
        "description": "Jeu de cartes tactique pour deux joueurs autour du commerce et des marchandises."
    },
    {
        "id": "CAD-549",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Iki – Édition française",
        "enseigne": "Philibert",
        "prix": 49.90,
        "devise": "EUR",
        "description": "Jeu de gestion et de stratégie situé dans le quartier commerçant d'Edo."
    },
    {
        "id": "CAD-550",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société The Crew – Mission sous-marine",
        "enseigne": "Fnac",
        "prix": 15.90,
        "devise": "EUR",
        "description": "Jeu de plis coopératif proposant une campagne de missions à accomplir en équipe."
    },
    {
        "id": "CAD-551",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Agricola – Édition révisée",
        "enseigne": "Philibert",
        "prix": 54.90,
        "devise": "EUR",
        "description": "Jeu de placement d'ouvriers consacré au développement d'une ferme familiale."
    },
    {
        "id": "CAD-552",
        "categorie": "Livres & BD",
        "titre": "Roman La Maison des feuilles – Mark Z. Danielewski",
        "enseigne": "Fnac",
        "prix": 29.00,
        "devise": "EUR",
        "description": "Roman expérimental mêlant récit fantastique, notes et mise en page atypique."
    },
    {
        "id": "CAD-553",
        "categorie": "Livres & BD",
        "titre": "BD L'Arabe du futur – Tome 1, Riad Sattouf",
        "enseigne": "Cultura",
        "prix": 20.00,
        "devise": "EUR",
        "description": "Premier volume du récit autobiographique de Riad Sattouf en bande dessinée."
    },
    {
        "id": "CAD-554",
        "categorie": "Livres & BD",
        "titre": "Manga Blue Period – Tome 1, Tsubasa Yamaguchi",
        "enseigne": "Fnac",
        "prix": 7.95,
        "devise": "EUR",
        "description": "Un lycéen découvre sa passion pour la peinture et prépare le concours des beaux-arts."
    },
    {
        "id": "CAD-555",
        "categorie": "Livres & BD",
        "titre": "Roman Le Maître et Marguerite – Mikhaïl Boulgakov, Folio",
        "enseigne": "Decitre",
        "prix": 11.50,
        "devise": "EUR",
        "description": "Classique de la littérature russe mêlant satire, fantastique et réflexion philosophique."
    },
    {
        "id": "CAD-556",
        "categorie": "Livres & BD",
        "titre": "Beau livre Le Design du XXe siècle – Éditions Taschen",
        "enseigne": "Fnac",
        "prix": 25.00,
        "devise": "EUR",
        "description": "Panorama illustré des objets, meubles et mouvements majeurs du design moderne."
    },
    {
        "id": "CAD-557",
        "categorie": "Gastronomie",
        "titre": "Four à pizza extérieur Ooni Koda 16",
        "enseigne": "Ooni",
        "prix": 599.00,
        "devise": "EUR",
        "description": "Four à gaz d'extérieur conçu pour cuire des pizzas à haute température."
    },
    {
        "id": "CAD-558",
        "categorie": "Gastronomie",
        "titre": "Moulin à café Baratza Encore ESP Noir",
        "enseigne": "MaxiCoffee",
        "prix": 179.90,
        "devise": "EUR",
        "description": "Moulin électrique à réglages précis pour espresso et méthodes douces."
    },
    {
        "id": "CAD-559",
        "categorie": "Gastronomie",
        "titre": "Couteau de chef japonais Kai Shun Classic 20 cm",
        "enseigne": "Couteauxduchef",
        "prix": 199.00,
        "devise": "EUR",
        "description": "Couteau de cuisine à lame damassée pour émincer et découper avec précision."
    },
    {
        "id": "CAD-560",
        "categorie": "Gastronomie",
        "titre": "Robot multifonction Magimix CS 5200 XL Premium",
        "enseigne": "Darty",
        "prix": 499.00,
        "devise": "EUR",
        "description": "Robot de cuisine polyvalent pour hacher, râper, émincer et préparer des pâtes."
    },
    {
        "id": "CAD-561",
        "categorie": "Gastronomie",
        "titre": "Coffret dégustation huiles d'olive Château d'Estoublon",
        "enseigne": "Château d'Estoublon",
        "prix": 59.00,
        "devise": "EUR",
        "description": "Sélection d'huiles d'olive de Provence pour découvrir différentes expressions aromatiques."
    },
    {
        "id": "CAD-562",
        "categorie": "Maison & Déco",
        "titre": "Lampe portable rechargeable Louis Poulsen Panthella 160",
        "enseigne": "Made In Design",
        "prix": 230.00,
        "devise": "EUR",
        "description": "Lampe nomade à lumière douce inspirée du modèle iconique de Verner Panton."
    },
    {
        "id": "CAD-563",
        "categorie": "Maison & Déco",
        "titre": "Fauteuil lounge Vitra Eames Plastic Armchair RAR",
        "enseigne": "Silvera",
        "prix": 695.00,
        "devise": "EUR",
        "description": "Fauteuil à bascule associant une coque moulée et un piètement métallique."
    },
    {
        "id": "CAD-564",
        "categorie": "Maison & Déco",
        "titre": "Miroir mural Umbra Hubba Arched 86 x 137 cm",
        "enseigne": "La Redoute",
        "prix": 249.00,
        "devise": "EUR",
        "description": "Grand miroir cintré avec cadre fin pour agrandir visuellement une pièce."
    },
    {
        "id": "CAD-565",
        "categorie": "Maison & Déco",
        "titre": "Enceinte purificatrice Dyson Purifier Humidify+Cool Formaldehyde PH04",
        "enseigne": "Dyson",
        "prix": 799.00,
        "devise": "EUR",
        "description": "Appareil combinant purification de l'air, humidification et ventilation."
    },
    {
        "id": "CAD-566",
        "categorie": "Maison & Déco",
        "titre": "Étagère murale String Pocket Chêne et blanc",
        "enseigne": "Made In Design",
        "prix": 165.00,
        "devise": "EUR",
        "description": "Étagère modulable scandinave avec deux montants et trois tablettes."
    },
    {
        "id": "CAD-567",
        "categorie": "Beauté & Parfums",
        "titre": "Eau de Parfum Maison Francis Kurkdjian Gentle Fluidity Gold 70 ml",
        "enseigne": "Printemps",
        "prix": 215.00,
        "devise": "EUR",
        "description": "Parfum ambré et musqué aux notes de vanille, de coriandre et de muscade."
    },
    {
        "id": "CAD-568",
        "categorie": "Beauté & Parfums",
        "titre": "Sèche-cheveux Dyson Supersonic Nural",
        "enseigne": "Dyson",
        "prix": 499.00,
        "devise": "EUR",
        "description": "Sèche-cheveux avec capteurs intelligents et accessoires de coiffage interchangeables."
    },
    {
        "id": "CAD-569",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret soin visage Augustinus Bader The Rich Cream",
        "enseigne": "Oh My Cream",
        "prix": 175.00,
        "devise": "EUR",
        "description": "Coffret de soin hydratant autour de la crème riche emblématique de la marque."
    },
    {
        "id": "CAD-570",
        "categorie": "Beauté & Parfums",
        "titre": "Palette yeux Huda Beauty Rose Quartz",
        "enseigne": "Sephora",
        "prix": 69.00,
        "devise": "EUR",
        "description": "Palette de fards à paupières aux teintes rosées, neutres et lumineuses."
    },
    {
        "id": "CAD-571",
        "categorie": "Sport & Bien-être",
        "titre": "Montre GPS Suunto Race Titanium Charcoal",
        "enseigne": "i-Run",
        "prix": 449.00,
        "devise": "EUR",
        "description": "Montre multisport avec GPS, cartographie et écran AMOLED."
    },
    {
        "id": "CAD-572",
        "categorie": "Sport & Bien-être",
        "titre": "Tapis de course NordicTrack Commercial 1750",
        "enseigne": "FitnessBoutique",
        "prix": 2499.00,
        "devise": "EUR",
        "description": "Tapis motorisé avec inclinaison et déclivité réglables pour l'entraînement à domicile."
    },
    {
        "id": "CAD-573",
        "categorie": "Sport & Bien-être",
        "titre": "Chaussures de trail Hoka Speedgoat 6 Homme",
        "enseigne": "i-Run",
        "prix": 160.00,
        "devise": "EUR",
        "description": "Chaussures de trail amortissantes avec semelle adhérente pour terrains variés."
    },
    {
        "id": "CAD-574",
        "categorie": "Sport & Bien-être",
        "titre": "Tente de randonnée MSR Elixir 3",
        "enseigne": "Au Vieux Campeur",
        "prix": 449.00,
        "devise": "EUR",
        "description": "Tente autoportante trois places conçue pour le trekking et le camping."
    },
    {
        "id": "CAD-575",
        "categorie": "Mode & Accessoires",
        "titre": "Sac à main Polène Numéro Neuf Mini Craie",
        "enseigne": "Polène",
        "prix": 390.00,
        "devise": "EUR",
        "description": "Sac compact en cuir au design sculptural et aux lignes arrondies."
    },
    {
        "id": "CAD-576",
        "categorie": "Mode & Accessoires",
        "titre": "Lunettes de soleil Persol PO0649 Steve McQueen",
        "enseigne": "Optical Center",
        "prix": 230.00,
        "devise": "EUR",
        "description": "Monture iconique en acétate avec verres solaires et pont caractéristique."
    },
    {
        "id": "CAD-577",
        "categorie": "Mode & Accessoires",
        "titre": "Bottines Chelsea Clarks Originals Desert London Cuir",
        "enseigne": "Clarks",
        "prix": 140.00,
        "devise": "EUR",
        "description": "Chaussures en cuir au style décontracté avec semelle confortable."
    },
    {
        "id": "CAD-578",
        "categorie": "Mode & Accessoires",
        "titre": "Portefeuille compagnon Sézane Victor Cuir Noir",
        "enseigne": "Sézane",
        "prix": 115.00,
        "devise": "EUR",
        "description": "Portefeuille en cuir avec compartiments pour cartes, monnaie et billets."
    },
    {
        "id": "CAD-579",
        "categorie": "Loisirs & Créatifs",
        "titre": "Appareil photo instantané Lomography Lomo'Instant Automat Glass",
        "enseigne": "Digit-Photo",
        "prix": 169.00,
        "devise": "EUR",
        "description": "Appareil instantané avec objectif en verre et réglages créatifs pour portraits."
    },
    {
        "id": "CAD-580",
        "categorie": "Loisirs & Créatifs",
        "titre": "Coffret calligraphie Manuscript Deluxe Calligraphy Set",
        "enseigne": "Rougier & Plé",
        "prix": 39.90,
        "devise": "EUR",
        "description": "Ensemble de plumes, porte-plume et encres pour découvrir différentes écritures calligraphiques."
    },
    {
        "id": "CAD-581",
        "categorie": "Loisirs & Créatifs",
        "titre": "Kit de linogravure Essdee Deluxe Printing Kit",
        "enseigne": "Boesner",
        "prix": 49.90,
        "devise": "EUR",
        "description": "Kit de gravure et d'impression comprenant outils, plaques et accessoires."
    },
    {
        "id": "CAD-582",
        "categorie": "Loisirs & Créatifs",
        "titre": "Métier à tisser circulaire Prym Maxi",
        "enseigne": "Cultura",
        "prix": 34.99,
        "devise": "EUR",
        "description": "Métier à tisser grand format pour réaliser bonnets, écharpes et accessoires en laine."
    },
    {
        "id": "CAD-583",
        "categorie": "Enfants & Ados",
        "titre": "LEGO Technic 42154 Ford GT 2022",
        "enseigne": "LEGO",
        "prix": 119.99,
        "devise": "EUR",
        "description": "Maquette détaillée à construire avec direction fonctionnelle et moteur V6 reproduit."
    },
    {
        "id": "CAD-584",
        "categorie": "Enfants & Ados",
        "titre": "Poupée Our Generation Deluxe Hally avec accessoires",
        "enseigne": "JouéClub",
        "prix": 79.99,
        "devise": "EUR",
        "description": "Poupée de 46 cm accompagnée d'accessoires pour inventer des histoires et des jeux de rôle."
    },
    {
        "id": "CAD-585",
        "categorie": "Enfants & Ados",
        "titre": "Globe interactif éducatif Oregon Scientific Smart Globe Explorer",
        "enseigne": "Nature & Découvertes",
        "prix": 89.95,
        "devise": "EUR",
        "description": "Globe éducatif proposant des informations géographiques et des activités de découverte."
    },
    {
        "id": "CAD-586",
        "categorie": "Enfants & Ados",
        "titre": "Jeu de construction Plus-Plus Learn to Build BIG 275 pièces",
        "enseigne": "Oxybul",
        "prix": 49.99,
        "devise": "EUR",
        "description": "Grandes pièces de construction colorées pour assembler des créations en deux ou trois dimensions."
    },
        {
        "id": "CAD-587",
        "categorie": "Cinéma & Séries",
        "titre": "Blu-ray 4K Ultra HD Le Dernier Empereur – Édition restaurée",
        "enseigne": "Fnac",
        "prix": 29.99,
        "devise": "EUR",
        "description": "Le film de Bernardo Bertolucci dans une restauration en ultra haute définition."
    },
    {
        "id": "CAD-588",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray The Americans – Intégrale des six saisons",
        "enseigne": "Amazon",
        "prix": 64.99,
        "devise": "EUR",
        "description": "Les six saisons de la série d'espionnage réunies dans un coffret."
    },
    {
        "id": "CAD-589",
        "categorie": "Cinéma & Séries",
        "titre": "Blu-ray 4K Ultra HD Le Géant de fer – Édition collector",
        "enseigne": "Cultura",
        "prix": 27.99,
        "devise": "EUR",
        "description": "Le film d'animation de Brad Bird dans une édition haute définition."
    },
    {
        "id": "CAD-590",
        "categorie": "Cinéma & Séries",
        "titre": "Coffret Blu-ray Rome – Intégrale de la série HBO",
        "enseigne": "Fnac",
        "prix": 49.99,
        "devise": "EUR",
        "description": "Les deux saisons de la fresque historique consacrée à la Rome antique."
    },
    {
        "id": "CAD-591",
        "categorie": "Cinéma & Séries",
        "titre": "Blu-ray 4K Ultra HD Le Loup de Wall Street",
        "enseigne": "Cultura",
        "prix": 24.99,
        "devise": "EUR",
        "description": "La comédie dramatique de Martin Scorsese proposée en ultra haute définition."
    },
    {
        "id": "CAD-592",
        "categorie": "High-Tech & Audio",
        "titre": "Amplificateur hi-fi Marantz Stereo 70s Noir",
        "enseigne": "Son-Vidéo",
        "prix": 999.00,
        "devise": "EUR",
        "description": "Amplificateur stéréo connecté avec entrées HDMI et compatibilité multiroom."
    },
    {
        "id": "CAD-593",
        "categorie": "High-Tech & Audio",
        "titre": "Moniteur gaming ASUS ROG Swift OLED PG27AQDM",
        "enseigne": "LDLC",
        "prix": 799.99,
        "devise": "EUR",
        "description": "Écran OLED 27 pouces conçu pour le jeu avec fréquence de rafraîchissement élevée."
    },
    {
        "id": "CAD-594",
        "categorie": "High-Tech & Audio",
        "titre": "Scanner photo Epson Perfection V600 Photo",
        "enseigne": "Boulanger",
        "prix": 329.99,
        "devise": "EUR",
        "description": "Scanner à plat destiné à la numérisation de photos, diapositives et négatifs."
    },
    {
        "id": "CAD-595",
        "categorie": "High-Tech & Audio",
        "titre": "Paire de moniteurs de studio Yamaha HS5",
        "enseigne": "Woodbrass",
        "prix": 389.00,
        "devise": "EUR",
        "description": "Enceintes de monitoring actives pour la production musicale et le mixage."
    },
    {
        "id": "CAD-596",
        "categorie": "High-Tech & Audio",
        "titre": "Console portable ASUS ROG Ally Z1 Extreme",
        "enseigne": "Fnac",
        "prix": 699.99,
        "devise": "EUR",
        "description": "Console portable sous Windows pour jouer à des titres PC en mobilité."
    },
    {
        "id": "CAD-597",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Brass: Birmingham – Édition française",
        "enseigne": "Philibert",
        "prix": 69.90,
        "devise": "EUR",
        "description": "Jeu de stratégie économique autour du développement industriel de l'Angleterre."
    },
    {
        "id": "CAD-598",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Orléans – Édition française",
        "enseigne": "Cultura",
        "prix": 49.90,
        "devise": "EUR",
        "description": "Jeu de gestion utilisant la construction de sac pour développer une cité médiévale."
    },
    {
        "id": "CAD-599",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Merveilles du Monde – Édition française",
        "enseigne": "Philibert",
        "prix": 44.90,
        "devise": "EUR",
        "description": "Jeu de stratégie et de construction consacré aux grandes civilisations historiques."
    },
    {
        "id": "CAD-600",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société Forêt Mixte – Édition française",
        "enseigne": "Fnac",
        "prix": 29.90,
        "devise": "EUR",
        "description": "Jeu de cartes stratégique où les joueurs développent un écosystème forestier."
    },
    {
        "id": "CAD-601",
        "categorie": "Jeux & Société",
        "titre": "Jeu de société La Famiglia – La Grande Guerre de la Mafia",
        "enseigne": "Philibert",
        "prix": 59.90,
        "devise": "EUR",
        "description": "Jeu de confrontation stratégique pour deux équipes dans la Sicile des années 1980."
    },
    {
        "id": "CAD-602",
        "categorie": "Livres & BD",
        "titre": "Roman Gagner la guerre – Jean-Philippe Jaworski",
        "enseigne": "Les Moutons électriques",
        "prix": 28.00,
        "devise": "EUR",
        "description": "Roman de fantasy politique et d'aventure suivant les intrigues d'un mercenaire."
    },
    {
        "id": "CAD-603",
        "categorie": "Livres & BD",
        "titre": "BD Le Transperceneige – Intégrale, Lob et Rochette",
        "enseigne": "Fnac",
        "prix": 39.00,
        "devise": "EUR",
        "description": "L'intégrale de la bande dessinée de science-fiction située à bord d'un train perpétuel."
    },
    {
        "id": "CAD-604",
        "categorie": "Livres & BD",
        "titre": "Manga Nausicaä de la Vallée du Vent – Tome 1, Hayao Miyazaki",
        "enseigne": "Glénat",
        "prix": 10.95,
        "devise": "EUR",
        "description": "Premier volume du manga de fantasy écologique créé par Hayao Miyazaki."
    },
    {
        "id": "CAD-605",
        "categorie": "Livres & BD",
        "titre": "Roman La Vie mode d'emploi – Georges Perec",
        "enseigne": "Gallimard",
        "prix": 14.50,
        "devise": "EUR",
        "description": "Roman construit comme une exploration minutieuse des habitants d'un immeuble parisien."
    },
    {
        "id": "CAD-606",
        "categorie": "Livres & BD",
        "titre": "Beau livre Architecture : Formes, espaces et ordre – Francis D.K. Ching",
        "enseigne": "Dunod",
        "prix": 39.00,
        "devise": "EUR",
        "description": "Ouvrage illustré présentant les principes fondamentaux de la conception architecturale."
    },
    {
        "id": "CAD-607",
        "categorie": "Gastronomie",
        "titre": "Machine à espresso automatique De'Longhi Rivelia EXAM440.55",
        "enseigne": "Boulanger",
        "prix": 799.00,
        "devise": "EUR",
        "description": "Machine à café avec broyeur intégré et profils de boissons personnalisables."
    },
    {
        "id": "CAD-608",
        "categorie": "Gastronomie",
        "titre": "Plancha électrique Forge Adour Modern 60",
        "enseigne": "Darty",
        "prix": 499.00,
        "devise": "EUR",
        "description": "Plancha de cuisson extérieure avec plaque en fonte émaillée."
    },
    {
        "id": "CAD-609",
        "categorie": "Gastronomie",
        "titre": "Cave de maturation sous vide Zwilling Fresh & Save",
        "enseigne": "Zwilling",
        "prix": 99.95,
        "devise": "EUR",
        "description": "Système de conservation sous vide conçu pour prolonger la fraîcheur des aliments."
    },
    {
        "id": "CAD-610",
        "categorie": "Gastronomie",
        "titre": "Service à fondue bourguignonne Baumalu en cuivre",
        "enseigne": "Mathon",
        "prix": 89.90,
        "devise": "EUR",
        "description": "Service traditionnel avec caquelon en cuivre et accessoires pour les repas conviviaux."
    },
    {
        "id": "CAD-611",
        "categorie": "Gastronomie",
        "titre": "Coffret épices du monde Terre Exotique – Collection découverte",
        "enseigne": "Terre Exotique",
        "prix": 54.90,
        "devise": "EUR",
        "description": "Assortiment d'épices et de mélanges aromatiques pour varier les recettes."
    },
    {
        "id": "CAD-612",
        "categorie": "Maison & Déco",
        "titre": "Horloge murale Mondaine Classic 40 cm",
        "enseigne": "The Conran Shop",
        "prix": 249.00,
        "devise": "EUR",
        "description": "Horloge murale inspirée du design des célèbres horloges ferroviaires suisses."
    },
    {
        "id": "CAD-613",
        "categorie": "Maison & Déco",
        "titre": "Table basse Noguchi Coffee Table",
        "enseigne": "Vitra",
        "prix": 2490.00,
        "devise": "EUR",
        "description": "Table basse sculpturale associant un plateau en verre et un piètement en bois."
    },
    {
        "id": "CAD-614",
        "categorie": "Maison & Déco",
        "titre": "Robot aspirateur laveur Ecovacs Deebot X2 Omni",
        "enseigne": "Boulanger",
        "prix": 999.00,
        "devise": "EUR",
        "description": "Robot autonome avec station multifonction pour aspirer et laver les sols."
    },
    {
        "id": "CAD-615",
        "categorie": "Maison & Déco",
        "titre": "Parure de lit en lin lavé La Redoute Intérieurs 240 x 220 cm",
        "enseigne": "La Redoute",
        "prix": 149.99,
        "devise": "EUR",
        "description": "Housse de couette en lin lavé pour une literie souple et respirante."
    },
    {
        "id": "CAD-616",
        "categorie": "Maison & Déco",
        "titre": "Bibliothèque modulable Montana Mini 1001",
        "enseigne": "Silvera",
        "prix": 395.00,
        "devise": "EUR",
        "description": "Module de rangement compact et coloré pour livres et objets décoratifs."
    },
    {
        "id": "CAD-617",
        "categorie": "Beauté & Parfums",
        "titre": "Eau de Parfum Byredo Bal d'Afrique 50 ml",
        "enseigne": "Printemps",
        "prix": 165.00,
        "devise": "EUR",
        "description": "Parfum aux notes d'agrumes, de fleurs et de bois inspiré par l'Afrique."
    },
    {
        "id": "CAD-618",
        "categorie": "Beauté & Parfums",
        "titre": "Soin visage Sisley Sisleÿa L'Intégral Anti-Âge 50 ml",
        "enseigne": "Nocibé",
        "prix": 490.00,
        "devise": "EUR",
        "description": "Crème de soin anti-âge globale destinée à améliorer l'apparence de la peau."
    },
    {
        "id": "CAD-619",
        "categorie": "Beauté & Parfums",
        "titre": "Coffret maquillage Yves Saint Laurent Touche Éclat",
        "enseigne": "Sephora",
        "prix": 49.90,
        "devise": "EUR",
        "description": "Coffret réunissant des essentiels de maquillage autour de l'enlumineur Touche Éclat."
    },
    {
        "id": "CAD-620",
        "categorie": "Beauté & Parfums",
        "titre": "Appareil de soin visage Foreo Luna 4 Plus",
        "enseigne": "Sephora",
        "prix": 299.00,
        "devise": "EUR",
        "description": "Appareil connecté de nettoyage facial avec massage et fonctions de soin."
    },
    {
        "id": "CAD-621",
        "categorie": "Sport & Bien-être",
        "titre": "Vélo de route Canyon Endurace CF 7",
        "enseigne": "Canyon",
        "prix": 2499.00,
        "devise": "EUR",
        "description": "Vélo de route en carbone conçu pour l'endurance et les longues sorties."
    },
    {
        "id": "CAD-622",
        "categorie": "Sport & Bien-être",
        "titre": "Montre cardio GPS Coros Apex 2 Pro",
        "enseigne": "i-Run",
        "prix": 449.00,
        "devise": "EUR",
        "description": "Montre multisport avec cartographie, GPS double fréquence et suivi d'entraînement."
    },
    {
        "id": "CAD-623",
        "categorie": "Sport & Bien-être",
        "titre": "Paddle gonflable Itiwit X100 10 pieds",
        "enseigne": "Decathlon",
        "prix": 299.99,
        "devise": "EUR",
        "description": "Stand up paddle gonflable polyvalent destiné aux sorties en eau calme."
    },
    {
        "id": "CAD-624",
        "categorie": "Sport & Bien-être",
        "titre": "Haltères réglables Bowflex SelectTech 552",
        "enseigne": "FitnessBoutique",
        "prix": 499.00,
        "devise": "EUR",
        "description": "Paire d'haltères à charge ajustable pour varier les exercices de musculation."
    },
    {
        "id": "CAD-625",
        "categorie": "Mode & Accessoires",
        "titre": "Sac de voyage Filson Rugged Twill Duffle Medium",
        "enseigne": "Filson",
        "prix": 595.00,
        "devise": "EUR",
        "description": "Sac de voyage robuste en toile épaisse avec finitions en cuir."
    },
    {
        "id": "CAD-626",
        "categorie": "Mode & Accessoires",
        "titre": "Montre automatique Hamilton Khaki Field Mechanical 38 mm",
        "enseigne": "Louis Pion",
        "prix": 595.00,
        "devise": "EUR",
        "description": "Montre mécanique au style militaire avec cadran lisible et boîtier en acier."
    },
    {
        "id": "CAD-627",
        "categorie": "Mode & Accessoires",
        "titre": "Baskets Autry Medalist Low Leather White",
        "enseigne": "Printemps",
        "prix": 175.00,
        "devise": "EUR",
        "description": "Sneakers en cuir au style rétro avec semelle légèrement patinée."
    },
    {
        "id": "CAD-628",
        "categorie": "Mode & Accessoires",
        "titre": "Écharpe Acne Studios Canada New Laine Vierge",
        "enseigne": "Acne Studios",
        "prix": 250.00,
        "devise": "EUR",
        "description": "Grande écharpe en laine douce avec étiquette logo et finitions frangées."
    },
    {
        "id": "CAD-629",
        "categorie": "Loisirs & Créatifs",
        "titre": "Appareil photo argentique Pentax 17",
        "enseigne": "Digit-Photo",
        "prix": 549.00,
        "devise": "EUR",
        "description": "Appareil argentique demi-format permettant de réaliser deux images sur une vue classique."
    },
    {
        "id": "CAD-630",
        "categorie": "Loisirs & Créatifs",
        "titre": "Set de gravure sur bois Pfeil outils de sculpture",
        "enseigne": "Boesner",
        "prix": 119.00,
        "devise": "EUR",
        "description": "Ensemble de gouges de précision pour la sculpture et la gravure sur bois."
    },
    {
        "id": "CAD-631",
        "categorie": "Loisirs & Créatifs",
        "titre": "Kit de reliure créative Rössler Papier",
        "enseigne": "Rougier & Plé",
        "prix": 39.90,
        "devise": "EUR",
        "description": "Matériel et fournitures pour fabriquer carnets, albums et petits livres reliés."
    },
    {
        "id": "CAD-632",
        "categorie": "Loisirs & Créatifs",
        "titre": "Coffret de crayons de couleur Caran d'Ache Luminance 40 couleurs",
        "enseigne": "Cultura",
        "prix": 149.00,
        "devise": "EUR",
        "description": "Crayons de couleur professionnels à forte concentration pigmentaire et excellente tenue à la lumière."
    },
    {
        "id": "CAD-633",
        "categorie": "Enfants & Ados",
        "titre": "LEGO Architecture 21061 Notre-Dame de Paris",
        "enseigne": "LEGO",
        "prix": 229.99,
        "devise": "EUR",
        "description": "Maquette architecturale détaillée de la cathédrale parisienne à construire en briques."
    },
    {
        "id": "CAD-634",
        "categorie": "Enfants & Ados",
        "titre": "Circuit de train en bois Brio World Grande gare centrale",
        "enseigne": "JouéClub",
        "prix": 119.99,
        "devise": "EUR",
        "description": "Ensemble ferroviaire en bois avec gare et accessoires pour imaginer des voyages."
    },
    {
        "id": "CAD-635",
        "categorie": "Enfants & Ados",
        "titre": "Kit robot programmable Makeblock mBot2",
        "enseigne": "Nature & Découvertes",
        "prix": 169.00,
        "devise": "EUR",
        "description": "Robot éducatif programmable pour découvrir la robotique et les bases du codage."
    },
    {
        "id": "CAD-636",
        "categorie": "Enfants & Ados",
        "titre": "Jeu de construction magnétique Connetix Pastel Creative Pack 120 pièces",
        "enseigne": "Oxybul",
        "prix": 119.95,
        "devise": "EUR",
        "description": "Grand assortiment de pièces magnétiques pastel pour réaliser des constructions en 3D."
    }
]


def _est_url_http_valide(url: str) -> bool:
    return isinstance(url, str) and url.strip().startswith(("https://", "http://"))


def _chercher_image_serper(requete: str, api_key: str) -> str:
    if not requete or not api_key:
        return ""
    try:
        corps = json.dumps({"q": requete, "gl": "fr", "hl": "fr", "num": 5}).encode("utf-8")
        req = Request(
            SERPER_IMAGES_URL,
            data=corps,
            headers={
                "X-API-KEY": api_key,
                "Content-Type": "application/json",
                "User-Agent": USER_AGENT,
            },
            method="POST",
        )
        with urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            if resp.status != 200:
                return ""
            donnees = json.loads(resp.read().decode("utf-8", errors="replace"))
    except Exception:
        return ""

    resultats = donnees.get("images") if isinstance(donnees, dict) else None
    if not isinstance(resultats, list):
        return ""

    for item in resultats:
        if not isinstance(item, dict):
            continue
        url = (item.get("imageUrl") or "").strip()
        if _est_url_http_valide(url):
            return url
    return ""


def trouver_image_article(article: dict, cache: dict, api_key: Optional[str] = None) -> str:
    cle_api = api_key if api_key is not None else os.environ.get("SERPER_API_KEY", "").strip()
    titre = article["titre"]
    categorie = article["categorie"]
    cle_cache = f"serper::{categorie}::{titre}"

    if cle_cache in cache:
        cached = cache[cle_cache]
        return cached if _est_url_http_valide(cached) else ""

    if not cle_api:
        return ""

    image_url = _chercher_image_serper(titre, cle_api)
    cache[cle_cache] = image_url
    time.sleep(REQUEST_PAUSE)
    return image_url


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


def generer_catalogue(chemin_sortie: Path, chemin_cache: Path) -> dict:
    cache: dict = {}
    if chemin_cache.exists():
        try:
            loaded = json.loads(chemin_cache.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                cache = loaded
        except Exception:
            cache = {}

    api_key = os.environ.get("SERPER_API_KEY", "").strip()
    if not api_key:
        print("Attention : SERPER_API_KEY non définie, aucune nouvelle image ne sera recherchée.")

    articles_enrichis = []
    images_trouvees = 0

    for article in CATALOGUE_ARTICLES:
        valider_article(article)
        copie = dict(article)
        img = trouver_image_article(copie, cache, api_key)
        copie["image"] = img
        if img:
            images_trouvees += 1
        articles_enrichis.append(copie)

    chemin_cache.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    payload = {
        "meta": {
            "projet": "Mon Noël organisé",
            "date_mise_a_jour": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "nombre_articles": len(articles_enrichis),
            "images_trouvees": images_trouvees,
            "devise": "EUR"
        },
        "articles": articles_enrichis
    }

    chemin_sortie.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )
    return payload


if __name__ == "__main__":
    racine = Path(__file__).resolve().parent.parent
    fichier_json = racine / "catalogue.json"
    fichier_cache = racine / "scripts" / "images_cache.json"
    resultat = generer_catalogue(fichier_json, fichier_cache)
    print(
        f"Catalogue généré : {resultat['meta']['nombre_articles']} articles "
        f"({resultat['meta']['images_trouvees']} avec image) dans {fichier_json}"
    )
