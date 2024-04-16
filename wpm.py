import curses
from curses import wrapper
import time
import random

# start_screen - Displays the welcome screen before the game starts
def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test!")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()
    stdscr.getkey()

# display_text - Displays the target and input text and the wpm value
def display_text(stdscr, target_text, current_text, wpm=0):
    stdscr.addstr(target_text)
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    # enumerate for loop to get the value and index
    for i, char in enumerate(current_text):
        correct_char = target_text[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)
        stdscr.addstr(0, i, char, color)

# load_text - Loads the text samples in from the text file
def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()




# wpm_test - Handles the logic for playing the WPM Game
def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break    

        try:
            key = stdscr.getkey()
        except:
            continue

        # Escape the program with the escape character
        if ord(key) == 27:
            break
        # If the key is a backspace delete a character
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

# main - The start of the WPM Game program
def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(2, 0, "You completed the text! Press any key to continue")
        key = stdscr.getkey()
        if ord(key) == 27:
            break

wrapper(main)

