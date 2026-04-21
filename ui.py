"""
J.A.R.V.I.S — MARK XXXVII
UI Module — PyQt6 Enhanced Edition
────────────────────────────────────────────────────────────────────────────────
All original public APIs are preserved:
  • JarvisUI(face_path, size=None)
  • ui.set_state(state)
  • ui.write_log(text)
  • ui.on_text_command   (callable attribute)
  • ui.muted             (bool property)
  • ui.start_speaking()
  • ui.stop_speaking()
  • ui.wait_for_api_key()
  • ui.root.mainloop()   (compat shim → calls QApplication.exec())
────────────────────────────────────────────────────────────────────────────────
"""

import os, json, time, math, random, threading, platform
import sys
from pathlib import Path
from collections import deque
import memory.config_manager as config_manager
from icons import SVG_ICONS

# ── PyQt6 ─────────────────────────────────────────────────────────────────────
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QFrame, QScrollArea,
    QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout,
    QSizePolicy, QGraphicsDropShadowEffect, QStackedWidget, QTextEdit,
)
from PyQt6.QtCore import (
    Qt, QTimer, QThread, pyqtSignal, QPoint, QRectF, QPointF,
    QPropertyAnimation, QEasingCurve, pyqtProperty,
)
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import (
    QIcon, 
    QPainter, QColor, QPen, QFont, QBrush, QLinearGradient,
    QRadialGradient, QPainterPath, QPixmap, QImage, QFontDatabase,
    QConicalGradient, QPalette, QMovie,
)

# ── Optional: PIL for face image loading ─────────────────────────────────────
try:
    from PIL import Image, ImageTk, ImageDraw
    _PIL = True
except ImportError:
    _PIL = False

# ── psutil for system metrics ─────────────────────────────────────────────────
try:
    import psutil
    _PSUTIL = True
except ImportError:
    _PSUTIL = False


# ═══════════════════════════════════════════════════════════════════════════════
#  PATH HELPERS  (preserved from original)
# ═══════════════════════════════════════════════════════════════════════════════

def get_base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent


BASE_DIR   = get_base_dir()


# ═══════════════════════════════════════════════════════════════════════════════
#  IDENTITY & COLOUR CONSTANTS  (preserved + extended from original)
# ═══════════════════════════════════════════════════════════════════════════════

SYSTEM_NAME = "J.A.R.V.I.S"
MODEL_BADGE = "MARK XXXVII"

C_BG     = "#000000"
C_PRI    = "#00d4ff"   # Electric Blue (Main)
C_CYAN   = "#00f2ff"   # Neon Cyan (Brightest)
C_MID    = "#00a3ff"   # Process Blue (Medium)
C_GLOW   = "#70efff"   # Glow Blue (Highlight)
C_DIM    = "#005f7f"   # Navi Blue (Dim)

C_BG_ACC = "#040914"
C_MID_LEGACY = "#0369a1"
C_DIM_ALT    = "#1e293b"
C_DIMMER     = "#0f172a"
C_ACC    = "#f97316"
C_ACC2   = "#eab308"
C_TEXT   = "#e2e8f0"
C_PANEL  = "#0b1324"
C_GREEN  = "#22c55e"
C_RED    = "#ef4444"
C_MUTED  = "#f43f5e"

C_PANEL2     = "#020617"
C_BORDER     = "#111827"
C_RADAR_GLOW = "#00d4ff"


# ── Color Helpers ─────────────────────────────────────────────────────────────
def qc(color_hex: str, alpha: int = 255) -> QColor:
    c = QColor(color_hex)
    c.setAlpha(alpha)
    return c

class _RootShim:
    """Drop-in replacement for tk.Tk() — gives main.py a `.mainloop()` call."""
    def __init__(self, app: QApplication):
        self._app = app

    def mainloop(self):
        sys.exit(self._app.exec())

    # Keep any other tk attributes that might be referenced
    def protocol(self, *_a, **_kw):
        pass

    def after(self, ms, func, *args):
        QTimer.singleShot(ms, lambda: func(*args))


# ═══════════════════════════════════════════════════════════════════════════════
#  PALETTE HELPER
# ═══════════════════════════════════════════════════════════════════════════════

def qc(hex_str: str, alpha: int = 255) -> QColor:
    c = QColor(hex_str)
    c.setAlpha(alpha)
    return c



# ═══════════════════════════════════════════════════════════════════════════════
#  HOLOGRAM WIDGET
# ═══════════════════════════════════════════════════════════════════════════════


def load_svg_icon(name: str, color: str, size: int):
    from PyQt6.QtGui import QIcon, QPixmap, QPainter
    from PyQt6.QtSvg import QSvgRenderer
    from PyQt6.QtCore import Qt
    from icons import SVG_ICONS
    
    key = name.replace(".svg", "")
    svg_str = SVG_ICONS.get(key, "")
    if not svg_str:
        return QIcon()
        
    svg_str = svg_str.replace("{color}", color)
    renderer = QSvgRenderer(svg_str.encode('utf-8'))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return QIcon(pixmap)

