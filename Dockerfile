FROM python:3.10
WORKDIR /discord_bot
COPY requirements.txt /discord_bot/
RUN pip3 install -r requirements.txt
COPY . /discord_bot
CMD python3 bot.py