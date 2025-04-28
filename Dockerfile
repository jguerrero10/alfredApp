# Usar imagen oficial de Python
FROM python:3.12-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar dependencias
COPY pyproject.toml poetry.lock README.md .coveragerc ./

# Instalar Poetry
RUN pip install poetry

# Instalar dependencias
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copiar el resto del código
COPY . .

# Exponer el puerto de Django
EXPOSE 8000

# Comando por defecto
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
