import serial
import cv2
import time
import mediapipe as mp

# Initialize serial communication with Arduino
arduino = serial.Serial('COM3', 9600)
time.sleep(2)  # Allow Arduino to initialize

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Initialize video capture
cap = cv2.VideoCapture(0)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        # Flip the frame horizontally for natural hand gestures
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe Hands
        results = hands.process(rgb_frame)

        # Initialize flags
        two_fingers_detected = False
        three_fingers_detected = False

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get the landmarks of the hand
                landmarks = hand_landmarks.landmark

                # Check fingers' status based on landmarks
                finger_status = []
                for tip_idx, pip_idx in [(8, 6), (12, 10), (16, 14), (20, 18)]:
                    finger_status.append(landmarks[tip_idx].y < landmarks[pip_idx].y)

                # Count raised fingers (excluding thumb)
                raised_fingers = sum(finger_status)

                if raised_fingers == 2:
                    two_fingers_detected = True
                    arduino.write(b'2')  # Send signal for 2 fingers
                    print("2 fingers detected: LED on pin 2 ON")
                elif raised_fingers == 3:
                    three_fingers_detected = True
                    arduino.write(b'3')  # Send signal for 3 fingers
                    print("3 fingers detected: LED on pin 3 ON")
                else:
                    arduino.write(b'0')  # No fingers or different count
                    print("No relevant gesture detected")

        # Display the output frame
        cv2.imshow('Hand Gesture Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('a'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    arduino.close()
