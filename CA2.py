import cv2
import numpy as np
import utils

# function to initialize Trackbars
'''
def nothing(x):
    pass

def initializeTrackbars(initialTrackbarVal=125):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 360, 240)
    cv2.createTrackbar("Threshold1", "Trackbars", initialTrackbarVal, 255, nothing)
    cv2.createTrackbar("Threshold2", "Trackbars", initialTrackbarVal, 255, nothing)

def valTrackbars():
    Threshold1 = cv2.getTrackbarPos("Threshold1", "Trackbars")
    Threshold2 = cv2.getTrackbarPos("Threshold2", "Trackbars")
    src = Threshold1, Threshold2
    return src 
'''

webCamFeed = False  # no webcam available therefore set to False
pathImage = "Images//image004.jpg"
# main webcam -> 0
cap = cv2.VideoCapture(0)
cap.set(10, 160)
heightImg = 600
widthImg = 480
count = 0



utils.initializeTrackbars()


while True:
    # input is either webcam or image
    if webCamFeed:
        success, img = cap.read()
    else:
        img = cv2.imread(pathImage)
    # RESIZE IMAGE
    img = cv2.resize(img, (widthImg, heightImg))
    # CREATE A BLANK IMAGE FOR TESTING DEBUGING IF REQUIRED
    imgBlank = np.zeros((heightImg, widthImg, 3), np.uint8)
    # CONVERT IMAGE TO GRAY SCALE
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)  # ADD GAUSSIAN BLUR
    thres = utils.valTrackbars()  # GET TRACK BAR VALUES FOR THRESHOLDS
    imgCanny = cv2.Canny(imgBlur, thres[0], thres[1])  # APPLY CANNY BLUR
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=2)  # APPLY DILATION
    imgThreshold = cv2.erode(imgDial, kernel, iterations=1)  # APPLY EROSION
    
    imgContours = img.copy()
    imgBigContour = img.copy()

    contours, hierachy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(imgContours, contours, -1, (0,255,0), 10)
   
    biggest, maxArea  = utils.biggestContour(contours)
    print(f'Biggest not ordered: {biggest}')
   
    if biggest.size != 0:
        biggest = utils.reorder(biggest)
        print(f'Biggest reordered: {biggest}')
        imgBigContour = utils.drawRectangle(imgBigContour, biggest, 2)

        pts1 = np.float32(biggest)
        pts2 = np.float32([[0, 0],[heightImg, 0], [0, widthImg], [heightImg, widthImg]])
        matrix = cv2.getPerspectiveTransform(pts1,pts2)
        imgWarpColored = cv2.warpPerspective(img, matrix, (heightImg, widthImg))




    imgFinal = imgCanny
    
    cv2.imshow("1. Original", img)
    #cv2.imshow("2. Grayscale", imgGray)
    #cv2.imshow("3. Blur", imgBlur)
    #cv2.imshow("4. Canny", imgCanny)
    #cv2.imshow("5. Dilate", imgDial)
    cv2.imshow("6. Treshold", imgThreshold)
    cv2.imshow("7. imgContours", imgContours) #detects edges and contours
    cv2.imshow("8. imgBigContour", imgBigContour) #detects edges and contoursv
    cv2.imshow("9. imgWarpColored", imgWarpColored)

#user interaction 
    # Press x  on keyboard to  exit
    # Close and break the loop after pressing "x" key
    if cv2.waitKey(1) & 0XFF == ord('x'):
        break  # exit infinite loop

     # SAVE IMAGE WHEN 's' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('s'):
        print("saving")
        # save image to folder using cv2.imwrite()
        cv2.imwrite("Scanned/myImage"+str(count)+".jpg", imgFinal)
        cv2.waitKey(300)
        count += 1


# When everything done, release
# the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()