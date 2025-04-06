import requests
from bs4 import BeautifulSoup

MAIN_URL = "https://west2-univ.jp/sp/menu.php"
LOAD_URL = "https://west2-univ.jp/sp/menu_load.php"
TENPO_ID = "917631"

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
        img_url = img_tag.get("src") if img_tag else ""
        
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
    for cat in CATEGORY_MAP.keys():
        all_items.extend(scrape_category(cat))
    return all_items

def scrape_main_page(cat_key="on_a"):
    # 安全のため、scrape_category を使いまわす
    return scrape_category(cat_key)