class HologramWidget(QWidget):
    """True 3D Volumetric Orbital Globe with Y-axis rotation and perspective projection."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(450, 450)
        self._tick = 0
        self._state = "IDLE"
        self._speaking = False
        self._muted = False
        
        # 3D State
        self._rot_y = 0.0
        self._rot_x = 12.0 # Master tilt
        self._rot_z = 0.0  # New Z-axis wobble
        self._pulse_mag = 1.0
        
        # Geometry Data
        self._arcs = []
        self._particles = []
        self._num_arcs = 45
        self._num_particles = 1200
        
        self._init_3d_engine()
        
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._step)
        self._timer.start(16)
        
    def _init_3d_engine(self):
        """Pre-generate the Multi-Axial 'Cage' geometry."""
        # 1. Arcs (Cage Lattice)
        for _ in range(self._num_arcs):
            radius = random.uniform(80, 190)
            # Randomly tilt each arc's orbital plane in 3D space
            tilt_x = random.uniform(0, 360)
            tilt_y = random.uniform(0, 360)
            tilt_z = random.uniform(0, 360)
            
            # 5-shade depth assignment
            r_val = random.random()
            if r_val > 0.8: col = C_CYAN
            elif r_val > 0.6: col = C_PRI
            elif r_val > 0.4: col = C_MID
            elif r_val > 0.2: col = C_GLOW
            else: col = C_DIM

            self._arcs.append({
                "radius": radius,
                "arc_len": random.uniform(60, 280),
                "speed": random.uniform(-1.0, 1.0),
                "angle_offset": random.uniform(0, 360),
                "tilt": (tilt_x, tilt_y, tilt_z),
                "width": random.uniform(0.5, 2.0),
                "dash": random.choice([[5, 10], [50, 10], [1, 5], []]),
                "opacity": random.randint(40, 180),
                "color": col
            })
            
        # 2. Fibonacci Sphere Particles (Uniform Distribution)
        for i in range(self._num_particles):
            # Fibonacci distribution for even spherical mapping
            phi = math.acos(1 - 2 * (i / self._num_particles))
            theta = math.pi * (1 + 5**0.5) * i
            
            radius = random.uniform(170, 195) # Outer shell
            if random.random() < 0.3: radius = random.uniform(40, 100) # Core shell
            
            # Particles use the brightest shades for "data nebula" effect
            p_col = random.choice([C_CYAN, C_PRI, C_GLOW])
            
            self._particles.append({
                "r": radius,
                "phi": phi,
                "theta": theta,
                "speed": random.uniform(0.1, 0.4),
                "size": random.uniform(0.5, 1.8),
                "opacity": random.randint(80, 240),
                "color": p_col
            })

    def set_state(self, state: str):
        self._state = state
        self._speaking = (state == "SPEAKING")
        self._muted = (state == "MUTED")
        self.update()

    def set_speaking(self, v: bool):
        self._speaking = v
        self.update()

    def set_muted(self, v: bool):
        self._muted = v
        self.update()
        
    def _step(self):
        self._tick += 1
        t = self._tick
        
        # Physics Multipliers
        speed_mult = 1.0
        if self._state == "SPEAKING": speed_mult = 2.5
        elif self._state == "THINKING": speed_mult = 5.0
        elif self._state == "LISTENING": speed_mult = 0.6
            
        # Update Master Globe Rotation (Tumble effect)
        self._rot_y = (self._rot_y + 0.3 * speed_mult) % 360
        self._rot_x = (self._rot_x + 0.15 * speed_mult) % 360
        self._rot_z = (self._rot_z + 0.08 * speed_mult) % 360 # Smooth Z-wobble
        
        # Update Internal Orbitals
        for a in self._arcs:
            a["angle_offset"] = (a["angle_offset"] + a["speed"] * speed_mult * 0.4) % 360
            
        # Update Particle Orbits
        for pt in self._particles:
            pt["theta"] += pt["speed"] * speed_mult * 0.01
            
        # Pulse
        if self._speaking:
            self._pulse_mag = 1.0 + math.sin(t * 0.3) * 0.12
        else:
            self._pulse_mag = 1.0 + math.sin(t * 0.08) * 0.02
            
        self.update()
        
    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        W, H = self.width(), self.height()
        cx, cy = W / 2, H / 2
        
        # NO BACKGROUND FILL - Allow transparency/free floating
        
        SCALE = min(W, H) / 450.0 * self._pulse_mag
        
        # 3D Math Setup
        ry = math.radians(self._rot_y)
        rx = math.radians(self._rot_x)
        rz = math.radians(self._rot_z)
        cos_y, sin_y = math.cos(ry), math.sin(ry)
        cos_x, sin_x = math.cos(rx), math.sin(rx)
        cos_z, sin_z = math.cos(rz), math.sin(rz)
        
        def project_3d(x, y, z):
            """Apply 3D Rotation and Projection."""
            # Rot Y (Globe spin)
            x1 = x * cos_y - z * sin_y
            z1 = x * sin_y + z * cos_y
            # Rot X (Tilt)
            y2 = y * cos_x - z1 * sin_x
            z2 = y * sin_x + z1 * ctx # note: ctx was pre-defined below in segments, 
                                      # using pre-calc cos_x here for master. 
                                      # Wait, using cos_x globally is cleaner.
            y2 = y * cos_x - z1 * sin_x
            z2 = y * sin_x + z1 * cos_x
            
            # Rot Z (Wobble)
            x3 = x1 * cos_z - y2 * sin_z
            y3 = x1 * sin_z + y2 * cos_z
            
            # Perspective
            persp = 600 / (600 - z2)
            return x3 * persp * SCALE, y3 * persp * SCALE, z2

        render_stack = []
        is_muted = self._muted

        # 1. ──── PREPARE CORE (Always in the stack) ────
        render_stack.append({
            "type": "core",
            "z": 1, # Slightly forward
            "center": QPointF(cx, cy)
        })

        # 2. ──── PREPARE ARCS (Multi-Axial) ────
        for a in self._arcs:
            segments = 35
            prev_pt = None
            arc_rad = math.radians(a["arc_len"])
            
            # Rotation matrix for this arc's fixed tilt
            tx, ty, tz = [math.radians(v) for v in a["tilt"]]
            ctx, stx = math.cos(tx), math.sin(tx)
            cty, sty = math.cos(ty), math.sin(ty)
            ctz, stz = math.cos(tz), math.sin(tz)
            
            for i in range(segments + 1):
                angle = math.radians(a["angle_offset"]) + (i / segments) * arc_rad
                
                # Base circle point
                lx = math.cos(angle) * a["radius"]
                ly = math.sin(angle) * a["radius"]
                lz = 0
                
                # Apply Fixed Tilt Rotation
                # Rot X
                y1 = ly * ctx - lz * stx
                z1 = ly * stx + lz * ctx
                # Rot Y
                x2 = lx * cty + z1 * sty
                z2 = -lx * sty + z1 * cty
                # Rot Z
                x3 = x2 * ctz - y1 * stz
                y3 = x2 * stz + y1 * ctz
                
                sx, sy, sz = project_3d(x3, y3, z2)
                curr_pt = {"x": cx + sx, "y": cy + sy, "z": sz}
                
                if prev_pt:
                    mid_z = (prev_pt["z"] + curr_pt["z"]) / 2
                    render_stack.append({
                        "type": "ring_seg",
                        "z": mid_z,
                        "p1": QPointF(prev_pt["x"], prev_pt["y"]),
                        "p2": QPointF(curr_pt["x"], curr_pt["y"]),
                        "width": a["width"],
                        "opacity": a["opacity"],
                        "dash": a["dash"],
                        "color": a["color"]
                    })
                prev_pt = curr_pt

        # 3. ──── PREPARE PARTICLES (Spherical Shell) ────
        for pt in self._particles:
            # Lat/Long to Cartesian
            x = pt["r"] * math.sin(pt["phi"]) * math.cos(pt["theta"])
            y = pt["r"] * math.sin(pt["phi"]) * math.sin(pt["theta"])
            z = pt["r"] * math.cos(pt["phi"])
            
            sx, sy, sz = project_3d(x, y, z)
            render_stack.append({
                "type": "particle",
                "z": sz,
                "pos": QPointF(cx + sx, cy + sy),
                "size": pt["size"] * SCALE,
                "opacity": pt["opacity"],
                "color": pt["color"]
            })

        # 🚀 ──── MASTER DEPTH SORT ────
        render_stack.sort(key=lambda o: o["z"])

        # 🎨 ──── FINAL RENDER ────
        for obj in render_stack:
            z_fac = (obj["z"] + 200) / 400
            
            if obj["type"] == "core":
                grad = QRadialGradient(obj["center"], 45 * SCALE)
                grad.setColorAt(0.0, Qt.GlobalColor.white)
                grad.setColorAt(0.3, QColor(C_PRI))
                grad.setColorAt(1.0, Qt.GlobalColor.transparent)
                p.setBrush(QBrush(grad))
                p.setPen(Qt.PenStyle.NoPen)
                p.drawEllipse(obj["center"], 40 * SCALE, 40 * SCALE)
                
            elif obj["type"] == "ring_seg":
                c = QColor(C_MUTED if is_muted else obj["color"])
                # Front segments are brighter, back are dimmer
                alpha = int(obj["opacity"] * max(0.2, min(1.0, z_fac)))
                c.setAlpha(alpha)
                p.setPen(QPen(c, obj["width"] * SCALE))
                p.drawLine(obj["p1"], obj["p2"])
                
            elif obj["type"] == "particle":
                c = QColor(C_MUTED if is_muted else obj["color"])
                alpha = int(obj["opacity"] * max(0.1, min(1.0, z_fac)))
                c.setAlpha(alpha)
                p.setBrush(QBrush(c))
                p.setPen(Qt.PenStyle.NoPen)
                size = obj["size"]
                p.drawEllipse(obj["pos"], size, size)

        # HUD Overlay (Minimal, non-blocking)
        p.setPen(QPen(qc(C_PRI, 80)))
        p.setFont(QFont("Courier New", 7, QFont.Weight.DemiBold))
        text = f"VOLUMETRIC_ENGINE // {self._state} >> SYNC_ACTIVE"
        p.drawText(self.rect().adjusted(0, 0, 0, -10), Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter, text)
        p.end()


# ═══════════════════════════════════════════════════════════════════════════════
#  BOOT HUD WIDGET (ATLAS Style)
# ═══════════════════════════════════════════════════════════════════════════════

class BootHUDWidget(QWidget):
    """
    Circular HUD loader inspired by the 'ATLAS' reference image.
    Features rotating rings, status text, and a progress bar.
    """
    ready_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._angle = 0
        self._percent = 0.0
        self._target_percent = 0.0
        self._tick_counter = 0
        self._progress_steps = [0.0, 10.0, 15.0, 22.0, 29.0, 51.0, 79.0, 87.0, 91.0, 95.0, 99.0]
        self._step_idx = 0
        self._status_idx = 0
        self._statuses = [
            "INITIALISING SYSTEM CORE...",
            "NEURAL LINK ESTABLISHED",
            "DECRYPTING SECURITY PROTOCOLS",
            "MAPPING SENSORY INPUTS",
            "VISION ANALYTICS READY",
            "ROUTING PROJECT DOMAIN...",
            "SECURE HANDSHAKE PENDING",
            "J.A.R.V.I.S. ONLINE"
        ]
        
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_anim)
        self._timer.start(16)

    def set_progress(self, p: float):
        self._target_percent = min(100.0, max(0.0, float(p)))
        self._percent = self._target_percent
        self._status_idx = int((self._percent / 100.0) * (len(self._statuses) - 1))
        if self._percent >= 100.0:
            self.ready_signal.emit()

    def _update_anim(self):
        self._angle = (self._angle + 2) % 360
        self._tick_counter += 1

        # Simulate dynamic progress if we haven't reached 100 externally
        if self._percent < 100.0:
            if self._tick_counter % 15 == 0 and random.random() < 0.7:
                if self._step_idx < len(self._progress_steps) - 1:
                    self._step_idx += 1
                    self._target_percent = self._progress_steps[self._step_idx]

            # Smoothly catch up to the target progress
            if self._percent < self._target_percent:
                self._percent += min(2.0, self._target_percent - self._percent)
                self._status_idx = int((self._percent / 100.0) * (len(self._statuses) - 1))

        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        
        W, H = self.width(), self.height()
        CX, CY = W // 2, H // 2
        R = int(min(CX, CY) * 0.28)
        
        p.translate(CX, CY)

        # --- DRAW BACKGROUND RINGS ---
        p.setPen(QPen(QColor(C_DIM), 1, Qt.PenStyle.DashLine))
        p.drawEllipse(QPointF(0, 0), R, R)
        p.drawEllipse(QPointF(0, 0), R + 40, R + 40)

        # --- ROTATING DASH RINGS ---
        p.save()
        p.rotate(self._angle)
        
        # Outer thick arc
        p.setPen(QPen(QColor(C_PRI), 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        p.drawArc(QRectF(-R-20, -R-20, (R+20)*2, (R+20)*2), 0 * 16, 60 * 16)
        p.drawArc(QRectF(-R-20, -R-20, (R+20)*2, (R+20)*2), 180 * 16, 45 * 16)
        
        # Middle fast ring
        p.rotate(-self._angle * 2.5)
        p.setPen(QPen(QColor(C_CYAN), 2, Qt.PenStyle.DotLine))
        p.drawEllipse(QPointF(0,0), R-10, R-10)
        p.restore()

        # --- CENTRAL TEXT "JARVIS" ---
        font = QFont("Orbitron", 30, QFont.Weight.Bold)
        font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 4)
        p.setFont(font)
        
        # We define a bounding box for the text centered at origin
        text_rect = QRectF(-200, -50, 400, 100)
        
        # Outer glow
        p.setPen(QColor(C_GLOW))
        txt = "JARVIS"
        p.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, txt)
        
        # Inner text
        font.setPointSize(29)
        p.setFont(font)
        p.setPen(QColor(C_PRI))
        p.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, txt)

        # --- STATUS TEXT ---
        p.setFont(QFont("Courier New", 9))
        p.setPen(QColor(C_PRI))
        status_txt = self._statuses[self._status_idx]
        # Offset further down to avoid clutter
        p.drawText(int(-150), int(R + 75), 300, 20, Qt.AlignmentFlag.AlignCenter, status_txt)

        # --- PROGRESS BAR ---
        bar_w = int(W * 0.22)
        bar_x = -bar_w // 2
        bar_y = int(R + 55)
        
        # Track
        p.setPen(QPen(QColor(C_DIM), 1))
        p.drawRect(int(bar_x), int(bar_y), bar_w, 4)
        
        # Fill
        p.setBrush(QBrush(QColor(C_CYAN)))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRect(int(bar_x), int(bar_y), int(bar_w * (self._percent / 100.0)), 4)
        
        # Percentage text - Aligned with the end of the bar or after
        p.setPen(QColor(C_CYAN))
        p.setFont(QFont("Courier New", 8))
        p.drawText(int(bar_x + bar_w + 10), int(bar_y + 4), f"{self._percent:05.2f}%")

        p.end()

# ═══════════════════════════════════════════════════════════════════════════════
#  WAVEFORM WIDGET
# ═══════════════════════════════════════════════════════════════════════════════

class WaveformWidget(QWidget):
    """Audio-level bars that pulse when JARVIS is speaking."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(38)
        self._speaking = False
        self._muted    = False
        self._tick     = 0
        self._bars: list[int] = [2] * 36
        t = QTimer(self)
        t.timeout.connect(self._step)
        t.start(40)

    def set_speaking(self, v: bool):
        self._speaking = v

    def set_muted(self, v: bool):
        self._muted = v

    def _step(self):
        self._tick += 1
        t = self._tick
        N = len(self._bars)
        for i in range(N):
            if self._muted:
                self._bars[i] = 2
            elif self._speaking:
                self._bars[i] = random.randint(4, 28)
            else:
                self._bars[i] = int(3 + 2 * math.sin(t * 0.08 + i * 0.55))
        self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        W, H = self.width(), self.height()
        N    = len(self._bars)
        bw   = W / N
        for i, hb in enumerate(self._bars):
            if self._muted:
                col = qc(C_MUTED, 180)
            elif self._speaking:
                col = qc(C_PRI if hb > 15 else C_MID, 220)
            else:
                col = qc(C_MID, 120)
            p.setBrush(QBrush(col))
            p.setPen(Qt.PenStyle.NoPen)
            x = int(i * bw + 1)
            y = H - hb
            p.drawRoundedRect(x, y, int(bw - 2), hb, 1, 1)
        p.end()



