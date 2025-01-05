import cv2
import time
import winsound
import smtplib
from email.mime.text import MIMEText

# Email configuration
EMAIL_ADDRESS = "parthu0497@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "rqejsohnrcqeiaeg"         # Replace with your email password
RECIPIENT_EMAIL = "ladshiv9086@gmail.com" # Replace with the recipient's email

def send_email():
    try:
        subject = "Alert: Eyes Closed!"
        body = "Alert!! Feeling Sleepy or Eyes are closed."
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = RECIPIENT_EMAIL

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())

        print("Alert email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Load the cascade for eye detection
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Capture video from webcam
cap = cv2.VideoCapture(0)

eye_closed_start_time = None
beep_count = 0
email_sent = False

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect eyes
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

    # Check if eyes are detected
    if len(eyes) == 0:
        if eye_closed_start_time is None:
            eye_closed_start_time = time.time()
        else:
            eye_closed_duration = time.time() - eye_closed_start_time
            if eye_closed_duration > 2:  # Trigger alert after 2 seconds
                winsound.Beep(1000, 1000)  # Frequency: 1000 Hz, Duration: 1000 ms
                beep_count += 1
                print(f"Beep count: {beep_count}")

                # Reset the timer after playing the sound to avoid continuous beeping
                eye_closed_start_time = time.time()

                # Send email if beep count exceeds 2 and email hasn't been sent yet
                if beep_count > 2 and not email_sent:
                    send_email()
                    email_sent = True
    else:
        eye_closed_start_time = None

    # Draw rectangles around detected eyes
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Eye Detector', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
