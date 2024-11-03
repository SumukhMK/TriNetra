from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import numpy as np

app = Flask(__name__)

# MediaPipe Face Mesh setup
mp_face_mesh = mp.solutions.face_mesh
LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]

def generate_iris_tracking():
    cap = cv2.VideoCapture(0)  # Capture from the webcam
    
    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)  # Flip the frame to provide mirror-like experience
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_h, img_w = frame.shape[:2]
            results = face_mesh.process(rgb_frame)

            if results.multi_face_landmarks:
                mesh_points = np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int) 
                                        for p in results.multi_face_landmarks[0].landmark])
                
                (l_cx, l_cy), l_radius = cv2.minEnclosingCircle(mesh_points[LEFT_IRIS])
                (r_cx, r_cy), r_radius = cv2.minEnclosingCircle(mesh_points[RIGHT_IRIS])
                
                center_left = np.array([l_cx, l_cy], dtype=np.int32)
                center_right = np.array([r_cx, r_cy], dtype=np.int32)
                
                cv2.circle(frame, center_left, int(l_radius), (255, 0, 255), 2)
                cv2.circle(frame, center_right, int(r_radius), (255, 0, 255), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/thrataka')
def thrataka():
    return render_template('thrataka.html')  # Ensure this template exists

@app.route('/saccades')
def saccades():
    return render_template('saccades.html')  # Ensure this template exists

@app.route('/balloon')
def balloon():
    return render_template('balloon.html')  # Ensure this template exists

@app.route('/video_feed')
def video_feed():
    return Response(generate_iris_tracking(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
