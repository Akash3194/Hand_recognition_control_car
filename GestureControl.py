##To control with hands we need to get hand recognised
## for that we used opencv vision library in python
##First of al, what we did is started camera and applied opencv algorithms on it
##The picture that Camera get, first we blur the image and then convert it into grey scale from BGR(Black,green red by which image forms)
##when we convert the picture then we apply threshold in this so that the picture now have only two types of color black an white
## it measn it will convert every image into pure black and white
##the object is converted into white and rest background in black
##after getting the object in white we draw lines around its perimeter which is called COUNTOUR
##After drawing contour we will calculate its defect, for examples which is the space between the fingures
##we calculate the defects by the traingle rule because it makes the triangle between to fingures, and then as many as defects there wil be 1 minus fingures
##with the help of this we calculate the fingures
##Then we draw a rotating rectngle around the hand which can give us the angle of the rotating
##As we get the rotating angle ang number of fingures, Now we will make a program that will give command according to the angle
##and according to the number of fingures.

import cv2
import numpy as np
import math
import pyfirmata

# (These are the variables to store Arduino differebt pins to give commands)
port = 'COM5'
board = pyfirmata.Arduino(port)
f_right_tyre = board.get_pin('d:3:p')
b_right_tyre = board.get_pin('d:9:p')
f_left_tyre = board.get_pin('d:5:p')
b_left_tyre = board.get_pin('d:11:p')

# (It is to start Front Camera)
cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()
    cv2.rectangle(frame, (80, 80), (450, 400), (0, 255, 0),
                  0)  # it will draw a rectangle where we will place our hand to recognize the hand for accurate results
    crop_img = frame[80:400, 80:450]
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)  # converts the image to bgray
    blur = cv2.GaussianBlur(gray, (41, 41), 0)  # blur the gray image
    ret, thresh1 = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)  # threshold it
    im2, contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE,
                                                cv2.CHAIN_APPROX_SIMPLE)  # find the perimetrer to draw lines around hand
    n = []  # to store area
    j = 0
    for k in contours:
        n.append(cv2.contourArea(k))
        j += 1
        if j == len(contours):
            g = max(n)
            p = n.index(g)  # this is to calculate the maximum area and it will select the object having maximum area

    cnt = contours[p]
    hull = cv2.convexHull(cnt, returnPoints=False)
    count_defects = 0
    defects = cv2.convexityDefects(cnt, hull)  # calculates the total defects

    cv2.drawContours(crop_img, contours, p, (0, 255, 0), 3)  # to draw the contours
    rect = cv2.minAreaRect(cnt)  # this is to create a rectangle around minimum boundary of the object which is focused
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    angal = (abs(rect[
                     2]))  # abs is absolute value and angal here is +ve value of rect[2] which is angle of the box we drawn around hands
    print(angal)
    cv2.drawContours(crop_img, [box], 0, (0, 0, 255), 2)
    # cv2.drawContours(crop_img, hull, -1, (0,255,0), 3)



    # () below code will draw a dot at the edge of fingure or can say it will draw the defect
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])

        # find length of all sides of triangle
        a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
        b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
        c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)

        # apply cosine rule here
        angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57

        # ignore angles > 90 and highlight rest with red dots
        if angle <= 90:
            count_defects += 1
            cv2.circle(crop_img, far, 1, [0, 0, 255], -1)
        cv2.line(crop_img, start, end, [0, 255, 0], 2)

    if count_defects == 1:
        print("moving forward")
        f_right_tyre.write(1)
        f_left_tyre.write(1)
    elif count_defects == 2:
        b_right_tyre.write(1)
        b_left_tyre.write(1)
        print("move backward")


    elif count_defects == 3 and angal > 0 and angal < 10:
        # straight
        b_right_tyre.write(0.5)
        b_left_tyre.write(0.5)
        print("moving backward straight")

    elif count_defects == 3 and angal < 50 and angal > 10:
        # turn right
        print("moving backward and turning right")
        f_right_tyre.write(0.2)
        b_left_tyre.write(0.5)
    elif count_defects == 3 and angal > 52:
        # turn left
        print("moving backward and turning left")
        b_right_tyre.write(0.5)
        f_left_tyre.write(0.2)


    elif count_defects == 4 and angal < 50 and angal > 10:
        print("moving forward and turning right")
        b_right_tyre.write(0.2)
        f_left_tyre.write(0.5)
    elif count_defects == 4 and angal > 52:
        print("moving forward and turning left")
        f_right_tyre.write(0.5)
        b_left_tyre.write(0.2)
    elif count_defects == 4 and angal > 0 and angal < 10:
        print("Moving forward straight")
        f_right_tyre.write(0.5)
        f_left_tyre.write(0.5)

    else:
        print("yes")
        f_right_tyre.write(0)
        f_left_tyre.write(0)
        b_right_tyre.write(0)
        b_left_tyre.write(0)
        # cv2.putText(frame,"Stop", (50, 50),
        #           cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        #   out.write(frame)
    cv2.imshow('m', thresh1)
    cv2.imshow('y', crop_img)
    cv2.imshow('s', frame)
    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break

cap.release()
# out.release()
cv2.destroyAllWindows()