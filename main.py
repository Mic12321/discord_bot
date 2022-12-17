# Author Mic12321

import discord


def main():

    client=discord.Client(intents=discord.Intents.default())


    @client.event
    async def on_ready():
        print("Bot is ready")


    # Read the token from token.txt
    client.run(open("token.txt", "r").readline())


if __name__ == "__main__":
    main()
