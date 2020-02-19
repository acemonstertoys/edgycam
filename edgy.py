import time
import cv2
import numpy as np
from escpos.exceptions import USBNotFoundError
from escpos.printer import Usb

## Event Name String - This will be on each printout. You can leave it blank if you like
EVENT_PRINT_STRING = "East Bay Mini Maker Faire 2019\n"
#EVENT_PRINT_STRING = "\n"

## USB IDs for our receipt printer. You can get these using the lsusb command
PRINTER_VENDOR_ID = 0x0471
PRINTER_PRODUCT_ID = 0x0055

## Initalize the printer
while True:
    try:
        p = Usb(PRINTER_VENDOR_ID, PRINTER_PRODUCT_ID, 0, 0x82,0x02)
        break
    except USBNotFoundError:
        print("Turn on the printer!")
        time.sleep(3)

## Initalize the video camera and openCV
cap = cv2.VideoCapture(0)
cap.set(3,1280) # Image width in pixels
cap.set(4,720)  # Image height in pixels

## Draw the window
cv2.namedWindow('window', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('window', cv2.WND_PROP_FULLSCREEN,1)
cv2.resizeWindow('window',1280,720)
cv2.moveWindow('window',0,40)


## Main Loop

while True:
    ret, frame = cap.read()

    ## Prep image for display
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Color to gray scale

    ## Some examples apply a blur at this point to reduce noise. Try as an experiment?
    gray = cv2.GaussianBlur(gray, (3,3), 0)

    # Canny thresholds calculations
    threshold_lower = 60 # originals from Ray
    threshold_upper = 60

    # auto_canny from
    # https://www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/
    # sigma = 0.33 # Auto threshold setting parameter
    # v = np.median(gray)
    # threshold_lower = int(max(0, (1.0 - sigma) * v))
    # threshold_upper = int(min(255, (1.0 + sigma) * v))
    # print("median=", v, " lower=", threshold_lower, " upper=", threshold_upper, "/n")
    can_image = cv2.Canny(gray, threshold_lower, threshold_upper) # Edge detection
    
    image1 = cv2.bitwise_not(can_image) # Flip black for white

    img = cv2.flip(image1,1) # Flip left for right (mirror)

    # Display the image
    cv2.imshow('window', img)

    c = cv2.waitKey(10) # Loop every 10 ms. If timeout, return val is -1.

    if 'X' == chr(c & 255):  #if the keypress is "X", bail out and quit the program
        break

    ## PRINT Handler
    if 'P' == chr(c & 255):  #if keypress "P", then print the current frame and reset
        image2=cv2.resize(image1,(1024,576), interpolation = cv2.INTER_AREA)
        image3=cv2.rotate(image2,cv2.ROTATE_90_CLOCKWISE)
        cv2.imwrite("test1.jpg",image3)

        # at this point the file "test1.jpg" holds the current frame picture ready to go
        p.set()
        p.set(font='b', align='center', width=2, height=2)
        p.text("Ace Monster Toys\n")
        p.text(EVENT_PRINT_STRING)
        p.set(font='a', align='center', width=1, height=1)
        p.text("http://acemonstertoys.org\n")
        p.set(font='b', align='center')
        p.text("A Makerspace in Oakland, CA Presents\n")
        p.set(font='b', align='center', width=2, height=3)
        p.text("The Edgy Printacular!\n")

        p.set(font='b')
        p.text(" \n")
        p.image("test1.jpg")
        p.cut()
        p.set()

cap.release()
cv2.destroyAllWindows()
