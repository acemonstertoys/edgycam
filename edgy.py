import cv2
import numpy as np

## Event Name String - This will be on each printout. You can leave it blank if you like
EVENT_PRINT_STRING = "East Bay Mini Maker Faire 2019\n"
#EVENT_PRINT_STRING = "\n"

## USB IDs for our receipt printer. You can get these using the lsusb command
PRINTER_VENDOR_ID = 0x0471
PRINTER_PRODUCT_ID = 0x0055

## Initalize the printer
## TODO - Catch exception and put it a loop so will work if printer not turned on first.
from escpos.printer import Usb
p = Usb(PRINTER_VENDOR_ID, PRINTER_PRODUCT_ID, 0, 0x82,0x02)

## Initalize the video camera and openCV
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

## Draw the window
cv2.namedWindow('window', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('window', cv2.WND_PROP_FULLSCREEN,1)
cv2.resizeWindow('window',1280,720)
cv2.moveWindow('window',0,40)



while True:
        ret, frame = cap.read()
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        image1 = cv2.bitwise_not(cv2.Canny(gray,60,60))

        img = cv2.flip(image1,1)

        cv2.imshow('window', img)
        
        c = cv2.waitKey(1)
        
        if 'X' == chr(c & 255):  #if the keypress is "X", bail out and quit the program
            break
        
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
