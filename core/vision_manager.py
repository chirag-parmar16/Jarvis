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
    _CV2 = True
except ImportError:
    _CV2 = False
    print("[VisionMgr] cv2 not installed - camera feed disabled.")

class VisionManager:
    """
    Runs the camera in a background thread.
    Pushes frames to JarvisUI for visual feedback and encodes JPEGs for Gemini.
    """

    def __init__(self, ui=None, camera_index: int = 0):
        self._ui           = ui
        self._camera_index = camera_index
        self._running      = False
        self._thread: Optional[threading.Thread] = None

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
        print("[VisionMgr] Started (Lite Mode)")

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

                time.sleep(0.042)

        finally:
            cap.release()

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
                    cap.set(cv2.CAP_PROP_FPS,          24)
                    print(f"[VisionMgr] Camera at index {idx}")
                    return cap
                cap.release()
            except Exception:
                pass
        print("[VisionMgr] No camera found")
        return None

def start_vision(ui=None, camera_index: int = 0) -> VisionManager:
    vm = VisionManager(ui=ui, camera_index=camera_index)
    vm.start()
    return vm
