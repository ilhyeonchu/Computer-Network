FROM debian:bullseye
WORKDIR /app
COPY ./main.py /app
RUN apt-get update && apt-get install -y --no-install-recommends tcpdump curl openssl libssl-dev python3 python3-venv python3-pip certbot python3-certbot-nginx python3-certbot-apache
RUN pip install fastapi uvicorn
CMD ["sleep", "infinity"]
