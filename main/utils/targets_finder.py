import json
import os

import requests

class TargetsFinder:

    @staticmethod
    def get_targets_from_json(base_path) -> dict:
        json_path = os.path.join(base_path, "targets.json")
        with open(json_path, "r") as file:
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