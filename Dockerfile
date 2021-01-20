FROM python:3.6

RUN mkdir -p /bot
WORKDIR /bot

COPY . /bot
RUN pip install -r requirements.txt

CMD ["python", "bot.py"]