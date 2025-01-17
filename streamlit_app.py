import streamlit as st
import requests
from geopy.geocoders import Nominatim

# Заголовок приложения
st.title("Прогнозирование температуры")

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
    latitude = st.number_input("Широта", value=0)
    longitude = st.number_input("Долгота", value=0)

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

# Кнопка для отправки запроса
if st.button("Прогнозировать температуру"):
    # Формируем данные для запроса
    data = {
        'latitude': latitude,
        'longitude': longitude,
        'elevation': elevation,
        'date': date.strftime('%Y-%m-%d')  # Преобразуем дату в строку
    }

    # URL вашего Flask-приложения
    url = 'http://localhost:5000/predict'

    # Отправка POST-запроса
    response = requests.post(url, json=data)

    # Проверка статуса ответа
    if response.status_code == 200:
        result = response.json()
        st.success(f"Максимальная температура (TMAX): {result['TMAX']}°F")
        st.success(f"Минимальная температура (TMIN): {result['TMIN']}°F")
    else:
        st.error(f"Ошибка: {response.status_code}, {response.text}")