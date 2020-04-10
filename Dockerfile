FROM python:3.7

WORKDIR /api
COPY start.sh ./
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["./start.sh"]
