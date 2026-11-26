#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'alimentation strictement orienté « Idées cadeaux de Noël » pour
« Mon Noël organisé ».
- Élimine tous les produits du quotidien non adaptés à un cadeau (entretien,
  lessive, javel, pharmacie, pansements, hygiène courante, puériculture
  jetable, alimentation de base).
- Ne conserve que des articles qui s'offrent réellement à Noël avec photo
  vérifiée (ODbL / CC-BY-SA / Open Library Covers), sans prix inventé ni lien
  marchand fabriqué.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import pathlib
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG_PATH = REPO_ROOT / "catalogue.json"
USER_AGENT = "MonNoelOrganise/2026 (+https://github.com/sommeetm/mon-noel-organise-app)"

ALLOWED_CATEGORIES = [
    "Livres",
    "DVD, Blu-ray et musique",
    "Jouets et jeux pour enfants",
    "Jeux de société",
    "High-tech et électronique",
    "Maison et décoration",
    "Beauté et soins",
    "Gastronomie et gourmandises",
    "Loisirs créatifs",
    "Mode et accessoires",
    "Bijoux",
    "Sport et bien-être",
    "Jardinage",
    "Produits artisanaux",
    "Cadeaux originaux et personnalisés",
]

# Liste noire stricte : exclut tout produit ménager, médical, hygiène de base ou épicerie courante
NON_GIFT_BLACKLIST = [
    "pansement", "sparadrap", "compresse", "bandage", "thermomètre", "thermometre",
    "médicament", "medicament", "paracétamol", "ibuprofène", "sirop toux", "spray nasal",
    "javel", "lessive", "adoucissant", "assouplissant", "liquide vaisselle", "tablette lave",
    "nettoyant", "détartrant", "detartrant", "désinfectant", "desinfectant", "déboucheur",
    "serpillière", "serpilliere", "éponge", "eponge", "balai", "sac poubelle", "insecticide",
    "papier toilette", "essuie-tout", "essuie tout", "mouchoir", "coton-tige", "coton tige",
    "serviette hygiénique", "tampon", "couche", "lingette", "dentifrice", "brosse à dents",
    "brosse a dents", "déodorant", "deodorant", "gel douche", "rasoir", "mousse à raser",
    "croquette", "litière", "litiere", "pâtée", "patee",
    "huile de tournesol", "huile d'olive", "vinaigre", "farine", "sucre en poudre", "sel fin",
    "pâtes", "pates", "riz basmati", "conserve", "haricots verts", "petits pois", "eau minérale",
    "eau gazeuse", "lait demi", "beurre doux", "fromage râpé", "jambon", "lardon",
]

# Mots-clés positifs obligatoires pour valider qu'un produit Open Products/Beauty/Food est bien un cadeau
POSITIVE_GIFT_KEYWORDS = [
    # Livres / Culture / Vidéo / Musique
    "livre", "roman", "bande dessinée", "bande dessinee", "bd", "manga", "atlas", "album",
    "dvd", "blu-ray", "bluray", "coffret film", "coffret série", "coffret serie", "vinyle", "cd audio",
    # Jeux & Jouets
    "jeu de société", "jeu de societe", "jeu de plateau", "jeu de cartes", "puzzle", "échecs", "echecs",
    "jouet", "lego", "playmobil", "peluche", "figurine", "poupée", "poupee", "circuit", "maquette",
    # High-Tech
    "casque", "enceinte", "bluetooth", "écouteurs", "ecouteurs", "appareil photo", "liseuse",
    "montre connectée", "montre connectee", "platine vinyle", "radio", "console", "manette",
    # Maison & Café / Thé
    "cafetière", "cafetiere", "expresso", "nespresso", "bouilloire", "théière", "theiere",
    "bougie parfumée", "bougie parfumee", "diffuseur", "mug", "tasse", "plaid", "lampe",
    "carafe", "verre à", "verre a", "coffret cuisine", "service à", "service a",
    # Beauté & Parfums
    "parfum", "eau de toilette", "eau de parfum", "coffret beauté", "coffret beaute",
    "coffret soin", "savon parfumé", "savon parfume", "savon artisanal", "crème mains", "creme mains",
    "huile sèche", "huile seche", "baume",
    # Gastronomie cadeau
    "coffret chocolat", "ballotin", "pralin", "truffe", "chocolat fin", "assortiment chocolat",
    "coffret thé", "coffret the", "thé vert", "thé noir", "infusion", "café en grains",
    "café moulu", "miel", "confiture", "calisson", "nougat", "macaron", "pain d'épices", "pain d'epices",
    "foie gras", "terrine", "champagne", "coffret gourmand",
    # Loisirs, Mode, Bijoux, Sport, Jardinage
    "aquarelle", "peinture", "crayons de couleur", "carnet", "broderie", "tricot",
    "écharpe", "echarpe", "foulard", "sac", "portefeuille", "parapluie",
    "bijou", "collier", "bracelet", "bague", "montre",
    "gourde", "yoga", "massage", "graines", "sécateur", "secateur", "nichoir", "arrosoir",
]

