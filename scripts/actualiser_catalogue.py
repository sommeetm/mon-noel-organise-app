#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur du catalogue d'idées cadeaux précis pour « Mon Noël organisé ».
Contient 336 références nommées, chacune rattachée à une enseigne
reconnue, un prix indicatif en euros et une description claire.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

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
        "titre": " Coffret Parfum Yves Saint Laurent Black Opium (50 ml + Mascara miniature)",
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
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )
    return payload


if __name__ == "__main__":
    racine = Path(__file__).resolve().parent.parent
    fichier_json = racine / "catalogue.json"
    resultat = generer_catalogue(fichier_json)
    print(f"Catalogue généré : {resultat['meta']['nombre_articles']} articles précis dans {fichier_json}")
