from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from .utils import iou

@dataclass
class FaceTrack:
    track_id: int
    bbox: Tuple[int, int, int, int]  # (top,right,bottom,left)
    last_seen_ts: float

    name_votes: List[str] = field(default_factory=list)
    stable_name: str = "Unknown"

    last_attrs: Dict[str, object] = field(default_factory=dict)
    last_attr_ts: float = 0.0
    last_analyzed_frame: int = -1

    def update_bbox(self, bbox, ts: float) -> None:
        self.bbox = bbox
        self.last_seen_ts = ts

    def vote_name(self, name: str, window: int) -> None:
        self.name_votes.append(name)
        if len(self.name_votes) > window:
            self.name_votes.pop(0)

        counts: Dict[str, int] = {}
        for n in self.name_votes:
            counts[n] = counts.get(n, 0) + 1
        self.stable_name = max(counts.items(), key=lambda kv: kv[1])[0]

class TrackManager:
    def __init__(self, iou_threshold: float, ttl_seconds: float):
        self.iou_threshold = iou_threshold
        self.ttl_seconds = ttl_seconds
        self._next_id = 1
        self.tracks: Dict[int, FaceTrack] = {}

    def update(self, detections: List[Tuple[int,int,int,int]], ts: float) -> None:
        if not detections:
            return
        if not self.tracks:
            for d in detections:
                self._create(d, ts)
            return

        pairs = []
        for tid, tr in self.tracks.items():
            for d in detections:
                pairs.append((iou(tr.bbox, d), tid, d))
        pairs.sort(key=lambda x: x[0], reverse=True)

        used_tracks = set()
        used_dets = set()

        for score, tid, d in pairs:
            if score < self.iou_threshold:
                break
            if tid in used_tracks or d in used_dets:
                continue
            self.tracks[tid].update_bbox(d, ts)
            used_tracks.add(tid)
            used_dets.add(d)

        for d in detections:
            if d not in used_dets:
                self._create(d, ts)

    def assign_track_id(self, bbox) -> Optional[int]:
        best_tid, best = None, 0.0
        for tid, tr in self.tracks.items():
            score = iou(tr.bbox, bbox)
            if score > best:
                best = score
                best_tid = tid
        return best_tid

    def cleanup(self, ts: float) -> None:
        stale = [tid for tid, tr in self.tracks.items() if (ts - tr.last_seen_ts) > self.ttl_seconds]
        for tid in stale:
            del self.tracks[tid]

    def _create(self, bbox, ts: float) -> None:
        tid = self._next_id
        self._next_id += 1
        self.tracks[tid] = FaceTrack(track_id=tid, bbox=bbox, last_seen_ts=ts)

