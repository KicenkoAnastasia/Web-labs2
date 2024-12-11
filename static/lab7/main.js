// main.js
function FillSeriesList() {
    fetch('/lab7/rest-api/series/')
        .then(response => response.json())
        .then(data => {
            const series = data.series;

            let tbody = document.getElementById('series-list');
            tbody.innerHTML = '';

            series.forEach(seriesItem => {
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
                editButton.onclick = function () {
                    editSeries(seriesItem);
                };

                let deleteButton = document.createElement('button');
                deleteButton.innerText = 'удалить';
                deleteButton.onclick = function () {
                    deleteSeries(seriesItem.id);
                };

                tdActions.append(editButton, deleteButton);
                tr.append(tdTitle, tdTitleRus, tdYear, tdActions);
                tbody.append(tr);
            });
        })
        .catch(error => console.error('Error fetching series:', error));
}

function deleteSeries(id) {
    if (!confirm('Вы точно хотите удалить сериал?')) return;

    fetch(`/lab7/rest-api/series/${id}`, { method: 'DELETE' })
        .then(response => {
            if (!response.ok) throw new Error('Ошибка при удалении сериала');
            FillSeriesList();
        })
        .catch(error => console.error('Error deleting series:', error));
}

function showModal() {
    document.querySelector('.modal').style.display = 'block';
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    document.getElementById('description-error').textContent = ''; // Очистка ошибки
}

function hideModal() {
    document.querySelector('.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

function addSeries() {
    showModal();
}

function sendSeries() {
    const id = document.getElementById('id').value;
    const descriptionField = document.getElementById('description');
    const descriptionError = document.getElementById('description-error');

    const series = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: document.getElementById('year').value,
        description: descriptionField.value.trim(),
    };

    if (!series.description) {
        descriptionError.textContent = 'Описание сериала обязательно для заполнения!';
        descriptionField.style.border = '2px solid red';
        return;
    }

    descriptionError.textContent = '';
    descriptionField.style.border = '';

    const url = id ? `/lab7/rest-api/series/${id}` : '/lab7/rest-api/series/';
    const method = id ? 'PUT' : 'POST';

    fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(series),
    })
        .then(response => {
            if (!response.ok) throw new Error('Ошибка при добавлении/редактировании сериала');
            FillSeriesList();
            hideModal();
        })
        .catch(error => {
            console.error('Error sending series:', error);
            alert('Не удалось выполнить действие. Попробуйте снова.');
        });
}

function editSeries(series) {
    showModal();
    document.getElementById('id').value = series.id;
    document.getElementById('title').value = series.title;
    document.getElementById('title-ru').value = series.title_ru;
    document.getElementById('year').value = series.year;
    document.getElementById('description').value = series.description;
}
