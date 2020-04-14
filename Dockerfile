FROM python:3.7

WORKDIR /service
COPY ./converter /service

EXPOSE 8000

CMD python3 main.py