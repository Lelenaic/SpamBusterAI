FROM python:3.11-alpine

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt && \
    pip cache purge

CMD ["python", "app.py"]
