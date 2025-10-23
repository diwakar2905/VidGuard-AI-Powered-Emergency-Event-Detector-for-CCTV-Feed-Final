import cv2
import numpy as np

def analyze_video_opencv(video_path):
    """
    OpenCV se video analyze karo (motion, fire, no motion detection).
    """
    cap = cv2.VideoCapture(video_path)
    prev_frame = None
    events = []
    frame_count = 0
    no_motion_frames = 0
    fps = cap.get(cv2.CAP_PROP_FPS) or 25

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if prev_frame is None:
            prev_frame = gray
            continue

        # Motion detection
        frame_delta = cv2.absdiff(prev_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        motion = cv2.countNonZero(thresh)

        # Fire-like color detection (lots of red/orange)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_fire = np.array([10, 100, 100])
        upper_fire = np.array([25, 255, 255])
        fire_mask = cv2.inRange(hsv, lower_fire, upper_fire)
        fire_pixels = cv2.countNonZero(fire_mask)

        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) // 1000
        time_str = f"{int(timestamp//60):02d}:{int(timestamp%60):02d}"

        # Large motion = possible fight/accident
        if motion > 10000:
            events.append({
                "label": "large_motion",
                "timestamp": time_str,
                "score": float(motion) / (frame.shape[0]*frame.shape[1])
            })
            no_motion_frames = 0
        # Fire color detected
        elif fire_pixels > 5000:
            events.append({
                "label": "fire_detected",
                "timestamp": time_str,
                "score": float(fire_pixels) / (frame.shape[0]*frame.shape[1])
            })
            no_motion_frames = 0
        # No motion for 5 seconds = possible fall/collapse
        elif motion < 100:
            no_motion_frames += 1
            if no_motion_frames > fps * 5:
                events.append({
                    "label": "no_motion_long",
                    "timestamp": time_str,
                    "score": 1.0
                })
                no_motion_frames = 0
        else:
            no_motion_frames = 0

        prev_frame = gray
        frame_count += 1

    cap.release()
    return {"events": events}
