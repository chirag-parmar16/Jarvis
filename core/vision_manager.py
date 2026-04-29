"""
J.A.R.V.I.S - MARK XXXVII
Computer Vision Interaction Module
--------------------------------------------------------------------------------
Simplified version: Only stable camera feed, NO gesture recognition.
--------------------------------------------------------------------------------
"""

from __future__ import annotations
import threading
import time
from typing import Optional

try:
    import cv2
    import mediapipe as mp
    _CV2 = True
    _MP  = True
except ImportError:
    _CV2 = False
    _MP  = False
    print("[VisionMgr] cv2 or mediapipe not installed - camera/gestures disabled.")

class VisionManager:
    """
    Runs the camera in a background thread.
    Pushes frames to JarvisUI and performs real-time gesture classification.
    """

    def __init__(self, ui=None, camera_index: int = 0, on_interrupt=None):
        self._ui           = ui
        self._camera_index = camera_index
        self._on_interrupt = on_interrupt
        self._running      = False
        self._thread: Optional[threading.Thread] = None

        self._notified_ready    = False
        self._latest_jpeg       = None
        self._jpeg_lock         = threading.Lock()
        self._jpeg_counter      = 0

        # Gesture Debouncing
        self._fist_frames       = 0
        self._FIST_THRESHOLD    = 4  # Confirmation frames

        # MediaPipe Setup
        self._mp_hands = None
        if _MP:
            self._mp_hands = mp.solutions.hands.Hands(
                static_image_mode=False,
                max_num_hands=1,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.5
            )

    def get_latest_jpeg(self) -> bytes | None:
        """Returns the most recent camera frame as JPEG bytes, or None."""
        with self._jpeg_lock:
            return self._latest_jpeg

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread  = threading.Thread(
            target=self._run_loop,
            daemon=True,
            name="VisionManagerThread",
        )
        self._thread.start()
        print("[VisionMgr] Started (Gesture Mode)")

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=3)
        print("[VisionMgr] Stopped")

    def _run_loop(self):
        if not _CV2:
            print("[VisionMgr] cv2 unavailable - aborting")
            return

        cap = self._open_camera()
        if cap is None:
            if self._ui: self._ui.notify_vision_ready()
            return

        try:
            while self._running:
                ret, frame = cap.read()
                if not ret:
                    time.sleep(0.05)
                    continue

                frame = cv2.flip(frame, 1)
                h, w  = frame.shape[:2]
                
                # ── GESTURE CLASSIFICATION (MediaPipe) ──────────────────────────
                if self._mp_hands:
                    self._process_gestures(frame)

                # Notify UI that first frame is ready
                if self._ui and not self._notified_ready:
                    self._ui.notify_vision_ready()
                    self._notified_ready = True

                # Push frame to UI
                if self._ui is not None:
                    try:
                        self._ui.update_camera_frame(frame.tobytes(), w, h)
                    except Exception:
                        pass

                # Encode JPEG for Gemini Live capture (throttle to ~8 FPS)
                self._jpeg_counter += 1
                if self._jpeg_counter % 3 == 0:
                    try:
                        resized = cv2.resize(frame, (640, int(640 * (h/w))))
                        ret_enc, buf = cv2.imencode('.jpg', resized, [cv2.IMWRITE_JPEG_QUALITY, 50])
                        if ret_enc:
                            with self._jpeg_lock:
                                self._latest_jpeg = buf.tobytes()
                    except Exception:
                        pass

                time.sleep(0.033) # ~30 FPS loop for gesture responsiveness

        finally:
            cap.release()

    def _process_gestures(self, frame):
        # MediaPipe expects RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self._mp_hands.process(rgb)

        is_fist = False
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Logic: Check if fingers are folded.
                # Landmark 8 (Index Tip) < Landmark 6 (Index MCP) etc.
                # In normalized coords (0,0 is top-left), y increases downwards.
                # Tip.y > MCP.y means tip is below (folded).
                
                landmarks = hand_landmarks.landmark
                # Finger tips: 8, 12, 16, 20
                # Finger MCPs: 6, 10, 14, 18
                fingers_folded = []
                for tip, mcp in [(8, 6), (12, 10), (16, 14), (20, 18)]:
                    fingers_folded.append(landmarks[tip].y > landmarks[mcp].y)
                
                # Thumb check (X-axis distance from Pinky MCP)
                thumb_folded = False
                if landmarks[4].x > landmarks[3].x: # Right hand perspective simplified
                    thumb_folded = True
                
                if all(fingers_folded):
                    is_fist = True

        if is_fist:
            self._fist_frames += 1
            if self._fist_frames == self._FIST_THRESHOLD:
                print("[VisionMgr] ✋ FIST DETECTED - Triggering Interrupt")
                if self._ui: self._ui.on_gesture_detected("FIST")
                if self._on_interrupt:
                    # Execute callback in a safe way
                    self._on_interrupt()
        else:
            self._fist_frames = 0

    def _open_camera(self):
        if not _CV2:
            return None
        # Indices to try
        indices = [self._camera_index, 0, 1]
        seen = set()
        for idx in indices:
            if idx in seen: continue
            seen.add(idx)
            try:
                # Use CAP_DSHOW for stability/speed on Windows
                cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
                if cap.isOpened():
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                    cap.set(cv2.CAP_PROP_FPS,          30)
                    print(f"[VisionMgr] Camera at index {idx}")
                    return cap
                cap.release()
            except Exception:
                pass
        print("[VisionMgr] No camera found")
        return None

def start_vision(ui=None, camera_index: int = 0, on_interrupt=None) -> VisionManager:
    vm = VisionManager(ui=ui, camera_index=camera_index, on_interrupt=on_interrupt)
    vm.start()
    return vm