# Requêtes ciblées Open Products Facts (France)
OPF_GIFT_QUERIES: list[tuple[str, str]] = [
    ("DVD, Blu-ray et musique", "dvd"),
    ("DVD, Blu-ray et musique", "blu-ray"),
    ("DVD, Blu-ray et musique", "vinyle"),
    ("Jouets et jeux pour enfants", "lego"),
    ("Jouets et jeux pour enfants", "playmobil"),
    ("Jouets et jeux pour enfants", "peluche"),
    ("Jouets et jeux pour enfants", "figurine"),
    ("Jouets et jeux pour enfants", "jouet"),
    ("Jeux de société", "jeu de société"),
    ("Jeux de société", "jeu de cartes"),
    ("Jeux de société", "puzzle"),
    ("High-tech et électronique", "casque audio"),
    ("High-tech et électronique", "enceinte bluetooth"),
    ("High-tech et électronique", "écouteurs"),
    ("High-tech et électronique", "appareil photo"),
    ("High-tech et électronique", "montre connectée"),
    ("Maison et décoration", "cafetière"),
    ("Maison et décoration", "expresso"),
    ("Maison et décoration", "bouilloire"),
    ("Maison et décoration", "théière"),
    ("Maison et décoration", "bougie parfumée"),
    ("Maison et décoration", "mug"),
    ("Maison et décoration", "plaid"),
    ("Maison et décoration", "lampe"),
    ("Loisirs créatifs", "crayons de couleur"),
    ("Loisirs créatifs", "peinture"),
    ("Loisirs créatifs", "carnet"),
    ("Sport et bien-être", "gourde"),
    ("Sport et bien-être", "yoga"),
    ("Jardinage", "graines"),
    ("Jardinage", "sécateur"),
    ("Mode et accessoires", "écharpe"),
    ("Mode et accessoires", "sac"),
    ("Bijoux", "bijou"),
]

# Requêtes Open Beauty Facts (France) -> Parfums & coffrets
OBF_GIFT_QUERIES: list[str] = [
    "coffret parfum",
    "eau de toilette",
    "eau de parfum",
    "coffret",
    "savon parfumé",
    "crème mains",
]

# Requêtes Open Food Facts France -> Coffrets gourmands & chocolats
OFF_GIFT_QUERIES: list[str] = [
    "coffret chocolat",
    "ballotin chocolat",
    "pralinés",
    "truffes chocolat",
    "calissons",
    "nougat",
    "coffret thé",
    "miel de france",
]

# Requêtes Open Library -> Livres français variés (romans, BD, jeunesse, cuisine, voyages)
OPENLIBRARY_GIFT_QUERIES: list[tuple[str, str]] = [
    ("Livres", "roman français prix"),
    ("Livres", "bande dessinée"),
    ("Livres", "manga français"),
    ("Livres", "cuisine française"),
    ("Livres", "pâtisserie française"),
    ("Livres", "album jeunesse"),
    ("Livres", "histoire de france"),
    ("Livres", "voyage france"),
    ("Livres", "polar français"),
    ("Livres", "science fiction français"),
]


def http_get_json(url: str, timeout: int = 20) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data if isinstance(data, dict) else {}
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
        print(f"[INFO] Requête ignorée ({url[:85]}...) : {exc}")
        return {}