# ═══════════════════════════════════════════════════════════════════════════════
#  STATS WIDGET  (CPU / RAM / Disk / Network)
# ═══════════════════════════════════════════════════════════════════════════════

class _StatBar(QWidget):
    def __init__(self, label: str, parent=None):
        super().__init__(parent)
        self.setFixedHeight(38)
        self._label  = label
        self._pct    = 0.0
        self._text   = "—"
        self._color  = C_PRI
        self._icon = None

    def set_icon(self, icon):
        self._icon = icon

    def set_value(self, pct: float, text: str, color: str = C_PRI):
        self._pct   = max(0.0, min(1.0, pct))
        self._text  = text
        self._color = color
        self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        W, H = self.width(), self.height()

        
        # Label
        if self._icon:
            p.drawPixmap(0, 2, self._icon.pixmap(14, 14))
            label_x = 20
        else:
            label_x = 0
            
        p.setPen(qc(C_TEXT, 200))
        p.setFont(QFont("Courier New", 8))
        p.drawText(label_x, 0, 80, 18, Qt.AlignmentFlag.AlignLeft, self._label)


        # Value
        p.setPen(qc(C_TEXT))
        p.setFont(QFont("Courier New", 8, QFont.Weight.Bold))
        p.drawText(W - 90, 0, 90, 18, Qt.AlignmentFlag.AlignRight, self._text)

        # Track
        track_y = 22
        track_h = 6
        p.setBrush(QBrush(qc(C_DIMMER)))
        p.setPen(QPen(qc(C_DIM), 1))
        p.drawRoundedRect(0, track_y, W, track_h, 3, 3)

        # Bar
        fill_w = int(W * self._pct)
        if fill_w > 4:
            grad = QLinearGradient(0, 0, W, 0)
            grad.setColorAt(0, qc(self._color, 180))
            grad.setColorAt(1, qc(self._color))
            p.setBrush(QBrush(grad))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(0, track_y, fill_w, track_h, 3, 3)

        p.end()


class StatsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(12, 10, 12, 10)
        self._layout.setSpacing(4)

        # Title
        title = QLabel("◈  PC HEALTH")
        title.setFont(QFont("Courier New", 9, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {C_PRI}; letter-spacing: 2px;")
        self._layout.addWidget(title)

        self._cpu_bar  = _StatBar("CPU")
        self._ram_bar  = _StatBar("RAM")
        self._dsk_bar  = _StatBar("Disk (C:)")
        self._net_dl   = _StatBar("Network")
        self._net_dl.set_icon(load_svg_icon("net_down.svg", C_TEXT, 14))
        self._net_ul   = _StatBar("Upload")
        self._net_ul.set_icon(load_svg_icon("net_up.svg", C_TEXT, 14))
        for w in [self._cpu_bar, self._ram_bar, self._dsk_bar,
                  self._net_dl, self._net_ul]:
            self._layout.addWidget(w)

        self._layout.addStretch()

        self._prev_net = None
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh)
        self._timer.start(1000)
        self._refresh()

    def _refresh(self):
        if not _PSUTIL:
            return

        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        dsk = psutil.disk_usage("C:\\")

        cpu_col = C_RED if cpu > 80 else (C_ACC2 if cpu > 60 else C_GREEN)
        self._cpu_bar.set_value(cpu / 100, f"{cpu:.0f}%", cpu_col)

        ram_pct = ram.percent / 100
        ram_col = C_RED if ram.percent > 85 else C_PRI
        self._ram_bar.set_value(ram_pct, f"{ram.percent:.0f}%", ram_col)

        dsk_pct = dsk.percent / 100
        used_gb = dsk.used / 1e9
        tot_gb  = dsk.total / 1e9
        self._dsk_bar.set_value(dsk_pct, f"{used_gb:.0f}GB / {tot_gb:.0f}GB", C_MID)

        # Network
        cur_net = psutil.net_io_counters()
        if self._prev_net is not None:
            dl = (cur_net.bytes_recv - self._prev_net.bytes_recv) / 1024
            ul = (cur_net.bytes_sent - self._prev_net.bytes_sent) / 1024
            dl_txt = f"{dl/1024:.1f} MB/s" if dl > 1024 else f"{dl:.0f} KB/s"
            ul_txt = f"{ul/1024:.1f} MB/s" if ul > 1024 else f"{ul:.0f} KB/s"
            self._net_dl.set_value(min(dl / 12500, 1.0), dl_txt, C_GREEN)
            self._net_ul.set_value(min(ul / 12500, 1.0), ul_txt, C_ACC2)
        self._prev_net = cur_net


# ═══════════════════════════════════════════════════════════════════════════════
#  SYSTEM INFO WIDGET
# ═══════════════════════════════════════════════════════════════════════════════

class SysInfoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(12, 10, 12, 10)
        self._layout.setSpacing(2)

        title = QLabel("◈  SYSTEM INFO")
        title.setFont(QFont("Courier New", 9, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {C_PRI}; letter-spacing: 2px;")
        self._layout.addWidget(title)

        self._lines: list[QLabel] = []
        for _ in range(5):
            lbl = QLabel("")
            lbl.setFont(QFont("Courier New", 8))
            lbl.setStyleSheet(f"color: {C_TEXT};")
            self._layout.addWidget(lbl)
            self._lines.append(lbl)

        self._layout.addStretch()

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh)
        self._timer.start(5000)
        self._refresh()

    def _refresh(self):
        os_name = f"OS:     {platform.system()} {platform.release()}"
        if _PSUTIL:
            boot   = time.time() - psutil.boot_time()
            h, rem = divmod(int(boot), 3600)
            m      = rem // 60
            up     = f"Uptime: {h}h {m}m"
            try:
                bat = psutil.sensors_battery()
                bat_str = f"Battery: {bat.percent:.0f}%"  if bat else "Battery: N/A"
            except Exception:
                bat_str = "Battery: N/A"
        else:
            up      = "Uptime: N/A"
            bat_str = "Battery: N/A"

        wifi_str = "Wi-Fi:  Active"
        node_str = f"Host:   {platform.node()}"

        data = [os_name, up, bat_str, wifi_str, node_str]
        for i, (lbl, text) in enumerate(zip(self._lines, data)):
            lbl.setText(text)


# ═══════════════════════════════════════════════════════════════════════════════
#  QUICK ACTIONS WIDGET
# ═══════════════════════════════════════════════════════════════════════════════

class QuickActionsWidget(QWidget):

    def _svg_to_pixmap(self, svg_str: str, size: int):
        if not svg_str: return QPixmap()
        svg_str = svg_str.replace("{color}", C_PRI)
        renderer = QSvgRenderer(svg_str.encode('utf-8'))
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        return pixmap

    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 10, 12, 10)
        lay.setSpacing(2)

        title = QLabel("◈  QUICK ACTIONS")
        title.setFont(QFont("Courier New", 9, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {C_PRI}; letter-spacing: 2px;")
        lay.addWidget(title)

        
        ACTIONS = [
            ("folder.svg", "File Explorer"),
            ("settings.svg", "Settings"),
            ("apps.svg", "Apps"),
            ("terminal.svg", "Terminal"),
            ("task_manager.svg", "Task Manager"),
        ]
        for icon_file, name in ACTIONS:
            btn = QPushButton(f"  {name}")
            btn.setIcon(load_svg_icon(icon_file, C_TEXT, 18))
            btn.setFont(QFont("Courier New", 9))

            btn.setStyleSheet(f"""
                QPushButton {{
                    color: {C_TEXT}; background: transparent;
                    border: none; text-align: left;
                    padding: 5px 4px;
                }}
                QPushButton:hover {{
                    color: {C_PRI};
                    background: {C_DIMMER};
                    border-radius: 3px;
                }}
            """)
            lay.addWidget(btn)

        lay.addStretch()


# ═══════════════════════════════════════════════════════════════════════════════
#  CHAT WIDGET
# ═══════════════════════════════════════════════════════════════════════════════

class ChatWidget(QWidget):
    """Scrollable chat log with typewriter effect — mirrors original log_text."""

    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        # Title bar
        header = QWidget()
        header.setFixedHeight(32)
        header.setStyleSheet(f"background: {C_PANEL2}; border-bottom: 1px solid {C_BORDER};")
        h_lay = QHBoxLayout(header)
        h_lay.setContentsMargins(12, 0, 12, 0)
        h_lay.addWidget(self._dot("green"))
        title = QLabel("  JARVIS CHAT")
        title.setFont(QFont("Courier New", 9, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {C_PRI}; letter-spacing: 2px;")
        h_lay.addWidget(title)
        h_lay.addStretch()
        lay.addWidget(header)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical { width: 4px; background: #001520; }
            QScrollBar::handle:vertical { background: #003344; border-radius: 2px; }
        """)
        inner = QWidget()
        inner.setStyleSheet("background: transparent;")
        self._msg_lay = QVBoxLayout(inner)
        self._msg_lay.setContentsMargins(8, 8, 8, 8)
        self._msg_lay.setSpacing(6)
        self._msg_lay.addStretch()
        scroll.setWidget(inner)
        self._scroll = scroll
        lay.addWidget(scroll, 1)

        # Typing queue
        self._typing_queue: deque = deque()
        self._is_typing = False

    def _dot(self, color):
        d = QLabel("●")
        d.setFont(QFont("Arial", 8))
        d.setStyleSheet(f"color: {'#00ff88' if color=='green' else C_RED};")
        return d

    def _add_bubble(self, text: str, tag: str):
        """Add a styled chat bubble to the layout."""
        if tag == "you":
            col   = "#e8e8e8"
            prefix = "YOU"
            align = Qt.AlignmentFlag.AlignRight
            bg    = "#001a25"
        elif tag == "ai":
            col   = C_PRI
            prefix = "J.A.R.V.I.S."
            align = Qt.AlignmentFlag.AlignLeft
            bg    = "#000d14"
        elif tag == "err":
            col   = C_RED
            prefix = "ERROR"
            align = Qt.AlignmentFlag.AlignLeft
            bg    = "#1a0005"
        else:
            col   = C_ACC2
            prefix = "SYS"
            align = Qt.AlignmentFlag.AlignLeft
            bg    = "#080600"

        bubble = QWidget()
        bubble.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        lay = QVBoxLayout(bubble)
        lay.setContentsMargins(6, 4, 6, 4)
        lay.setSpacing(2)

        sender_lbl = QLabel(prefix + "  " + time.strftime("%H:%M"))
        sender_lbl.setFont(QFont("Courier New", 7, QFont.Weight.Bold))
        sender_lbl.setStyleSheet(f"color: {col}; letter-spacing: 1px;")
        sender_lbl.setAlignment(align)
        lay.addWidget(sender_lbl)

        msg_lbl = QLabel()
        msg_lbl.setFont(QFont("Courier New", 9))
        msg_lbl.setStyleSheet(f"color: {col}; background: {bg}; border-radius: 4px; padding: 4px 6px;")
        msg_lbl.setWordWrap(True)
        msg_lbl.setAlignment(align)
        msg_lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        lay.addWidget(msg_lbl)

        self._msg_lay.insertWidget(self._msg_lay.count() - 1, bubble)

        # Auto scroll
        QTimer.singleShot(50, lambda: self._scroll.verticalScrollBar().setValue(
            self._scroll.verticalScrollBar().maximum()))

        return msg_lbl

    # ── public typing-queue API (same as original) ────────────────────────────

    def write_log(self, text: str):
        self._typing_queue.append(text)
        if not self._is_typing:
            self._start_typing()

    def _start_typing(self):
        if not self._typing_queue:
            self._is_typing = False
            return
        self._is_typing = True
        text = self._typing_queue.popleft()
        tl   = text.lower()
        if tl.startswith("you:"):
            tag   = "you"
            text2 = text[4:].strip()
        elif tl.startswith("jarvis:") or tl.startswith("ai:"):
            tag   = "ai"
            text2 = text.split(":", 1)[1].strip()
        elif tl.startswith("err:") or "error" in tl or "failed" in tl:
            tag   = "err"
            text2 = text
        else:
            tag   = "sys"
            text2 = text

        lbl = self._add_bubble("", tag)
        self._type_char(lbl, text2, 0)

    def _type_char(self, lbl, text, i):
        if i < len(text):
            lbl.setText(text[:i + 1])
            QTimer.singleShot(8, lambda: self._type_char(lbl, text, i + 1))
        else:
            QTimer.singleShot(25, self._start_typing)


# ═══════════════════════════════════════════════════════════════════════════════
#  CAMERA WIDGET
# ═══════════════════════════════════════════════════════════════════════════════

class CameraWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(220, 160)
        self._frame_pixmap: QPixmap | None = None
        self._gesture_text: str = ""
        self._gesture_alpha: float = 0.0
        self._overlay_active: bool = False
        self._gesture_timer = QTimer(self)
        self._gesture_timer.timeout.connect(self._fade_gesture)
        self._gesture_timer.start(50)

    def set_frame(self, bgr_bytes: bytes, w: int, h: int):
        """Update display with a new BGR frame (from OpenCV)."""
        try:
            import numpy as np
            arr = np.frombuffer(bgr_bytes, dtype="uint8").reshape((h, w, 3))
            rgb = arr[:, :, ::-1].copy()
            img = QImage(rgb.data, w, h, w * 3, QImage.Format.Format_RGB888)
            self._frame_pixmap = QPixmap.fromImage(img)
            self.update()
        except Exception:
            pass

    def show_gesture(self, text: str):
        self._gesture_text  = text
        self._gesture_alpha = 255.0
        self._overlay_active = True
        self.update()

    def _fade_gesture(self):
        if self._gesture_alpha > 0:
            self._gesture_alpha = max(0.0, self._gesture_alpha - 5)
            self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        W, H = self.width(), self.height()

        p.fillRect(0, 0, W, H, QColor("#000508"))

        if self._frame_pixmap:
            scaled = self._frame_pixmap.scaled(
                W, H,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation)
            # Center-crop
            x = (scaled.width()  - W) // 2
            y = (scaled.height() - H) // 2
            p.drawPixmap(0, 0, scaled, x, y, W, H)

            # Scan line overlay
            for gy in range(0, H, 4):
                c = QColor(0, 0, 0, 20)
                p.fillRect(0, gy, W, 2, c)

            # HUD border
            pen = QPen(qc(C_PRI, 120), 1)
            p.setPen(pen)
            p.drawRect(0, 0, W - 1, H - 1)

            # Corner brackets
            blen = 14
            bc   = qc(C_GREEN, 200)
            p.setPen(QPen(bc, 2))
            for bx, by, sdx, sdy in [(0, 0, 1, 1), (W-1, 0, -1, 1),
                                       (0, H-1, 1, -1), (W-1, H-1, -1, -1)]:
                p.drawLine(QPointF(bx, by), QPointF(bx + sdx * blen, by))
                p.drawLine(QPointF(bx, by), QPointF(bx, by + sdy * blen))
        else:
            # No feed placeholder
            p.setPen(qc(C_DIM))
            p.setFont(QFont("Courier New", 8))
            p.drawText(QRectF(0, 0, W, H), Qt.AlignmentFlag.AlignCenter,
                       "CAMERA\nOFFLINE")
            p.setPen(QPen(qc(C_DIM, 80), 1))
            p.drawRect(0, 0, W - 1, H - 1)

        # Status dot
        dot_col = qc(C_GREEN if self._frame_pixmap else C_RED)
        p.setBrush(QBrush(dot_col))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(QPointF(8, 8), 4, 4)

        # Gesture overlay
        if self._gesture_text and self._gesture_alpha > 0:
            c = qc(C_GREEN, int(self._gesture_alpha))
            p.setPen(QPen(c))
            p.setFont(QFont("Courier New", 10, QFont.Weight.Bold))
            p.drawText(QRectF(0, H - 28, W, 24),
                       Qt.AlignmentFlag.AlignCenter, f"{self._gesture_text}")

        p.end()


# ═══════════════════════════════════════════════════════════════════════════════
#  STATUS LABEL WIDGET
# ═══════════════════════════════════════════════════════════════════════════════

class StatusWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(30)
        self._state = "INITIALISING"
        self._blink = True
        self._tick  = 0
        t = QTimer(self)
        t.timeout.connect(self._blink_tick)
        t.start(500)

    def set_state(self, state: str):
        self._state = state
        self.update()

    def _blink_tick(self):
        self._blink = not self._blink
        self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        W, H = self.width(), self.height()

        state = self._state
        if state == "MUTED":
            txt, col = " MUTED", C_MUTED
        elif state == "SPEAKING":
            txt, col = "● SPEAKING", C_ACC
        elif state == "THINKING":
            sym = "◈" if self._blink else "◇"
            txt, col = f"{sym} THINKING", C_ACC2
        elif state == "PROCESSING":
            sym = "▷" if self._blink else "▶"
            txt, col = f"{sym} PROCESSING", C_ACC2
        elif state == "LISTENING":
            sym = "●" if self._blink else "○"
            txt, col = f"{sym} LISTENING", C_GREEN
        else:
            sym = "●" if self._blink else "○"
            txt, col = f"{sym} {state}", C_PRI

        p.setPen(qc(col))
        p.setFont(QFont("Courier New", 10, QFont.Weight.Bold))
        p.drawText(QRectF(0, 0, W, H), Qt.AlignmentFlag.AlignCenter, txt)
        p.end()


# ═══════════════════════════════════════════════════════════════════════════════
#  INPUT BAR WIDGET
# ═══════════════════════════════════════════════════════════════════════════════

class InputBarWidget(QWidget):
    submitted = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(6)

        self._entry = QLineEdit()
        self._entry.setPlaceholderText("Type a message...")
        self._entry.setFont(QFont("Courier New", 10))
        self._entry.setStyleSheet(f"""
            QLineEdit {{
                background: #000d12; color: {C_TEXT};
                border: 1px solid {C_DIM}; border-radius: 4px;
                padding: 5px 10px;
            }}
            QLineEdit:focus {{ border: 1px solid {C_PRI}; }}
        """)
        self._entry.returnPressed.connect(self._submit)
        lay.addWidget(self._entry, 1)

        self._btn = QPushButton("▸")
        self._btn.setFixedSize(36, 32)
        self._btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        self._btn.setStyleSheet(f"""
            QPushButton {{
                background: {C_PANEL2}; color: {C_PRI};
                border: 1px solid {C_MID}; border-radius: 4px;
            }}
            QPushButton:hover {{
                background: {C_PRI}; color: {C_BG};
            }}
        """)
        self._btn.clicked.connect(self._submit)
        lay.addWidget(self._btn)

    def _submit(self):
        text = self._entry.text().strip()
        if text:
            self._entry.clear()
            self.submitted.emit(text)


# ═══════════════════════════════════════════════════════════════════════════════
#  MUTE BUTTON WIDGET
# ═══════════════════════════════════════════════════════════════════════════════

class MuteButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._muted = False
        self.setFixedSize(110, 32)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._refresh()

    @property
    def muted(self):
        return self._muted

    def toggle(self):
        self._muted = not self._muted
        self._refresh()

    def _refresh(self):
        if self._muted:
            self.setText(" MUTED")
            self.setIcon(load_svg_icon("mic_off.svg", C_MUTED, 16))
            self.setStyleSheet(f"""
                QPushButton {{
                    background: #1a0008; color: {C_MUTED};
                    border: 1px solid {C_MUTED}; border-radius: 3px;
                    font-family: Courier New; font-size: 9pt; font-weight: bold;
                }}
            """)
        else:
            self.setText(" LIVE")
            self.setIcon(load_svg_icon("mic_on.svg", C_GREEN, 16))
            self.setStyleSheet(f"""
                QPushButton {{
                    background: {C_PANEL}; color: {C_GREEN};
                    border: 1px solid {C_MID}; border-radius: 3px;
                    font-family: Courier New; font-size: 9pt; font-weight: bold;
                }}
                QPushButton:hover {{
                    background: {C_DIMMER};
                }}
            """)


# ═══════════════════════════════════════════════════════════════════════════════
#   PANEL FRAME HELPER
# ═══════════════════════════════════════════════════════════════════════════════

def _make_panel(parent=None) -> QFrame:
    f = QFrame(parent)
    f.setStyleSheet(f"""
        QFrame {{
            background: {C_PANEL};
            border: 1px solid {C_BORDER};
            border-radius: 6px;
        }}
    """)
    return f


# ═══════════════════════════════════════════════════════════════════════════════
#  SETUP DIALOG  (API Key configuration — preserves original flow)
# ═══════════════════════════════════════════════════════════════════════════════

class SetupDialog(QWidget):
    done_signal = pyqtSignal()

    def __init__(self, detected_os: str, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Widget)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"""
            background: rgba(0,8,13,0.97);
            border: 1px solid {C_PRI};
            border-radius: 8px;
        """)

        self._selected_os = detected_os
        lay = QVBoxLayout(self)
        lay.setContentsMargins(32, 24, 32, 24)
        lay.setSpacing(12)

        title = QLabel("◈  INITIALISATION REQUIRED")
        title.setFont(QFont("Courier New", 13, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {C_PRI}; background: transparent; border: none;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(title)

        sub = QLabel("Configure J.A.R.V.I.S. before first boot.")
        sub.setFont(QFont("Courier New", 9))
        sub.setStyleSheet(f"color: {C_MID}; background: transparent; border: none;")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(sub)

        key_lbl = QLabel("GEMINI API KEY")
        key_lbl.setFont(QFont("Courier New", 9))
        key_lbl.setStyleSheet(f"color: {C_DIM}; background: transparent; border: none;")
        lay.addWidget(key_lbl)

        self._key_entry = QLineEdit()
        self._key_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self._key_entry.setPlaceholderText("Enter Gemini API Key…")
        self._key_entry.setFont(QFont("Courier New", 10))
        self._key_entry.setStyleSheet(f"""
            QLineEdit {{
                background: #000d12; color: {C_TEXT};
                border: 1px solid {C_DIM}; border-radius: 4px; padding: 6px 10px;
            }}
            QLineEdit:focus {{ border: 1px solid {C_PRI}; }}
        """)
        lay.addWidget(self._key_entry)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {C_DIM}; background: {C_DIM}; border: none; max-height: 1px;")
        lay.addWidget(sep)

        os_title = QLabel("SELECT OPERATING SYSTEM")
        os_title.setFont(QFont("Courier New", 9))
        os_title.setStyleSheet(f"color: {C_DIM}; background: transparent; border: none;")
        lay.addWidget(os_title)

        detect_map = {"windows": "Windows", "mac": "macOS", "linux": "Linux"}
        detect_lbl = QLabel(f"AUTO-DETECTED: {detect_map.get(detected_os, detected_os)}")
        detect_lbl.setFont(QFont("Courier New", 8))
        detect_lbl.setStyleSheet(f"color: {C_ACC2}; background: transparent; border: none;")
        lay.addWidget(detect_lbl)

        os_row = QHBoxLayout()
        os_row.setSpacing(8)
        os_options = [("windows", "WINDOWS"), ("mac", "macOS"), ("linux", "LINUX")]
        self._os_btns: dict[str, QPushButton] = {}
        for os_key, os_label in os_options:
            btn = QPushButton("  " + os_label)
            btn.setIcon(load_svg_icon({ "windows": "windows.svg", "mac": "mac.svg", "linux": "linux.svg"}[os_key], C_PRI, 18))
            btn.setFont(QFont("Courier New", 10, QFont.Weight.Bold))
            btn.setFixedHeight(36)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, k=os_key: self._select_os(k))
            self._os_btns[os_key] = btn
            os_row.addWidget(btn)
        lay.addLayout(os_row)
        self._select_os(detected_os)

        sep2 = QFrame(); sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setStyleSheet(f"color: {C_DIM}; background: {C_DIM}; border: none; max-height: 1px;")
        lay.addWidget(sep2)

        self._err_lbl = QLabel("")
        self._err_lbl.setFont(QFont("Courier New", 8))
        self._err_lbl.setStyleSheet(f"color: {C_RED}; background: transparent; border: none;")
        self._err_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self._err_lbl)

        go_btn = QPushButton("▸  INITIALISE SYSTEMS")
        go_btn.setFont(QFont("Courier New", 10))
        go_btn.setFixedHeight(40)
        go_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        go_btn.setStyleSheet(f"""
            QPushButton {{
                background: {C_BG}; color: {C_PRI};
                border: 1px solid {C_PRI}; border-radius: 4px;
            }}
            QPushButton:hover {{
                background: {C_DIM}; color: white;
            }}
        """)
        go_btn.clicked.connect(self._save)
        lay.addWidget(go_btn)

    def _select_os(self, os_key: str):
        self._selected_os = os_key
        styles = {
            "windows": (C_PRI,   "#001a22"),
            "mac":     (C_ACC2,  "#1a1500"),
            "linux":   (C_GREEN, "#001a0d"),
        }
        for key, btn in self._os_btns.items():
            if key == os_key:
                fg, bg = styles[key]
                btn.setStyleSheet(f"""
                    QPushButton {{
                        color: {bg}; background: {fg};
                        border: 1px solid {fg}; border-radius: 4px;
                        font-family: Courier New; font-size: 10pt; font-weight: bold;
                    }}
                """)
                btn.setIcon(load_svg_icon({ "windows": "windows.svg", "mac": "mac.svg", "linux": "linux.svg"}[key], bg, 18))
            else:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        color: {C_DIM}; background: {C_BG};
                        border: 1px solid {C_DIM}; border-radius: 4px;
                        font-family: Courier New; font-size: 10pt; font-weight: bold;
                    }}
                    QPushButton:hover {{ color: {C_TEXT}; background: {C_PANEL}; }}
                """)
                btn.setIcon(load_svg_icon({ "windows": "windows.svg", "mac": "mac.svg", "linux": "linux.svg"}[key], C_DIM, 18))

    def _save(self):
        gemini = self._key_entry.text().strip()
        if not gemini:
            self._err_lbl.setText("⚠  API key cannot be empty.")
            self._key_entry.setStyleSheet(self._key_entry.styleSheet() +
                                           f" border: 1px solid {C_RED};")
            return
        config_manager.save_api_keys(gemini)
        config_manager.save_os_system(self._selected_os)
        self.done_signal.emit()


# ═══════════════════════════════════════════════════════════════════════════════
#  HEADER  (title bar replica)
# ═══════════════════════════════════════════════════════════════════════════════

class HeaderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(62)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.update)
        self._timer.start(1000)

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        W, H = self.width(), self.height()

        p.fillRect(0, 0, W, H, QColor(C_PANEL2))
        p.setPen(QPen(qc(C_MID), 1))
        p.drawLine(0, H - 1, W, H - 1)

        p.setPen(qc(C_PRI))
        font = QFont("Orbitron", 18, QFont.Weight.Bold)
        font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 4)
        p.setFont(font)
        p.drawText(QRectF(0, 4, W, 32), Qt.AlignmentFlag.AlignHCenter,
                   SYSTEM_NAME)

        p.setPen(qc(C_MID))
        p.setFont(QFont("Courier New", 9))
        p.drawText(QRectF(0, 36, W, 20), Qt.AlignmentFlag.AlignHCenter,
                   "Just A Rather Very Intelligent System")

        p.setPen(qc(C_DIM))
        p.setFont(QFont("Courier New", 9))
        p.drawText(QRectF(12, 20, 200, 20),
                   Qt.AlignmentFlag.AlignLeft, MODEL_BADGE)

        p.setPen(qc(C_PRI))
        p.setFont(QFont("Courier New", 14, QFont.Weight.Bold))
        p.drawText(QRectF(W - 120, 18, 108, 26),
                   Qt.AlignmentFlag.AlignRight, time.strftime("%H:%M:%S"))
        p.end()


# ═══════════════════════════════════════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════════════════════════════════════

class FooterWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(28)

    def paintEvent(self, _):
        p = QPainter(self)
        W, H = self.width(), self.height()
        p.fillRect(0, 0, W, H, QColor(C_PANEL2))
        p.setPen(QPen(qc(C_DIM), 1))
        p.drawLine(0, 0, W, 0)
        p.setPen(qc(C_DIM))
        p.setFont(QFont("Courier New", 8))
        p.drawText(QRectF(W - 120, 0, 108, H),
                   Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                   "[F4] MUTE")
        p.drawText(QRectF(0, 0, W, H), Qt.AlignmentFlag.AlignCenter,
                   "FatihMakes Industries  ·  CLASSIFIED  ·  MARK XXXVII")
        p.end()


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN WINDOW — JarvisUI
# ═══════════════════════════════════════════════════════════════════════════════

class JarvisUI(QMainWindow):
    """
    Complete PyQt6 implementation of J.A.R.V.I.S.
    ──────────────────────────────────────────────
    All public APIs from the original tkinter version are preserved.
    """

    # Qt signal for thread-safe log updates
    _log_signal         = pyqtSignal(str)
    _state_signal       = pyqtSignal(str)
    _camera_signal      = pyqtSignal(bytes, int, int)
    _gesture_signal     = pyqtSignal(str)
    _boot_done_signal   = pyqtSignal()
    _request_setup_signal = pyqtSignal()

    def __init__(self, face_path, size=None):
        # ── QApplication must exist before QMainWindow ────────────────────────
        if not QApplication.instance():
            self._app = QApplication(sys.argv)
        else:
            self._app = QApplication.instance()

        self._app.setStyle("Fusion")
        pal = QPalette()
        pal.setColor(QPalette.ColorRole.Window, QColor(C_BG))
        pal.setColor(QPalette.ColorRole.WindowText, QColor(C_TEXT))
        self._app.setPalette(pal)

        super().__init__()
        self.setWindowTitle("J.A.R.V.I.S — MARK XXXVII")

        # ── Geometry ─────────────────────────────────────────────────────────
        screen = self._app.primaryScreen().geometry()
        W = 1000
        H = 750
        self.setMinimumSize(600, 450)
        self.move((screen.width() - W) // 2, (screen.height() - H) // 2)
        self.setStyleSheet(f"background: {C_BG};")
        self.showMaximized()

        # ── State ─────────────────────────────────────────────────────────────
        self.muted           = False
        self.speaking        = False
        self.boot_finished   = False
        self.on_text_command = None       # preserved callback

        self.FACE_SZ        = 400         # kept for back-compat
        self.FCX            = W // 2
        self.FCY            = int(H * 0.13) + 200

        self._jarvis_state  = "INITIALISING"
        self.status_text    = "INITIALISING"
        self.status_blink   = True
        self.typing_queue   = deque()
        self.is_typing      = False

        self._api_key_ready = False

        # ── Build UI ──────────────────────────────────────────────────────────
        self._build_ui()

        # ── Load face image (preserved) ───────────────────────────────────────
        self._face_pil         = None
        self._has_face         = False
        self._face_scale_cache = None
        self._load_face(face_path)

        # ── Signals (thread-safe bridge) ──────────────────────────────────────
        self._log_signal.connect(self._on_log_signal)
        self._state_signal.connect(self._on_state_signal)
        self._camera_signal.connect(self._on_camera_signal)
        self._gesture_signal.connect(self._cam_widget.show_gesture)
        self._boot_done_signal.connect(self._on_boot_done)
        self._request_setup_signal.connect(self._show_setup_ui)

        # ── API Key check ─────────────────────────────────────────────────────
        self._api_key_ready = self._api_keys_exist()
        if not self._api_key_ready:
            self._show_setup_ui()

        # ── Compat shim ───────────────────────────────────────────────────────
        self.root = _RootShim(self._app)

        # ── Show ──────────────────────────────────────────────────────────────
        self.show()

    # ─────────────────────────────────────────────────────────────────────────
    #  UI CONSTRUCTION
    # ─────────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        self._stack = QStackedWidget()
        self.setCentralWidget(self._stack)

        # ── BOOT SEQUENCE VIEW ───────────────────────────────────────────────
        self._boot_view = BootHUDWidget()
        self._stack.addWidget(self._boot_view)

        # ── MAIN DASHBOARD VIEW ──────────────────────────────────────────────
        main_view = QWidget()
        main_view.setStyleSheet(f"background: {C_BG};")
        self._stack.addWidget(main_view)
        
        root_lay = QVBoxLayout(main_view)
        root_lay.setContentsMargins(0, 0, 0, 0)
        root_lay.setSpacing(0)

        # Header
        self._header = HeaderWidget()
        root_lay.addWidget(self._header)

        # Body (3 columns)
        body = QWidget()
        body.setStyleSheet("background: transparent;")
        body_lay = QHBoxLayout(body)
        body_lay.setContentsMargins(8, 8, 8, 8)
        body_lay.setSpacing(8)

        # ── LEFT PANEL ───────────────────────────────────────────────────────
        left = QWidget()
        left.setFixedWidth(225)
        left.setStyleSheet("background: transparent;")
        left_lay = QVBoxLayout(left)
        left_lay.setContentsMargins(0, 0, 0, 0)
        left_lay.setSpacing(8)

        stats_panel = _make_panel()
        stats_panel.setFixedHeight(240)
        self._stats = StatsWidget(stats_panel)
        sp_lay = QVBoxLayout(stats_panel)
        sp_lay.setContentsMargins(0, 0, 0, 0)
        sp_lay.addWidget(self._stats)
        left_lay.addWidget(stats_panel)

        sysinfo_panel = _make_panel()
        sysinfo_panel.setFixedHeight(150)
        self._sysinfo = SysInfoWidget(sysinfo_panel)
        si_lay = QVBoxLayout(sysinfo_panel)
        si_lay.setContentsMargins(0, 0, 0, 0)
        si_lay.addWidget(self._sysinfo)
        left_lay.addWidget(sysinfo_panel)

        qa_panel = _make_panel()
        self._qa = QuickActionsWidget(qa_panel)
        qa_lay = QVBoxLayout(qa_panel)
        qa_lay.setContentsMargins(0, 0, 0, 0)
        qa_lay.addWidget(self._qa)
        left_lay.addWidget(qa_panel, 1)

        body_lay.addWidget(left)

        # ── CENTER PANEL ─────────────────────────────────────────────────────
        center = QWidget()
        center.setStyleSheet("background: transparent;")
        center_lay = QVBoxLayout(center)
        center_lay.setContentsMargins(0, 0, 0, 0)
        center_lay.setSpacing(6)

        self._globe = HologramWidget()
        center_lay.addWidget(self._globe, 1, Qt.AlignmentFlag.AlignCenter)

        self._status_widget = StatusWidget()
        center_lay.addWidget(self._status_widget)

        # Waveform + mute bar
        wave_bar = QWidget()
        wave_bar.setStyleSheet("background: transparent;")
        wb_lay = QHBoxLayout(wave_bar)
        wb_lay.setContentsMargins(0, 0, 0, 0)
        wb_lay.setSpacing(8)

        self._mute_btn = MuteButton()
        self._mute_btn.clicked.connect(self._toggle_mute)
        wb_lay.addWidget(self._mute_btn)

        self._waveform = WaveformWidget()
        wb_lay.addWidget(self._waveform, 1)

        center_lay.addWidget(wave_bar)

        # Input bar
        self._input_bar = InputBarWidget()
        self._input_bar.submitted.connect(self._on_input_submit)
        center_lay.addWidget(self._input_bar)

        body_lay.addWidget(center, 1)

        # ── RIGHT PANEL ──────────────────────────────────────────────────────
        right = QWidget()
        right.setFixedWidth(265)
        right.setStyleSheet("background: transparent;")
        right_lay = QVBoxLayout(right)
        right_lay.setContentsMargins(0, 0, 0, 0)
        right_lay.setSpacing(8)

        # Chat panel
        chat_panel = _make_panel()
        self._chat = ChatWidget()
        chat_inner = QVBoxLayout(chat_panel)
        chat_inner.setContentsMargins(0, 0, 0, 0)
        chat_inner.addWidget(self._chat)
        right_lay.addWidget(chat_panel, 2)

        # Camera panel
        cam_panel = _make_panel()
        cam_panel.setFixedHeight(220)
        cam_header = QWidget(cam_panel)
        cam_header.setFixedHeight(28)
        cam_header.setStyleSheet(f"background: {C_PANEL2}; border-radius: 4px 4px 0 0;")
        ch_lay = QHBoxLayout(cam_header)
        ch_lay.setContentsMargins(10, 0, 10, 0)
        cam_dot = QLabel("●")
        cam_dot.setStyleSheet(f"color: {C_GREEN}; font-size: 8pt; background: transparent;")
        ch_lay.addWidget(cam_dot)
        cam_title = QLabel("  CAMERA")
        cam_title.setFont(QFont("Courier New", 9, QFont.Weight.Bold))
        cam_title.setStyleSheet(f"color: {C_PRI}; background: transparent;")
        ch_lay.addWidget(cam_title)
        ch_lay.addStretch()

        cam_inner = QVBoxLayout(cam_panel)
        cam_inner.setContentsMargins(0, 0, 0, 0)
        cam_inner.setSpacing(0)
        cam_inner.addWidget(cam_header)

        self._cam_widget = CameraWidget()
        cam_inner.addWidget(self._cam_widget, 1)

        right_lay.addWidget(cam_panel)

        body_lay.addWidget(right)

        root_lay.addWidget(body, 1)

        # Footer
        self._footer = FooterWidget()
        root_lay.addWidget(self._footer)

    # ─────────────────────────────────────────────────────────────────────────
    #  KEYBOARD SHORTCUTS
    # ─────────────────────────────────────────────────────────────────────────

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_F4:
            self._toggle_mute()
        super().keyPressEvent(event)

    def closeEvent(self, _):
        os._exit(0)

    # ─────────────────────────────────────────────────────────────────────────
    #  ORIGINAL PRESERVED: _load_face
    # ─────────────────────────────────────────────────────────────────────────

    def _load_face(self, path):
        FW = self.FACE_SZ
        try:
            if _PIL:
                img  = Image.open(path).convert("RGBA").resize((FW, FW), Image.LANCZOS)
                mask = Image.new("L", (FW, FW), 0)
                ImageDraw.Draw(mask).ellipse((2, 2, FW - 2, FW - 2), fill=255)
                img.putalpha(mask)
                self._face_pil = img
                self._has_face = True
        except Exception:
            self._has_face = False

    # ─────────────────────────────────────────────────────────────────────────
    #  ORIGINAL PRESERVED: _ac (alpha colour helper)
    # ─────────────────────────────────────────────────────────────────────────

    @staticmethod
    def _ac(r, g, b, a):
        f = a / 255.0
        return f"#{int(r*f):02x}{int(g*f):02x}{int(b*f):02x}"

    # ─────────────────────────────────────────────────────────────────────────
    #  ORIGINAL PRESERVED: set_state
    # ─────────────────────────────────────────────────────────────────────────

    def set_state(self, state: str):
        """Thread-safe — callable from any thread."""
        self._jarvis_state = state
        if state == "MUTED":
            self.status_text = "MUTED"
            self.speaking    = False
        elif state == "SPEAKING":
            self.status_text = "SPEAKING"
            self.speaking    = True
        elif state == "THINKING":
            self.status_text = "THINKING"
            self.speaking    = False
        elif state == "LISTENING":
            self.status_text = "LISTENING"
            self.speaking    = False
        elif state == "PROCESSING":
            self.status_text = "PROCESSING"
            self.speaking    = False
        else:
            self.status_text = "ONLINE"
            self.speaking    = False

        self._state_signal.emit(state)

    def _on_state_signal(self, state: str):
        self._status_widget.set_state(state)
        self._globe.set_state(state) # Sync matrix state (e.g. THINKING physics)
        self._globe.set_speaking(self.speaking)
        self._globe.set_muted(self.muted)
        self._waveform.set_speaking(self.speaking)
        self._waveform.set_muted(self.muted)

    def notify_vision_ready(self):
        """Thread-safe signal to finish boot sequence."""
        self._boot_done_signal.emit()

    def _on_boot_done(self):
        """Perform the actual UI transition on the main thread."""
        if self.boot_finished:
            return
        self._boot_view.set_progress(100.0)
        
        def _on_finish():
            self._stack.setCurrentIndex(1)
            self.boot_finished = True
            self.write_log("SYS: Vision systems active.")
        
        QTimer.singleShot(800, _on_finish)

    # ─────────────────────────────────────────────────────────────────────────
    #  ORIGINAL PRESERVED: write_log
    # ─────────────────────────────────────────────────────────────────────────

    def write_log(self, text: str):
        """Thread-safe — callable from any thread."""
        tl = text.lower()
        if tl.startswith("you:"):
            self.set_state("PROCESSING")
        elif tl.startswith("jarvis:") or tl.startswith("ai:"):
            self.set_state("SPEAKING")
        self._log_signal.emit(text)

    def _on_log_signal(self, text: str):
        self._chat.write_log(text)

    # ─────────────────────────────────────────────────────────────────────────
    #  ORIGINAL PRESERVED: start_speaking / stop_speaking
    # ─────────────────────────────────────────────────────────────────────────

    def start_speaking(self):
        self.set_state("SPEAKING")

    def stop_speaking(self):
        if not self.muted:
            self.set_state("LISTENING")

    # ─────────────────────────────────────────────────────────────────────────
    #  ORIGINAL PRESERVED: _toggle_mute
    # ─────────────────────────────────────────────────────────────────────────

    def keyPressEvent(self, event):
        """Handle global UI hotkeys."""
        if event.key() == Qt.Key.Key_Escape:
            if self.isMaximized():
                self.showNormal()
                self.resize(1000, 750)
            else:
                self.showMaximized()
        elif event.key() == Qt.Key.Key_F4:
            self._toggle_mute()
        super().keyPressEvent(event)

    def _toggle_mute(self):
        self.muted = not self.muted
        self._mute_btn.toggle()
        if self.muted:
            self.set_state("MUTED")
            self.write_log("SYS: Microphone muted.")
        else:
            self.set_state("LISTENING")
            self.write_log("SYS: Microphone active.")

    # ─────────────────────────────────────────────────────────────────────────
    #  ORIGINAL PRESERVED: _on_input_submit / _build_input_bar
    # ─────────────────────────────────────────────────────────────────────────

    def _on_input_submit(self, text: str):
        """Called by InputBarWidget.submitted signal."""
        self.write_log(f"You: {text}")
        if self.on_text_command:
            threading.Thread(
                target=self.on_text_command,
                args=(text,),
                daemon=True,
            ).start()

    # ─────────────────────────────────────────────────────────────────────────
    #  ORIGINAL PRESERVED: _api_keys_exist / wait_for_api_key
    # ─────────────────────────────────────────────────────────────────────────

    def _api_keys_exist(self) -> bool:
        return config_manager.is_configured()

    def wait_for_api_key(self):
        while not self._api_key_ready:
            time.sleep(0.1)

    # ─────────────────────────────────────────────────────────────────────────
    #  ORIGINAL PRESERVED: _detect_os / _show_setup_ui
    # ─────────────────────────────────────────────────────────────────────────

    @staticmethod
    def _detect_os() -> str:
        s = platform.system().lower()
        if s == "darwin":   return "mac"
        if s == "windows":  return "windows"
        return "linux"

    def _show_setup_ui(self):
        self._api_key_ready = False
        self._setup_overlay = QWidget(self.centralWidget())
        self._setup_overlay.setStyleSheet("background: rgba(0,0,0,180);")
        self._setup_overlay.resize(self.centralWidget().size())
        self._setup_overlay.show()

        self._setup_dialog = SetupDialog(self._detect_os(), self._setup_overlay)
        self._setup_dialog.done_signal.connect(self._on_setup_done)

        # Center the dialog
        dialog_w, dialog_h = 480, 420
        ox = (self._setup_overlay.width()  - dialog_w) // 2
        oy = (self._setup_overlay.height() - dialog_h) // 2
        self._setup_dialog.setGeometry(ox, oy, dialog_w, dialog_h)
        self._setup_dialog.show()

    def _on_setup_done(self):
        self._setup_overlay.hide()
        self._api_key_ready = True
        self.set_state("LISTENING")
        self.write_log("SYS: Systems initialised. JARVIS online.")

    # ─────────────────────────────────────────────────────────────────────────
    #  CAMERA FEED  (called by vision_manager.py)
    # ─────────────────────────────────────────────────────────────────────────

    def update_camera_frame(self, bgr_bytes: bytes, w: int, h: int):
        """Thread-safe camera frame update."""
        self._camera_signal.emit(bgr_bytes, w, h)

    def _on_camera_signal(self, bgr_bytes: bytes, w: int, h: int):
        self._cam_widget.set_frame(bgr_bytes, w, h)

    def on_gesture_detected(self, gesture: str):
        """Thread-safe gesture callback — called by VisionManager."""
        self._gesture_signal.emit(gesture)