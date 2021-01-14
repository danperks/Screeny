from tkinter import filedialog, Tk
from win10toast import ToastNotifier
import gui

import itertools
import glob
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

from system_hotkey import SystemHotkey
hk = SystemHotkey()

toast = ToastNotifier()

root = Tk()
root.withdraw()


keyboard = Controller()

appdata = os.getenv('APPDATA')

if not os.path.exists(appdata + r"\Screeny"):
    os.mkdir(appdata + r"\Screeny")
if not os.path.exists(appdata + r"\Screeny\icon.ico"):
    shutil.copyfile("icon.ico", appdata + r"\Screeny\icon.ico")
settings = open(appdata + r"\Screeny\settings.ini", "w+")
icon = open(appdata + r"\Screeny\icon.ico")

icons = itertools.cycle(glob.glob('*.ico'))
hover_text = "SCREENY - Screenshot Assistant\n\nUse Win+Shift+S to use default mode\nRight click for all modes"


# ----------- GENERAL -------------


def blank(sysTrayIcon):
    pass


def close(sysTrayIcon):
    if os.path.exists("image.png"):
        os.remove("image.png")


def clearClip():
    if windll.user32.OpenClipboard(None):
        windll.user32.EmptyClipboard()
        windll.user32.CloseClipboard()


def getSS(sysTrayIcon):
    keyboard.press(Key.cmd)
    keyboard.press(Key.shift_l)
    keyboard.press('s')
    keyboard.release('s')
    keyboard.release(Key.shift_l)
    keyboard.release(Key.cmd)


def grabSS():
    clearClip()
    time.sleep(0.2)
    image = ImageGrab.grabclipboard()
    getSS(None)
    while image is None:
        image = ImageGrab.grabclipboard()
        time.sleep(0.1)
    return image


def openDir(dir):
    pass


def openLink(link):
    webbrowser.open(link)

# ------------- TOOLS -------------

# -------- OCR TOOLS


def ocrSave(sysTrayIcon):
    image = grabSS()
    image.save("image.png")
    try:
        var = pytesseract.image_to_string(Image.open('image.png'))
    except pytesseract.pytesseract.TesseractNotFoundError:
        toast.show_toast(title="Screeny - Error", msg="You don't have PyTesseract installed properly, make sure you followed the install steps correctly.",
                         icon_path="icon.ico", duration=5, threaded=True)
        var = "ERROR - No PyTesseract - See github.com/danperks/Screeny"
    toast.show_toast(title="Screeny - Text Copied", msg="The screenshotted text has been copied to your clipboard successfully.",
                     icon_path="icon.ico", duration=5, threaded=True)
    pyperclip.copy(var)


def ocrSearch(sysTrayIcon):
    image = grabSS()
    image.save("image.png")
    var = pytesseract.image_to_string(Image.open('image.png'))
    query = var.replace(" ", "+")
    webbrowser.open("http://www.google.co.uk/search?q="+query)
    return 0

# -------- IMAGE TOOLS


def imgUpload(sysTrayIcon):
    image = grabSS()
    image.save("image.png")
    headers = {"Authorization": "Client-ID b7cdb801d615f30"}
    j1 = requests.post(
        "https://api.imgur.com/3/image",
        headers=headers,
        data={'image': b64encode(open('image.png', 'rb').read()), 'type': 'base64', })
    data = json.loads(j1.text)['data']
    if "link" not in data:
        toast.show_toast(title="Screeny - Upload Failed", msg="An error occured with the image upload. Check your connection and try again later.",
                         icon_path="icon.ico", duration=5, threaded=True)
        return False
    else:
        link = data["link"]
        pyperclip.copy(link)
        toast.show_toast(title="Screeny - Upload Complete", msg="The link has been copied to your clipboard. Click me to open the link.",
                         icon_path="icon.ico", duration=5, threaded=True, callback_on_click=lambda: openLink(link))


