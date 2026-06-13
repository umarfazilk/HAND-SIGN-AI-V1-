import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
            model_complexity=0
        )

        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, frame):
        small_frame = cv2.resize(frame, (320, 240))
        rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        landmarks = []

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:

                # 🔥 Draw LIGHT skeleton (less lag)
                self.mp_draw.draw_landmarks(
                    frame,
                    handLms,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_draw.DrawingSpec(color=(0,255,255), thickness=1, circle_radius=1),
                    self.mp_draw.DrawingSpec(color=(0,100,255), thickness=1)
                )

                for id, lm in enumerate(handLms.landmark):
                    h, w, _ = frame.shape
                    cx = int(lm.x * w)
                    cy = int(lm.y * h)
                    landmarks.append((id, cx, cy))

        return frame, landmarks