#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'alimentation et d'actualisation de catalogue.json pour « Mon Noël organisé ».
Respecte les principes du cahier des charges :
- Priorité au marché français (FR / France) et aux fiches en français.
- Aucun prix inventé ou estimé arbitrairement (price = None si non vérifié).
- Aucun lien d'achat fabriqué ni disponibilité en stock inventée.
- Déduplication et conservation des références fiables existantes en cas d'indisponibilité réseau.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import pathlib
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG_PATH = REPO_ROOT / "catalogue.json"

OPEN_PRODUCTS_FACTS_SEARCH_URL = (
    "https://world.openproductsfacts.org/cgi/search.pl"
    "?search_simple=1&action=process&json=1&page_size=50"
    "&tagtype_0=countries&tag_contains_0=contains&tag_0=France"
    "&tagtype_1=languages&tag_contains_1=contains&tag_1=French"
)

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


def map_category(raw_categories: str, name_fr: str) -> str | None:
    text = f"{raw_categories} {name_fr}".lower()
    rules: list[tuple[str, list[str]]] = [
        ("Livres", ["livre", "book", "roman", "bd", "bande dessinee", "bande dessinée", "edition"]),
        ("Jeux de société", ["jeu de societe", "jeu de société", "plateau", "cartes"]),
        ("Jouets et jeux pour enfants", ["jouet", "peluche", "puzzle enfant", "eveil", "éveil", "construction"]),
        ("Loisirs créatifs", ["loisir creatif", "loisirs créatifs", "aquarelle", "peinture", "broderie", "tricot", "dessin"]),
        ("Sport et bien-être", ["sport", "yoga", "fitness", "bien-etre", "bien-être", "massage", "gourde"]),
        ("Jardinage", ["jardin", "graine", "plante", "secateur", "sécateur", "arrosoir", "nichoir"]),
        ("Gastronomie et gourmandises", ["chocolat", "the", "thé", "cafe", "café", "miel", "confiture", "epicerie", "épicerie", "gourmet"]),
        ("Bijoux", ["bijou", "collier", "bracelet", "bague", "boucle d'oreille"]),
        ("Beauté et soins", ["beaute", "beauté", "soin", "savon", "cosmetique", "cosmétique", "creme", "crème", "huile"]),
        ("Mode et accessoires", ["echarpe", "écharpe", "bonnet", "sac", "mode", "accessoire", "parapluie"]),
        ("Maison et décoration", ["maison", "decoration", "décoration", "lampe", "bougie", "plaid", "cuisine", "carafe"]),
        ("High-tech et électronique", ["audio", "casque", "enceinte", "liseuse", "numerique", "numérique", "electronique", "électronique"]),
    ]
    for category, keywords in rules:
        if any(kw in text for kw in keywords):
            return category
    return None


def is_french_entry(item: dict[str, Any]) -> bool:
    countries_tags = [str(c).lower() for c in (item.get("countries_tags") or [])]
    countries_str = str(item.get("countries") or "").lower()
    has_france = any("france" in t for t in countries_tags) or ("france" in countries_str)
    if not has_france:
        return False

    lang = str(item.get("lang") or "").lower()
    languages_tags = [str(l).lower() for l in (item.get("languages_tags") or [])]
    has_french = (
        lang in ("fr", "french", "en:fr")
        or any("french" in t or t.endswith(":fr") for t in languages_tags)
        or bool(str(item.get("product_name_fr") or "").strip())
    )
    return has_french


def fetch_open_products_facts(timeout: int = 20) -> list[dict[str, Any]]:
    req = urllib.request.Request(
        OPEN_PRODUCTS_FACTS_SEARCH_URL,
        headers={"User-Agent": "MonNoelOrganise/2026 (+https://github.com/)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
            products = payload.get("products")
            return products if isinstance(products, list) else []
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
        print(f"[AVERTISSEMENT] Impossible de récupérer Open Products Facts : {exc}")
        return []


def normalize_existing_products(existing_data: Any) -> list[dict[str, Any]]:
    if isinstance(existing_data, list):
        raw_list = existing_data
    elif isinstance(existing_data, dict) and isinstance(existing_data.get("products"), list):
        raw_list = existing_data["products"]
    else:
        return []

    cleaned: list[dict[str, Any]] = []
    for item in raw_list:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or "").strip()
        if not name:
            continue
        category = str(item.get("category") or "").strip()
        if category not in ALLOWED_CATEGORIES:
            category = "Cadeaux originaux et personnalisés"
        price = item.get("price")
        valid_price = float(price) if isinstance(price, (int, float)) and not isinstance(price, bool) and price >= 0 else None
        cleaned.append({
            "id": str(item.get("id") or "").strip() or hashlib.sha1(name.lower().encode("utf-8")).hexdigest()[:10],
            "name": name,
            "category": category,
            "brand": str(item.get("brand") or "Marque / Référence française").strip(),
            "merchant": str(item.get("merchant") or "Marché français").strip(),
            "merchant_type": str(item.get("merchant_type") or "").strip(),
            "description": str(item.get("description") or "").strip(),
            "price": valid_price,
            "image": is_valid_http_url(item.get("image")),
            "url": is_valid_http_url(item.get("url")),
            "source": str(item.get("source") or "Catalogue Mon Noël organisé").strip(),
        })
    return cleaned


def main() -> None:
    existing_payload: Any = {}
    if CATALOG_PATH.exists():
        try:
            existing_payload = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing_payload = {}

    products = normalize_existing_products(existing_payload)
    seen_keys = {
        f"{p['name'].strip().lower()}|{p['brand'].strip().lower()}"
        for p in products
    }

    raw_opf_items = fetch_open_products_facts()
    added_count = 0

    for raw in raw_opf_items:
        if not isinstance(raw, dict) or not is_french_entry(raw):
            continue

        name_fr = str(raw.get("product_name_fr") or raw.get("product_name") or "").strip()
        if len(name_fr) < 3:
            continue

        category = map_category(str(raw.get("categories") or ""), name_fr)
        if not category:
            continue

        brands_raw = str(raw.get("brands") or "").split(",")[0].strip()
        brand = brands_raw if brands_raw else "Marque française / Référence"

        dedup_key = f"{name_fr.lower()}|{brand.lower()}"
        if dedup_key in seen_keys:
            continue
        seen_keys.add(dedup_key)

        generic_name = str(raw.get("generic_name_fr") or raw.get("generic_name") or "").strip()
        description = generic_name or f"Produit commercialisé en France ({category.lower()})."
        image_url = is_valid_http_url(raw.get("image_front_small_url") or raw.get("image_url"))

        product_id = "opf-" + hashlib.sha1(dedup_key.encode("utf-8")).hexdigest()[:10]
        products.append({
            "id": product_id,
            "name": name_fr,
            "category": category,
            "brand": brand,
            "merchant": "France (Open Products Facts)",
            "merchant_type": "Donnée ouverte (ODbL)",
            "description": description,
            "price": None,  # Jamais de prix inventé ou non vérifié
            "image": image_url,
            "url": "",
            "source": "Open Products Facts (France, ODbL)",
        })
        added_count += 1

    output = {
        "project": "Mon Noël organisé",
        "market": "FR",
        "language": "fr",
        "updated_at": dt.date.today().isoformat(),
        "products": products,
    }

    CATALOG_PATH.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "
",
        encoding="utf-8",
    )
    print(f"Catalogue mis à jour : {len(products)} référence(s) au total (+{added_count} nouvelle(s) depuis Open Products Facts).")


if __name__ == "__main__":
    main()
