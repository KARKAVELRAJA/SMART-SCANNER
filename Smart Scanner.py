# Importing Necessary Libraries
import urllib.request as request
import numpy as np
from PIL import Image
import time
import cv2

# Video Capturing URL
url = "http://192.168.43.1:8080/shot.jpg"

while True:
    # Opening and Decoding the Video
    img       = request.urlopen(url)
    img_bytes = bytearray(img.read())
    img_np    = np.array(img_bytes, dtype=np.uint8)
    frame     = cv2.imdecode(img_np, -1)
    
    # Pre-Processing the Video
    frame_cvt  = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_blur = cv2.GaussianBlur(frame_cvt, (5,5), 0)
    frame_edge = cv2.Canny(frame_blur, 30, 50)
    
    # Obtaining the Contours
    contours, h = cv2.findContours(frame_edge, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    # Obtaining the Maximum Contour
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(max_contour)
        
        # Displaying, Scanning and Saving the Result
        if cv2.contourArea(max_contour) > 5000:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
            object_only = frame[y:y+h, x:x+w]
            cv2.imshow("Smart Scanner", frame)
            if cv2.waitKey(1) == ord('s'):
                img_pil  = Image.fromarray(object_only)
                time_str = time.strftime('%Y-%m-%d-%H-%M-%S')
                img_pil.save(f'{time_str}.pdf')
                print(time_str)