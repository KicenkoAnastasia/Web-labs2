#lab7.py
from flask import Blueprint, render_template, request, jsonify

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

series = [
    {
        "title": "Lost",
        "title_ru": "Остаться вживых",
        "year": "2004–2010", 
        "description": "Красавец-лайнер, совершающий полет из Сиднея в Лос-Анджелес...",
    },
    {
        "title": "Grotesquerie",
        "title_ru": "Гротеск",
        "year": "2024",
        "description": "Сестра Меган и детектив Лоис Трион расследуют серию...",
    }
]

@lab7.route('/lab7/rest-api/series/', methods=['GET'])
def get_series():
    return jsonify({"series": [{"id": idx, **item} for idx, item in enumerate(series)]})

@lab7.route('/lab7/rest-api/series/<int:id>', methods=['DELETE'])
def delete_series(id):
    if 0 <= id < len(series):
        del series[id]
        return '', 204
    return jsonify({"error": "Сериал не найден"}), 404

@lab7.route('/lab7/rest-api/series/', methods=['POST'])
def add_series():
    new_series = request.get_json()
    errors = validate_series(new_series)
    if errors:
        return jsonify({"errors": errors}), 400

    if not new_series.get("title"):
        new_series["title"] = new_series["title_ru"]

    series.append(new_series)
    return jsonify({"id": len(series) - 1}), 201

@lab7.route('/lab7/rest-api/series/<int:id>', methods=['PUT'])
def update_series(id):
    if id < 0 or id >= len(series):
        return jsonify({"error": "Сериал не найден"}), 404

    updated_series = request.get_json()
    errors = validate_series(updated_series)
    if errors:
        return jsonify({"errors": errors}), 400

    if not updated_series.get("title"):
        updated_series["title"] = updated_series["title_ru"]

    series[id] = updated_series
    return jsonify(series[id]), 200

# Функция для валидации сериалов
def validate_series(series_data):
    errors = []
    if not series_data.get("title_ru"):
        errors.append("Название на русском языке обязательно.")
    if not series_data.get("description"):
        errors.append("Описание обязательно.")
    elif len(series_data["description"]) > 2000:
        errors.append("Описание не должно превышать 2000 символов.")
    try:
        year = int(series_data["year"])
        if year < 1895 or year > 2023:
            errors.append("Год должен быть в пределах от 1895 до текущего.")
    except (ValueError, TypeError):
        errors.append("Год должен быть числом.")
    return errors