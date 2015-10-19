import cv2
import time
from subprocess import call

NOTES = [130.8, 146.8, 164.8, 174.6, 195.0, 220.0, 246.9, 261.6]
SCREEN_TIME = 3000
LASER_WIDTH = 5

mask = 0
tZero = int(round(time.time() * 1000))
lastLaserPosition = 0xBADBEEF

cv2.namedWindow("preview")
vc = cv2.VideoCapture(1)

substractor = cv2.BackgroundSubtractorMOG()

if vc.isOpened():  # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    rval, frame = vc.read()

    frame = cv2.GaussianBlur(frame, (21, 21), 0)

    mask = substractor.apply(frame, mask)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    coolImage = cv2.bitwise_and(frame, frame, mask=mask)

    # Draw lines
    height = len(coolImage)
    width = len(coolImage[0])
    cv2.line(coolImage, (width / 6, 0), (width / 6, height), (0, 0, 255))
    cv2.line(coolImage, (width / 2, 0), (width / 2, height), (0, 0, 255))
    cv2.line(coolImage, (width * 5 / 6, 0), (width * 5 / 6, height), (0, 0, 255))

    # Draw the laser
    millis = int(round(time.time() * 1000))
    laserPosition = ((millis - tZero) % SCREEN_TIME) * width / SCREEN_TIME
    cv2.line(coolImage, (laserPosition, 0), (laserPosition, height), (0, 255, 0), LASER_WIDTH)

    cv2.imshow("preview", coolImage)

    if (abs(laserPosition - lastLaserPosition) > LASER_WIDTH or lastLaserPosition == 0xBADBEEF):
        filteredPos = filter(lambda pos: abs(pos - laserPosition) < LASER_WIDTH, [width / 6, width / 2, width * 5 / 6])

        if (len(filteredPos) > 0):
            posToCheck = filteredPos[0]

            for i in range(0, len(coolImage)):
                if (mask[i][posToCheck]):
                    call(["python", "music.py", "44100", str(height - i), str(0.75)])
                    print "position : " + str(posToCheck) + " " + str(i) + "\n\n\n"
                    break

        lastLaserPosition = laserPosition

    key = cv2.waitKey(10)
    if key == 27:  # exit on ESC
        break
cv2.destroyWindow("preview")
