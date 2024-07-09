FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR src

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "src/main.py"]