import json
from itertools import product

with open("menu_data.json", encoding="utf-8") as f:
    MENU_DATA = json.load(f)

RICE_IMAGE_URL = "https://west2-univ.jp/menu_img/png_sp/814702.png"

RICE_OPTIONS = [
    {"name": "ライスミニ", "price": 77, "foodImageUrl": RICE_IMAGE_URL},
    {"name": "ライス小", "price": 140, "foodImageUrl": RICE_IMAGE_URL},
    {"name": "ライス中", "price": 154, "foodImageUrl": RICE_IMAGE_URL},
    {"name": "ライス大", "price": 187, "foodImageUrl": RICE_IMAGE_URL},
    {"name": "ライス特大", "price": 253, "foodImageUrl": RICE_IMAGE_URL},
]

def parse_price(item):
    try:
        return int(item["price"])
    except:
        return 0

def find_best_combinations(budget):
    main = [m for m in MENU_DATA if m["category"] == "主菜"]
    side = [s for s in MENU_DATA if s["category"] in ["副菜", "デザート"]]
    noodles = [n for n in MENU_DATA if n["category"] == "麺類"]
    bowl = [b for b in MENU_DATA if b["category"] == "丼・カレー"]

    results = []

    for rice in RICE_OPTIONS:
        for m, s in product(main, side):
            total = rice["price"] + parse_price(m) + parse_price(s)
            if total <= budget:
                results.append({
                    "pattern": "主菜＋ライス＋副菜orデザート",
                    "items": [rice, m, s],
                    "total": total
                })

    for n, s in product(noodles, side):
        total = parse_price(n) + parse_price(s)
        if total <= budget:
            results.append({
                "pattern": "麺類＋副菜orデザート",
                "items": [n, s],
                "total": total
            })

    for d, s in product(bowl, side):
        total = parse_price(d) + parse_price(s)
        if total <= budget:
            results.append({
                "pattern": "丼・カレー＋副菜orデザート",
                "items": [d, s],
                "total": total
            })

    results.sort(key=lambda x: x["total"], reverse=True)
    return results[:5]
