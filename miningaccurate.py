

import random
import time
import keyboard
import win32gui
import win32ui
import win32con
import numpy
import cv2
import os
import win32api

hwnds = []
#default size
w = 1366
h = 768
mouseX,mouseY = 0,0

targetFPS = 72 #change this to change the FPS
sleep = 0.2 #change this to change the speed of the keysend
variant = 0 #set to 1 if add variant

# data
matchFound = False
imageData = []
imageSelected = None
imageCut = None

currentLevel = 0
currentCandyLocation = -1
previousLocation = -1
kValue = 's' #S key, set to your NPC key
shouldStabilize = True

#window finder
def winEnumHandler( hwnd, ctx ):
    if win32gui.IsWindowVisible( hwnd ):
        if (win32gui.GetWindowText(hwnd) == "MapleStory"):
            print ( hex( hwnd ), win32gui.GetWindowText( hwnd ) )
            hwnds.append(hwnd)

def findMyLevel(datasmol):
    global currentLevel
    cakedata = numpy.where((datasmol[:,:,0] == 51) & (datasmol[:,:,1] == 102) & (datasmol[:,:,2] == 17))
    if (len(cakedata[0]) > 0):
        currentLevel = 1
    else:
        currentLevel = 2

def findCurrentCandyLocation(datashow):
    global currentCandyLocation
    global currentLevel

    if currentLevel == 1:
        #split this into 3 dots
        # cv2.rectangle(datashow, (286, 540), (386, 541), (0, 255, 0), 2)
        # cv2.rectangle(datashow, (653, 540), (753, 541), (0, 255, 0), 2)
        # cv2.rectangle(datashow, (993, 540), (1093, 541), (0, 255, 0), 2)

        #left star
        # cv2.rectangle(datashow, (310, 540), (311, 541), (0, 255, 0), 1)
        # cv2.rectangle(datashow, (340, 540), (341, 541), (0, 255, 0), 1)
        # cv2.rectangle(datashow, (360, 540), (361, 541), (0, 255, 0), 1)

        leftStarBlueCheck = datashow[540:541, 310:311]
        leftStarRedCheck = datashow[540:541, 340:341]
        leftStarYellowCheck = datashow[540:541, 360:361]
        # print(leftStarBlueCheck, leftStarRedCheck, leftStarYellowCheck)
        #check that blue = 255 255 204
        #check that red = 170 136 221
        #check that yellow = 221 255 255

        isLeftStarBlue = numpy.where((leftStarBlueCheck[:,:,0] == 255) & (leftStarBlueCheck[:,:,1] == 255) & (leftStarBlueCheck[:,:,2] == 204))
        isLeftStarRed = numpy.where((leftStarRedCheck[:,:,0] == 170) & (leftStarRedCheck[:,:,1] == 136) & (leftStarRedCheck[:,:,2] == 221))
        isLeftStarYellow = numpy.where((leftStarYellowCheck[:,:,0] == 221) & (leftStarYellowCheck[:,:,1] == 255) & (leftStarYellowCheck[:,:,2] == 255))
        
        

        #middle star
        # cv2.rectangle(datashow, (677, 540), (678, 541), (0, 255, 0), 1)
        # cv2.rectangle(datashow, (707, 540), (708, 541), (0, 255, 0), 1)
        # cv2.rectangle(datashow, (727, 540), (728, 541), (0, 255, 0), 1)

        middleStarBlueCheck = datashow[540:541, 677:678]
        middleStarRedCheck = datashow[540:541, 707:708]
        middleStarYellowCheck = datashow[540:541, 727:728]

        #check that blue = 255 255 204
        #check that red = 204 153 238
        #check that yellow = 221 238 255

        isMiddleStarBlue = numpy.where((middleStarBlueCheck[:,:,0] == 255) & (middleStarBlueCheck[:,:,1] == 255) & (middleStarBlueCheck[:,:,2] == 204))
        isMiddleStarRed = numpy.where((middleStarRedCheck[:,:,0] == 204) & (middleStarRedCheck[:,:,1] == 153) & (middleStarRedCheck[:,:,2] == 238))
        isMiddleStarYellow = numpy.where((middleStarYellowCheck[:,:,0] == 221) & (middleStarYellowCheck[:,:,1] == 238) & (middleStarYellowCheck[:,:,2] == 255))

        

        #right star
        # cv2.rectangle(datashow, (1017, 540), (1018, 541), (0, 255, 0), 1)
        # cv2.rectangle(datashow, (1047, 540), (1048, 541), (0, 255, 0), 1)
        # cv2.rectangle(datashow, (1067, 540), (1068, 541), (0, 255, 0), 1)  

        rightStarBlueCheck = datashow[540:541, 1017:1018]
        rightStarRedCheck = datashow[540:541, 1047:1048]
        rightStarYellowCheck = datashow[540:541, 1067:1068]

        #check that blue = 255 255 204
        #check that red = 204 136 238
        #check that yellow = 204 238 255

        isRightStarBlue = numpy.where((rightStarBlueCheck[:,:,0] == 255) & (rightStarBlueCheck[:,:,1] == 255) & (rightStarBlueCheck[:,:,2] == 204))
        isRightStarRed = numpy.where((rightStarRedCheck[:,:,0] == 204) & (rightStarRedCheck[:,:,1] == 136) & (rightStarRedCheck[:,:,2] == 238))
        isRightStarYellow = numpy.where((rightStarYellowCheck[:,:,0] == 204) & (rightStarYellowCheck[:,:,1] == 238) & (rightStarYellowCheck[:,:,2] == 255))

        if len(isLeftStarBlue[0]) > 0 and len(isLeftStarRed[0]) > 0 and len(isLeftStarYellow[0]) > 0:
            print("left star available")
            currentCandyLocation = 1
            return True
        
        elif len(isMiddleStarBlue[0]) > 0 and len(isMiddleStarRed[0]) > 0 and len(isMiddleStarYellow[0]) > 0:
            print("middle star available")
            currentCandyLocation = 2
            return True
        
        elif len(isRightStarBlue[0]) > 0 and len(isRightStarRed[0]) > 0 and len(isRightStarYellow[0]) > 0:
            print("right star available")
            currentCandyLocation = 3
            return True
        
        else:
            # print("no star available at this level")
            currentCandyLocation = -1
            return False
    
    if currentLevel == 2:
        # cv2.rectangle(datashow, (265, 480), (1115, 481), (0, 0, 255), 1)
        # cv2.rectangle(datashow, (286, 480), (386, 481), (255, 0, 0), 2)
        # cv2.rectangle(datashow, (653, 480), (753, 481), (255, 0, 0), 2)
        # cv2.rectangle(datashow, (1001, 480), (1101, 481), (255, 0, 0), 2)

        leftStarBlueCheck = datashow[480:481, 310:311]
        leftStarRedCheck = datashow[480:481, 340:341]
        leftStarYellowCheck = datashow[480:481, 360:361]

        #check that blue = 255 255 238
        #check that red = 238 204 255
        #check that yellow = 204 238 255

        isLeftStarBlue = numpy.where((leftStarBlueCheck[:,:,0] == 255) & (leftStarBlueCheck[:,:,1] == 255) & (leftStarBlueCheck[:,:,2] == 238))
        isLeftStarRed = numpy.where((leftStarRedCheck[:,:,0] == 238) & (leftStarRedCheck[:,:,1] == 204) & (leftStarRedCheck[:,:,2] == 255))
        isLeftStarYellow = numpy.where((leftStarYellowCheck[:,:,0] == 204) & (leftStarYellowCheck[:,:,1] == 238) & (leftStarYellowCheck[:,:,2] == 255))
        
        #middle star
        middleStarBlueCheck = datashow[480:481, 677:678]
        middleStarRedCheck = datashow[480:481, 707:708]
        middleStarYellowCheck = datashow[480:481, 727:728]

        #is there even a middle star

        #right star
        rightStarBlueCheck = datashow[480:481, 1025:1026]
        rightStarRedCheck = datashow[480:481, 1055:1056]
        rightStarYellowCheck = datashow[480:481, 1075:1076]

        #check that blue = 255 255 204
        #check that red = 238 204 255
        #check that yellow = 204 238 255

        isRightStarBlue = numpy.where((rightStarBlueCheck[:,:,0] == 255) & (rightStarBlueCheck[:,:,1] == 255) & (rightStarBlueCheck[:,:,2] == 204))
        isRightStarRed = numpy.where((rightStarRedCheck[:,:,0] == 238) & (rightStarRedCheck[:,:,1] == 204) & (rightStarRedCheck[:,:,2] == 255))
        isRightStarYellow = numpy.where((rightStarYellowCheck[:,:,0] == 204) & (rightStarYellowCheck[:,:,1] == 238) & (rightStarYellowCheck[:,:,2] == 255))


        if len(isLeftStarBlue[0]) > 0 and len(isLeftStarRed[0]) > 0 and len(isLeftStarYellow[0]) > 0:
            print("top left star available")
            currentCandyLocation = 4
            return True
        
        elif len(isRightStarBlue[0]) > 0 and len(isRightStarRed[0]) > 0 and len(isRightStarYellow[0]) > 0:
            print("top right star available")
            currentCandyLocation = 6
            return True
        
        else:
            currentCandyLocation = -1
            return False
    
    return False

