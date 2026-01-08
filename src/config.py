from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class AppConfig:
    faces_dir: str = "faces"
    camera_index: int = 0

    # Recognition
    tolerance: float = 0.6
    vote_window: int = 7

    # Tracking
    track_iou_threshold: float = 0.3
    track_ttl_seconds: float = 1.0

    # DeepFace scheduling
    detect_every_n_frames: int = 3
    analysis_every_n_frames: int = 90
    attribute_ttl_seconds: float = 5.0
    max_queue_size: int = 1
    deepface_backend: str = "opencv"     # "opencv" o "retinaface"
    deepface_align: bool = False
    deepface_enforce_detection: bool = False

    # Performance
    resize_width_for_speed: int = 640

    # UI
    color_known_bgr: Tuple[int, int, int] = (0, 255, 80)   # neon green
    color_unknown_bgr: Tuple[int, int, int] = (0, 0, 255)  # red
    color_hud_bgr: Tuple[int, int, int] = (80, 255, 0)
    color_text_bgr: Tuple[int, int, int] = (230, 230, 230)