def is_valid_http_url(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    cleaned = value.strip()
    if not cleaned:
        return ""
    parsed = urllib.parse.urlparse(cleaned)
    if parsed.scheme in ("http", "https") and parsed.netloc:
        return cleaned
    return ""


def clean_text(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return re.sub(r"\s+", " ", value).strip()


def is_giftable_item(name: str, categories: str = "", description: str = "") -> bool:
    blob = f"{name} {categories} {description}".lower()
    if any(bad in blob for bad in NON_GIFT_BLACKLIST):
        return False
    return any(good in blob for good in POSITIVE_GIFT_KEYWORDS)


def is_french_market(item: dict[str, Any]) -> bool:
    countries_tags = [str(c).lower() for c in (item.get("countries_tags") or [])]
    countries_str = str(item.get("countries") or "").lower()
    if not (any("france" in t for t in countries_tags) or ("france" in countries_str)):
        return False
    name_fr = clean_text(item.get("product_name_fr") or item.get("product_name"))
    return len(name_fr) >= 4


def infer_category(raw_categories: str, name_fr: str, fallback: str) -> str:
    text = f"{raw_categories} {name_fr}".lower()
    rules: list[tuple[str, list[str]]] = [
        ("DVD, Blu-ray et musique", ["dvd", "blu-ray", "bluray", "vinyle", "cd audio", "coffret film", "coffret série", "coffret serie"]),
        ("Livres", ["livre", "roman", "bande dessinée", "bande dessinee", "manga", "atlas", "album illustré"]),
        ("Jeux de société", ["jeu de société", "jeu de societe", "jeu de plateau", "jeu de cartes", "puzzle", "échecs", "echecs"]),
        ("Jouets et jeux pour enfants", ["jouet", "peluche", "lego", "playmobil", "figurine", "poupée", "poupee", "éveil", "eveil"]),
        ("Loisirs créatifs", ["peinture", "aquarelle", "crayon", "feutre", "broderie", "tricot", "dessin", "loisir créatif", "carnet"]),
        ("Sport et bien-être", ["sport", "yoga", "fitness", "gourde", "massage", "bien-être", "bien-etre"]),
        ("Jardinage", ["jardin", "graine", "plante", "sécateur", "secateur", "arrosoir", "nichoir"]),
        ("Gastronomie et gourmandises", ["chocolat", "ballotin", "pralin", "truffe", "thé", "the", "infusion", "café", "cafe", "miel", "confiture", "biscuit", "nougat", "calisson", "macaron", "foie gras"]),
        ("Bijoux", ["bijou", "collier", "bracelet", "bague", "boucle"]),
        ("Beauté et soins", ["parfum", "eau de toilette", "eau de parfum", "savon", "crème", "creme", "huile", "baume", "soin", "coffret beauté"]),
        ("Mode et accessoires", ["écharpe", "echarpe", "bonnet", "foulard", "sac", "portefeuille", "parapluie", "mode"]),
        ("Maison et décoration", ["cafetière", "cafetiere", "expresso", "nespresso", "bouilloire", "bougie", "lampe", "plaid", "mug", "tasse", "théière", "theiere", "carafe"]),
        ("High-tech et électronique", ["casque", "enceinte", "audio", "bluetooth", "appareil photo", "liseuse", "montre connectée", "écouteurs", "ecouteurs", "console"]),
    ]
    for cat, keywords in rules:
        if any(kw in text for kw in keywords):
            return cat
    return fallback if fallback in ALLOWED_CATEGORIES else "Cadeaux originaux et personnalisés"


def extract_best_image(item: dict[str, Any]) -> str:
    for key in ("image_front_url", "image_url", "image_front_small_url", "image_small_url"):
        candidate = is_valid_http_url(item.get(key))
        if candidate:
            return candidate

    selected = item.get("selected_images")
    if isinstance(selected, dict):
        front = selected.get("front")
        if isinstance(front, dict):
            display = front.get("display")
            if isinstance(display, dict):
                for lang_key in ("fr", "en"):
                    candidate = is_valid_http_url(display.get(lang_key))
                    if candidate:
                        return candidate
    return ""


def format_stores(item: dict[str, Any], default_merchant: str) -> tuple[str, str]:
    stores_raw = clean_text(item.get("stores"))
    if not stores_raw:
        return default_merchant, "Enseignes françaises"
    stores_list = [s.strip() for s in stores_raw.split(",") if s.strip()]
    unique_stores = list(dict.fromkeys(stores_list))[:3]
    merchant_label = " / ".join(unique_stores)
    big_retailers = {
        "carrefour", "leclerc", "auchan", "fnac", "cultura", "boulanger", "darty",
        "intermarché", "super u", "monoprix", "sephora", "marionnaud", "yves rocher",
        "nocibé", "nature & découvertes", "jouéclub", "king jouet", "la grande récré",
        "galeries lafayette", "la redoute"
    }
    is_big = any(any(br in s.lower() for br in big_retailers) for s in unique_stores)
    merchant_type = "Grande enseigne" if is_big else "Commerce spécialisé / Boutique"
    return merchant_label, merchant_type


def fetch_open_price_eur(barcode: str) -> float | None:
    if not barcode or not barcode.isdigit():
        return None
    url = (
        f"https://prices.openfoodfacts.org/api/v1/prices"
        f"?product_code={urllib.parse.quote(barcode)}&currency=EUR&size=5"
    )
    payload = http_get_json(url, timeout=10)
    items = payload.get("items")
    if not isinstance(items, list):
        return None
    for entry in items:
        if not isinstance(entry, dict):
            continue
        country = str(entry.get("location_osm_address_country") or "").lower()
        if country and "france" not in country:
            continue
        price = entry.get("price")
        if isinstance(price, (int, float)) and not isinstance(price, bool) and 2.0 <= float(price) <= 1500:
            return round(float(price), 2)
    return None


def collect_off_family(
    base_domain: str,
    source_label: str,
    default_merchant: str,
    query_terms: list[tuple[str, str]],
    page_size: int = 50,
    max_price_lookups: int = 30,
) -> list[dict[str, Any]]:
    collected: list[dict[str, Any]] = []
    price_lookups = 0
    fields = (
        "code,product_name,product_name_fr,generic_name,generic_name_fr,"
        "brands,categories,stores,countries,countries_tags,"
        "image_front_url,image_front_small_url,image_url,selected_images"
    )

    for default_category, term in query_terms:
        encoded = urllib.parse.quote(term)
        urls = [
            (
                f"https://{base_domain}/api/v2/search"
                f"?countries_tags_en=france&search_terms={encoded}&page_size={page_size}"
                f"&fields={fields}"
            ),
            (
                f"https://{base_domain}/cgi/search.pl"
                f"?search_terms={encoded}&search_simple=1&action=process&json=1&page_size={page_size}"
                f"&tagtype_0=countries&tag_contains_0=contains&tag_0=France"
                f"&fields={fields}"
            ),
        ]

        raw_products: list[Any] = []
        for url in urls:
            payload = http_get_json(url, timeout=20)
            cand = payload.get("products")
            if isinstance(cand, list) and cand:
                raw_products = cand
                break

        for raw in raw_products:
            if not isinstance(raw, dict) or not is_french_market(raw):
                continue

            name_fr = clean_text(raw.get("product_name_fr") or raw.get("product_name"))
            raw_cats = clean_text(raw.get("categories"))
            generic_fr = clean_text(raw.get("generic_name_fr") or raw.get("generic_name"))

            # Filtrage strict : uniquement de vrais cadeaux !
            if not is_giftable_item(name_fr, raw_cats, generic_fr):
                continue

            image_url = extract_best_image(raw)
            if not image_url:
                continue

            brands_raw = clean_text(raw.get("brands"))
            brand = brands_raw.split(",")[0].strip() if brands_raw else "Marque / Édition française"
            category = infer_category(raw_cats, name_fr, default_category)
            merchant, merchant_type = format_stores(raw, default_merchant)
            description = generic_fr if len(generic_fr) >= 8 else f"{name_fr} — idée cadeau ({category.lower()})."

            code = clean_text(raw.get("code"))
            verified_price: float | None = None
            if code and price_lookups < max_price_lookups:
                verified_price = fetch_open_price_eur(code)
                price_lookups += 1

            uid_seed = f"{base_domain}|{code or name_fr.lower()}|{brand.lower()}"
            product_id = "od-" + hashlib.sha1(uid_seed.encode("utf-8")).hexdigest()[:12]

            collected.append({
                "id": product_id,
                "name": name_fr,
                "category": category,
                "brand": brand,
                "merchant": merchant,
                "merchant_type": merchant_type,
                "description": description,
                "price": verified_price,
                "image": image_url,
                "image_license": "CC-BY-SA",
                "url": "",
                "source": source_label,
            })

        time.sleep(0.2)

    return collected


def collect_open_library_books(queries: list[tuple[str, str]], limit_per_query: int = 30) -> list[dict[str, Any]]:
    books: list[dict[str, Any]] = []
    for category, q in queries:
        encoded = urllib.parse.quote(q)
        url = (
            f"https://openlibrary.org/search.json"
            f"?q={encoded}&language=fre&limit={limit_per_query}"
            f"&fields=key,title,author_name,publisher,first_publish_year,cover_i"
        )
        payload = http_get_json(url, timeout=20)
        docs = payload.get("docs")
        if not isinstance(docs, list):
            continue

        for doc in docs:
            if not isinstance(doc, dict):
                continue
            title = clean_text(doc.get("title"))
            cover_id = doc.get("cover_i")
            if len(title) < 3 or not isinstance(cover_id, int):
                continue
            if any(bad in title.lower() for bad in NON_GIFT_BLACKLIST):
                continue

            authors = doc.get("author_name") if isinstance(doc.get("author_name"), list) else []
            author_str = clean_text(authors[0]) if authors else "Auteur francophone"
            publishers = doc.get("publisher") if isinstance(doc.get("publisher"), list) else []
            pub_str = clean_text(publishers[0]) if publishers else "Édition française"
            year = doc.get("first_publish_year")
            year_txt = f" ({year})" if isinstance(year, int) else ""

            image_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
            uid_seed = f"ol|{title.lower()}|{author_str.lower()}"

            books.append({
                "id": "ol-" + hashlib.sha1(uid_seed.encode("utf-8")).hexdigest()[:12],
                "name": title,
                "category": category,
                "brand": author_str,
                "merchant": "Fnac / Cultura / Librairies indépendantes",
                "merchant_type": "Librairie & Grande enseigne",
                "description": f"Livre en français de {author_str} — {pub_str}{year_txt}.",
                "price": None,
                "image": image_url,
                "image_license": "Open Library Covers",
                "url": "",
                "source": "Open Library (français)",
            })

        time.sleep(0.2)

    return books


def main() -> None:
    fresh_items: list[dict[str, Any]] = []

    fresh_items.extend(collect_open_library_books(OPENLIBRARY_GIFT_QUERIES, limit_per_query=30))
    fresh_items.extend(
        collect_off_family(
            "world.openproductsfacts.org",
            "Open Products Facts (France, ODbL)",
            "Fnac / Darty / Boulanger / Cultura / JouéClub",
            OPF_GIFT_QUERIES,
            page_size=50,
            max_price_lookups=25,
        )
    )
    fresh_items.extend(
        collect_off_family(
            "world.openbeautyfacts.org",
            "Open Beauty Facts (France, ODbL)",
            "Sephora / Marionnaud / Nocibé / Yves Rocher",
            [("Beauté et soins", q) for q in OBF_GIFT_QUERIES],
            page_size=50,
            max_price_lookups=20,
        )
    )
    fresh_items.extend(
        collect_off_family(
            "fr.openfoodfacts.org",
            "Open Food Facts France (ODbL)",
            "Chocolatiers / Épiceries fines / Grandes enseignes",
            [("Gastronomie et gourmandises", q) for q in OFF_GIFT_QUERIES],
            page_size=50,
            max_price_lookups=25,
        )
    )

    merged: list[dict[str, Any]] = []
    seen: set[str] = set()

    for item in fresh_items:
        key = f"{item['name'].lower()}|{item['brand'].lower()}"
        if key in seen:
            continue
        seen.add(key)
        merged.append(item)

    merged.sort(key=lambda x: (0 if x.get("image") else 1, x.get("category", ""), x.get("name", "")))

    output = {
        "project": "Mon Noël organisé",
        "market": "FR",
        "language": "fr",
        "updated_at": dt.date.today().isoformat(),
        "total_products": len(merged),
        "products_with_images": sum(1 for p in merged if p.get("image")),
        "products": merged,
    }

    CATALOG_PATH.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Catalogue cadeaux actualisé : {output['total_products']} idée(s) cadeau "
        f"dont {output['products_with_images']} avec photo vérifiée."
    )


if __name__ == "__main__":
    main()
