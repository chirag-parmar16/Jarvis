"""
J.A.R.V.I.S - MARK XXXVII
Computer Vision Interaction Module
--------------------------------------------------------------------------------
Uses OpenCV + Mediapipe for:
  1. Live camera feed -> pushed to JarvisUI.update_camera_frame()
  2. Hand gesture recognition (Palm, Thumbs Up, Thumbs Down, Fist)
  3. Presence detection (face in frame)
--------------------------------------------------------------------------------
"""

from __future__ import annotations

import threading
import time
from typing import Callable, Optional

# -- Optional imports ----------------------------------------------------------

try:
    import cv2
    _CV2 = True
except ImportError:
    _CV2 = False
    print("[VisionMgr] cv2 not installed - camera feed disabled.")

try:
    import mediapipe as mp
    # Mediapipe >= 0.10 uses the new Tasks API
    from mediapipe.tasks import python as mp_python
    from mediapipe.tasks.python import vision as mp_vision
    _MP = True
    _MP_NEW = True
except Exception:
    _MP = False
    _MP_NEW = False
    print("[VisionMgr] mediapipe not available - gestures disabled.")

try:
    import numpy as np
    _NP = True
except ImportError:
    _NP = False


# =============================================================================
#  GESTURE LOGIC  (landmark-based, model-agnostic)
# =============================================================================

def _finger_up(lm, tip: int, pip: int) -> bool:
    return lm[tip].y < lm[pip].y


def _count_fingers(lm) -> int:
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    return sum(1 for t, pp in zip(tips, pips) if _finger_up(lm, t, pp))


def _thumb_up(lm) -> bool:
    tip, wrist = lm[4], lm[0]
    mid = lm[9]
    return tip.y < wrist.y - 0.10 and tip.y < mid.y


def _thumb_down(lm) -> bool:
    tip, wrist = lm[4], lm[0]
    mid = lm[9]
    return tip.y > wrist.y + 0.08 and tip.y > mid.y


def classify_gesture(lm) -> str | None:
    if not lm:
        return None
    fingers = _count_fingers(lm)
    thm_up  = _thumb_up(lm)
    thm_dn  = _thumb_down(lm)

    if fingers >= 4:
        return "OPEN_PALM"
    if thm_up and fingers <= 1:
        return "THUMBS_UP"
    if thm_dn and fingers <= 1:
        return "THUMBS_DOWN"
    if fingers == 0:
        return "FIST"
    return None


# =============================================================================
#  MEDIAPIPE WRAPPER  (supports both legacy and new Task API)
# =============================================================================

class _HandDetector:
    """Thin wrapper that works with whichever mediapipe API is available."""

    def __init__(self):
        self._hands = None
        self._init()

    def _init(self):
        try:
            # Try legacy solutions API first (older pip installs sometimes keep it)
            import mediapipe as mp
            sol = getattr(mp, "solutions", None)
            if sol is not None:
                self._hands = sol.hands.Hands(
                    static_image_mode=False,
                    max_num_hands=1,
                    min_detection_confidence=0.6,
                    min_tracking_confidence=0.55,
                )
                self._mode = "legacy"
                print("[VisionMgr] Hand detector: legacy solutions API")
                return
        except Exception:
            pass

        # New Tasks API
        try:
            import mediapipe as mp
            base_opts = mp.tasks.BaseOptions(
                model_asset_path=self._download_model(),
            )
            opts = mp.tasks.vision.HandLandmarkerOptions(
                base_options=base_opts,
                running_mode=mp.tasks.vision.RunningMode.VIDEO,
                num_hands=1,
                min_hand_detection_confidence=0.6,
                min_hand_presence_confidence=0.5,
            )
            self._hands = mp.tasks.vision.HandLandmarker.create_from_options(opts)
            self._mode  = "tasks"
            self._ts    = 0
            print("[VisionMgr] Hand detector: Tasks API")
        except Exception as e:
            print(f"[VisionMgr] Hand detector unavailable: {e}")
            self._hands = None
            self._mode  = "none"

    def _download_model(self) -> str:
        import urllib.request, os
        path = os.path.join(os.path.dirname(__file__), "hand_landmarker.task")
        if not os.path.exists(path):
            url = ("https://storage.googleapis.com/mediapipe-models/"
                   "hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task")
            print("[VisionMgr] Downloading hand_landmarker model...")
            urllib.request.urlretrieve(url, path)
            print("[VisionMgr] Model downloaded.")
        return path

    def detect(self, rgb_frame, timestamp_ms: int = 0):
        """Returns list-of-landmark-lists (one per hand) or []."""
        if self._hands is None:
            return []

        if self._mode == "legacy":
            res = self._hands.process(rgb_frame)
            if res.multi_hand_landmarks:
                return [hl.landmark for hl in res.multi_hand_landmarks]
            return []

        if self._mode == "tasks":
            import mediapipe as mp
            mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            res    = self._hands.detect_for_video(mp_img, timestamp_ms)
            if res.hand_landmarks:
                return [hand for hand in res.hand_landmarks]
            return []

        return []

    def draw(self, bgr_frame, landmarks_list, rgb_frame):
        """Draw hand skeleton overlay (legacy API only)."""
        if self._mode != "legacy":
            return bgr_frame
        try:
            import mediapipe as mp
            sol = mp.solutions
            for lm in landmarks_list:
                # lm here is a NormalizedLandmarkList-compatible object
                pass  # drawing optional
        except Exception:
            pass
        return bgr_frame

    def close(self):
        if self._hands and hasattr(self._hands, "close"):
            self._hands.close()


