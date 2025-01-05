from flask import Flask, render_template, request, jsonify
import threading
import cv2
import time
import winsound
import smtplib
from email.mime.text import MIMEText
# Flask app setup
app = Flask(__name__)
# Email configuration
EMAIL_ADDRESS = "parthu0497@gmail.com"
EMAIL_PASSWORD = "rqejsohnrcqeiaeg"
RECIPIENT_EMAIL = "ladshiv9086@gmail.com"
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
# Eye detection function
def eye_detection():
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    cap = cv2.VideoCapture(0)
    eye_closed_start_time = None
    beep_count = 0
    email_sent = False
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
        if len(eyes) == 0:
            if eye_closed_start_time is None:
                eye_closed_start_time = time.time()
            else:
                eye_closed_duration = time.time() - eye_closed_start_time
                if eye_closed_duration > 2:
                    winsound.Beep(1000, 1000)
                    beep_count += 1
                    print(f"Beep count: {beep_count}")
                    eye_closed_start_time = time.time()
                    if beep_count > 2 and not email_sent:
                        send_email()
                        email_sent = True
        else:
            eye_closed_start_time = None
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        cv2.imshow('Eye Detector', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
# Flask routes
@app.route("/")
def index():
    return render_template("index.html")  # Your HTML file
@app.route("/start_detection", methods=["POST"])
def start_detection():
    threading.Thread(target=eye_detection, daemon=True).start()
    return jsonify({"status": "Eye detection started."})
if __name__ == "__main__":
    app.run(debug=True)