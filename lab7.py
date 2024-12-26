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

# Обработчик для получения списка всех сериалов
@lab7.route('/lab7/rest-api/series/', methods=['GET'])
def get_series():
    # Формируем список сериалов с id, добавляя их в формате JSON
    return jsonify({"series": [{"id": idx, **item} for idx, item in enumerate(series)]})

# Обработчик для удаления сериала по ID
@lab7.route('/lab7/rest-api/series/<int:id>', methods=['DELETE'])
def delete_series(id):
    #  существует ли сериал с таким ID
    if 0 <= id < len(series):
        del series[id]  # Удаляем сериал из списка по индексу
        return '', 204  # Возвращаем статус 204 (No Content)
    return jsonify({"error": "Сериал не найден"}), 404

# Обработчик для добавления нового сериала
@lab7.route('/lab7/rest-api/series/', methods=['POST'])
def add_series():
    #  данные о сериале в формате JSON 
    new_series = request.get_json()
    # Валидируем данные сериала
    errors = validate_series(new_series)
    if errors:
        return jsonify({"errors": errors}), 400
    # Если название сериала отсутствует, используем название на русском языке 
    if not new_series.get("title"):
        new_series["title"] = new_series["title_ru"]
    # Добавляем новый сериал в список и возвращаем его ID
    series.append(new_series)
    return jsonify({"id": len(series) - 1}), 201  # Возвращаем статус 201 (Created) и ID нового сериала



# Обработчик для обновления данных существующего сериала по ID
@lab7.route('/lab7/rest-api/series/<int:id>', methods=['PUT'])
def update_series(id):
    # Проверяем, существует ли сериал с таким ID
    if id < 0 or id >= len(series):
        return jsonify({"error": "Сериал не найден"}), 404  

    # Получаем данные обновленного сериала в формате JSON
    updated_series = request.get_json()
    errors = validate_series(updated_series)
    if errors:
        return jsonify({"errors": errors}), 400

    if not updated_series.get("title"):
        updated_series["title"] = updated_series["title_ru"]

    # Обновляем сериал в списке по ID
    series[id] = updated_series
    return jsonify(series[id]), 200  # Возвращаем обновленные данные сериала с кодом 200 (OK)

# Функция для валидации данных о сериале
def validate_series(series_data):
    errors = []  # Список для хранения ошибок валидации

    if not series_data.get("title_ru"):
        errors.append("Название на русском языке обязательно.")
    if not series_data.get("description"):
        errors.append("Описание обязательно.")
    elif len(series_data["description"]) > 2000:
        errors.append("Описание не должно превышать 2000 символов.")
    try:
        year = int(series_data["year"])
        if year < 1895 or year > 2024:
            errors.append("Год должен быть в пределах от 1895 до текущего.")
    except (ValueError, TypeError):
        errors.append("Год должен быть числом.")
    return errors  #  список ошибок (если есть)
