FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
RUN mkdir -p /app/static /app/data
COPY index.html /app/static/index.html
COPY style.css /app/static/style.css
ENV DB_PATH=/app/data/wero1.db
ENV WERO_MODE=production
EXPOSE 10000
CMD ["sh","-c","uvicorn main:app --host 0.0.0.0 --port ${PORT:-10000}"]
