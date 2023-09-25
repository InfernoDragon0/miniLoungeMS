import random
import time
import win32gui
import win32ui
import win32con
import numpy
import cv2
import os
import keyboard
import win32api

hwnds = []
#default size
w = 1366
h = 768
mouseX,mouseY = 0,0

targetFPS = 360 #change this to change the FPS
sleep = 0.01 #change this to change the speed of the keysend
variant = 0.01 #change this to add a random timer to the keysend

# data
matchFound = False
imageData = []
imageSelected = None
imageCut = None

kValue = 's' #S key, set to your NPC key

#window finder
def winEnumHandler( hwnd, ctx ):
    if win32gui.IsWindowVisible( hwnd ):
        if (win32gui.GetWindowText(hwnd) == "MapleStory"):
            print ( hex( hwnd ), win32gui.GetWindowText( hwnd ) )
            hwnds.append(hwnd)

def loadAllImages():
    for filename in os.listdir('./lowestquality'):
        print("Loading " + filename)
        img = cv2.imread(os.path.join('./lowestquality', filename))
        #img = cv2.resize(img, (100, 100))
        imageData.append(img)
        # cv2.imshow(filename, img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

def winKey(event, duration):
    win32api.keybd_event(event, 0, 0, 0)

    start = time.time()
    while time.time() - start < duration:
        time.sleep(0.001)
        pass

    win32api.keybd_event(event, 0, win32con.KEYEVENTF_KEYUP, 0)

def keyPress(key, duration):
    keyboard.press(key)
    
    start = time.time()
    while time.time() - start < duration:
        #time.sleep(0.001)
        pass

    keyboard.release(key)

def keyJump(duration):
    keyboard.press('left')
    keyboard.press('space')
    keyboard.press('up')
    
    start = time.time()
    while time.time() - start < duration:
        time.sleep(0.005)

    keyboard.release('space')
    keyboard.release('left')
    keyboard.release('up')

def keyJumpDown(duration):
    keyboard.press('down')
    keyboard.press('left')
    
    start = time.time()
    while time.time() - start < duration:
        time.sleep(0.005)
    
    keyboard.release('down')
    keyboard.press('space')

    start = time.time()
    while time.time() - start < duration:
        time.sleep(0.005)

    keyboard.release('space')
    keyboard.release('left')

def runMines2():
    #use the winKey() and keyPress() instead
    print("Running in 3 seconds.. Place your character on the 2nd platform, aligned to the 1st ladder")
    time.sleep(3)
    print("Now running")
    initial = True

    while True:
        if initial:
            print("Moving to the start of the platform")
            winKey(0x25, 1.5)
            initial = False

        print("Collecting the first star")
        collectAndReturn()

        print("Moving to the center of the first platform")
        winKey(0x27, 2.5)

        print("Collecting the middle star")
        collectAndReturn(False)

        print("Moving to the end of the first platform")
        winKey(0x27, 2.5)

        print("Collecting the last star")
        collectAndReturn()

        print("Moving to the ladder")
        winKey(0x25, 0.55)
        keyJump(0.35)

        print("Moving up the ladder")
        winKey(0x26, 2.1)

        print("Moving to the right")
        winKey(0x27, 0.8)

        print("Collecting the right star")
        collectAndReturn(False)

        print("Moving to the middle")
        winKey(0x25, 2)

        print("Collecting the center star")
        collectAndReturn(False)

        print("Moving to the left")
        winKey(0x25, 2.4)

        print("Collecting the left star")
        collectAndReturn(False)

        print("Moving to the ladder")
        winKey(0x27, 1.3)

        print("Jumping down the ladder")
        keyJumpDown(0.3)
        winKey(0x25, 1.1)


def runMines():
    
    print("Running in 3 seconds.. Place your character on the 2nd platform, aligned to the 1st ladder")
    time.sleep(3)
    print("Now running")

    while True:
        #move to the start of the platform
        print("Moving to the start of the platform")
        win32api.keybd_event(0x25, 0, 0, 0)
        time.sleep(1.75)
        win32api.keybd_event(0x25, 0, win32con.KEYEVENTF_KEYUP, 0)
        
        #move to the right of the first platform
        print("Moving to the center of the first platform")
        win32api.keybd_event(0x27, 0, 0, 0)

        #collect the first star
        print("Collecting the first star")
        collectAndReturn()
        
        time.sleep(2.35)
        # keyboard.release('right')

        #collect the middle star
        print("Collecting the middle star")
        collectAndReturn()

        #move to the right of the first platform
        print("Moving to the end of the first platform")
        # keyboard.press('right')
        time.sleep(2.35)
        win32api.keybd_event(0x27, 0, win32con.KEYEVENTF_KEYUP, 0)

        #collect the last star
        print("Collecting the last star")
        collectAndReturn()

        #go left and up the ladder
        print("Moving to the ladder")
        win32api.keybd_event(0x25, 0, 0, 0)
        time.sleep(0.55)
        
        #jump to the ladder
        print("Jumping to the ladder")
        keyboard.press('space')
        time.sleep(0.35)
        keyboard.release('space')
        win32api.keybd_event(0x25, 0, win32con.KEYEVENTF_KEYUP, 0)

        #up the ladder
        print("Moving up the ladder")
        win32api.keybd_event(0x26, 0, 0, 0)
        time.sleep(2.1)
        win32api.keybd_event(0x26, 0, win32con.KEYEVENTF_KEYUP, 0)

        #move to the right
        print("Moving to the right")
        win32api.keybd_event(0x27, 0, 0, 0)
        time.sleep(0.8)
        win32api.keybd_event(0x27, 0, win32con.KEYEVENTF_KEYUP, 0)

        #move to the center
        print("Moving to the center")
        win32api.keybd_event(0x25, 0, 0, 0)

        print("Collecting the right star")
        collectAndReturn()

        time.sleep(2)
        # keyboard.release('left')

        print("Collecting the center star")
        collectAndReturn()

        #move to the left
        print("Moving to the left")
        # keyboard.press('left')
        time.sleep(2.3)
        win32api.keybd_event(0x25, 0, win32con.KEYEVENTF_KEYUP, 0)

        #move to the ladder
        print("Moving to the ladder")
        win32api.keybd_event(0x27, 0, 0, 0)

        print("Collecting the left star")
        collectAndReturn()

        time.sleep(1.55)
        win32api.keybd_event(0x27, 0, win32con.KEYEVENTF_KEYUP, 0)

        #jump down the ladder
        print("Jumping down the ladder")
        #key down arrow
        win32api.keybd_event(0x28, 0, 0, 0)
        time.sleep(2.3)
        win32api.keybd_event(0x28, 0, win32con.KEYEVENTF_KEYUP, 0)
        

def collectAndReturn(esc = True):
    #collect
    print("Collecting")
    keyPress(kValue, 0.15)

    #escape
    if esc:
        print("Sending esc key")
        keyPress('esc', 0.3)

    # #press kValue key using win32api
    # print("Sending key")
    # keyboard.press(kValue)
    # time.sleep(0.15)
    # keyboard.release(kValue)

    # #escape
    # print("Sending esc key")
    # keyboard.press('esc')
    # time.sleep(0.15)
    # keyboard.release('esc')

runMines2()