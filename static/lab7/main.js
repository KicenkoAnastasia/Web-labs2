function FillSeriesList() {
    fetch('/lab7/rest-api/series/')
        .then(response => response.json())
        .then(data => {
            const series = data.series; // Извлекаем массив сериалов
            console.log(series); // Для проверки

            let tbody = document.getElementById('series-list');
            if (!tbody) {
                console.error('Element with ID "series-list" not found');
                return;
            }

            tbody.innerHTML = ''; // Очищаем 

            series.forEach((seriesItem, index) => { 
                let tr = document.createElement('tr');

                let tdTitle = document.createElement('td');
                let tdTitleRus = document.createElement('td');
                let tdYear = document.createElement('td');
                let tdActions = document.createElement('td');

                tdTitle.innerText = seriesItem.title || 'N/A';
                tdTitleRus.innerText = seriesItem.title_ru || 'N/A';
                tdYear.innerText = seriesItem.year || 'N/A';

                let editButton = document.createElement('button');
                editButton.innerText = 'редактировать';

                let deleteButton = document.createElement('button');
                deleteButton.innerText = 'удалить';
                deleteButton.onclick = function () {
                    deleteSeries(index); // Передаём индекс
                };

                tdActions.append(editButton, deleteButton);

                tr.append(tdTitle, tdTitleRus, tdYear, tdActions);

                tbody.append(tr);
            });
        })
        .catch(error => console.error('Error fetching series:', error));
}

function deleteSeries(id) {
    if (!confirm('Вы точно хотите удалить сериал?'))
        return;

    fetch(`/lab7/rest-api/series/${id}`, { method: 'DELETE' }) // Исправлено использование шаблонной строки
        .then(() => {
            FillSeriesList(); // Обновляем список после удаления
        })
        .catch(error => console.error('Error deleting series:', error));
}
