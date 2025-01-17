from flask import Flask, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
import pandas as pd

# Загрузка модели
model = load_model('65epoch_lstm_model.keras')

# Создание Flask-приложения
app = Flask(__name__)

# Функция для подготовки входных данных
def prepare_input(latitude, longitude, elevation, date):
    # Преобразуем дату в признаки
    date = pd.to_datetime(date)
    month = date.month
    day_of_year = date.dayofyear
    day_of_week = date.dayofweek

    # Создаём массив признаков (здесь предполагаем, что у вас 8 признаков)
    input_data = np.array([[latitude, longitude, elevation, month, day_of_year, day_of_week, 0, 0]])
    
    # Добавляем фиктивные данные для 30 временных шагов
    input_data = np.tile(input_data, (30, 1))  # Повторяем данные 30 раз

    # Изменяем форму на (1, 30, 8)
    input_data = input_data.reshape(1, 30, 8)  # Добавляем размерность для батча

    return input_data


# Маршрут для прогнозирования
@app.route('/predict', methods=['POST'])
def predict():
    # Получаем данные из запроса
    data = request.json
    latitude = data['latitude']
    longitude = data['longitude']
    elevation = data['elevation']
    date = data['date']

    # Подготавливаем входные данные
    input_data = prepare_input(latitude, longitude, elevation, date)

    # Прогнозируем
    prediction = model.predict(input_data)

    # Возвращаем результат
    return jsonify({
        'TMAX': float(prediction[0][0]),
        'TMIN': float(prediction[0][1])
    })

# Запуск сервера
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)