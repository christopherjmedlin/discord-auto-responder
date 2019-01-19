#!/usr/bin/env python3.6

from discord import Client
from discord.errors import LoginFailure
import asyncio
import configparser
from getpass import getpass
import os
import json

client = Client()
message_map = {}
default_message = "¯\_(ツ)_/¯"

@client.event
async def on_ready():
    print('\033[92m\nLogged in as\033[92m\n\033[95m------\033[0m')
    print(client.user.name)
    print(client.user.id)
    print('\033[95m------\033[0m')


@client.event
async def on_message(message):
    mentioned = client.user.mentioned_in(message)
    if (message.channel.is_private and message.author.id != client.user.id) or mentioned:
        response = message_map.get(str(message.author.id), default_message)
        await client.send_message(message.channel, response)
 

if __name__ == "__main__":
    config = {"config": {}}
    if os.path.isfile('config.json'):
        config = json.load(open('config.json'))
    
    groups = config.get("groups", [])
    for group in groups:
        for num in group["ids"]:
            message_map[str(num)] = group["message"]
    
    email = config.get("email")
    if not email:
        email = input("Email: ")
    password = config.get("password")
    if not password:
        password = getpass()
    default_message = config.get("default_message")
    if not email:
        default_message = input("Default Message: ")

    try:
        client.run(email, password)
    except LoginFailure:
        print("\033[91mInvalid login.\033[0m")
