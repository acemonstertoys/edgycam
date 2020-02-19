# edgycam
Code for the EdgyCam kiosk

The kiosk is a cabinet that contains 
1) A Raspberry Pi computer
2) A USB webcam
3) A video monitor
4) A receipt printer
5) A big red button

Users stand in front. The webcam is looking at them. On the screen is displayed a full screen image of the scene turned into a line drawing using the openCV.canny (https://pypi.org/project/opencv-python/). When the big red button is pressed, the image is printed on the receipt printer.


Currently installed versions of things

OpenCV = 3.4.1

escpos = 2.2.0

numpy = 1.12.1

Camera default parameters in openCV for Microsoft HD USB Camera
CAP_PROP_FRAME_WIDTH = 640
CAP_PROP_FRAME_HEIGHT = 480
CAP_PROP_FPS = 30
CAP_PROP_FORMAT = 16
CAP_PROP_CONTRAST = 0.5
CAP_PROP_EXPOSURE = inf
