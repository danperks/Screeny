# Screeny

A taskbar screenshot tool built in Python, with OCR and Imgur Upload

## Installation

- Install the required modules with ```pip install -r requirements.txt```
- Install PyTesseract to the default directory: https://github.com/UB-Mannheim/tesseract/wiki
- Add that directory to the Path enviromental variables
- Run the program, and check the Notification Icons

## Usage

To use the program regularly, just run Screeny.py and everything should work fine.
Let me know with a Issue if you find an issue.


### Keybinds

To use keybinds, edit keybinds.csv with the following format:

- The left most cell should contain the keybind as it would be written
    - E.G. 'CTRL+K' or 'CTRL+ALT+T'
    - Be careful using just single letter binds, like 'K'
    - Keybinds should be surrounded by single quotes, like the examples
- The right cell should have the name of one of the following functions:
    - Options: 
        - 'ocrSave' - Copies the text from an image to your clipboard
        - 'ocrSearch' - Searches the text from an image on google.co.uk
        - 'imgUpload' - Uploads the screenshot to imgur.com
        - 'imgSearch' - Runs a reverse image search on google.co.uk
        - 'imgSave' - Lets you choose where to save the screenshot once it's taken
    - The name should be surrounded by single quotes, as shown above

If you have any issues with keybinds, raise an Issue here and I'll try to figure out why it's not working.

## Credits

- Google's TesseractOCR Library
- A GUI library that I didn't write, but I can't find who did