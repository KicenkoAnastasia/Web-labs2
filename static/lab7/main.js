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

            tbody.innerHTML = ''; // Очищаем содержимое таблицы

            series.forEach(series => {
                let tr = document.createElement('tr');

                let tdTitle = document.createElement('td');
                let tdTitleRus = document.createElement('td');
                let tdYear = document.createElement('td');
                let tdActions = document.createElement('td');

                tdTitle.innerText = series.title || 'N/A';
                tdTitleRus.innerText = series.title_ru || 'N/A';
                tdYear.innerText = series.year || 'N/A';

                let editButton = document.createElement('button');
                editButton.innerText = 'редактировать';

                let deleteButton = document.createElement('button');
                deleteButton.innerText = 'удалить';

                tdActions.append(editButton, deleteButton);

                tr.append(tdTitle, tdTitleRus, tdYear, tdActions);

                tbody.append(tr);
            });
        })
        .catch(error => console.error('Error fetching series:', error));
}
