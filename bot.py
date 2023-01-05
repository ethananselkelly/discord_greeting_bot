import os
import requests
import json
import random
import discord
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
# channel_id must be int for client.get_channel()
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
CHANNEL_NAME = os.getenv('CHANNEL_NAME')
TENOR_API = os.getenv('TENOR_API_KEY')
TENOR_CLIENT = os.getenv('TENOR_API_CLIENT')
BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')


def main():
    run_bot()


def run_bot():

    intents = discord.Intents.default()
    # have to toggle 'message content intent' in Bot settings on Discord dev portal
    intents.message_content = True
    # need intents.members = True for on_member_join
    intents.members = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        guild = discord.utils.get(client.guilds, name=GUILD)

        print(
            f'{client.user} has connected to Discord Server:\n'
            f'{guild.name} (id: {guild.id})\n'
            # f'{guild.channels}'
        )

        return guild

    @client.event
    async def on_member_join(member):
        print('new channel member!')
        channel = client.get_channel(CHANNEL_ID)
        gif = await get_gif(TENOR_API, TENOR_CLIENT)
        await channel.send(gif)

    @client.event
    async def on_message(message):
        username = str(message.author).split('#')[0]
        user_message = str(message.content)

        if message.author == client.user:
            return

        if message.channel.name == CHANNEL_NAME:
            if 'hello' in user_message.lower():
                await message.channel.send(f'Hello {username}')
            elif user_message.lower().startswith('!greetings'):
                gif = await get_gif(TENOR_API, TENOR_CLIENT)
                await message.channel.send(gif)
            elif user_message.lower().startswith('!quote'):
                await message.channel.send(get_random_tweet(get_tweet(bearer_oauth)))

    client.run(TOKEN)


async def get_gif(api, client):
    r = requests.get(
        f"https://tenor.googleapis.com/v2/search?q={get_gif_params()}&key={api}&client_key={client}&limit=1"
    )

    if r.status_code == 200:
        gif = json.loads(r.content)[
            'results'][0]["media_formats"]["mediumgif"]['url']
        return gif


def get_gif_params():
    search_terms = [
        'simpsons eyebrows',
        'simpsons flanders hi diddly ho',
        'simpsons hi',
        'simpsons hi homer',
        'simpsons barney yoo hoo',
        'simpsons hi everybody',
        'simpsons ahoy',
        'simpsons join us',
        'simpsons uncle moe',
        'simpsons duffman',
        'simpsons super nintendo chalmers',

    ]
    return random.choice(search_terms)

# TWITTER API STUFF


def random_date():
    # RFC3339 date-time format for end_date of retrieved tweets
    # Seems that request will return 0 results (status 200) if date is before 2020. Don't know why that is...
    year = random.randrange(2020, 2022)
    month = f'{random.randrange(1, 12):02d}'
    if month == 2:
        day = f'{random.randrange(1, 28):02d}'
    elif month == 4 or 6 or 9 or 11:
        day = f'{random.randrange(1, 30):02d}'
    else:
        day = f'{random.randrange(1, 31):02d}'
    return (str(year) + '-' + str(month) + '-' + str(day) + 'T00:00:00Z')


def bearer_oauth(r):
    r.headers['Authorization'] = f'Bearer {BEARER_TOKEN}'
    r.headers['User-Agent'] = 'v2UserTweetsPython'
    return r


def get_tweet(bearer):
    params = {
        'max_results': 10,
        'end_time': random_date(),
        'exclude': 'retweets',
    }
    r = requests.get('https://api.twitter.com/2/users/1094922224/tweets',
                     auth=bearer, params=params)
    if r.status_code != 200:
        raise Exception(r.status_code, r.text)
    return r.json()


def get_random_tweet(tweets):
    try:
        tweet_id = random.choice(tweets['data'])['id']
        return f'https://fxtwitter.com/twitter/status/{tweet_id}'
    except KeyError:
        return KeyError


if __name__ == "__main__":
    main()
