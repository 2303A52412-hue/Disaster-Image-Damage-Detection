import cv2
import numpy as np
import os

def detect_damage(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (900, 600))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect irregular debris texture
    lap = cv2.Laplacian(gray, cv2.CV_64F)
    lap = np.uint8(np.absolute(lap))

    _, thresh = cv2.threshold(lap, 35, 255, cv2.THRESH_BINARY)

    kernel = np.ones((5,5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    img_h = img.shape[0]
    floor_pixel = img_h // 10

    for cnt in contours:
        area = cv2.contourArea(cnt)

        # Ignore smooth wall areas
        if 3000 < area < 50000:
            x, y, w, h = cv2.boundingRect(cnt)

            floors = max(1, h // floor_pixel)

            cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255), 3)
            cv2.putText(img, f"Damage ~ {floors} floors",
                        (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0,0,255), 2)

    os.makedirs('static', exist_ok=True)
    output_path = 'static/output.jpg'
    cv2.imwrite(output_path, img)

    return output_path