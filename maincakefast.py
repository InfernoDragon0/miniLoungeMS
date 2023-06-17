#todo: get the color of the line of the cake endings
#the first 7-10 layers are different heights, record at different heights
#the regular layers always appear aroudn the window grill area
#record a small area near the left of the starting point to determine the speed of the current layer
#use the speed to determine when to press the button (can check via the color index of the layer, then 0.1 seconds later check again)


#alternatively:
#run slower method
#determine the size of the available area, by having one recording on the left and right
#first 7 layers are different heights, record at different heights
#the regular layers always appear aroudn the window grill area
#record slightly above the layer to determine the current placement of the layer
#press the button when the entire scene is the color of the layer (this might create a delay)

import random
import time
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


#window finder
def winEnumHandler( hwnd, ctx ):
    if win32gui.IsWindowVisible( hwnd ):
        if (win32gui.GetWindowText(hwnd) == "MapleStory"):
            print ( hex( hwnd ), win32gui.GetWindowText( hwnd ) )
            hwnds.append(hwnd)

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
    length = -1
    height = 0
    doOffset = False
    currentEdges = [-1,-1]
    previousEdges = [270, 765]

    while True:
        #get the image from the window
        timestart = time.time()
        cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)

        #make CV image
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = numpy.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (h,w,4)
        datashow = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)


        # GET SPEED
        #check for [238 238 255] on the first value, then check on the last value
        cakestart = 480 - (height * 40)
        cakeend = 481 - (height * 40)

        if doOffset:
            cakestart += 1
            cakeend += 1

        cakestartPrev = cakestart + 40
        cakeendPrev = cakeend + 40

        cakestartY = 15
        cakeendY = 290
        offset = 0

        datasmol = datashow[cakestart:cakeend, cakestartY:cakeendY]
        
            #constantly get the current location of the cake
        cakedata = numpy.where((datasmol[:,:,0] == 238) & (datasmol[:,:,1] == 238) & (datasmol[:,:,2] == 255))
        try:
            currentEdges = [cakedata[1][0] + 15, cakedata[1][-1 -offset] + 15]
        except:
            # print("waiting for cake")
            pass
            
        if (currentEdges[0] != -1):
            cv2.rectangle(datashow, (currentEdges[0], cakestart), (currentEdges[1], cakeend), (0, 255, 0), 2)
        
        cv2.rectangle(datashow, (previousEdges[0], cakestartPrev), (previousEdges[1], cakeendPrev), (255, 0, 0), 2)

        #press space if the current edge[0] is within 3 pixels of the previous edge[0]
        offset2 = 4 #NOTE: set this lower to make it more accurate, higher for faster but less accurate
        if (currentEdges[0] >= 270 - offset2 and currentEdges[0] <= 270 + offset2):
            #press space
            win32api.keybd_event(0x20, 0, 0, 0)
            win32api.keybd_event(0x20, 0, win32con.KEYEVENTF_KEYUP, 0)
            print("stacked at ", currentEdges[0], " and ", previousEdges[0], " height: ", height)
            if height < 5:
                height += 1
            else:
                doOffset = True
            if currentEdges[0] != -1:
                previousEdges = currentEdges
            currentEdges = [-1,-1]
            time.sleep(sleep)

        #draw rectangle on the image related to datasmol
        cv2.imshow("datA", datashow)
        cv2.imshow("Stage", datasmol)


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

runCV()