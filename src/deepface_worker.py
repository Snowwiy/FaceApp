import threading
import queue
from dataclasses import dataclass
from typing import Dict, Optional
import numpy as np
from deepface import DeepFace

@dataclass
class AnalysisRequest:
    face_roi_bgr: np.ndarray
    track_id: int
    frame_index: int
    ts: float

@dataclass
class AnalysisResult:
    track_id: int
    frame_index: int
    ts: float
    attrs: Dict[str, object]

class DeepFaceWorker:
    def __init__(
        self,
        detector_backend: str,
        enforce_detection: bool,
        align: bool,
        max_queue_size: int = 4,
        actions = ("age", "gender", "emotion"),
    ):
        self.detector_backend = detector_backend
        self.enforce_detection = enforce_detection
        self.align = align
        self.actions = list(actions)

        self.req_q: "queue.Queue[AnalysisRequest]" = queue.Queue(maxsize=max_queue_size)
        self.res_q: "queue.Queue[AnalysisResult]" = queue.Queue()
        self._stop = threading.Event()
        self._t = threading.Thread(target=self._loop, daemon=True)

    def start(self) -> None:
        self._t.start()

    def stop(self) -> None:
        self._stop.set()

    def try_submit(self, req: AnalysisRequest) -> bool:
        try:
            self.req_q.put_nowait(req)
            return True
        except queue.Full:
            return False

    def drain_results(self):
        out = []
        while True:
            try:
                out.append(self.res_q.get_nowait())
            except queue.Empty:
                break
        return out

    def _loop(self) -> None:
        while not self._stop.is_set():
            try:
                req = self.req_q.get(timeout=0.1)
            except queue.Empty:
                continue

            attrs = {"age": None, "gender": None, "emotion": None, "confidence": None}
            try:
                analysis = DeepFace.analyze(
                    img_path=req.face_roi_bgr,
                    actions=self.actions,
                    enforce_detection=self.enforce_detection,
                    detector_backend=self.detector_backend,
                    align=self.align,
                )

                if isinstance(analysis, list) and analysis:
                    analysis = analysis[0]

                if isinstance(analysis, dict):
                    if "age" in analysis:
                        try:
                            attrs["age"] = int(round(float(analysis["age"])))
                        except Exception:
                            pass

                    if "gender" in analysis:
                        g = analysis["gender"]
                        if isinstance(g, str):
                            attrs["gender"] = g
                        elif isinstance(g, dict) and g:
                            attrs["gender"] = max(g.items(), key=lambda kv: kv[1])[0]

                    if "dominant_emotion" in analysis:
                        attrs["emotion"] = analysis["dominant_emotion"]
                    elif "emotion" in analysis:
                        e = analysis["emotion"]
                        if isinstance(e, dict) and e:
                            attrs["emotion"] = max(e.items(), key=lambda kv: kv[1])[0]
                        elif isinstance(e, str):
                            attrs["emotion"] = e

                    if "face_confidence" in analysis:
                        try:
                            attrs["confidence"] = float(analysis["face_confidence"])
                        except Exception:
                            pass
            except Exception:
                pass

            try:
                self.res_q.put_nowait(AnalysisResult(req.track_id, req.frame_index, req.ts, attrs))
            except queue.Full:
                pass
