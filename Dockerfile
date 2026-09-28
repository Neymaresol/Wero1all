FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY static ./static
RUN mkdir -p /app/data
ENV DB_PATH=/app/data/wero1.db WERO_MODE=production
EXPOSE 10000
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","10000"]
