from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, PartialEmoji

# STEP 0: LOAD OUR TOKEN FROM SOMEWHERE SAFE
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# ALLOWED CHANNELS: comma-separated channel IDs, e.g. "123456789,987654321"
# If empty or not set, the bot will react in ALL channels
_raw_channels = os.getenv('ALLOWED_CHANNEL_IDS', '')
ALLOWED_CHANNEL_IDS: list[int] = [
    int(cid.strip()) for cid in _raw_channels.split(',') if cid.strip()
]

# REACTION EMOJIS
REACTION_EMOJIS = [
    PartialEmoji(name='058', id=1493314458230063164, animated=True),
    PartialEmoji(name='061', id=1493314460633530528, animated=True),
]

# STEP 1: BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client: Client = Client(intents=intents)


# STEP 2: HANDLING THE STARTUP FOR OUR BOT
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')


# STEP 3: HANDLING INCOMING MESSAGES
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    # If a channel whitelist is configured, ignore other channels
    if ALLOWED_CHANNEL_IDS and message.channel.id not in ALLOWED_CHANNEL_IDS:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')

    for emoji in REACTION_EMOJIS:
        try:
            await message.add_reaction(emoji)
            print(f'Reacted with {emoji} successfully')
        except Exception as e:
            print(f'Failed to react with {emoji}: {e}')


# STEP 4: MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()
