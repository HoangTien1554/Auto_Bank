import json
import os

CONFIG_PATH = "data/config.json"

def load_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4, ensure_ascii=False)

def update_config(key, value):
    config = load_config()
    config[key] = value
    save_config(config)