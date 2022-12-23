import os
import requests
import json
import asyncio
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
    CHANNEL = int(os.getenv('CHANNEL_ID'))

    intents = discord.Intents.default()
    # have to toggle 'message content intent' in Bot settings on Discord dev portal
    intents.message_content = True
    intents.members = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        # for guild in client.guilds:
        #     if guild.name == GUILD:
        #         break
        # this does the same as the above code block:
        guild = discord.utils.get(client.guilds, name=GUILD)

        print(
            f'{client.user} has connected to Discord Server:\n'
            f'{guild.name} (id: {guild.id})\n'
        )

        return guild

    # need intents.members = True
    @client.event
    async def on_member_join(member):
        print('new channel member!')
        channel = client.get_channel(CHANNEL)
        await channel.send(
            get_gif()
        )

    @client.event
    async def on_message(message):
        username = str(message.author).split('#')[0]
        user_message = str(message.content)
        channel = str(message.channel.name)

        if message.author == client.user:
            return

        if message.channel.name == 'general':
            if user_message.lower() == 'hello':
                await message.channel.send(f'Hello {username}')
                return
            elif user_message.lower() == 'greetings':
                gif = get_gif()
                await message.channel.send(gif)

    client.run(TOKEN)


def get_gif():
    api_key = os.getenv('TENOR_API_KEY')
    limit = 5
    client_key = os.getenv('TENOR_API_CLIENT')
    search_term, index_choice = get_gif_params()

    r = requests.get(
        f"https://tenor.googleapis.com/v2/search?q={search_term}&key={api_key}&client_key={client_key}&limit={limit}"
    )
    if r.status_code == 200:
        return json.loads(r.content)['results'][index_choice]["media_formats"]["mediumgif"]['url']


def get_gif_params():
    search_terms = ['welcome', 'greetings', 'hi', 'sup',
                    'hello there obi wan', 'hey', 'howdy', 'hi simpsons', 'hi seinfeld', 'hi spongebob']
    return random.choice(search_terms), random.randint(0, 4)


if __name__ == "__main__":
    main()
