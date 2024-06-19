from flask import Flask, render_template, Response
import cv2 as cv
import time
import mediapipe as mp
import posture_detection_module as pdm
import numpy as np

app = Flask(__name__)
cap = cv.VideoCapture(0)
pTime = 0
detector = pdm.poseDetector(detectioncon=0.8)

count = 0
dir = 0

def generate_frames():
    global pTime, count, dir
    while True:
        success, img = cap.read()
        if not success:
            break
        else:
            img = detector.findPose(img, draw=False)
            lmList = detector.findPosition(img, False)
            if len(lmList) != 0:
                angle = detector.findAngle(img, 12, 14, 16)
                if angle < 200 and angle > 0:
                    per = np.interp(angle, (60, 160), (100, 0))
                    bar = np.interp(angle, (60, 160), (100, 650))
                elif angle > 180 and angle <= 360:
                    angle = 360 - angle
                    per = np.interp(angle, (60, 160), (100, 0))
                    bar = np.interp(angle, (60, 160), (100, 650))

                color = (0, 0, 255)
                if per == 100:
                    color = (0, 255, 0)
                    if dir == 0:
                        count += 0.5
                        dir = 1
                if per == 0:
                    if dir == 1:
                        count += 0.5
                        dir = 0

                cv.rectangle(img, (1100, 100), (1175, 650), color, 2)
                cv.rectangle(img, (1100, int(bar)), (1175, 650), color, cv.FILLED)
                cv.putText(img, f'{int(per)}%', (1070, 75), cv.FONT_HERSHEY_COMPLEX_SMALL, 4, color, 4)

                cv.rectangle(img, (0, 450), (250, 720), (51, 51, 51), cv.FILLED)
                cv.putText(img, str(int(count)), (90, 620), cv.FONT_HERSHEY_COMPLEX_SMALL, 5, (255, 0, 0), 10)

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv.putText(img, f'FPS: {int(fps)}', (10, 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

            ret, buffer = cv.imencode('.jpg', img)
            img = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
