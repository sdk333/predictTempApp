import streamlit as st
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from geopy.geocoders import Nominatim

# Заголовок приложения
st.title("Прогнозирование температуры")

# Загрузка модели
model = load_model('65epoch_lstm_model.keras')

# Функция для подготовки входных данных
def prepare_input(latitude, longitude, elevation, date):
    date = pd.to_datetime(date)
    month = date.month
    day_of_year = date.dayofyear
    day_of_week = date.dayofweek

    input_data = np.array([[latitude, longitude, elevation, month, day_of_year, day_of_week, 0, 0]])
    input_data = np.tile(input_data, (30, 1))  # Повторяем данные 30 раз
    input_data = input_data.reshape(1, 30, 8)  # Добавляем размерность для батча
    return input_data

# Переключатель между вводом координат и поиском по месту
input_method = st.radio(
    "Выберите способ ввода:",
    options=["Ввод координат вручную", "Поиск по названию места"]
)

# Инициализация переменных
latitude, longitude = None, None

# Ввод координат вручную
if input_method == "Ввод координат вручную":
    st.write("Введите координаты вручную:")
    latitude = st.number_input("Широта", value=0.0)
    longitude = st.number_input("Долгота", value=0.0)

# Поиск по названию места
else:
    st.write("Введите название места (например, Атланта):")
    location_name = st.text_input("Название места:")

    if location_name:
        geolocator = Nominatim(user_agent="streamlit_app")
        location = geolocator.geocode(location_name)
        if location:
            st.success(f"Место найдено: {location.address}")
            latitude = location.latitude
            longitude = location.longitude
            st.write(f"Координаты:")
            st.write(f"Широта = {latitude}")
            st.write(f"Долгота = {longitude}")
        else:
            st.error("Место не найдено. Пожалуйста, уточните запрос.")

# Остальные поля
elevation = st.number_input("Высота над уровнем моря", value=150)
date = st.date_input("Дата")

# Кнопка для прогнозирования
if st.button("Прогнозировать температуру"):
    if latitude is not None and longitude is not None:
        # Подготавливаем входные данные
        input_data = prepare_input(latitude, longitude, elevation, date)

        # Прогнозируем
        prediction = model.predict(input_data)

        # Выводим результат
        st.success(f"Максимальная температура (TMAX): {prediction[0][0]:.2f}°F")
        st.success(f"Минимальная температура (TMIN): {prediction[0][1]:.2f}°F")
    else:
        st.error("Пожалуйста, введите корректные координаты или название места.")