# Use the official Playwright Python image as base
FROM mcr.microsoft.com/playwright/python:v1.54.0-noble

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers (they should already be installed in the base image)
# But we'll run this to ensure they're available
RUN playwright install --with-deps

# Copy application code
COPY . .

# Create a non-root user for running the application (recommended for web scraping)
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health', timeout=5)" || exit 1

# Run the application
CMD ["python", "main.py"]
