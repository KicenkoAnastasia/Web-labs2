# lab7.py
from flask import Blueprint, render_template, request, session

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

series = [
    {
        "title": "Lost",
        "title_ru": "Остаться вживых",
        "year": "2004–2010",
        "description": "Красавец-лайнер, совершающий полет из Сиднея в Лос-Анджелес, неожиданно терпит крушение. 48 пассажиров оказываются на пустынном острове посреди океана. Люди в панике. Надежда быть найденными довольно призрачна. Поэтому остается только одно: собраться с силами и постараться выжить на острове, начиненном множеством опасностей..."
    },
    {
        "title": "Grotesquerie",
        "title_ru": "Гротеск",
        "year": "2024",
        "description": "Сестра Меган и детектив Лоис Трион расследуют серию ужасающих преступлений, которые оказывают влияние не только на сообщества, к которым они принадлежат, но и на их личную жизнь."
    },
    {
        "title": "Bad Sisters",
        "title_ru": "Заговор сестёр Гарви",
        "year": "2022",
        "description": "Сестры Гарви всегда заботились друг о друге. После гибели их зятя страховая компания начинает расследование, и подозрение падает на сестер, ведь у каждой из них было немало причин совершить это убийство."
    },
    {
        "title": "Dark",
        "title_ru": "Тьма",
        "year": "2017–2020",
        "description": "История четырёх семей, живущих спокойной и размеренной жизнью в маленьком немецком городке. Видимая идиллия рушится, когда бесследно исчезают двое детей и воскресают тёмные тайны прошлого."
    },
    {
        "title": "Behind Her Eyes",
        "title_ru": "В её глазах",
        "year": "2021",
        "description": "Мать-одиночка Луиза заводит роман с привлекательным незнакомцем в баре, но вскоре выясняется, что это ее новый босс Дэвид. Мужчина к тому же женат, но Луиза не может прекратить эту связь. Через какое-то время запутавшаяся женщина становится лучшей подругой жены Дэвида и начинает подозревать, что за их супружескими отношениями скрывается нечто зловещее."
    }
]


# Возвращаем все сериалы
@lab7.route('/lab7/rest-api/series/', methods=['GET'])
def get_series():
    return {"series": series}

# Возвращаем сериал по ID, с проверкой на диапазон
@lab7.route('/lab7/rest-api/series/<int:id>', methods=['GET'])
def get_series_by_id(id):
    if 0 <= id < len(series):
        return series[id]  # Возвращаем сериал с указанным id
    else:
        return {"error": "Series not found"}, 404  # Ошибка 404, если id не в пределах диапазона

# Удаляем сериал по ID
@lab7.route('/lab7/rest-api/series/<int:id>', methods=['DELETE'])
def del_series(id):
    if 0 <= id < len(series):
        del series[id]  # Удаляем сериал с указанным id
        return '', 204  # Успешное удаление, возвращаем код 204
    else:
        return {"error": "Series not found"}, 404  # Ошибка 404, если id не в пределах диапазона


@lab7.route('/lab7/rest-api/series/<int:id>', methods=['PUT'])
def put_series(id):
    # Проверка корректности диапазона ID
    if id < 0 or id >= len(series):
        return {"error": "Series not found"}, 404

    series_item = request.get_json()

    # Проверка корректности данных
    if not series_item or not all(key in series_item for key in ["title", "title_ru", "year", "description"]):
        return {"error": "Invalid data provided"}, 400

    # Обновление записи
    series[id] = series_item
    return series[id], 200

@lab7.route('/lab7/rest-api/series/', methods=['POST'])
def add_film():
    # Получение данных нового фильма из тела запроса
    new_series = request.get_json()

    # Проверка корректности данных
    if not new_series or not all(key in new_series for key in ["title", "title_ru", "year", "description"]):
        return {"error": "Invalid data provided"}, 400

    # Добавление нового фильма в конец списка
    series.append(new_series)

    # Возвращаем индекс нового фильма
    return {"id": len(series) - 1}, 201
