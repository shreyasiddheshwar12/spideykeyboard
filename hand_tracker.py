import os
import time
import math
import urllib.request
import cv2
import mediapipe as mp

MODEL_NAME = "hand_landmarker.task"
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"

def ensure_model():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), MODEL_NAME)
    if os.path.exists(path) and os.path.getsize(path) > 100000:
        return path
    print("Downloading MediaPipe hand model (first run only)...")
    try:
        urllib.request.urlretrieve(MODEL_URL, path)
    except Exception as e:
        if os.path.exists(path):
            try: os.remove(path)
            except OSError: pass
        raise RuntimeError("Could not download hand_landmarker.task. Connect to the internet and run python app.py again.") from e
    return path

class HandTracker:
    def __init__(self):
        model = ensure_model()
        options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=model),
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=0.55,
            min_hand_presence_confidence=0.55,
            min_tracking_confidence=0.55,
        )
        self.detector = mp.tasks.vision.HandLandmarker.create_from_options(options)
        self.timestamp = 0

    def process(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        self.timestamp += 1
        return self.detector.detect_for_video(image, self.timestamp)

    def get_index_fingertip(self, result, shape):
        if not result.hand_landmarks:
            return None
        h, w = shape[:2]
        p = result.hand_landmarks[0][8]
        return int(p.x * w), int(p.y * h)

    def is_pinching(self, result, shape):
        if not result.hand_landmarks:
            return False
        h, w = shape[:2]
        hand = result.hand_landmarks[0]
        dx = (hand[8].x - hand[4].x) * w
        dy = (hand[8].y - hand[4].y) * h
        return math.hypot(dx, dy) < 48

    def draw_landmarks(self, frame, result):
        if not result.hand_landmarks:
            return
        h, w = frame.shape[:2]
        connections = [(0,1),(1,2),(2,3),(3,4),(0,5),(5,6),(6,7),(7,8),(0,9),(9,10),(10,11),(11,12),(0,13),(13,14),(14,15),(15,16),(0,17),(17,18),(18,19),(19,20),(5,9),(9,13),(13,17)]
        for hand in result.hand_landmarks:
            for p in hand:
                cv2.circle(frame, (int(p.x*w), int(p.y*h)), 5, (0,255,0), -1)
            for a,b in connections:
                p1=(int(hand[a].x*w), int(hand[a].y*h))
                p2=(int(hand[b].x*w), int(hand[b].y*h))
                cv2.line(frame, p1, p2, (255,255,255), 2)

    def close(self):
        self.detector.close()
