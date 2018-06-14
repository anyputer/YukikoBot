# from copypaste import copy, paste
from ctypes import windll

def aesthetic(text, spaces):
    # This function adds  s p a c e s  to the text.
    
    between = ''
    for i in range(1, spaces):
        between += ' '
    return '**```css\n' + between.join(text) + '```**'

if __name__ == "__main__":
    charLimit = 50
    try:
        text = paste()
    except:
        windll.user32.MessageBoxW(None, "Erm, that wasn't text that you copied...", "Aestheticifier", 0x10)

    try:
        if text == "": # If the user copied text without words,
            windll.user32.MessageBoxW(None, "You probably forgot to copy something that you want to add spaces to.", "Aestheticifier", 0x10)

        elif len(text) > charLimit: # If the text is over the character limit,
            windll.user32.MessageBoxW(
                None,
                "Whoa chill... you copied more than " + str(charLimit) + " characters for the Aestheticifier! ( " + str(len(text)) + " characters )\n\nThis would cause spam on Discord, and spam is not good...",
                "Aestheticifier",
                0x30
                )

        else: # Otherwise, everything went according to plan! :D
            copy(aesthetic(text, 2))
    except:
        pass
