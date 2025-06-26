FROM --platform=linux/amd64 python:3.10-slim
RUN apt-get update && apt-get install -y libgl1 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --prefer-binary --default-timeout=300 --no-cache-dir -r requirements.txt

# Copy the pre-downloaded ONNX model to the expected path
COPY u2net.onnx /root/.u2net/u2net.onnx

COPY . .

EXPOSE 9000
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT:-9000} --timeout 600 --workers 1"]