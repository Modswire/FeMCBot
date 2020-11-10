from json import load

def get_token(token):
    with open("bot-settings/token.json", "r") as f:
        data = load(f)
    return data[token]