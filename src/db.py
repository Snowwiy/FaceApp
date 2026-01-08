<<<<<<< HEAD
import os
from typing import List, Tuple
import numpy as np
import face_recognition

def load_face_database(faces_dir: str) -> Tuple[np.ndarray, List[str]]:
    """
    Scan faces_dir and compute encodings once.
    Returns:
        known_encodings: (N,128) float32 array
        known_names: list[str]
    """
    if not os.path.isdir(faces_dir):
        os.makedirs(faces_dir, exist_ok=True)

    exts = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
    files = [f for f in os.listdir(faces_dir) if f.lower().endswith(exts)]
    files.sort()

    encodings = []
    names = []

    if not files:
        print(f"[INFO] No images in {faces_dir}. All faces will be Unknown.")

    for fname in files:
        path = os.path.join(faces_dir, fname)
        name = os.path.splitext(fname)[0]
        try:
            img = face_recognition.load_image_file(path)
            locs = face_recognition.face_locations(img, model="hog", number_of_times_to_upsample=1)
            if not locs:
                print(f"[WARN] No face detected in '{path}', skipping.")
                continue
            enc = face_recognition.face_encodings(img, known_face_locations=locs)
            if not enc:
                print(f"[WARN] Encoding failed for '{path}', skipping.")
                continue
            encodings.append(enc[0].astype(np.float32))
            names.append(name)
            print(f"[OK] Loaded: {name}")
        except Exception as e:
            print(f"[WARN] Error loading '{path}': {e}")

    if encodings:
        return np.vstack(encodings), names
    return np.empty((0, 128), dtype=np.float32), []
=======
import os
from typing import List, Tuple
import numpy as np
import face_recognition

def load_face_database(faces_dir: str) -> Tuple[np.ndarray, List[str]]:
    """
    Scan faces_dir and compute encodings once.
    Returns:
        known_encodings: (N,128) float32 array
        known_names: list[str]
    """
    if not os.path.isdir(faces_dir):
        os.makedirs(faces_dir, exist_ok=True)

    exts = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
    files = [f for f in os.listdir(faces_dir) if f.lower().endswith(exts)]
    files.sort()

    encodings = []
    names = []

    if not files:
        print(f"[INFO] No images in {faces_dir}. All faces will be Unknown.")

    for fname in files:
        path = os.path.join(faces_dir, fname)
        name = os.path.splitext(fname)[0]
        try:
            img = face_recognition.load_image_file(path)
            locs = face_recognition.face_locations(img, model="hog", number_of_times_to_upsample=1)
            if not locs:
                print(f"[WARN] No face detected in '{path}', skipping.")
                continue
            enc = face_recognition.face_encodings(img, known_face_locations=locs)
            if not enc:
                print(f"[WARN] Encoding failed for '{path}', skipping.")
                continue
            encodings.append(enc[0].astype(np.float32))
            names.append(name)
            print(f"[OK] Loaded: {name}")
        except Exception as e:
            print(f"[WARN] Error loading '{path}': {e}")

    if encodings:
        return np.vstack(encodings), names
    return np.empty((0, 128), dtype=np.float32), []
>>>>>>> 000509f (Initial commit)
