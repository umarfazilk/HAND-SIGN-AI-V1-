class GestureRecognizer:
    def __init__(self):
        self.tip_ids = [4, 8, 12, 16, 20]

    def get_finger_states(self, landmarks):
        if len(landmarks) != 21:
            return []

        fingers = []

        # Ignore thumb
        fingers.append(0)

        for i in range(1, 5):
            if landmarks[self.tip_ids[i]][2] < landmarks[self.tip_ids[i] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def recognize(self, landmarks):
        if len(landmarks) != 21:
            return ""

        fingers = self.get_finger_states(landmarks)

        print("Fingers:", fingers)

        if fingers == [0, 1, 0, 0, 0]:
            return "FOOD"

        if fingers == [0, 1, 1, 0, 0]:
            return "WATER"

        if fingers == [0, 0, 1, 1, 1]:
            return "MEDICINE"

        if fingers == [0, 1, 1, 1, 1]:
            return "REST"

        return ""