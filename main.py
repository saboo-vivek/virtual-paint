import cv2
import numpy as np

frameWidth = 1280
frameHeight = 720
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(100, 150)

color_explore = np.zeros((100,200, 3), np.uint8)
color_selected = np.zeros((100,200, 3), np.uint8)
color_explore=cv2.putText(color_explore, "EXPLORE", (5, 15), cv2.FONT_HERSHEY_COMPLEX, .5, (255, 255, 255), 1)
color_selected=cv2.putText(color_selected, "SELECTED", (5, 15), cv2.FONT_HERSHEY_COMPLEX, .5, (255, 255, 255), 1)

boardimg = np.zeros((800,1100,3),np.uint8)
boardimg[:]= (255,255,255)

mypencolors = [[99,91,87,179, 255, 255],
               [71,82,88,101,255,255]]##pen detection hsv

pos1,s=0,1
mycolorvalues=[0,0,0]
points =  []
################################################################################################
# Mouse Callback function
def show_color(event, x, y, flags, param):
    global mycolorvalues
    B = colimg[y, x][0]
    G = colimg[y, x][1]
    R = colimg[y, x][2]

    color_explore[:] = (B,G,R)

    if event == cv2.EVENT_RBUTTONDOWN:
        mycolorvalues = [B, G, R]
        color_selected[:] = mycolorvalues
##############################################################################################


##############################################################################################

def empty(a):
    pass

trackimg=np.zeros((1,400,3),np.uint8)
cv2.namedWindow('COLOR PICKER')
cv2.createTrackbar("Size",'COLOR PICKER',9,15,empty)
cv2.createTrackbar("0N/0FF",'COLOR PICKER',1,1,empty)
cv2.namedWindow('COLOR PICKER')
colimg = cv2.imread('colortable.png')
colimg=cv2.resize(colimg,(400,600))
cv2.setMouseCallback('COLOR PICKER', show_color)

#######################################################################################################
def findColor(img, mypencolors):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    global pos1,s
    print(pos1)
    b = int(mycolorvalues[0])
    g = int(mycolorvalues[1])
    r = int(mycolorvalues[2])
    for color in mypencolors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)

        x, y = getContours(mask)

        if s==0:
            cv2.circle(boardimg, (x, y), pos1, (b,g,r), cv2.FILLED)



def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            # cv2.drawContours(imgresult,cnt,-1,(0,255,0),3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y

#################################################################################################

# while loop to live update
while (1):

    success, img = cap.read()
    img = cv2.flip(img, 1)
    # imgresult=img.copy()

    findColor(img,mypencolors)
    cv2.imshow("Result", boardimg)
    # cv2.imshow("contour",imgresult)
#########################################################################################

    imgcolstack = np.hstack((color_explore, color_selected))
    imgstack = np.vstack((colimg, imgcolstack, trackimg))
    cv2.imshow('COLOR PICKER', imgstack)

    pos1 = cv2.getTrackbarPos("Size", 'COLOR PICKER')
    s=cv2.getTrackbarPos("0N/0FF",'COLOR PICKER')

    k = cv2.waitKey(1) & 0xFF
    if k ==ord('q') or k ==ord('Q') :
        break

cv2.destroyAllWindows()

