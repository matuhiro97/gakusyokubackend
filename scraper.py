import requests
from bs4 import BeautifulSoup
import json

MAIN_URL = "https://west2-univ.jp/sp/menu.php"
LOAD_URL = "https://west2-univ.jp/sp/menu_load.php"
TENPO_ID = "917631"
BASE_IMG_URL = "https://west2-univ.jp"

CATEGORY_MAP = {
    "on_a": "主菜",
    "on_b": "副菜",
    "on_c": "麺類",
    "on_d": "丼・カレー",
    "on_e": "デザート"
}

def scrape_category(a_value):
    params = {"t": TENPO_ID, "a": a_value}
    r = requests.get(LOAD_URL, params=params)
    soup = BeautifulSoup(r.text, "html.parser")

    menu_items = soup.find_all("li")
    results = []

    for li in menu_items:
        a_tag = li.find("a")
        if not a_tag:
            continue
        img_tag = li.find("img")
        img_url = BASE_IMG_URL + img_tag.get("src") if img_tag else ""

        h3 = a_tag.find("h3")
        if not h3:
            continue
        name_jp = h3.contents[0].strip()
        price_tag = h3.find("span", class_="price")
        price = price_tag.text.replace("¥", "").strip() if price_tag else ""

        results.append({
            "foodName": name_jp,
            "foodImageUrl": img_url,
            "price": price,
            "category": CATEGORY_MAP.get(a_value, "不明")
        })

    return results

def scrape_all():
    all_items = []
    for cat in CATEGORY_MAP:
        all_items.extend(scrape_category(cat))
    return all_items

def save_menu_to_json():
    data = scrape_all()
    with open("menu_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("menu_data.jsonに保存しました")
