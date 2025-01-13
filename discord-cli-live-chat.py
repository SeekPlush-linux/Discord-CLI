import time
import requests
import os

token = open("token.txt", "r")
BOT_TOKEN = token.read()
BASE_URL = "https://discord.com/api/v9"

HEADERS = {
    "Authorization": BOT_TOKEN,
    "Content-Type": "application/json"
}

def get_channel_messages(channel_id):
    url = f"{BASE_URL}/channels/{channel_id}/messages"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get messages. Status code: {response.status_code}")
        input()
        return []

def get_guilds():
    response = requests.get(f"{BASE_URL}/users/@me/guilds", headers=HEADERS)
    os.system('clear')
    num = 0
    if response.status_code == 200:
        guilds = response.json()
        print("Your servers:")
        for guild in guilds:
            print(f" {num}: {guild['name']}")
            num = num + 1
        return guilds
    else:
        print(f"Failed to retrieve guilds: {response.status_code} - {response.text}")
        time.sleep(1)
        print("Press Enter to continue.")
        input()
        return None

def get_channels(guild_id, guild_name):
    response = requests.get(f"{BASE_URL}/guilds/{guild_id}/channels", headers=HEADERS)
    os.system('clear')
    num = 0
    if response.status_code == 200:
        channels = response.json()
        print(f"Channels in server \"{guild_name}\":")
        for channel in channels:
            if channel['type'] == 0:
                print(f" {num}: # {channel['name']}")
            if channel['type'] == 2:
                print(f" {num}: [loud_sound] {channel['name']}")
            if channel['type'] == 4:
                print(f"> {channel['name']}")
            if channel['type'] == 5:
                print(f" {num}: [loudspeaker] {channel['name']}")
            if channel['type'] == 13:
                print(f" {num}: [studio_microphone] {channel['name']}")
            if channel['type'] == 15:
                print(f" {num}: [left_speech_bubble] {channel['name']}")
            num = num + 1
        return channels
    else:
        print(f"Failed to retrieve channels: {response.status_code} - {response.text}")
        time.sleep(1)
        print("Press Enter to continue.")
        input()

