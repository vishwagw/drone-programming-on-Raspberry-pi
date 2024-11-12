import cv2 as cv

cap = cv.VideoCapture(0)

if cap.isOpened() == False:
    print('----')
    exit(1)

while(True):
    ret, img_frame = cap.read()
    if ret == False:
        print('---')
        break

    #change HSV space
    img_hsv = cv.cvtColor(img_frame, cv.COLOR_BGR2HSV)

    
    # find blue color's area by the value of Hue
    lower_blue = (120-20, 70, 0)
    upper_blue = (120+20, 255, 255)
    img_mask = cv.inRange(img_hsv, lower_blue, upper_blue)

    # improve binary image using morphology 
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (11, 11))
    img_mask = cv.morphologyEx(img_mask, cv.MORPH_CLOSE, kernel)

    # detect blue color's area from ariginal image
    img_result = cv.bitwise_and(img_frame, img_frame, mask=img_mask)

    # labeling
    nlabels, labels, stats, centroids = cv.connectedComponentsWithStats(img_mask)

    for i in range(nlabels):

        if i < 1:
            continue
        # Get information about the size, center coordinates, and bounding rectangle of the region. 
        area = stats[i, cv.CC_STAT_AREA]
        center_x = int(centroids[i, 0])
        center_y = int(centroids[i, 1])
        left = stats[i, cv.CC_STAT_LEFT]
        top = stats[i, cv.CC_STAT_TOP]
        width = stats[i, cv.CC_STAT_WIDTH]
        height = stats[i, cv.CC_STAT_HEIGHT]

        # if the size of area is 10000 over 
        # show the information of the area 
        if area > 10000:
            # draw the bouding rectangle of region
            cv.rectangle(img_frame, (left, top), (left + width, top + height), (0, 0, 255), 3)
            # draw the circle of the ceter coordinates
            cv.circle(img_frame, (center_x, center_y), 5, (255, 0, 0), 3)
            # show the number of label
            cv.putText(img_frame, str(i), (left + 20, top + 20), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

cap.release()
cv.destroyAllWindows()

