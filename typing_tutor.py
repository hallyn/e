#!/usr/bin/python3
#
# Copyright Serge and Edward Hallyn 2015
# GPL v2 license

import sys
import termios
import fcntl
import random

# from code.activestate.com/recipes/134892

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()

kbd = [ ["left home", "asdfg"],
        ["right home", "hkl;'"],
        ["left top", "qwert"],
        ["right top", "yuiop[]"],
        ["left bottom", "zxcvb"],
        ["right bottom", "nm,./"],
        ["left numbers", "`12345"],
        ["right numbers", "67890-="]]

def practice(which):
    chars = ""
    for i in range(len(which)):
        try:
            idx = int(which[i])
        except:
            print("Bad input: ", which[i], "\n")
            continue
        if idx < 0 or idx > len(kbd):
            print("Skipping ", idx, "\n")
            continue
        chars = chars + kbd[idx][1]
    nchrs = len(chars)
    print("Character set: ", chars, "\n")
    while True:
        current = chars[random.randint(0,nchrs-1)]
        done = False
        while done == False:
            print(current, "     (or space to stop)\n")
            ch = getch()
            if ch == ' ':
                return
            if ch == current:
                print("Correct!\n")
                done = True
            else:
                print("Wrong.  You typed ", ch, " instead of ", current, "\n")

while True:
    print("Which rows would you like to practice on?")
    for i in range(len(kbd)):
        print("  ", i, ":", kbd[i][0])
    print("(Enter all rows you'd like, or 'q' to quit: ")
    answer = sys.stdin.readline()
    answer = answer.rstrip()
    if answer == "q":
        sys.exit(0)
    practice(answer)
