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


                let tdTitleRus = document.createElement('td');
                tdTitleRus.innerText = seriesItem.title_ru || 'N/A';

                let tdTitle = document.createElement('td');
                tdTitle.classList.add('italic'); 
                tdTitle.innerHTML = seriesItem.title
                    ? `(${seriesItem.title})` 
                    : '(N/A)'; 

    
                let tdYear = document.createElement('td');
                tdYear.innerText = seriesItem.year || 'N/A';

              
                let tdActions = document.createElement('td');
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

                tr.append(tdTitleRus, tdTitle, tdYear, tdActions);
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
    document.getElementById('description-error').textContent = ''; 
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

    const url = id ? `/lab7/rest-api/series/${id}` : '/lab7/rest-api/series/';
    const method = id ? 'PUT' : 'POST';

    fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(series),
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => {
                    throw new Error(
                        err.errors ? err.errors.join("; ") : "Не удалось выполнить действие"
                    );
                });
            }
            return response.json();
        })
        .then(() => {
            FillSeriesList();
            hideModal();
        })
        .catch(error => {
            descriptionError.textContent = error.message; // Отображаем ошибку в интерфейсе
            descriptionField.style.border = '2px solid red';
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
