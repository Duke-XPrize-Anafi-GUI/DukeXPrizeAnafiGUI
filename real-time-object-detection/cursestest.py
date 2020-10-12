import curses
from curses import wrapper
import time

def main(stdscr):
    stdscr.clear()
    while True:
        # Store the key value in the variable `c`
        c = stdscr.getch()
        # Clear the terminal
        stdscr.clear()
        if c == ord('a'):
            stdscr.addstr("You pressed the 'a' key.")
        elif c == curses.KEY_UP:
            stdscr.addstr("You pressed the up arrow.")
        else:
            stdscr.addstr("This program doesn't know that key.....")

# wrapper is a function that does all of the setup and teardown, and makes sure
# your program cleans up properly if it errors!
wrapper(main)
"""
Calling stdscr.nodelay(True) made stdscr.getch() non-blocking. If Python gets to
that line and the user hasn't typed anything since last time, getch will return
-1, which doesn't match any key.

What if the user managed to type more than one character since the last time
getch was called? All of those characters will start to build up, and getch will
return the value for each one in the order that they came. This can cause
delayed reactions if you're writing a game. After getch, you can call
curses.flushinp to clear out the rest of the characters that the user typed.

This is a good place to talk more about getch.

Every time the user presses a key, that key's value gets stored in a list. When
getch is called, it goes to that list and pops that value. If the user manages
to press several keys before getch is called, getch will pop the least recently
added value (the oldest key pressed). The rest of the keys remain in the list!
The process continues like this. So there's a problem if there is a delay
between calls to getch: Key values can build up. If you don't want this to
happen, curses.flushinp() clears the list of inputted values. This ensures that
the next key the user presses after curses.flushinp() is what getch will return
next time it is called.
"""

"""
To continue learning about curses, checkout the addstr method to see how you can
print strings at certain y, x coordinates. You can start here:
https://docs.python.org/3/library/curses.html#window-objects
"""
