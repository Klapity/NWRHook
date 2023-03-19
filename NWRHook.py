import dhooks
import term
import os
import requests
import threading
import time
import json

messagesSent = 0

# Classes
class Config():
    webhook = dhooks.Webhook
    wbURL = ""
    exists = False

    def readCFG(self) -> dict:
        try: return eval(open("config.json", "r").read())
        except: return False
    def writeCFG(self, config:dict) -> bool:
        try: open("config.json", "+w").write(str(json.dumps(config, indent=4, sort_keys=True)))
        except Exception: pass

    def __init__(self) -> None:
        cfg = self.readCFG()
        if not cfg: return

        self.webhook = dhooks.Webhook(cfg['userWebhook'])
        self.wbURL = cfg['userWebhook']
        if os.path.exists("config.json"): self.exists = True
        if requests.get(self.wbURL).status_code != 200: self.exists = False

# Functions
def load():
    global config
    config = Config()

# Variables
config = None

# Main
def main():
    term.cls()
    load()
    global messagesSent
    
    if not config.exists:
        print(f"{term.Fore.RED}!{term.Fore.WHITE}){term.Fore.LIGHTRED_EX} Seems like a config with a webhook doesnt exist. Please input a webhook!")
        webhook = term.prompt("Webhook")
        config.writeCFG(config={"userWebhook":webhook})
        config.webhook = dhooks.Webhook(webhook)
        config.wbURL = webhook
    
    while True:
        term.banner()
        chosen = term.printOptions({"Send":"", "Delete":"", "Spam":"", "Info":""})
        if chosen == "1":
            term.banner("Send")
            message = term.prompt("Message")
            config.webhook.send(message)
        if chosen == "2":
            config.webhook.delete()
            term.alert("Deleted!")
            input()
            term.cls()
            load()
    
            if not config.exists:
                print(f"{term.Fore.RED}!{term.Fore.WHITE}){term.Fore.LIGHTRED_EX} Seems like a config with a webhook doesnt exist. Please input a webhook!")
                webhook = term.prompt("Webhook")
                config.writeCFG(config={"userWebhook":webhook})
                config.webhook = dhooks.Webhook(webhook)
                config.wbURL = webhook
        if chosen == "3":
            term.banner("Spam")
            message = term.prompt("Message")
            try: amount = int(term.prompt("Threads"))
            except Exception: amount = 1
            messagesSent = 1
            try:
                print()
                while True:
                    def sendMessage(message):
                        global messagesSent
                        config.webhook.send(message)
                        print(f"{term.Fore.GREEN}!{term.Fore.WHITE}){term.Fore.LIGHTGREEN_EX} Sent Message{term.Fore.WHITE}: {term.Fore.GREEN}{messagesSent}", end="\r")
                        messagesSent+=1
                    for i in range(amount): threading.Thread(target=sendMessage, args=(message, )).start()
                    time.sleep(0.3)
            except: pass
        if chosen == "4":
            term.banner("Info")
            term.printOptions({"Avatar URL": config.webhook.avatar_url, "Channel ID": config.webhook.channel_id, "Default Avatar": config.webhook.default_avatar_url, "Default Name": config.webhook.default_name, "Guild ID": config.webhook.guild_id, "Webhook ID": config.webhook.id, "Token": config.webhook.token, "URL": config.webhook.url, "Username": config.webhook.username}, "")

            input()

try: main()
except: pass