FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["bash", "scripts/run_all.sh"]
