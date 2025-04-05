# Базовий образ для Python 3.12
FROM python:3.12-slim

# Встановлюємо Poetry
RUN pip install --no-cache-dir poetry

# Додаємо poetry до PATH (якщо треба)
ENV PATH="/root/.local/bin:$PATH"

# Створюємо директорію для застосунку
WORKDIR /app

# Копіюємо файли проєкту
COPY pyproject.toml poetry.lock ./

# Встановлюємо залежності
RUN poetry install --no-root

# Копіюємо код проєкту
COPY . .

# Вказуємо команду для запуску
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]