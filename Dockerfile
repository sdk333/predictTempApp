# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Открываем порты для Flask и Streamlit
EXPOSE 5000 8501

# Команда для запуска Flask и Streamlit
CMD streamlit run streamlit_app.py --server.port 8501 & python app.py