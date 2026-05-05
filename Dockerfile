FROM python:3.12-slim

# Рабочая директория — именно сюда мы скопируем код
WORKDIR /app

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код приложения (импорты from db.engine и т.д. будут работать)
COPY app/ .

# Открываем порт
EXPOSE 8000

# Запуск (именно "main:app", потому что мы находимся внутри /app)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]