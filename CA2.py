import cv2
import numpy as np

webCamFeed = False 
pathImage = "Images\\image.jpg"
cap = cv2.VideoCapture(0)
cap.set(10, 160)
heightImg = 480
widthImg = 640

count = 0

while True:
    # input is either webcam or image
    if webCamFeed:
        success, img = cap.read()
    else:
        img = cv2.imread(pathImage)
    # RESIZE IMAGE
    #img = cv2.resize(img, (widthImg, heightImg))
    # CREATE A BLANK IMAGE FOR TESTING DEBUGING IF REQUIRED
    #imgBlank = np.zeros((heightImg, widthImg, 3), np.uint8)
    # CONVERT IMAGE TO GRAY SCALE
    #imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)  # ADD GAUSSIAN BLUR
    # thres = valTrackbars()  # GET TRACK BAR VALUES FOR THRESHOLDS
    #imgCanny = cv2.Canny(imgBlur, 150, 200)  # APPLY CANNY BLUR
    #kernel = np.ones((5, 5))
    #imgDial = cv2.dilate(imgCanny, kernel, iterations=2)  # APPLY DILATION
    # imgThreshold = cv2.erode(imgDial, kernel, iterations=1)  # APPLY EROSION
    cv2.imshow("1. Original", img)
    
    if cv2.waitKey(10 & 0XFF) == ord('x'):
        break