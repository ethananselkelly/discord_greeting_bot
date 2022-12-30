import os
import requests
import json
import random
import discord
from dotenv import load_dotenv


def main():
    run_bot()


def run_bot():
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD = os.getenv('DISCORD_GUILD')
    # channel_id must be int for client.get_channel()
    CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
    CHANNEL_NAME = os.getenv('CHANNEL_NAME')
    TENOR_API = os.getenv('TENOR_API_KEY')
    TENOR_CLIENT = os.getenv('TENOR_API_CLIENT')

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
            if user_message.lower() == 'hello':
                await message.channel.send(f'Hello {username}')
            elif user_message.lower() == 'greetings':
                gif = await get_gif(TENOR_API, TENOR_CLIENT)
                await message.channel.send(gif)
            elif user_message.lower() == 'quote':
                await message.channel.send(get_quote())

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


def get_quote():
    r = requests.get('https://thesimpsonsquoteapi.glitch.me/quotes').json()
    return f"{r[0]['quote']} - {r[0]['character']}"


if __name__ == "__main__":
    main()
