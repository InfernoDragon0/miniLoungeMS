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

targetFPS = 60 #change this to change the FPS
sleep = 0.16 #change this to change the speed of the keysend
variant = 0 #change this to add a random timer to the keysend

# data
matchFound = False
imageData = []
imageSelected = None
imageCut = None


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

    while True:
        #get the image from the window
        timestart = time.time()
        cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)

        #make CV image
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = numpy.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (h,w,4)
        datashow = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        datasmol = datashow[525:526, 510:511]
        datafever = datashow[640:680, 410:630]
        #datascaled = cv2.resize(datasmol, interpolation=cv2.INTER_AREA, dsize=(datasmol.shape[1]//6, datasmol.shape[0]//6))
        #[[[102 255 221]]] GREEN
        #[[[119 255 221]]]

        #[[[255 238 153]]] BLUE
        #[[[255 238 136]]]

        #[[[153 119 255]]] RED
        #[[[170 119 255]]] 

        blue = numpy.where((datasmol[:, :, 0] == 255))
        green = numpy.where((datasmol[:, :, 1] == 255))
        red = numpy.where((datasmol[:, :, 2] == 255))
        
        color = -1
        
        if (len(blue[0]) > 0):
            color = 0
        if (len(green[0]) > 0):
            color = 1
        if (len(red[0]) > 0):
            color = 2


        # cv2.rectangle(datashow, (410,400), (610,600), (0,255,0), 2)
        # cv2.rectangle(datashow, (410,640), (630,680), (0,0,255), 2)
        #cv2.imshow("datA", datashow)
        # cv2.imshow("Stage", datasmol)
        # cv2.imshow("Fever", datafever)
        #fever
        fevercheck = cv2.matchTemplate(datafever, imageData[0], cv2.TM_CCOEFF_NORMED)
        fmin_val, fmax_val, fmin_loc, fmax_loc = cv2.minMaxLoc(fevercheck)

        if fmax_val > 0.9:
            print("Fever")
            win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_SPACE, 0x001E0001)
            win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_SPACE, 0x001E0001)
            matchFound = True
            time.sleep(0.1)

        else:
            # print("End Fever")
            matchFound = False

            #NOTE: must run in admin mode 
            if (color == 1): #left
                #send key LEFT ARROW 
                win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_LEFT, 0x001E0001)
                win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_LEFT, 0x001E0001)
                print("LEFT")
            elif (color == 0): #right
                #send key RIGHT ARROW
                win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RIGHT, 0x00200001)
                win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RIGHT, 0x00200001)
                print("RIGHT")
            elif (color == 2): #up
                #send key UP ARROW
                win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_UP, 0x001C0001)
                win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_UP, 0x001C0001)
                print("UP")
        
            #random sleep between 0.01 and 0.05
            sleeprand = random.uniform(0.01, 0.05)
            time.sleep(sleep + sleeprand)

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

loadAllImages()
runCV()