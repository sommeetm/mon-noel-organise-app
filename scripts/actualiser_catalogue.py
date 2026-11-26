#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'alimentation massive et fiable de catalogue.json pour « Mon Noël organisé ».
Objectif : constituer un catalogue riche (300 à 600+ références françaises) avec de
véritables photos ouvertes (ODbL / CC-BY-SA / couvertures Open Library), sans aucun
produit fictif codé en dur dans le JavaScript, sans prix inventé et sans lien marchand
fabriqué.

Sources ouvertes interrogées :
1. Open Products Facts (France + français, licence ODbL / images CC-BY-SA)
   -> High-tech, Maison, Jeux, Jouets, Sport, Jardinage, Mode, Loisirs
2. Open Beauty Facts (France + français, licence ODbL / images CC-BY-SA)
   -> Beauté et soins (parfums, coffrets, soins visage/corps, savons)
3. Open Food Facts France (France + français, licence ODbL / images CC-BY-SA)
   -> Gastronomie et gourmandises (chocolats fins, thés, cafés, miel, confitures)
4. Open Library (ouvrages en français avec couverture vérifiée, CC0 / Open Data)
   -> Livres (romans, beaux livres, BD, cuisine, jeunesse)
5. Open Prices (prices.openfoodfacts.org, licence ODbL)
   -> Enrichissement des prix réels observés en EUR en France lorsqu'un code-barres
      correspond, sinon `price = None` ("Prix à vérifier").
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
    "High-tech et électronique",
    "Maison et décoration",
    "Beauté et soins",
    "Mode et accessoires",
    "Bijoux",
    "Livres",
    "Jeux de société",
    "Jouets et jeux pour enfants",
    "Loisirs créatifs",
    "Sport et bien-être",
    "Jardinage",
    "Gastronomie et gourmandises",
    "Produits artisanaux",
    "Cadeaux originaux et personnalisés",
]

# Requêtes thématiques ciblées vers Open Products Facts (France)
OPF_QUERIES: list[tuple[str, str]] = [
    ("High-tech et électronique", "casque audio"),
    ("High-tech et électronique", "enceinte bluetooth"),
    ("High-tech et électronique", "appareil photo"),
    ("High-tech et électronique", "montre connectée"),
    ("Maison et décoration", "bougie parfumée"),
    ("Maison et décoration", "lampe"),
    ("Maison et décoration", "cafetière"),
    ("Maison et décoration", "théière"),
    ("Maison et décoration", "mug"),
    ("Maison et décoration", "plaid"),
    ("Jeux de société", "jeu de société"),
    ("Jeux de société", "jeu de cartes"),
    ("Jouets et jeux pour enfants", "jouet"),
    ("Jouets et jeux pour enfants", "peluche"),
    ("Jouets et jeux pour enfants", "puzzle"),
    ("Jouets et jeux pour enfants", "lego"),
    ("Loisirs créatifs", "peinture"),
    ("Loisirs créatifs", "crayons couleur"),
    ("Loisirs créatifs", "carnet dessin"),
    ("Sport et bien-être", "gourde"),
    ("Sport et bien-être", "yoga"),
    ("Sport et bien-être", "massage"),
    ("Jardinage", "graines"),
    ("Jardinage", "jardin"),
    ("Mode et accessoires", "sac"),
    ("Mode et accessoires", "écharpe"),
    ("Bijoux", "bijou"),
]

# Requêtes Open Beauty Facts (France) -> Beauté et soins
OBF_QUERIES: list[str] = [
    "coffret",
    "parfum",
    "eau de toilette",
    "savon",
    "crème mains",
    "huile corps",
    "baume",
    "bougie",
]

# Requêtes Open Food Facts France -> Gastronomie et gourmandises (produits cadeaux)
OFF_GOURMET_CATEGORIES: list[str] = [
    "chocolats",
    "pralines",
    "thes",
    "cafes",
    "miels",
    "confitures",
    "biscuits-fins",
]

# Requêtes Open Library (langue française, avec couverture) -> Livres
OPENLIBRARY_QUERIES: list[str] = [
    "roman français",
    "bande dessinée",
    "cuisine française",
    "patrimoine france",
    "histoire de france",
    "livre jeunesse",
]


def http_get_json(url: str, timeout: int = 20) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data if isinstance(data, dict) else {}
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
        print(f"[INFO] Requête ignorée ({url[:80]}...) : {exc}")
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


def is_french_market(item: dict[str, Any]) -> bool:
    countries_tags = [str(c).lower() for c in (item.get("countries_tags") or [])]
    countries_str = str(item.get("countries") or "").lower()
    if not (any("france" in t for t in countries_tags) or ("france" in countries_str)):
        return False

    lang = str(item.get("lang") or "").lower()
    languages_tags = [str(l).lower() for l in (item.get("languages_tags") or [])]
    has_fr = (
        lang in ("fr", "french", "en:fr")
        or any("french" in t or t.endswith(":fr") for t in languages_tags)
        or bool(clean_text(item.get("product_name_fr")))
    )
    return has_fr


