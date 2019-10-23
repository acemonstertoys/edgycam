import cv2
import numpy as np

from escpos.printer import Usb
p = Usb(0x0471, 0x0055, 0, 0x82,0x02)
#p = File("/dev/usb/lp0")

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)


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
            p.text("East Bay Mini Maker Faire 2019\n")
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