def GimgSearch(sysTrayIcon, filePath=None):
    if filePath is None:
        image = grabSS()
        image.save("image.png")
        filePath = os.path.abspath("image.png")
    files = {'encoded_image': (filePath, open(
        filePath, 'rb')), 'image_content': ''}
    response = requests.post(
        'http://www.google.co.uk/searchbyimage/upload', files=files, allow_redirects=False)
    fetchUrl = response.headers['Location']
    toast.show_toast(title="Screeny - Opening Google", msg="Your image has been uploaded successfully. Google will now open in your default browser.",
                     icon_path="icon.ico", duration=5, threaded=True)
    webbrowser.open(fetchUrl)


def YimgSearch(sysTrayIcon):
    image = grabSS()
    image.save("image.png")
    filePath = os.path.abspath("image.png")
    searchUrl = 'https://yandex.ru/images/search'
    files = {'upfile': ('blob', open(filePath, 'rb'), 'image/jpeg')}
    params = {'rpt': 'imageview', 'format': 'json',
              'request': '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}'}
    response = requests.post(searchUrl, params=params, files=files)
    if "captcha" in response.content.decode("UTF-8"):
        toast.show_toast(title="Screeny - Yandex Failed", msg="Yandex reverse search failed, resorting to Google reverse.",
                         icon_path="icon.ico", duration=5, threaded=True)
        GimgSearch(sysTrayIcon, filePath)
    else:
        query_string = json.loads(response.content)[
            'blocks'][0]['params']['url']
        img_search_url = searchUrl + '?' + query_string
        toast.show_toast(title="Screeny - Opening Yandex", msg="Your image has been uploaded successfully. Yandex will now open in your default browser.",
                         icon_path="icon.ico", duration=5, threaded=True)
        webbrowser.open(img_search_url)


def imgSave(sysTrayIcon):
    image = grabSS()
    image.save("image.png")
    file = filedialog.asksaveasfile(
        filetypes=[('PNG Image', '*.png')], defaultextension=[('PNG Image', '*.png')])
    if file is not None:
        image.save(file.name)
        toast.show_toast(title="Screeny - Screenshot Saved", msg="Your image has been saved successfully.",
                         icon_path="icon.ico", duration=5, threaded=True)
    else:
        toast.show_toast(title="Screeny - Opening Yandex", msg="Your did not pick where to save the screenshot, so it was cancelled.",
                         icon_path="icon.ico", duration=3, threaded=True)


def getColour(sysTrayIcon):
    image = grabSS()
    width, height = image.size

    r_total = 0
    g_total = 0
    b_total = 0

    count = 0
    for x in range(0, width):
        for y in range(0, height):
            r, g, b = image.getpixel((x, y))
            r_total += r
            g_total += g
            b_total += b
            count += 1

    rgb = (int(r_total/count), int(g_total/count), int(b_total/count))
    hex = '#%02x%02x%02x' % rgb
    pyperclip.copy(hex)
    toast.show_toast(title="Screeny - Colour Grabbed", msg="The colour " + hex + " was copied to your clipboard",
                     icon_path="icon.ico", duration=3, threaded=True)


# ------------- SETUP -------------

menu_options = (
    ('SS to Clip', None, getSS),
    ('SS to File', None, imgSave),
    ('--------------', None, blank),
    ('Text Copy', None, ocrSave),
    ('Text Search', None, ocrSearch),
    ('--------------', None, blank),
    ('Imgur Upload', None, imgUpload),
    ('Yandex Reverse', None, YimgSearch),
    ('Google Reverse', None, GimgSearch),
    ('--------------', None, blank),
    ('Colour Picker', None, getColour),
    ('--------------', None, blank))

print("\n"*60)
clearClip()

# ====================================
# REGISTER HOTKEYS LIKE THIS:
# hk.register(['shift', 'f'], callback=lambda event: getColour())
# ====================================

gui.SysTrayIcon(next(icons), hover_text, menu_options,
                on_quit=close, default_menu_index=1)