def infer_category(raw_categories: str, name_fr: str, fallback: str) -> str:
    text = f"{raw_categories} {name_fr}".lower()
    rules: list[tuple[str, list[str]]] = [
        ("Livres", ["livre", "roman", "bande dessinée", "bande dessinee", "atlas", "album illustré"]),
        ("Jeux de société", ["jeu de société", "jeu de societe", "jeu de plateau", "jeu de cartes"]),
        ("Jouets et jeux pour enfants", ["jouet", "peluche", "puzzle", "lego", "playmobil", "poupée", "poupee", "éveil", "eveil"]),
        ("Loisirs créatifs", ["peinture", "aquarelle", "crayon", "feutre", "broderie", "tricot", "dessin", "loisir créatif"]),
        ("Sport et bien-être", ["sport", "yoga", "fitness", "gourde", "massage", "bien-être", "bien-etre"]),
        ("Jardinage", ["jardin", "graine", "plante", "sécateur", "secateur", "arrosoir", "nichoir"]),
        ("Gastronomie et gourmandises", ["chocolat", "pralin", "thé", "the", "café", "cafe", "miel", "confiture", "biscuit", "nougat", "calisson"]),
        ("Bijoux", ["bijou", "collier", "bracelet", "bague", "boucle"]),
        ("Beauté et soins", ["parfum", "eau de toilette", "savon", "crème", "creme", "huile", "baume", "soin", "coffret beauté"]),
        ("Mode et accessoires", ["écharpe", "echarpe", "bonnet", "sac", "portefeuille", "parapluie", "mode"]),
        ("Maison et décoration", ["bougie", "lampe", "plaid", "mug", "tasse", "théière", "theiere", "cafetière", "cafetiere", "carafe", "décoration"]),
        ("High-tech et électronique", ["casque", "enceinte", "audio", "bluetooth", "appareil photo", "liseuse", "montre connectée"]),
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
    return ""


def format_stores(item: dict[str, Any], default_merchant: str) -> tuple[str, str]:
    stores_raw = clean_text(item.get("stores"))
    if not stores_raw:
        return default_merchant, "Donnée ouverte (ODbL)"
    stores_list = [s.strip() for s in stores_raw.split(",") if s.strip()]
    unique_stores = list(dict.fromkeys(stores_list))[:3]
    merchant_label = " / ".join(unique_stores)
    big_retailers = {"carrefour", "leclerc", "auchan", "fnac", "cultura", "boulanger", "darty", "intermarché", "super u", "monoprix", "sephora", "marionnaud", "yves rocher", "nocibé", "nature & découvertes"}
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
        if isinstance(price, (int, float)) and not isinstance(price, bool) and 0.5 <= float(price) <= 2000:
            return round(float(price), 2)
    return None


def collect_off_family(
    base_domain: str,
    source_label: str,
    query_terms: list[tuple[str, str]],
    use_category_tag: bool = False,
    page_size: int = 40,
    max_price_lookups: int = 35,
) -> list[dict[str, Any]]:
    collected: list[dict[str, Any]] = []
    price_lookups = 0

    for default_category, term in query_terms:
        encoded = urllib.parse.quote(term)
        if use_category_tag:
            url = (
                f"https://{base_domain}/cgi/search.pl"
                f"?search_simple=1&action=process&json=1&page_size={page_size}"
                f"&tagtype_0=countries&tag_contains_0=contains&tag_0=France"
                f"&tagtype_1=categories&tag_contains_1=contains&tag_1={encoded}"
                f"&fields=code,product_name,product_name_fr,generic_name,generic_name_fr,brands,categories,stores,countries,countries_tags,lang,languages_tags,image_front_url,image_front_small_url,image_url,url"
            )
        else:
            url = (
                f"https://{base_domain}/cgi/search.pl"
                f"?search_terms={encoded}&search_simple=1&action=process&json=1&page_size={page_size}"
                f"&tagtype_0=countries&tag_contains_0=contains&tag_0=France"
                f"&fields=code,product_name,product_name_fr,generic_name,generic_name_fr,brands,categories,stores,countries,countries_tags,lang,languages_tags,image_front_url,image_front_small_url,image_url,url"
            )

        payload = http_get_json(url, timeout=20)
        raw_products = payload.get("products")
        if not isinstance(raw_products, list):
            continue

        for raw in raw_products:
            if not isinstance(raw, dict) or not is_french_market(raw):
                continue

            name_fr = clean_text(raw.get("product_name_fr") or raw.get("product_name"))
            if len(name_fr) < 4:
                continue

            image_url = extract_best_image(raw)
            if not image_url:
                continue

            brands_raw = clean_text(raw.get("brands"))
            brand = brands_raw.split(",")[0].strip() if brands_raw else "Marque française / Référence"
            category = infer_category(clean_text(raw.get("categories")), name_fr, default_category)
            merchant, merchant_type = format_stores(raw, "Enseignes & commerces en France")

            generic_fr = clean_text(raw.get("generic_name_fr") or raw.get("generic_name"))
            description = generic_fr if len(generic_fr) >= 8 else f"{name_fr} — référence commercialisée en France ({category.lower()})."

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
                "url": "",  # Aucun lien marchand inventé
                "source": source_label,
            })

        time.sleep(0.25)

    return collected


