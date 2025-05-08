FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:$PATH" \
    POETRY_VERSION=2.1.2

# Install pipx and poetry
RUN pip install --no-cache-dir pipx && \
    pipx ensurepath && \
    pipx install poetry==${POETRY_VERSION}

# Set work directory
WORKDIR /app

# Copy only dependency files first (for Docker layer caching)
COPY pyproject.toml poetry.lock ./

# Copy Alembic config and migration scripts
COPY alembic.ini /app/
COPY migrations/ /app/migrations/

# Install dependencies (main only, no dev, no building this package)
RUN poetry config virtualenvs.create false && \
    poetry install --only main,prod --no-root --no-interaction --no-ansi

# Copy application code
COPY ./src ./src

# Set PYTHONPATH
ENV PYTHONPATH=/app/src

# Expose port (optional, helps with clarity and docs)
EXPOSE 8088

# Copy and set entrypoint
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]