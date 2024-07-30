FROM python:3.9.13

ENV PYTHONUNBUFFERED=1

WORKDIR src

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "src/main.py"]