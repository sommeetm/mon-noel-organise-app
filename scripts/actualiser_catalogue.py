#!/usr/bin/env python3
"""
Actualise catalogue.json avec des références précises par enseigne et prix
pour l'application « Mon Noël organisé ».
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

SPECIFIC_GIFTS = [
    ("DVD, Blu-ray et musique", "Coffret Blu-ray Intégrale Batman (The Dark Knight Trilogy)", "Warner Bros.", "Amazon", "Coffret Blu-ray réunissant Batman Begins, The Dark Knight et The Dark Knight Rises.", 24.99),
    ("DVD, Blu-ray et musique", "Coffret Blu-ray 4K Ultra HD Le Seigneur des Anneaux (Version Longue)", "Warner Bros.", "Fnac", "Édition Blu-ray 4K de la trilogie en version longue pour soirées cinéma à la maison.", 59.99),
    ("DVD, Blu-ray et musique", "Coffret DVD Intégrale Kaamelott (Livres I à VI)", "M6 Vidéo", "Cultura", "L'intégrale des six livres de la série culte d'Alexandre Astier en coffret DVD.", 39.99),
    ("DVD, Blu-ray et musique", "Blu-ray Dune : Deuxième Partie", "Warner Bros.", "Boulanger", "Édition Blu-ray du film de science-fiction réalisé par Denis Villeneuve.", 19.99),
    ("DVD, Blu-ray et musique", "Vinyle 33 tours Pink Floyd — The Dark Side of the Moon", "EMI / Parlophone", "Fnac", "Édition vinyle 33 tours de l'album emblématique à offrir aux amateurs de musique.", 29.99),
    ("DVD, Blu-ray et musique", "Vinyle 33 tours Daft Punk — Random Access Memories", "Columbia", "Cultura", "Double vinyle 33 tours de l'album de Daft Punk.", 34.99),
    ("DVD, Blu-ray et musique", "Coffret CD Intégrale Brassens — 18 albums", "Universal Music", "Amazon", "Coffret CD réunissant les enregistrements studio de Georges Brassens.", 44.90),

    ("Livres", "Le Comte de Monte-Cristo — Édition illustrée reliée", "Gallimard / Folio", "Fnac", "Le grand classique d'Alexandre Dumas dans une belle édition à offrir.", 18.50),
    ("Livres", "Astérix en Lusitanie — Album Bande Dessinée", "Albert René", "Cultura", "Album de bande dessinée Astérix à glisser sous le sapin.", 10.95),
    ("Livres", "One Piece — Coffret découverte Tomes 1 à 12", "Glénat", "Amazon", "Coffret manga pour débuter ou compléter une collection.", 79.90),
    ("Livres", "Simplissime — Le livre de cuisine le plus facile du monde", "Hachette Pratique", "Cultura", "Recettes rapides et accessibles illustrées pour cuisiner au quotidien.", 19.95),
    ("Livres", "Pâtisserie — L'encyclopédie du savoir-faire", "Flammarion", "Fnac", "Ouvrage de référence sur les techniques et recettes de pâtisserie.", 45.00),
    ("Livres", "Les Chevaliers d'Émeraude — Coffret Intégrale Tome 1", "Michel Lafon", "Amazon", "Roman de fantasy jeunesse / adolescents.", 16.90),
    ("Livres", "Histoire de France racontée aux curieux", "Perrin", "Cultura", "Panorama illustré des grandes périodes de l'histoire de France.", 24.90),
    ("Livres", "La Femme de ménage — Thriller psychologique", "City Éditions", "Fnac", "Roman à suspense très populaire en lecture de fin d'année.", 8.90),

    ("Jouets et jeux pour enfants", "LEGO Icons — Le Bouquet de Roses (10328)", "LEGO", "Fnac", "Coffret de construction LEGO à assembler pour créer un bouquet décoratif.", 59.99),
    ("Jouets et jeux pour enfants", "LEGO Star Wars — Le Faucon Millenium (75257)", "LEGO", "Boulanger", "Vaisseau articulé et figurines LEGO Star Wars pour enfants et fans.", 169.99),
    ("Jouets et jeux pour enfants", "Playmobil — La Maison Familiale Moderne", "Playmobil", "Cultura", "Maison complète avec personnages et accessoires pour jeux d'imitation.", 64.99),
    ("Jouets et jeux pour enfants", "Peluche Stitch Disney — Format 35 cm", "Simba / Disney", "Amazon", "Peluche douce à l'effigie de Stitch pour les enfants.", 24.90),
    ("Jouets et jeux pour enfants", "Figurine Funko POP! Harry Potter avec Hedwige", "Funko", "Cultura", "Figurine de collection vinyle à exposer ou offrir aux fans.", 14.99),
    ("Jouets et jeux pour enfants", "Circuit voiture Carrera GO! Mario Kart", "Carrera", "Boulanger", "Circuit de course électrique avec voitures Mario Kart et manettes.", 54.99),

    ("Jeux de société", "Jeu de société Azul", "Plan B Games", "Cultura", "Jeu de plateau stratégique et coloré autour de la mosaïque d'azulejos.", 34.99),
    ("Jeux de société", "Jeu de société Blanc-Manger Coco", "Distributeur FR", "Fnac", "Jeu d'ambiance d'association d'idées pour soirées entre amis ou en famille.", 27.50),
    ("Jeux de société", "Jeu de cartes Skyjo", "Magilano", "Amazon", "Jeu de cartes familial convivial et rapide à prendre en main.", 14.99),
    ("Jeux de société", "Puzzle 1000 pièces — Tour Eiffel au coucher du soleil", "Ravensburger", "Cultura", "Puzzle de 1000 pièces avec technologie Softclick.", 16.99),
    ("Jeux de société", "Jeu d'enquête Unlock! — Mystère à la maison", "Space Cowboys", "Fnac", "Escape game coopératif de cartes avec application compagnon.", 13.50),

    ("High-tech et électronique", "Casque sans fil Sony WH-1000XM5", "Sony", "Boulanger", "Casque arceau Bluetooth à réduction de bruit active.", 329.00),
    ("High-tech et électronique", "Enceinte Bluetooth portable JBL Flip 6", "JBL", "Darty", "Enceinte sans fil compacte et résistante à l'eau et à la poussière.", 119.99),
    ("High-tech et électronique", "Écouteurs sans fil Apple AirPods 4", "Apple", "Fnac", "Écouteurs Bluetooth intra/semi-ouverts pour musique et appels.", 149.00),
    ("High-tech et électronique", "Appareil photo instantané Fujifilm Instax Mini 12", "Fujifilm", "Fnac", "Appareil photo instantané compact imprimant des photos format carte de visite.", 79.99),
    ("High-tech et électronique", "Montre connectée Garmin Forerunner 165", "Garmin", "Boulanger", "Montre GPS connectée orientée course à pied et suivi quotidien.", 249.00),
    ("High-tech et électronique", "Liseuse numérique Kobo Clara BW", "Kobo", "Fnac", "Liseuse avec écran antireflet et réglage de la lumière chaude.", 139.99),

    ("Maison et décoration", "Machine expresso Nespresso Vertuo Pop", "Nespresso", "Darty", "Machine à café expresso et grandes tasses à capsules.", 99.99),
    ("Maison et décoration", "Cafetière filtre programmable Philips Daily Collection", "Philips", "Boulanger", "Cafetière filtre avec verseuse en verre et départ différé.", 49.99),
    ("Maison et décoration", "Bouilloire électrique KitchenAid 1,5 L", "KitchenAid", "Darty", "Bouilloire en acier inoxydable avec réglage de température.", 129.00),
    ("Maison et décoration", "Théière en fonte japonaise 0,8 L", "Arts du Thé", "Nature & Découvertes", "Théière en fonte avec filtre inox pour préparer le thé en feuilles.", 39.90),
    ("Maison et décoration", "Bougie parfumée Yankee Candle — Sapin & Cèdre", "Yankee Candle", "Cultura", "Grande jarre parfumée aux notes boisées et hivernales.", 29.99),
    ("Maison et décoration", "Mug isotherme Stanley Quencher 0,88 L", "Stanley", "Amazon", "Gobelet / mug isotherme avec poignée et paille.", 45.00),
    ("Maison et décoration", "Plaid en fausse fourrure 150 x 200 cm", "Maison & Confort", "Boulanger", "Plaid chaud et doux pour le canapé en hiver.", 29.99),
    ("Maison et décoration", "Lampe de chevet tactile LED bois et verre", "Luminaire FR", "Darty", "Lampe d'appoint à intensité variable pour chambre ou salon.", 34.99),

    ("Beauté et soins", "Coffret Eau de Parfum Chloé Signature 50 ml + lait corps", "Chloé", "Sephora", "Coffret parfum floral poudré accompagné de son lait parfumé pour le corps.", 98.00),
    ("Beauté et soins", "Eau de Toilette Terre d'Hermès 50 ml", "Hermès", "Sephora", "Eau de toilette boisée et minérale.", 89.00),
    ("Beauté et soins", "Coffret savons parfumés de Marseille (4 x 100 g)", "Savonnerie FR", "Nature & Découvertes", "Assortiment de savons parfumés présentés dans un coffret cadeau.", 19.90),
    ("Beauté et soins", "Coffret crèmes mains douceur d'hiver", "Soins & Botanique", "Cultura", "Duo ou trio de crèmes mains pour protéger la peau du froid.", 16.50),

    ("Gastronomie et gourmandises", "Coffret de chocolats pralinés Léonidas (500 g)", "Leonidas", "Cultura", "Assortiment de chocolats belges pralinés, ganaches et giandujas.", 26.90),
    ("Gastronomie et gourmandises", "Ballotin de chocolats fins Valrhona — Coffret dégustation", "Valrhona", "Fnac", "Sélection de chocolats noirs et au lait de couverture.", 32.00),
    ("Gastronomie et gourmandises", "Boîte métallique de Calissons d'Aix (250 g)", "Confiserie d'Aix", "Amazon", "Spécialité provençale aux amandes, melon confit et glaçage royal.", 18.50),
    ("Gastronomie et gourmandises", "Coffret Nougat de Montélimar assortiment (300 g)", "Nougaterie FR", "Cultura", "Nougats tendres aux amandes et pistaches dans un coffret cadeau.", 15.90),
    ("Gastronomie et gourmandises", "Coffret découverte grands thés de Noël (24 sachets / boîtes)", "Maison de Thé", "Nature & Découvertes", "Assortiment de thés noirs, verts et infusions épicées pour les fêtes.", 24.90),
]


def build_catalogue() -> dict:
    products = []
    for cat, name, brand, merchant, desc, price in SPECIFIC_GIFTS:
        uid = hashlib.sha1(f"{cat}|{name}|{merchant}".encode("utf-8")).hexdigest()[:12]
        products.append({
            "id": f"gift-{uid}",
            "name": name,
            "category": cat,
            "brand": brand,
            "merchant": merchant,
            "merchant_type": "Enseigne FR",
            "description": desc,
            "price": price,
            "image": "",
            "image_license": "",
            "url": "",
            "source": "Catalogue cadeaux Noël (FR)",
        })

    return {
        "project": "Mon Noël organisé",
        "market": "FR",
        "language": "fr",
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "total_products": len(products),
        "products_with_images": sum(1 for p in products if p.get("image")),
        "products": products,
    }


def main() -> None:
    out_path = Path("catalogue.json")
    catalogue = build_catalogue()
    out_path.write_text(
        json.dumps(catalogue, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"catalogue.json généré avec {catalogue['total_products']} références.")


if __name__ == "__main__":
    main()
