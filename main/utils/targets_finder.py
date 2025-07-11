import json

import requests

class TargetsFinder:

    @staticmethod
    def get_targets_from_json() -> dict:
        with open("targets.json", "r") as file:
            json_text = file.read()
        return json.loads(json_text)

    @staticmethod
    def get_targets_from_github() -> dict:
        url = "https://raw.githubusercontent.com/MrBrain-YT/AntiBlock/refs/heads/main/main/targets.json"
        try:
            json_text = requests.get(url).text
            return json.loads(json_text)
        except:
            return {}