# =============================================================================
#  VISION MANAGER
# =============================================================================

class VisionManager:
    """
    Runs the camera in a background thread.
    Pushes frames to JarvisUI and dispatches gesture events.

    AUTO-MUTE FIX: Gestures only show an overlay label.
    Mute/unmute is NOT triggered automatically — user controls it manually (F4).
    A gesture must be held for CONFIRM_FRAMES consecutive frames before firing.
    """

    GESTURE_COOLDOWN  = 3.0   # seconds between repeated gesture events
    CONFIRM_FRAMES    = 8     # frames gesture must be held (~0.33s at 24fps)

    def __init__(self, ui=None, camera_index: int = 0):
        self._ui           = ui
        self._camera_index = camera_index
        self._running      = False
        self._thread: Optional[threading.Thread] = None

        # Public callbacks
        self.on_gesture:  Callable[[str], None] | None = None
        self.on_presence: Callable[[bool], None] | None = None

        self._last_gesture_time  = 0.0
        self._last_gesture_label = ""
        self._presence           = False

        self._pending_gesture   = ""
        self._pending_count     = 0
        self._notified_ready    = False

        self._latest_jpeg       = None
        self._jpeg_lock         = threading.Lock()
        self._jpeg_counter      = 0

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
        print("[VisionMgr] Started")

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

        detector = _HandDetector() if _MP else None
        ts_ms    = 0

        try:
            while self._running:
                ret, frame = cap.read()
                if not ret:
                    time.sleep(0.05)
                    continue

                frame  = cv2.flip(frame, 1)
                h, w   = frame.shape[:2]
                rgb    = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                ts_ms += 42  # ~24 fps timestamps

                # Notify UI that first frame is ready (only once)
                if self._ui and not self._notified_ready:
                    self._ui.notify_vision_ready()
                    self._notified_ready = True

                # Gesture detection with consecutive-frame confirmation
                raw_gesture = None
                if detector is not None:
                    lm_list = detector.detect(rgb, ts_ms)
                    for lm in lm_list:
                        raw_gesture = classify_gesture(lm)

                confirmed_gesture = self._confirm_gesture(raw_gesture)

                if confirmed_gesture:
                    self._dispatch_gesture(confirmed_gesture)

                # Push frame to UI
                if self._ui is not None:
                    try:
                        self._ui.update_camera_frame(frame.tobytes(), w, h)
                    except Exception:
                        pass

                # Encode a low-res JPEG for the LLM Live capture (throttle to ~8 FPS to save CPU)
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

                time.sleep(0.042)

        finally:
            cap.release()
            if detector:
                detector.close()

    def _confirm_gesture(self, gesture: str | None) -> str | None:
        """
        Require the same gesture for CONFIRM_FRAMES consecutive frames.
        Also enforce cooldown. Returns the gesture only when confirmed.
        """
        if gesture is None:
            # Reset pending on no detection
            self._pending_gesture = ""
            self._pending_count   = 0
            return None

        if gesture == self._pending_gesture:
            self._pending_count += 1
        else:
            # New gesture started — reset counter
            self._pending_gesture = gesture
            self._pending_count   = 1

        if self._pending_count < self.CONFIRM_FRAMES:
            return None  # Not held long enough yet

        # Gesture confirmed — check cooldown
        now = time.time()
        if (gesture != self._last_gesture_label or
                now - self._last_gesture_time > self.GESTURE_COOLDOWN):
            self._last_gesture_label = gesture
            self._last_gesture_time  = now
            # Reset so it won't fire again until released and re-held
            self._pending_count = 0
            return gesture

        return None

    def _open_camera(self):
        if not _CV2:
            return None
        # Use a unique set of indices to avoid redundant slow checks
        indices = []
        for i in [self._camera_index, 0, 1]:
            if i not in indices:
                indices.append(i)

        for idx in indices:
            try:
                # Use CAP_DSHOW for faster startup on Windows
                cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
                if cap.isOpened():
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                    cap.set(cv2.CAP_PROP_FPS,          24)
                    print(f"[VisionMgr] Camera at index {idx}")
                    return cap
                cap.release()
            except Exception:
                pass
        print("[VisionMgr] No camera found")
        return None

    def _dispatch_gesture(self, gesture: str):
        print(f"[VisionMgr] Gesture confirmed: {gesture}")
        label_map = {
            "OPEN_PALM":   "Ruko (Stop)",
            "THUMBS_UP":   "Theek hai (OK)",
            "THUMBS_DOWN": "Nahi (No)",
            "FIST":        "Pause",
        }
        # Show gesture label overlay on camera widget (UI only — NO auto-mute)
        if self._ui is not None:
            try:
                self._ui.on_gesture_detected(label_map.get(gesture, gesture))
            except Exception:
                pass

        # Notify external callback (e.g. send to JARVIS session)
        if self.on_gesture:
            try:
                self.on_gesture(gesture)
            except Exception as e:
                print(f"[VisionMgr] on_gesture error: {e}")



# =============================================================================
#  CONVENIENCE FACTORY
# =============================================================================

def start_vision(ui=None, camera_index: int = 0) -> VisionManager:
    """Create, start, and return a VisionManager."""
    vm = VisionManager(ui=ui, camera_index=camera_index)
    vm.start()
    return vm
