#!/usr/bin/env python3
"""Convertit catalogue.json (format meta/articles) vers le format products attendu par app.js."""

import json
from datetime import datetime, timezone
from pathlib import Path

CATEGORY_MAP = {
    "Cinéma & Séries": "DVD, Blu-ray et musique",
    "Jeux & Société": "Jeux de société",
    "Maison & Déco": "Maison et décoration",
    "Beauté & Parfums": "Beauté et soins",
    "Loisirs & Créatifs": "Loisirs créatifs",
    "Enfants & Ados": "Jouets et jeux pour enfants",
    "Gastronomie": "Gastronomie et gourmandises",
}


def main() -> None:
    path = Path("catalogue.json")
    raw = json.loads(path.read_text(encoding="utf-8"))

    # Si déjà au format products, ne rien casser
    if isinstance(raw, dict) and isinstance(raw.get("products"), list):
        print(f"Déjà au format products ({len(raw['products'])} articles).")
        return

    source_items = (
        raw.get("articles", [])
        if isinstance(raw, dict)
        else raw if isinstance(raw, list) else []
    )
    meta = raw.get("meta", {}) if isinstance(raw, dict) else {}

    products = []
    for i, item in enumerate(source_items, start=1):
        if not isinstance(item, dict):
            continue
        title = str(item.get("titre") or item.get("name") or "").strip()
        if not title:
            continue

        cat_raw = str(item.get("categorie") or item.get("category") or "").strip()
        category = CATEGORY_MAP.get(cat_raw, cat_raw or "Cadeaux originaux et personnalisés")

        price_val = item.get("prix", item.get("price"))
        try:
            price = float(price_val) if price_val is not None and float(price_val) > 0 else None
        except (TypeError, ValueError):
            price = None

        item_id = str(item.get("id") or f"cat-{i}").strip()
        merchant = str(item.get("enseigne") or item.get("merchant") or "Marché français").strip()
        description = str(item.get("description") or "").strip()

        products.append({
            "id": item_id.lower().replace(" ", "-"),
            "name": title,
            "category": category,
            "brand": str(item.get("marque") or item.get("brand") or "Marque / Référence française").strip(),
            "merchant": merchant,
            "merchant_type": "Enseigne FR",
            "description": description,
            "price": price,
            "image": "",
            "image_license": "",
            "url": "",
            "source": str(meta.get("projet") or "Catalogue cadeaux Noël (FR)").strip(),
        })

    updated_at = (
        str(meta.get("date_mise_a_jour") or "")[:10]
        or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    )

    output = {
        "project": str(meta.get("projet") or "Mon Noël organisé"),
        "market": "FR",
        "language": "fr",
        "updated_at": updated_at,
        "total_products": len(products),
        "products_with_images": sum(1 for p in products if p["image"]),
        "products": products,
    }

    path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"catalogue.json converti avec {len(products)} produits.")


if __name__ == "__main__":
    main()
