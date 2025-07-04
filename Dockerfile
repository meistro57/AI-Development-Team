FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV WORK_DIR=/app/projects
ENV FRONTEND_PORT=5000
CMD ["python", "web_frontend.py"]
