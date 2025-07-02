FROM python:3.10-slim

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x boot.sh
ENV FLASK_APP=microblog.py

# 如果用 Babel 翻译
RUN flask translate compile

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
