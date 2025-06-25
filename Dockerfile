FROM python:3.10-slim

RUN apt-get update && apt-get install -y libgl1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["flask", "run", "--host=0.0.0.0", "--port=9000"]