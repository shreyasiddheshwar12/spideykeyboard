import cv2
import time
from hand_tracker import HandTracker
from keyboard import VirtualKeyboard

WIDTH, HEIGHT = 1280, 720

def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise RuntimeError("Webcam could not be opened. Check Windows Camera permissions.")

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

    tracker = HandTracker()
    keyboard = VirtualKeyboard(WIDTH, HEIGHT)

    last_press = 0.0
    cooldown = 0.65
    typed = ""

    print("\nGESTURE AIR KEYBOARD")
    print("--------------------")
    print("A camera window will open.")
    print("Move INDEX finger over the on-screen keyboard.")
    print("PINCH thumb + index to type.")
    print("Press Q to quit.\n")

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            frame = cv2.flip(frame, 1)
            result = tracker.process(frame)
            fingertip = tracker.get_index_fingertip(result, frame.shape)

            keyboard.highlight = None
            status = "Show your hand"

            if fingertip:
                x, y = fingertip
                key = keyboard.key_at(x, y)

                cv2.circle(frame, (x, y), 13, (0, 255, 255), 3)
                cv2.circle(frame, (x, y), 4, (0, 255, 255), -1)

                if key:
                    keyboard.highlight = key
                    status = f"Hovering: {key}"

                    if tracker.is_pinching(result, frame.shape):
                        now = time.monotonic()
                        if now - last_press >= cooldown:
                            keyboard.press(key)
                            last_press = now

                            if key == "SPACE":
                                typed += " "
                            elif key == "BACK":
                                typed = typed[:-1]
                            elif key == "ENTER":
                                typed += "\n"
                            else:
                                typed += key

                            status = f"Pressed: {key}"
                else:
                    status = "Move finger onto a key"

            cv2.rectangle(frame, (0, 0), (WIDTH, 92), (20, 20, 20), -1)
            cv2.putText(frame, "GESTURE AIR KEYBOARD", (25, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, status, (25, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.62, (0, 220, 255), 2, cv2.LINE_AA)

            preview = typed[-55:].replace("\n", " ")
            cv2.putText(frame, "Typed: " + preview, (500, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2, cv2.LINE_AA)

            keyboard.draw(frame)
            tracker.draw_landmarks(frame, result)

            cv2.putText(frame, "INDEX = MOVE   PINCH = PRESS   Q = QUIT", (25, HEIGHT - 12), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (230, 230, 230), 1, cv2.LINE_AA)
            cv2.imshow("Gesture Air Keyboard", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        tracker.close()

if __name__ == "__main__":
    main()
