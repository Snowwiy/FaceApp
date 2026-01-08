from typing import Dict, Tuple, List
import cv2
import numpy as np

FONT = cv2.FONT_HERSHEY_DUPLEX

def font_scale_for_frame(frame_bgr: np.ndarray) -> float:
    h, _ = frame_bgr.shape[:2]
    base = max(0.5, min(1.2, h / 720.0))
    return 0.6 * base

def draw_summary_box(
    frame_bgr: np.ndarray,
    lines: List[str],
    color_border_bgr: Tuple[int,int,int],
    color_text_bgr: Tuple[int,int,int],
) -> None:
    pad = 10
    fs = font_scale_for_frame(frame_bgr)
    thickness = 1
    sizes = [cv2.getTextSize(t, FONT, fs, thickness)[0] for t in lines]
    box_w = max(w for w, h in sizes) + 2 * pad
    box_h = sum(h for w, h in sizes) + (len(lines) + 1) * pad

    x1, y1 = 12, 12
    x2, y2 = x1 + box_w, y1 + box_h
    cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), (0,0,0), -1)
    cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), color_border_bgr, 1)

    y = y1 + pad + sizes[0][1]
    for i, t in enumerate(lines):
        cv2.putText(frame_bgr, t, (x1 + pad, y), FONT, fs, color_text_bgr, thickness, cv2.LINE_AA)
        if i + 1 < len(lines):
            y += sizes[i+1][1] + pad

def draw_face_label(
    frame_bgr: np.ndarray,
    bbox: Tuple[int,int,int,int],
    lines: List[str],
    color_border_bgr: Tuple[int,int,int],
    color_text_bgr: Tuple[int,int,int],
) -> None:
    top, right, bottom, left = bbox
    cv2.rectangle(frame_bgr, (left, top), (right, bottom), color_border_bgr, 2)

    pad = 6
    fs = font_scale_for_frame(frame_bgr)
    thickness = 1

    sizes = [cv2.getTextSize(t, FONT, fs, thickness)[0] for t in lines]
    box_w = max(w for w, h in sizes) + 2 * pad
    box_h = sum(h for w, h in sizes) + (len(lines) + 1) * pad

    x1 = left
    y1 = top - box_h - 4
    if y1 < 0:
        y1 = top + 4
    x2 = min(frame_bgr.shape[1]-1, x1 + box_w)
    y2 = min(frame_bgr.shape[0]-1, y1 + box_h)

    cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), (0,0,0), -1)
    cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), color_border_bgr, 1)

    y = y1 + pad + sizes[0][1]
    for i, t in enumerate(lines):
        cv2.putText(frame_bgr, t, (x1 + pad, y), FONT, fs, color_text_bgr, thickness, cv2.LINE_AA)
        if i + 1 < len(lines):
            y += sizes[i+1][1] + pad
