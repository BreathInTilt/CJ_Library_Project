# Используем официальный Python образ как базу
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Пробрасываем порт
EXPOSE 5000

# Команда запуска Flask-приложения
CMD ["python", "app.py"]
