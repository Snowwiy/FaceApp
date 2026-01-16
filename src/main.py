# src/main 
from .config import AppConfig
from .face_analyzer import FaceAnalyzer

def configure_gpu(use_gpu: bool):
    """
    Configura TensorFlow para usar GPU sin consumir toda la VRAM.
    """
    if not use_gpu:
        return

    try:
        import tensorflow as tf
        gpus = tf.config.list_physical_devices("GPU")
        if gpus:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            print(f"[INFO] GPU configurada: {gpus}")
        else:
            print("[INFO] No se detectó GPU, usando CPU")
    except Exception as e:
        print(f"[WARN] No se pudo configurar GPU: {e}")

def main():
    cfg = AppConfig()
    configure_gpu(cfg.use_gpu)

    app = FaceAnalyzer(cfg)
    app.run()

if __name__ == "__main__":
    main()
