import cv2
import time
import winsound
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
cap = cv2.VideoCapture(0)
eye_closed_start_time = None
eye_closed_duration_threshold = 3 
def play_sound():
    winsound.Beep(1000, 1000) 
while True:
   
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
   
    if len(eyes) == 0:
        if eye_closed_start_time is None:
            eye_closed_start_time = time.time()
        else:
            eye_closed_duration = time.time() - eye_closed_start_time
            if eye_closed_duration > eye_closed_duration_threshold:
                play_sound()
                
                eye_closed_start_time = time.time()
    else:
        eye_closed_start_time = None
   
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    cv2.imshow('Eye Detector', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()