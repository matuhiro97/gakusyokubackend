# menu_optimizer.py
from scraper import scrape_category
from itertools import product

# ① ライス中の画像URLを定義
RICE_IMAGE_URL = "https://west2-univ.jp/menu_img/png_sp/814702.png"  # 実際のURLに合わせてください

RICE_OPTIONS = [
    {
        "name": "ライスミニ",
        "price": 77,
        "foodImageUrl": RICE_IMAGE_URL
    },
    {
        "name": "ライス小",
        "price": 100,
        "foodImageUrl": RICE_IMAGE_URL
    },
    {
        "name": "ライス中",
        "price": 154,
        "foodImageUrl": RICE_IMAGE_URL
    },
    {
        "name": "ライス大",
        "price": 187,
        "foodImageUrl": RICE_IMAGE_URL
    },
    {
        "name": "ライス特大",
        "price": 253,
        "foodImageUrl": RICE_IMAGE_URL
    }
]

def parse_price(item):
    try:
        return int(item["price"])
    except:
        return 0

def find_best_combinations(budget):
    main = scrape_category("on_a")
    side = scrape_category("on_b") + scrape_category("on_e")
    noodles = scrape_category("on_c")
    bowl = scrape_category("on_d")

    results = []

    # パターン1: ライス＋主菜＋副菜orデザート
    for rice in RICE_OPTIONS:
        for m, s in product(main, side):
            total = rice["price"] + parse_price(m) + parse_price(s)
            if total <= budget:
                results.append({
                    "pattern": "主菜＋ライス＋副菜orデザート",
                    "items": [rice, m, s],
                    "total": total
                })

    # パターン2: 麺類＋副菜orデザート
    for n, s in product(noodles, side):
        total = parse_price(n) + parse_price(s)
        if total <= budget:
            results.append({
                "pattern": "麺類＋副菜orデザート",
                "items": [n, s],
                "total": total
            })

    # パターン3: 丼・カレー＋副菜orデザート
    for d, s in product(bowl, side):
        total = parse_price(d) + parse_price(s)
        if total <= budget:
            results.append({
                "pattern": "丼・カレー＋副菜orデザート",
                "items": [d, s],
                "total": total
            })

    # ギリギリに近い順にソートして上位5件
    results.sort(key=lambda x: x["total"], reverse=True)
    return results[:5]
