import cv2
import mediapipe as mp
import pyautogui
screen_w,screen_h =pyautogui.size()
index_y=0
def track_hand_landmarks():
    # Initialize VideoCapture and MediaPipe Hands
    cap = cv2.VideoCapture(0)
    hand_detector = mp.solutions.hands.Hands()
    drawing_utils = mp.solutions.drawing_utils

    # Initialize list to store positions of the index finger tip
    positions = []
    circle_radius = 10
    line_thickness = circle_radius

    while True:
        # Capture frame-by-frame
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame_h, frame_w, _ = frame.shape

        # Convert frame to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = hand_detector.process(rgb_frame)
        hands = output.multi_hand_landmarks

        # Draw landmarks and lines connecting the index finger tips
        if hands:
            for hand in hands:
                drawing_utils.draw_landmarks(frame, hand)
                landmarks = hand.landmark
                index_tip_position = None
                for id, landmark in enumerate(landmarks):
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)
                    if id == 8:  # Index finger tip
                        index_x = screen_w / frame_w * x
                        index_y = screen_h / frame_h * y
                        index_tip_position = (x, y)

                        # Add current position to the list
                        positions.append((x, y))
                        # Draw a circle at the current position
                        cv2.circle(frame, (x, y), circle_radius, (0, 255, 0), -1)  # Green circle with radius 10
                        # Draw lines connecting previous positions
                        if len(positions) > 1:
                            for i in range(len(positions) - 1):
                                cv2.line(frame, positions[i], positions[i + 1], (0, 255, 0), line_thickness)  # Green line with thickness 10
                        # Optionally, limit the number of stored positions to avoid memory issues
                        if len(positions) > 10000:  # Adjust the limit as needed
                            positions.pop(0)
                            # Remove the oldest position
                    if id == 12:
                        cv2.circle(frame, (x, y), 10, (0, 255, 255))
                        thumb_x = screen_w / frame_w * x
                        thumb_y = screen_h / frame_h * y
                        print(abs(thumb_y-index_y))
                        if abs(thumb_y - index_y) < 60:
                            positions.clear()


        # Display the resulting frame
        cv2.imshow('Virtual Pen with finger', frame)

        # Break loop on 'Esc' key press
        key = cv2.waitKey(1)
        if key == 27:
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

# Call the function to start tracking hand landmarks
if __name__ == "__main__":
    track_hand_landmarks()