def discord_cli_live_chat():
    try:
        os.system('clear')
        print("Welcome to Discord CLI Live Chat!\n\nRemember, this python script is only for reading the selected channel\nin real-time, not for chatting and other stuff.\n")
        print("To exit the program at any time, press Ctrl+C.")
        print("Press Enter to continue.")
        input()
        guilds = get_guilds()
        if guilds:
            num = int(input("\u001b[36;1mEnter the number of the server to check: \u001b[0m"))
            guild_id = guilds[num]['id']
            if any(guild['id'] == guild_id for guild in guilds):
                channels = get_channels(guild_id, guilds[num]['name'])
            else:
                print("Invalid guild ID.")
                time.sleep(1)
                print("Press Enter to continue.")
                input()
            num = int(input("\u001b[36;1mEnter the number of the channel to check: \u001b[0m"))
            channel_id = channels[num]['id']
        method = int(input("\u001b[36;1mEnter the method to use (1 for single-updating, 2 for full-updating): \u001b[0m"))
        messages = get_channel_messages(channel_id)
        os.system('clear')
        last_message = messages[0]['content']
        for i in range(0, 10):
            num = 9-i
            if messages[num]['author']['global_name'] == None:
                if messages[num]['type'] == 19:
                    if messages[num]['referenced_message']['author']['global_name'] == None:
                        print(f"\u001b[0m\u001b[37m┌──({messages[num]['referenced_message']['author']['username']}: {messages[num]['referenced_message']['content']})\u001b[37;1m\n{messages[num]['author']['username']}: {messages[num]['content']}\n")
                    else:
                        print(f"\u001b[0m\u001b[37m┌──({messages[num]['referenced_message']['author']['global_name']}: {messages[num]['referenced_message']['content']})\u001b[37;1m\n{messages[num]['author']['username']}: {messages[num]['content']}\n")
                else:
                    print(f"\u001b[37;1m{messages[num]['author']['username']}: {messages[num]['content']}\n")
            else:
                if messages[num]['type'] == 19:
                    if messages[num]['referenced_message']['author']['global_name'] == None:
                        print(f"\u001b[0m\u001b[37m┌──({messages[num]['referenced_message']['author']['username']}: {messages[num]['referenced_message']['content']})\u001b[37;1m\n{messages[num]['author']['global_name']}: {messages[num]['content']}\n")
                    else:
                        print(f"\u001b[0m\u001b[37m┌──({messages[num]['referenced_message']['author']['global_name']}: {messages[num]['referenced_message']['content']})\u001b[37;1m\n{messages[num]['author']['global_name']}: {messages[num]['content']}\n")
                else:
                    print(f"\u001b[37;1m{messages[num]['author']['global_name']}: {messages[num]['content']}\n")
        time.sleep(5) # change the refresh rate of the chat here (in seconds)
        if method == 1:
            while True:
                messages = get_channel_messages(channel_id)
                if last_message != messages[0]['content']:
                    if messages[0]['author']['global_name'] == None:
                        if messages[0]['type'] == 19:
                            if messages[0]['referenced_message']['author']['global_name'] == None:
                                print(f"\u001b[0m\u001b[37m┌──({messages[0]['referenced_message']['author']['username']}: {messages[0]['referenced_message']['content']})\u001b[37;1m\n{messages[0]['author']['username']}: {messages[0]['content']}\n")
                            else:
                                print(f"\u001b[0m\u001b[37m┌──({messages[0]['referenced_message']['author']['global_name']}: {messages[0]['referenced_message']['content']})\u001b[37;1m\n{messages[0]['author']['username']}: {messages[0]['content']}\n")
                        else:
                            print(f"\u001b[37;1m{messages[0]['author']['username']}: {messages[0]['content']}\n")
                    else:
                        if messages[0]['type'] == 19:
                            if messages[0]['referenced_message']['author']['global_name'] == None:
                                print(f"\u001b[0m\u001b[37m┌──({messages[0]['referenced_message']['author']['username']}: {messages[0]['referenced_message']['content']})\u001b[37;1m\n{messages[0]['author']['global_name']}: {messages[0]['content']}\n")
                            else:
                                print(f"\u001b[0m\u001b[37m┌──({messages[0]['referenced_message']['author']['global_name']}: {messages[0]['referenced_message']['content']})\u001b[37;1m\n{messages[0]['author']['global_name']}: {messages[0]['content']}\n")
                        else:
                            print(f"\u001b[37;1m{messages[0]['author']['global_name']}: {messages[0]['content']}\n")
                last_message = messages[0]['content']
                time.sleep(5) # change the refresh rate of the chat here (in seconds)

        if method == 2:
            while True:
                messages = get_channel_messages(channel_id)
                os.system('clear')
                for i in range(0, 10):
                    num = 9-i
                    if messages[num]['author']['global_name'] == None:
                        if messages[num]['type'] == 19:
                            if messages[num]['referenced_message']['author']['global_name'] == None:
                                print(f"\u001b[0m\u001b[37m┌──({messages[num]['referenced_message']['author']['username']}: {messages[num]['referenced_message']['content']})\u001b[37;1m\n{messages[num]['author']['username']}: {messages[num]['content']}\n")
                            else:
                                print(f"\u001b[0m\u001b[37m┌──({messages[num]['referenced_message']['author']['global_name']}: {messages[num]['referenced_message']['content']})\u001b[37;1m\n{messages[num]['author']['username']}: {messages[num]['content']}\n")
                        else:
                            print(f"\u001b[37;1m{messages[num]['author']['username']}: {messages[num]['content']}\n")
                    else:
                        if messages[num]['type'] == 19:
                            if messages[num]['referenced_message']['author']['global_name'] == None:
                                print(f"\u001b[0m\u001b[37m┌──({messages[num]['referenced_message']['author']['username']}: {messages[num]['referenced_message']['content']})\u001b[37;1m\n{messages[num]['author']['global_name']}: {messages[num]['content']}\n")
                            else:
                                print(f"\u001b[0m\u001b[37m┌──({messages[num]['referenced_message']['author']['global_name']}: {messages[num]['referenced_message']['content']})\u001b[37;1m\n{messages[num]['author']['global_name']}: {messages[num]['content']}\n")
                        else:
                            print(f"\u001b[37;1m{messages[num]['author']['global_name']}: {messages[num]['content']}\n")
                time.sleep(5) # change the refresh rate of the chat here (in seconds)
    except KeyboardInterrupt:
        print("\nExiting program...")
        time.sleep(1)
        return 0

discord_cli_live_chat()