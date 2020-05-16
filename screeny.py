import gui
import itertools, glob
import os
from PIL import ImageGrab, Image
import requests
import json
from pynput.keyboard import Key, Controller
import shutil
import pytesseract
from ctypes import windll
import time
import webbrowser
from base64 import b64encode
import pyperclip

keyboard = Controller()

appdata = os.getenv('APPDATA')

if not os.path.exists(appdata + "\Screeny"):
    os.mkdir(appdata + "\Screeny")
if not os.path.exists(appdata + "\Screeny\icon.ico"):
    shutil.copyfile("icon.ico", appdata + "\Screeny\icon.ico")
settings = open(appdata + "\Screeny\settings.ini", "w+")
icon = open(appdata + "\Screeny\icon.ico")

icons = itertools.cycle(glob.glob('*.ico'))
hover_text = "SCREENY - Screenshot Assistant\n\nUse Win+Shift+S to use default mode\nRight click for all modes"

def hello(sysTrayIcon):
    pass
    
def close(sysTrayIcon): 
    os.remove("image.png")

def clearClip():
    if windll.user32.OpenClipboard(None):
        windll.user32.EmptyClipboard()
        windll.user32.CloseClipboard()

def runSS(sysTrayIcon):
    keyboard.press(Key.cmd)
    keyboard.press(Key.shift_l)
    keyboard.press('s')
    keyboard.release('s')
    keyboard.release(Key.shift_l)
    keyboard.release(Key.cmd)


def ocrSave(sysTrayIcon):
    clearClip()
    time.sleep(0.2)
    image = ImageGrab.grabclipboard()
    runSS(None)
    print("Loading: ", end="")
    while image is None:
        print(".", end="")
        image = ImageGrab.grabclipboard()
        time.sleep(0.1)
    print("\nDone")
    print("\nText:")
    image.save("image.png")
    var = pytesseract.image_to_string(Image.open('image.png'))
    print(var)
    pyperclip.copy(var)
    print("\n\n")
    
def ocrSearch(sysTrayIcon):
    clearClip()
    time.sleep(0.2)
    image = ImageGrab.grabclipboard()
    runSS(None)
    print("Loading: ", end="")
    while image is None:
        print(".", end="")
        image = ImageGrab.grabclipboard()
        time.sleep(0.1)
    print("\nDone")
    print("\nText:")
    image.save("image.png")
    var = pytesseract.image_to_string(Image.open('image.png'))
    print(var)
    print("\n\n")
    query = var.replace(" ", "+")
    webbrowser.open("http://www.google.co.uk/search?q="+query)
    
def imgUpload(sysTrayIcon):
    clearClip()
    time.sleep(0.2)
    image = ImageGrab.grabclipboard()
    runSS(None)
    print("Loading: ", end="")
    while image is None:
        print(".", end="")
        image = ImageGrab.grabclipboard()
        time.sleep(0.1)
    print("\nDone")
    image.save("image.png")
    headers = {"Authorization": "Client-ID b7cdb801d615f30"}
    j1 = requests.post(
        "https://api.imgur.com/3/image",
        headers = headers,
        data = {'image': b64encode(open('image.png', 'rb').read()),'type': 'base64',})
    data = json.loads(j1.text)['data']
    if "link" not in data:
        print("Error")
        return False
    webbrowser.open(data["link"])

    
def imgSearch(sysTrayIcon):
    clearClip()
    time.sleep(0.2)
    image = ImageGrab.grabclipboard()
    runSS(None)
    print("Loading: ", end="")
    while image is None:
        print(".", end="")
        image = ImageGrab.grabclipboard()
        time.sleep(0.1)
    print("\nDone")
    image.save("image.png")
    filePath = os.path.abspath("image.png")
    multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
    response = requests.post('http://www.google.co.uk/searchbyimage/upload', files=multipart, allow_redirects=False)
    fetchUrl = response.headers['Location']
    webbrowser.open(fetchUrl)

menu_options = (
    ('Screenshot', None, runSS),
    ('--------------', None, hello),
    ('Text Copy', None, ocrSave),
    ('Text Search', None, ocrSearch),
    ('--------------', None, hello),
    ('Imgur Uplaod', None, imgUpload),
    ('Image Search', None, imgSearch),
    ('--------------', None, hello))

print("\n"*60)
clearClip()
gui.SysTrayIcon(next(icons), hover_text, menu_options, on_quit=close, default_menu_index=1)