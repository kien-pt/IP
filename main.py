import cv2
import numpy as np
import imutils

image_origin = cv2.imread('logo_origin.png')
origin_height, origin_width, channels = image_origin.shape

grey_origin = cv2.imread('logo_origin.png', 0)
grey_template = cv2.imread('logo_template.png', 0)

grey_origin = cv2.bilateralFilter(grey_origin, 10, 20, 20)
grey_template = cv2.bilateralFilter(grey_template, 10, 20, 20)

for scale in np.arange(1, 0.25, -0.25):
    ok = False
    for threshold in np.arange(0.95, 0.5, -0.05):
        width = int(grey_template.shape[1] * scale)
        resized = imutils.resize(grey_template, width)
        for angle in np.arange(0, 360, 10):

            rotated = imutils.rotate_bound(resized, angle)
            w, h = rotated.shape[::-1]

            if (w >= origin_width and h >= origin_height):
                continue

            res = cv2.matchTemplate(grey_origin, rotated, cv2.TM_CCOEFF_NORMED)

            loc = np.where(res >= threshold)

            if loc:
                for pt in zip(*loc[::-1]):
                    print('Matching template size scale: ', round(scale, 2))
                    print('Matching template angle: ', round(angle, 2))
                    print('Matching template accepted threshold: ', round(threshold, 2))
                    cv2.rectangle(image_origin, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
                    ok = True
                    break

            if ok:
                break
        if ok:
            break
    if ok:
        break

cv2.imshow('Matched Template', image_origin)
cv2.waitKey(0)
cv2.destroyAllWindows()
