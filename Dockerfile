FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
RUN mkdir -p /app/static /app/data
COPY index.html /app/static/index.html
COPY style.css /app/static/style.css
COPY app.js /app/static/app.js
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
