from flask import Flask, jsonify
from flask_cors import CORS
import scraper
from menu_optimizer import find_best_combinations  # ← 追加

app = Flask(__name__)
CORS(app)

@app.route("/menu", methods=["GET"])
def get_menu():
    data = scraper.scrape_all()
    return jsonify(data)

@app.route("/menu/<category>", methods=["GET"])
def get_menu_by_category(category):
    if category == "on_a":
        data = scraper.scrape_main_page(category)
    elif category in ["on_b", "on_c", "on_d", "on_e"]:
        data = scraper.scrape_category(category)
    else:
        return jsonify({"error": "Invalid category"}), 400
    return jsonify(data)

@app.route("/recommend/<int:budget>", methods=["GET"])  # ← 新API
def recommend_menu(budget):
    data = find_best_combinations(budget)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
