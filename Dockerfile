FROM python:3.7

WORKDIR /api

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0", "--workers", "4", "--log-file", "-"]
