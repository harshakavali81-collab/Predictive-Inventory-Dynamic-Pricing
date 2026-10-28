# Local demonstration container, not a hardened public commerce system.
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ src/
COPY backend/ backend/
COPY scripts/ scripts/
COPY frontend/ frontend/
COPY sql/ sql/
COPY data/ data/
RUN mkdir -p data/generated && python -m scripts.run_pipeline
RUN useradd --create-home --uid 10001 inventoryiq && chown -R inventoryiq:inventoryiq /app
USER inventoryiq
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD python -c "from urllib.request import urlopen; assert urlopen('http://127.0.0.1:8000/api/health', timeout=3).status==200"
CMD ["python","-m","uvicorn","backend.app.main:app","--host","0.0.0.0","--port","8000","--workers","1"]