def ladderUp():
    winKey(0x26, 2.1)

def moveRight(duration):
    winKey(0x27, duration)

def moveLeft(duration):
    winKey(0x25, duration)

def ladderDown():
    winKey(0x28, 2.1)

def winKey(event, duration):
    win32api.keybd_event(event, 0, 0, 0)

    start = time.time()
    while time.time() - start < duration:
        # time.sleep(0.001)
        pass

    win32api.keybd_event(event, 0, win32con.KEYEVENTF_KEYUP, 0)

def keyPress(key, duration):
    keyboard.press(key)
    
    start = time.time()
    while time.time() - start < duration:
        #time.sleep(0.001)
        pass

    keyboard.release(key)

def collectAndReturn(esc = True):
    #collect
    print("Collecting")
    keyPress(kValue, 0.20)

    #escape
    if esc:
        print("Sending esc key")
        keyPress('esc', 0.3)

def moveMe():
    global previousLocation
    global currentCandyLocation
    global shouldStabilize
    #create a set of 2 numbers from 1 to 6 such as (1, 3) or (5, 2), must not have the same number in each set
    #(1, 1) or (2, 2) is not allowed
    #sets:
    #1 = (1, 2), (1, 3), (1, 4), (1, 5), (1, 6)
    #2 = (2, 1), (2, 3), (2, 4), (2, 5), (2, 6)
    #3 = (3, 1), (3, 2), (3, 4), (3, 5), (3, 6)
    #4 = (4, 1), (4, 2), (4, 3), (4, 5), (4, 6)
    #5 = (5, 1), (5, 2), (5, 3), (5, 4), (5, 6)
    #6 = (6, 1), (6, 2), (6, 3), (6, 4), (6, 5)
    #for each set, create a path from the first number to the second number

    #if same level
    if previousLocation in [-2,-1,1,2,3] and currentCandyLocation in [1,2,3]:
        print("Moving to same level star ", currentCandyLocation)
        if previousLocation == -2 and currentCandyLocation == 3:
            moveRight(0.8)
        elif previousLocation == -2 and currentCandyLocation <= 2: #move 1.75 if 2, move 4 if 1
            moveLeft(4 - (currentCandyLocation - 1) * 2.25)

        if previousLocation == -1 and currentCandyLocation == 1:
            moveLeft(1.75)
        elif previousLocation == -1 and currentCandyLocation >= 2: #move 0.8 if 2, move 0.8 + 1.75 if 3
            moveRight(0.8 + (currentCandyLocation - 2) * 2.35)
        
        if previousLocation == 1 and currentCandyLocation >= 2:
            moveRight(2.5 * (currentCandyLocation - 1))
        
        if previousLocation == 2:
            if currentCandyLocation == 1:
                moveLeft(2.5)
            if currentCandyLocation == 3:
                moveRight(2.5)
        
        if previousLocation == 3:
            if currentCandyLocation <= 2:
                moveLeft(2.5 * (3 - currentCandyLocation))
            
        collectAndReturn()
        previousLocation = currentCandyLocation
        shouldStabilize = False
    
    elif previousLocation in [4,5,6,7,8] and currentCandyLocation in [4,5,6]:
        print("Moving to same level star ", currentCandyLocation)
        if previousLocation == 8:
            if currentCandyLocation == 6:
                moveRight(0.8)
            if currentCandyLocation <= 5:
                moveLeft(4 - (currentCandyLocation - 4) * 2.25)
        
        if previousLocation == 7:
            if currentCandyLocation == 4:
                moveLeft(1.75)
            if currentCandyLocation >= 5:
                moveRight(0.8 + (currentCandyLocation - 5) * 2.35)
        
        if previousLocation == 6:
            if currentCandyLocation <= 5:
                moveLeft(2.5 * (6 - currentCandyLocation))
        
        if previousLocation == 5:
            if currentCandyLocation == 6:
                moveRight(2.5)
            if currentCandyLocation == 4:
                moveLeft(2.5)
        
        if previousLocation == 4:
            if currentCandyLocation >= 5:
                moveRight(2.5 * (currentCandyLocation - 4))
        
        collectAndReturn()
        previousLocation = currentCandyLocation
        shouldStabilize = False

    #if previous location is -1,1,2,3 and currentLocation is not found, then go up ladder and track again
    if previousLocation in [-2,-1,1,2,3] and currentCandyLocation == -1:
        if previousLocation < 0:
            print("Going up the ladder")
            ladderUp()
            previousLocation = 6 - previousLocation #7 is left ladder top, 8 is right ladder top
        elif previousLocation == 1:
            print("Using First ladder")
            moveRight(1.75)
            ladderUp()
            previousLocation = 7
        elif previousLocation == 2:
            print("Using second ladder")
            moveRight(1.7)
            ladderUp()
            previousLocation = 8
        elif previousLocation == 3:
            moveLeft(0.83)
            ladderUp()
            previousLocation = 8
        shouldStabilize = True

    elif previousLocation in [4,5,6,7,8] and currentCandyLocation == -1:
        if previousLocation >= 7:
            print("Going down the ladder")
            ladderDown()
            previousLocation = 6 - previousLocation
        elif previousLocation == 6 or previousLocation == 5:
            moveLeft(0.9)
            ladderDown()
            previousLocation = -2
        elif previousLocation == 4:
            moveRight(1.66)
            ladderDown()
            previousLocation = -1
        shouldStabilize = True

