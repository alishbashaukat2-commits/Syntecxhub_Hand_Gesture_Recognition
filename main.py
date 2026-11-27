import math
import time
import cv2
import mediapipe as mp
import pyautogui
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# ---------- Model tayyar karna (video mode, sirf 1 haath) ----------
options = vision.HandLandmarkerOptions(
    base_options=python.BaseOptions(model_asset_path="hand_landmarker.task"),
    running_mode=vision.RunningMode.VIDEO,
    num_hands=1,
)
landmarker = vision.HandLandmarker.create_from_options(options)

# ---------- Haath ke points ko jodne wali lines ----------
CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17),
]

# Har ungli: (nok ka point, beech ke jod ka point)
FINGERS = [(8, 6), (12, 10), (16, 14), (20, 18)]

# Thumbs up detect na ho to 0.2 karein, fist se mix ho to 0.4 karein
THUMB_MARGIN = 0.3


def dist(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def get_gesture(hand):
    # Kitni ungliyan upar hain (y chhota matlab upar)
    fingers_up = sum(hand[tip].y < hand[pip].y for tip, pip in FINGERS)

    # Angootha tab "upar" hai jab uski nok, saari ungliyon ke knuckles se
    # kaafi upar ho (haath ke size ke hisaab se naapa gaya)
    hand_size = dist(hand[0], hand[9])
    knuckle_top = min(hand[5].y, hand[9].y, hand[13].y, hand[17].y)
    thumb_up = hand[4].y < knuckle_top - THUMB_MARGIN * hand_size

    if fingers_up == 4:
        return "OPEN PALM"
    if fingers_up == 0 and thumb_up:
        return "THUMBS UP"
    if fingers_up == 0:
        return "FIST"
    return "UNKNOWN"


# Gesture -> (key, kitni baar dabana, do actions ke beech gap in seconds)
ACTIONS = {
    "THUMBS UP": ("volumeup", 5, 0.4),
    "OPEN PALM": ("volumedown", 5, 0.4),
    "FIST": ("playpause", 1, 1.5),
}

actions_on = False       # shuru mein band (safe)
last_action_time = 0     # pichle action ka waqt
last_seen = ""           # pichla gesture
same_count = 0           # wahi gesture kitne frames se aa raha hai

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)                     # aaine jaisa video
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)   # MediaPipe ko RGB chahiye
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = landmarker.detect_for_video(mp_image, int(time.time() * 1000))

    gesture = "NO HAND"
    for hand in result.hand_landmarks:
        # 21 points ko pixel position mein badalna
        points = [(int(lm.x * w), int(lm.y * h)) for lm in hand]
        for a, b in CONNECTIONS:                   # lines
            cv2.line(frame, points[a], points[b], (0, 255, 0), 2)
        for p in points:                           # points
            cv2.circle(frame, p, 5, (0, 0, 255), -1)

        gesture = get_gesture(hand)

    # Gesture tabhi maana jaye jab 5 frames tak wahi rahe
    if gesture == last_seen:
        same_count += 1
    else:
        last_seen = gesture
        same_count = 1

    # Action (sirf jab ON ho aur gesture pakka ho)
    if actions_on and gesture in ACTIONS and same_count >= 5:
        key_name, presses, gap = ACTIONS[gesture]
        if time.time() - last_action_time > gap:
            pyautogui.press(key_name, presses=presses)
            last_action_time = time.time()

    # Screen par likhna
    cv2.putText(frame, f"Gesture: {gesture}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)
    status = "ON" if actions_on else "OFF"
    cv2.putText(frame, f"Actions: {status} (A = on/off, Q = quit)", (10, 65),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.imshow("Hand Gesture Recognition", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('a'):
        actions_on = not actions_on

cap.release()
cv2.destroyAllWindows()