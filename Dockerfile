FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "-m", "waitress", "--host=0.0.0.0", "--port=8000", "app:app"]