def runCV():
    global matchFound
    win32gui.EnumWindows( winEnumHandler, None )

    hwnd = hwnds[0]
    if (len(hwnds) > 1): #player has chat external
        hwnd = hwnds[1]

    #get the correct size
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y

    # hwnd = win32gui.FindWindow(None, "MapleStory")
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    # cv2.namedWindow('image')
    # cv2.setMouseCallback('image',draw_circle)

    while True:
        #stabilize the camera for 5 seconds
        timestart = time.time()
        
        if shouldStabilize:
            print("waiting for camera stabilize")
            while (time.time() - timestart < 3.35):
                cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)

                #make CV image
                signedIntsArray = dataBitMap.GetBitmapBits(True)
                img = numpy.fromstring(signedIntsArray, dtype='uint8')
                img.shape = (h,w,4)
                datashow = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
                datasmol = datashow[221:222, 22:23]
                cv2.imshow("Finding Candy", datashow)

                timend = time.time()
            
                if (1/targetFPS - (timend-timestart) > 0):
                    time.sleep(1/targetFPS - (timend-timestart))

                #end when Q is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                        # Free Resources
                    dcObj.DeleteDC()
                    cDC.DeleteDC()
                    win32gui.ReleaseDC(hwnd, wDC)
                    win32gui.DeleteObject(dataBitMap.GetHandle())
                    break
        # print(datasmol)
        
        #find if we are at first or second level
        print("Finding level")
        findMyLevel(datasmol)
        print("we are at level ", currentLevel)

        #for the next 3 seconds, check if the candy is available
        timeTofind = time.time()

        print("Finding candy at level ", currentLevel)
        while (time.time() - timeTofind < 1.75):
            time.sleep(0.001)

            #recapture
            cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)

            #make CV image
            signedIntsArray = dataBitMap.GetBitmapBits(True)
            img = numpy.fromstring(signedIntsArray, dtype='uint8')
            img.shape = (h,w,4)
            datashow = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
            datasmol = datashow[221:222, 22:23]

            if currentLevel == 1:
            #firstlevel stars
                cv2.rectangle(datashow, (286, 500), (386, 580), (255, 0, 0), 2)
                cv2.rectangle(datashow, (653, 500), (753, 580), (255, 0, 0), 2)
                cv2.rectangle(datashow, (993, 500), (1093, 580), (255, 0, 0), 2)
            else:
                #secondlevel stars
                cv2.rectangle(datashow, (286, 440), (386, 520), (255, 0, 0), 2)
                cv2.rectangle(datashow, (653, 440), (753, 520), (255, 0, 0), 2)
                cv2.rectangle(datashow, (1001, 440), (1101, 520), (255, 0, 0), 2)
                
            cv2.imshow("Finding Candy", datashow)

            if findCurrentCandyLocation(datashow):
                print("Candy found at location ", currentCandyLocation)
                break
            
            timend = time.time()
        
            if (1/targetFPS - (timend-timestart) > 0):
                time.sleep(1/targetFPS - (timend-timestart))

            #end when Q is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                    # Free Resources
                dcObj.DeleteDC()
                cDC.DeleteDC()
                win32gui.ReleaseDC(hwnd, wDC)
                win32gui.DeleteObject(dataBitMap.GetHandle())
                break

        #move to the candy's position
        print("Moving to candy position from P", previousLocation, "to P", currentCandyLocation)
        moveMe()
        #do the movement based on previousLocation and currentCandyLocation
        time.sleep(0.1)


        

runCV()