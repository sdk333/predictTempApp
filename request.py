import requests

# URL вашего Flask-приложения
url = 'http://localhost:5000/predict'

# Данные для запроса
data = {
    'latitude': 42.3584,   # Пример: широта для Москвы
    'longitude': -71.0598,  # Пример: долгота для Москвы
    'elevation': 150,      # Пример: высота над уровнем моря
    'date': '2022-02-01'   # Пример: дата в формате YYYY-MM-DD
}

# Отправка POST-запроса
response = requests.post(url, json=data)

# Проверка статуса ответа
if response.status_code == 200:
    # Получение и вывод предсказанных значений
    result = response.json()
    print(f"TMAX: {result['TMAX']}, TMIN: {result['TMIN']}")
else:
    print(f"Ошибка: {response.status_code}, {response.text}")