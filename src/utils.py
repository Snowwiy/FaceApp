<<<<<<< HEAD
import time
from typing import Tuple
import numpy as np
import cv2

def resize_keep_aspect(frame_bgr: np.ndarray, target_width: int) -> Tuple[np.ndarray, float]:
    h, w = frame_bgr.shape[:2]
    if target_width <= 0 or w <= target_width:
        return frame_bgr, 1.0
    scale = target_width / float(w)
    new_h = int(round(h * scale))
    resized = cv2.resize(frame_bgr, (target_width, new_h), interpolation=cv2.INTER_LINEAR)
    return resized, scale

def iou(a, b) -> float:
    # a,b in (top, right, bottom, left)
    at, ar, ab, al = a
    bt, br, bb, bl = b
    ax1, ay1, ax2, ay2 = al, at, ar, ab
    bx1, by1, bx2, by2 = bl, bt, br, bb

    inter_x1 = max(ax1, bx1)
    inter_y1 = max(ay1, by1)
    inter_x2 = min(ax2, bx2)
    inter_y2 = min(ay2, by2)

    inter_w = max(0, inter_x2 - inter_x1)
    inter_h = max(0, inter_y2 - inter_y1)
    inter_area = inter_w * inter_h

    area_a = max(0, ax2 - ax1) * max(0, ay2 - ay1)
    area_b = max(0, bx2 - bx1) * max(0, by2 - by1)

    denom = float(area_a + area_b - inter_area)
    return 0.0 if denom <= 0 else inter_area / denom

class FPSCounter:
    def __init__(self):
        self._fps = 0.0
        self._last_ts = time.time()
        self._frames = 0

    def update(self) -> float:
        self._frames += 1
        now = time.time()
        dt = now - self._last_ts
        if dt >= 0.5:
            self._fps = self._frames / dt
            self._frames = 0
            self._last_ts = now
        return self._fps

    @property
    def fps(self) -> float:
        return self._fps

=======
import time
from typing import Tuple
import numpy as np
import cv2

def resize_keep_aspect(frame_bgr: np.ndarray, target_width: int) -> Tuple[np.ndarray, float]:
    h, w = frame_bgr.shape[:2]
    if target_width <= 0 or w <= target_width:
        return frame_bgr, 1.0
    scale = target_width / float(w)
    new_h = int(round(h * scale))
    resized = cv2.resize(frame_bgr, (target_width, new_h), interpolation=cv2.INTER_LINEAR)
    return resized, scale

def iou(a, b) -> float:
    # a,b in (top, right, bottom, left)
    at, ar, ab, al = a
    bt, br, bb, bl = b
    ax1, ay1, ax2, ay2 = al, at, ar, ab
    bx1, by1, bx2, by2 = bl, bt, br, bb

    inter_x1 = max(ax1, bx1)
    inter_y1 = max(ay1, by1)
    inter_x2 = min(ax2, bx2)
    inter_y2 = min(ay2, by2)

    inter_w = max(0, inter_x2 - inter_x1)
    inter_h = max(0, inter_y2 - inter_y1)
    inter_area = inter_w * inter_h

    area_a = max(0, ax2 - ax1) * max(0, ay2 - ay1)
    area_b = max(0, bx2 - bx1) * max(0, by2 - by1)

    denom = float(area_a + area_b - inter_area)
    return 0.0 if denom <= 0 else inter_area / denom

class FPSCounter:
    def __init__(self):
        self._fps = 0.0
        self._last_ts = time.time()
        self._frames = 0

    def update(self) -> float:
        self._frames += 1
        now = time.time()
        dt = now - self._last_ts
        if dt >= 0.5:
            self._fps = self._frames / dt
            self._frames = 0
            self._last_ts = now
        return self._fps

    @property
    def fps(self) -> float:
        return self._fps

>>>>>>> 000509f (Initial commit)
    