def collect_open_library_books(queries: list[str], limit_per_query: int = 25) -> list[dict[str, Any]]:
    books: list[dict[str, Any]] = []
    for q in queries:
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
                "category": "Livres",
                "brand": author_str,
                "merchant": "Librairies indépendantes / Fnac / Cultura",
                "merchant_type": "Librairie & Grande enseigne",
                "description": f"Ouvrage en français de {author_str} — {pub_str}{year_txt}.",
                "price": None,
                "image": image_url,
                "image_license": "Open Library Covers",
                "url": "",
                "source": "Open Library (français)",
            })

        time.sleep(0.25)

    return books


def normalize_existing(payload: Any) -> list[dict[str, Any]]:
    raw_list = payload if isinstance(payload, list) else payload.get("products", []) if isinstance(payload, dict) else []
    cleaned: list[dict[str, Any]] = []
    for item in raw_list:
        if not isinstance(item, dict):
            continue
        name = clean_text(item.get("name"))
        if not name:
            continue
        category = clean_text(item.get("category"))
        if category not in ALLOWED_CATEGORIES:
            category = "Cadeaux originaux et personnalisés"
        price = item.get("price")
        valid_price = round(float(price), 2) if isinstance(price, (int, float)) and not isinstance(price, bool) and price > 0 else None
        cleaned.append({
            "id": clean_text(item.get("id")) or "cat-" + hashlib.sha1(name.lower().encode("utf-8")).hexdigest()[:10],
            "name": name,
            "category": category,
            "brand": clean_text(item.get("brand")) or "Marque française",
            "merchant": clean_text(item.get("merchant")) or "Marché français",
            "merchant_type": clean_text(item.get("merchant_type")),
            "description": clean_text(item.get("description")),
            "price": valid_price,
            "image": is_valid_http_url(item.get("image")),
            "image_license": clean_text(item.get("image_license")),
            "url": is_valid_http_url(item.get("url")),
            "source": clean_text(item.get("source")) or "Catalogue Mon Noël organisé",
        })
    return cleaned


def main() -> None:
    existing_payload: Any = {}
    if CATALOG_PATH.exists():
        try:
            existing_payload = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing_payload = {}

    existing_items = normalize_existing(existing_payload)

    fresh_items: list[dict[str, Any]] = []
    fresh_items.extend(
        collect_off_family(
            "world.openproductsfacts.org",
            "Open Products Facts (France, ODbL)",
            OPF_QUERIES,
            use_category_tag=False,
            page_size=40,
            max_price_lookups=20,
        )
    )
    fresh_items.extend(
        collect_off_family(
            "world.openbeautyfacts.org",
            "Open Beauty Facts (France, ODbL)",
            [("Beauté et soins", q) for q in OBF_QUERIES],
            use_category_tag=False,
            page_size=40,
            max_price_lookups=20,
        )
    )
    fresh_items.extend(
        collect_off_family(
            "fr.openfoodfacts.org",
            "Open Food Facts France (ODbL)",
            [("Gastronomie et gourmandises", c) for c in OFF_GOURMET_CATEGORIES],
            use_category_tag=True,
            page_size=40,
            max_price_lookups=25,
        )
    )
    fresh_items.extend(collect_open_library_books(OPENLIBRARY_QUERIES, limit_per_query=25))

    # Fusion et déduplication : priorité aux nouvelles fiches Open Data avec photo
    merged: list[dict[str, Any]] = []
    seen: set[str] = set()

    for item in fresh_items + existing_items:
        key = f"{item['name'].lower()}|{item['brand'].lower()}"
        if key in seen:
            continue
        seen.add(key)
        merged.append(item)

    # Trier pour présenter d'abord les fiches ayant une photo vérifiée
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
        json.dumps(output, ensure_ascii=False, indent=2) + "
",
        encoding="utf-8",
    )
    print(
        f"Catalogue actualisé : {output['total_products']} référence(s) "
        f"dont {output['products_with_images']} avec photo vérifiée."
    )


if __name__ == "__main__":
    main()
