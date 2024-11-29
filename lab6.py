# lab6.py
from flask import Blueprint, render_template, request, session

lab6 = Blueprint('lab6', __name__)

# Список офисов
offices = []
for i in range(1, 11):
    offices.append({"number": i, "tenant": "", "price": 1000 + (i % 2)})

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rps-api', methods=['POST'])
def api():
    data = request.json
    id = data.get('id')

    # Метод info: возвращаем список офисов и общую стоимость аренды
    if data.get('method') == 'info':
        # Подсчитываем общую стоимость аренды
        total_rent = sum(office['price'] for office in offices if office['tenant'])
        return {
            'jsonrpc': '2.0',
            'result': {
                'offices': offices,
                'total_rent': total_rent
            },
            'id': id
        }

    # Проверяем авторизацию
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        }

    # Метод booking: бронирование офиса
    if data.get('method') == 'booking':
        office_number = data.get('params')
        for office in offices:
            if office['number'] == office_number:
                if office['tenant']:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': 'Already booked'
                        },
                        'id': id
                    }
                office['tenant'] = login
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }

    # Метод cancelation: снятие аренды
    if data.get('method') == 'cancelation':
        office_number = data.get('params')
        for office in offices:
            if office['number'] == office_number:
                if not office['tenant']:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': 'Office is not booked'
                        },
                        'id': id
                    }
                if office['tenant'] != login:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 3,
                            'message': 'You cannot cancel someone else\'s booking'
                        },
                        'id': id
                    }
                office['tenant'] = ''
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }

    # Если метод не найден
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }