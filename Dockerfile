FROM python:3.8

LABEL dev="Rohan Purekar"

COPY techtrends /app

WORKDIR  /app

RUN pip install -r requirements.txt && python3 init_db.py

EXPOSE 3111

CMD ["python3", "app.py"]