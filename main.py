import discord
from dotenv import load_dotenv
import os
import psycopg2
load_dotenv()

database_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(
    # password=database_url.split(':')[2].split('@')[0],
    # database_url=database_url.split('/')[3],
    database_url
)


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message: discord.Message):
        #print channel name and message content
        content = message.content
        author_id = message.author.id
        author_name = message.author.name
        message_id = message.id
        date = message.created_at
        channel_id = message.channel.id
        channel = message.channel.name

        #save message to database
        cur = conn.cursor()
        cur.execute("INSERT INTO messages (message_id, author_id, author_name, channel_id, channel, content, date) VALUES (%s, %s, %s, %s, %s, %s, %s)", (message_id, author_id, author_name, channel_id, channel, content, date))
        conn.commit()
        cur.close()



intents = discord.Intents.default()
intents.message_content = True


token = os.getenv('TOKEN')


client = MyClient(intents=intents)
client.run(token)