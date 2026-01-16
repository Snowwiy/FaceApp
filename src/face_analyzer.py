import time
from typing import List, Tuple
import numpy as np
import cv2
import face_recognition

from .config import AppConfig
from .db import load_face_database
from .tracker import TrackManager
from .deepface_worker import DeepFaceWorker, AnalysisRequest
from .utils import resize_keep_aspect, FPSCounter
from .ui import draw_face_label, draw_summary_box

class FaceAnalyzer:
    """
    cámara + reconocimiento + tracking + scheduling de DeepFace + UI.
    """

    def __init__(self, cfg: AppConfig) -> None:
        self.cfg = cfg
        self.known_encodings, self.known_names = load_face_database(cfg.faces_dir)

        self.tracks = TrackManager(cfg.track_iou_threshold, cfg.track_ttl_seconds)
        self._last_face_locations = []
        self._last_face_encodings = []


        self.worker = DeepFaceWorker(
            detector_backend=cfg.deepface_backend,
            enforce_detection=cfg.deepface_enforce_detection,
            align=cfg.deepface_align,
            max_queue_size=cfg.max_queue_size,
            actions=("age", "gender", "emotion"),
            use_gpu=cfg.use_gpu,
        )

        self.fps = FPSCounter()

    def match_identity(self, face_encoding: np.ndarray) -> str:
        if self.known_encodings.shape[0] == 0:
            return "Unknown"
        dists = face_recognition.face_distance(self.known_encodings, face_encoding)
        best_idx = int(np.argmin(dists))
        best_dist = float(dists[best_idx])
        return self.known_names[best_idx] if best_dist <= self.cfg.tolerance else "Unknown"

    def run(self) -> None:
        self.worker.start()

        cap = cv2.VideoCapture(self.cfg.camera_index, cv2.CAP_DSHOW)
        if not cap.isOpened():
            raise RuntimeError(f"No se pudo abrir la cámara {self.cfg.camera_index}")
        
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
        cap.set(cv2.CAP_PROP_FPS, 60)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)


        frame_index = 0
        win = "FaceAnalyzer"
        cv2.namedWindow(win, cv2.WINDOW_NORMAL)

        try:
            while True:
                ok, frame_bgr = cap.read()
                if not ok or frame_bgr is None:
                    continue

                frame_index += 1
                ts = time.time()

                frame_bgr, _ = resize_keep_aspect(frame_bgr, self.cfg.resize_width_for_speed)
                frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

                # Consumir resultados DeepFace
                for res in self.worker.drain_results():
                    tr = self.tracks.tracks.get(res.track_id)
                    if tr:
                        tr.last_attrs = res.attrs
                        tr.last_attr_ts = res.ts

                # Detectar caras
                do_detect = (frame_index % self.cfg.detect_every_n_frames == 0)
                if do_detect:
                    face_locations = face_recognition.face_locations(frame_rgb, model="hog")
                    face_encs = (face_recognition.face_encodings(frame_rgb, face_locations) if face_locations else []
                    )
                    self._last_face_locations = face_locations
                    self._last_face_encodings = face_encs
                else:
                    face_locations = self._last_face_locations
                    face_encs = self._last_face_encodings

                # Tracking
                self.tracks.update(face_locations, ts)

                # Reconocimiento + scheduling
                for loc, enc in zip(face_locations, face_encs):
                    tid = self.tracks.assign_track_id(loc)
                    if tid is None:
                        continue

                    name = self.match_identity(enc)
                    self.tracks.tracks[tid].vote_name(name, self.cfg.vote_window)

                    self._maybe_schedule_deepface(frame_bgr, loc, tid, frame_index, ts)

                self.tracks.cleanup(ts)
                self.fps.update()

                # Overlay UI
                out = frame_bgr.copy()
                for tid, tr in self.tracks.tracks.items():
                    name = tr.stable_name
                    color = self.cfg.color_known_bgr if name != "Unknown" else self.cfg.color_unknown_bgr

                    lines = [f"{name}  (ID:{tid})"]
                    if tr.last_attrs and (ts - tr.last_attr_ts) <= self.cfg.attribute_ttl_seconds:
                        age = tr.last_attrs.get("age")
                        gender = tr.last_attrs.get("gender")
                        emo = tr.last_attrs.get("emotion")
                        parts = []
                        if age is not None: parts.append(f"Age: {age}")
                        if gender: parts.append(f"Gender: {gender}")
                        if emo: parts.append(f"Emotion: {emo}")
                        if parts:
                            lines.append(" | ".join(parts))

                    draw_face_label(out, tr.bbox, lines, color, self.cfg.color_text_bgr)

                draw_summary_box(
                    out,
                    [f"Faces: {len(self.tracks.tracks)}", f"FPS: {self.fps.fps:.1f}"],
                    self.cfg.color_hud_bgr,
                    self.cfg.color_text_bgr,
                )

                cv2.imshow(win, out)
                if (cv2.waitKey(1) & 0xFF) == ord("q"):
                    break
        finally:
            self.worker.stop()
            cap.release()
            cv2.destroyAllWindows()

    def _maybe_schedule_deepface(self, frame_bgr, bbox, track_id, frame_index, ts) -> None:
        tr = self.tracks.tracks.get(track_id)
        if not tr:
            return

        # TTL de atributos
        if tr.last_attrs and (ts - tr.last_attr_ts) < self.cfg.attribute_ttl_seconds:
            return

        # Cadencia por frames
        if tr.last_analyzed_frame >= 0 and (frame_index - tr.last_analyzed_frame) < self.cfg.analysis_every_n_frames:
            return

        top, right, bottom, left = bbox
        h, w = frame_bgr.shape[:2]
        top = max(0, top); left = max(0, left)
        bottom = min(h, bottom); right = min(w, right)
        if bottom <= top or right <= left:
            return

        roi = frame_bgr[top:bottom, left:right]
        if roi.size == 0:
            return

        submitted = self.worker.try_submit(AnalysisRequest(roi, track_id, frame_index, ts))
        if submitted:
            tr.last_analyzed_frame = frame_index
