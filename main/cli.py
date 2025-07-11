import json
import random
import keyboard
import os
import ast
from datetime import datetime, timedelta

from utils.request_sender import RequestSender
from utils.targets_finder import TargetsFinder

base_path = os.path.dirname(os.path.abspath(__file__))
targets = TargetsFinder.get_targets_from_json(base_path)

targets_request = {}
for name, url in targets.items():
    targets_request[name] = RequestSender(url)
    

def requests_cycle():
    old = datetime.now()
    new_timer = 0
    all_requests_count = 0
    success_requests_count = 0

    while True:
        now = datetime.now()
        if old + timedelta(0,int(new_timer)) < now:
            # get targets list
            new_targets = os.environ.get("targets")
            if new_targets is not None:
                targets.clear()
                targets.update(ast.literal_eval(new_targets))
            # send requests
            error = False
            os.system('cls' if os.name == 'nt' else 'clear')
            for name, url in targets.items():
                if targets_request[name].send() != 200:
                    print(f"[{name}] Error in pakcage for {url}")
                    error = True
                else:
                    print(f"[{name}] Good send pakcage for {url}")
            if not error:
                success_requests_count += 1
            all_requests_count += 1
            print(f"Requests without errors: {success_requests_count}/{all_requests_count}")
            
            # work with timer
            old = datetime.now()
            new_timer = 60 * round(random.uniform(1, 2), 1)
        else:
            if __name__ == "__main__":
                if keyboard.is_pressed("ctrl+c"):
                    break
            if bool(os.environ.get("stop")) == True:
                break
            
if __name__ == "__main__":
    requests_cycle()