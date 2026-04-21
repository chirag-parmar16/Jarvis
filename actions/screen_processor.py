from __future__ import annotations

import io
from typing import Optional

try:
    import mss
    import mss.tools
    _MSS = True
except ImportError:
    _MSS = False

try:
    import PIL.Image
    _PIL = True
except ImportError:
    _PIL = False

_IMG_MAX_W = 640
_IMG_MAX_H = 360
_JPEG_Q    = 60

def _compress(img_bytes: bytes, source_format: str = "PNG") -> tuple[bytes, str]:
    if not _PIL:
        return img_bytes, f"image/{source_format.lower()}"

    try:
        img = PIL.Image.open(io.BytesIO(img_bytes)).convert("RGB")
        img.thumbnail((_IMG_MAX_W, _IMG_MAX_H), PIL.Image.BILINEAR)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=_JPEG_Q, optimize=False)
        return buf.getvalue(), "image/jpeg"
    except Exception as e:
        print(f"[Vision] ⚠️  Image compress failed: {e}")
        return img_bytes, f"image/{source_format.lower()}"

def _capture_screen() -> tuple[bytes, str]:
    if not _MSS:
        raise RuntimeError("mss is not installed. Run: pip install mss")

    with mss.mss() as sct:
        monitors = sct.monitors          # [0] = all combined, [1..n] = real screens
        target   = monitors[1] if len(monitors) > 1 else monitors[0]
        shot     = sct.grab(target)
        png      = mss.tools.to_png(shot.rgb, shot.size)

    return _compress(png, "PNG")

def screen_process(
    parameters:     dict,
    response=None,
    player=None,
    session_memory=None,
):
    params = parameters or {}
    angle  = params.get("angle", "screen").lower().strip()

    if angle == "camera":
        return "You are natively receiving camera frames. Skip using this tool to view the camera."

    try:
        image_bytes, mime_type = _capture_screen()
        print(f"[Vision] 🖥️  Screen captured: {len(image_bytes):,} bytes")
        return {"data": image_bytes, "mime_type": mime_type}
    except Exception as e:
        print(f"[Vision] ❌ Capture error: {e}")
        return f"Could not capture screen: {e}"

if __name__ == "__main__":
    print("[TEST] screen_processor.py")
    res = screen_process({"angle": "screen"})
    if isinstance(res, dict):
        print(f"Captured {len(res['data'])} bytes.")
    else:
        print(res)
