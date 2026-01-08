<<<<<<< HEAD
from .config import AppConfig
from .face_analyzer import FaceAnalyzer

def main() -> None:
    cfg = AppConfig(
        faces_dir="faces",
        camera_index=0,
        tolerance=0.6,
        analysis_every_n_frames=30,
        vote_window=7,
        deepface_backend="opencv",
    )
    FaceAnalyzer(cfg).run()

if __name__ == "__main__":
    main()
=======
from .config import AppConfig
from .face_analyzer import FaceAnalyzer

def main() -> None:
    cfg = AppConfig(
        faces_dir="faces",
        camera_index=0,
        tolerance=0.6,
        analysis_every_n_frames=30,
        vote_window=7,
        deepface_backend="opencv",
    )
    FaceAnalyzer(cfg).run()

if __name__ == "__main__":
    main()
>>>>>>> 000509f (Initial commit)
