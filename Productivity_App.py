#############################################################################################################
#                                             Sources                                                       #
#############################################################################################################
# https://likegeeks.com/python-gui-examples-tkinter-tutorial/                                               #
# https://datatofish.com/entry-box-tkinter/                                                                 #
# https://thispointer.com/python-get-list-of-all-running-processes-and-sort-by-highest-memory-usage/        #
# https://www.semicolonworld.com/question/56593/finding-the-current-active-window-in-mac-os-x-using-python  #
# https://www.youtube.com/watch?v=ZBLYcvPl1MA                                                               #
# https://realpython.com/python-dicts                                                                       #
# https://www.youtube.com/watch?v=TbMKwl11itQ                                                               #
# https://stackoverflow.com/questions/45973453/using-mouse-and-keyboard-listeners-together-in-python        #
#############################################################################################################

import tkinter as tk
from pynput import *
from pynput.keyboard import Listener, Key
from pynput.mouse import Listener as MouseListener
# https://www.semicolonworld.com/question/56593/finding-the-current-active-window-in-mac-os-x-using-python
from AppKit import NSWorkspace
import time
import numpy as np
import os

# Initialize global variables
words = 0;
# https://realpython.com/python-dicts/
activityDict = {}
running = True
previous_key = None
currentAppName = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
start_time = time.time()
end_time = time.time()
activity_totalTime = 0
total_mouse_clicks = 0

# Function that finds and returns the active window on the machine
# Also determines of the active window is different
# If it is different the data is added the appropriate dictionary entry
# Or a new entry, if a current entry does not exist
# https://www.youtube.com/watch?v=ZBLYcvPl1MA
def get_active_window():
    global activityDict, words, currentAppName, start_time, end_time, activity_totalTime, total_mouse_clicks
    def calculate_activity_totals(activity_totalTime, currentAppName):
        global activityDict, words, start, total_mouse_clicks
        total_mouse_clicks = int(total_mouse_clicks / 2)
        if currentAppName in activityDict.keys():
            activity_totalTime += activityDict[currentAppName][0]
            words += activityDict[currentAppName][1]
            total_mouse_clicks += activityDict[currentAppName][2]

        activityDict[currentAppName] = (activity_totalTime, words, total_mouse_clicks)

    activeAppName = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
    if currentAppName != activeAppName:
        end_time = time.time()
        activity_totalTime = end_time - start_time
        calculate_activity_totals(activity_totalTime, currentAppName)
        start_time = time.time()
        currentAppName = activeAppName
        words = 0
        total_mouse_clicks = 0
        previous_key = None
        print(activityDict)

# Finds the amount of words typed by searching each space, the first word, or a newlilne
# Checks active window function for new window
# Uses listener
#https://www.youtube.com/watch?v=TbMKwl11itQ
# https://stackoverflow.com/questions/45973453/using-mouse-and-keyboard-listeners-together-in-python
def words_typed():
    def on_press(key):
        global currentAppName
        global words, previous_key, listener
        get_active_window()
        if key == Key.space and previous_key != Key.space:
            words+=1
            previous_key = Key.space
        elif previous_key == None:
            words+=1
            previous_key = "Other"
        elif key != Key.space:
            previous_key = "Other"
        elif key == Key.enter and previous_key != Key.enter:
            words+=1
            previous_key = Key.enter

    def on_release(key):
        if running == False:
            listener.stop()
            return False

    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()

# Checks for mouse clicks on the machine
# Checks active window function for new window
# Uses listener
# https://stackoverflow.com/questions/45973453/using-mouse-and-keyboard-listeners-together-in-python
def mouse_clicks():
    def on_click(x, y, button, pressed):
        global total_mouse_clicks
        get_active_window()
        total_mouse_clicks+=1
        if running == False:
            MouseListener.stop()
            return False

    mouselistener = MouseListener(on_click=on_click)
    mouselistener.start()

# Start of Gui
# https://likegeeks.com/python-gui-examples-tkinter-tutorial/
# Has three Buttons - “Start Tracker”, “Stop Tracker”, and “Reset Tracker”
root = tk.Tk()

canvas1 = tk.Canvas(root, width = 400, height = 300)
canvas1.pack()

# “Start Tracker”
def start():
    global running, start_time, activity_totalTime, total_mouse_clicks, words, activityDict
    start_time = time.time()
    running = True
    mouse_clicks()
    words_typed()

# “Stop Tracker”
def stop():
    global running, listener, words
    running = False

# “Reset Tracker”
def reset():
    global activity_totalTime, total_mouse_clicks, words, activityDict, running
    activity_totalTime = 0
    total_mouse_clicks = 0
    words = 0;
    activityDict = {}
    running = False
# https://datatofish.com/entry-box-tkinter/
button1 = tk.Button(root, text='Start Tracker', command=start)
button2 = tk.Button(root, text='Stop Tracker', command=stop)
button3 = tk.Button(text='Reset Tracker', command=reset)
canvas1.create_window(100, 180, window=button1)
canvas1.create_window(200, 180, window=button2)
canvas1.create_window(300, 180, window=button3)

root.mainloop()
