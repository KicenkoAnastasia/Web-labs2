// main.js
// Функция для заполнения списка сериалов на странице
function FillSeriesList() {
    // fetch запрос к API для получения списка сериалов
    fetch('/lab7/rest-api/series/')
        .then(response => response.json()) //  ответ в формат JSON
        .then(data => {
            const series = data.series; // Извлекаем сериалы из ответа

            let tbody = document.getElementById('series-list'); // Получаем элемент таблицы для вывода данных
            tbody.innerHTML = '';

            // Проходим по каждому сериалу и добавляем его в таблицу
            series.forEach(seriesItem => {
                let tr = document.createElement('tr'); // Создаем строку 

                // Создаем ячейку для названия сериала на русском языке
                let tdTitleRus = document.createElement('td');
                tdTitleRus.innerText = seriesItem.title_ru || 'N/A'; // Если название на русском отсутствует

                // Создаем ячейку для названия сериала на оригинальном языке
                let tdTitle = document.createElement('td');
                tdTitle.classList.add('italic'); // Добавляем класс для оформления (например, курсив)
                tdTitle.innerHTML = seriesItem.title
                    ? `(${seriesItem.title})`  // Если название присутствует, вывод в скобках
                    : '(N/A)';  // Если нет

                //  ячейка для года выпуска сериала
                let tdYear = document.createElement('td');
                tdYear.innerText = seriesItem.year || 'N/A'; 

                //  ячейка для кнопок действий
                let tdActions = document.createElement('td');
                let editButton = document.createElement('button'); 
                editButton.innerText = 'редактировать';
                editButton.onclick = function () {
                    editSeries(seriesItem); // При нажатии  функция редактирования
                };

                let deleteButton = document.createElement('button'); // Кнопка для удаления
                deleteButton.innerText = 'удалить';
                deleteButton.onclick = function () {
                    deleteSeries(seriesItem.id); // При нажатии  функция удаления
                };

                tdActions.append(editButton, deleteButton); // Добавляем кнопки в ячейку

                // Добавляем все ячейки в строку таблицы
                tr.append(tdTitleRus, tdTitle, tdYear, tdActions);
                tbody.append(tr); // Добавляем строку в таблицу
            });
        })
        .catch(error => console.error('Error fetching series:', error)); // Обработка ошибок
}

// Функция для удаления сериала по ID
function deleteSeries(id) {
    if (!confirm('Вы точно хотите удалить сериал?')) return; 

    //  запрос DELETE на сервер для удаления сериала
    fetch(`/lab7/rest-api/series/${id}`, { method: 'DELETE' })
        .then(response => {
            if (!response.ok) throw new Error('Ошибка при удалении сериала');
            FillSeriesList(); // Перезагрузка списка сериалов
        })
        .catch(error => console.error('Error deleting series:', error)); // Обработка ошибок
}

// Функция для отображения модального окна
function showModal() {
    document.querySelector('.modal').style.display = 'block'; // Показываем 
    // Очищаем поля формы
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    document.getElementById('description-error').textContent = ''; // Очищаем сообщение об ошибке
}

// Функция для скрытия модального окна
function hideModal() {
    document.querySelector('.modal').style.display = 'none';
}

// Функция для отмены операции и закрытия модального окна
function cancel() {
    hideModal(); // Закрываем
}

// Функция для вызова модального окна для добавления нового сериала
function addSeries() {
    showModal(); // Показываем 
}

// Функция для отправки данных о сериале на сервер
function sendSeries() {
    const id = document.getElementById('id').value; // Получаем ID сериала
    const descriptionField = document.getElementById('description'); //  поле с описанием
    const descriptionError = document.getElementById('description-error'); // место для отображения ошибки

    // Создаем объект с данными о сериале
    const series = {
        title: document.getElementById('title').value, 
        title_ru: document.getElementById('title-ru').value,
        year: document.getElementById('year').value, 
        description: descriptionField.value.trim(), 
    };

    // Определяем URL и метод (POST для добавления, PUT для редактирования)
    const url = id ? `/lab7/rest-api/series/${id}` : '/lab7/rest-api/series/';
    const method = id ? 'PUT' : 'POST';

    //  запрос на сервер
    fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(series), // Отправляем данные в формате JSON
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => {
                    throw new Error(
                        err.errors ? err.errors.join("; ") : "Не удалось выполнить действие"
                    ); 
                });
            }
            return response.json(); //  ответ от сервера
        })
        .then(() => {
            FillSeriesList(); // Обновляем список 
            hideModal(); // Закрываем модальное окно
        })
        .catch(error => {
            descriptionError.textContent = error.message; // Отображаем ошибку в интерфейсе
            descriptionField.style.border = '2px solid red'; 
        });
}

// Функция для редактирования существующего сериала
function editSeries(series) {
    showModal(); //  модальное окно
    document.getElementById('id').value = series.id; 
    document.getElementById('title').value = series.title;
    document.getElementById('title-ru').value = series.title_ru;
    document.getElementById('year').value = series.year;
    document.getElementById('description').value = series.description;
}
