import random
import sys
import time
import win32gui
import win32ui
import win32con
import numpy
import cv2
import os
import win32api
import keyboard

hwnds = []
#default size
w = 1366
h = 768
mouseX,mouseY = 0,0

targetFPS = 120 #change this to change the FPS
sleep = 0.01 #change this to change the speed of the keysend
variant = 0.01 #change this to add a random timer to the keysend

# data
matchFound = False
imageData = []
imageSelected = None
imageCut = None

kValue = 's' #S key, set to your NPC key


#debug to get the X Y axis
def draw_circle(event,x,y,flags,param):
    global mouseX,mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img,(x,y),100,(255,0,0),-1)
        mouseX,mouseY = x,y

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
    keyboard.press_and_release('space')
    count = 1

    while True:
        #get the image from the window
        timestart = time.time()
        cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)

        #make CV image
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = numpy.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (h,w,4)
        datashow = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        datasmol = datashow[666:667, 443:1043] #640-700 and 430-1060 is the area
        #datascaled = cv2.resize(datasmol, interpolation=cv2.INTER_AREA, dsize=(datasmol.shape[1]//6, datasmol.shape[0]//6))


        ##colors
        #[119  34  68] [119  34  51] [136  51  68] are purples (the one on the background color)
        #[ 85 255 255] is the spots that are safe to press the button (yellow)
        # [255 255 255] is the starting and ending spot of the seesaw (white)
        # [ 54 122 112] [ 83 239 240] these are the colors if the points collide
        
        #try with a where clause
        found = numpy.where((datasmol[:, :, 0] == 83) &  (datasmol[:, :, 1] == 239) & (datasmol[:, :, 2] == 240))
        if (len(found[0]) > 0):
            #NOTE: must run in admin mode 
            
            if count < 40:
                count+= 1
            else:
                count = 1
            
            time.sleep(0.045 - (count*0.001))

            keyboard.press(kValue)
            time.sleep(0.1)
            keyboard.release(kValue)

            print("SEND NPC KEY")
            time.sleep(0.965)
            print("Awake for ", count)

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

#loadAllImages()
runCV()