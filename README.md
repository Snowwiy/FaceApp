# FaceAnalyzer
FaceAnalyzer es una aplicación en Python para **reconocimiento facial en tiempo real** con un HUD visual.  
Permite identificar rostros conocidos y mostrar atributos básicos (edad, género y emoción) usando procesamiento en segundo plano.

## Funcionalidades

- Reconocimiento facial
- Detección facial en tiempo real
- Tracking facial
- Análisis de emociones
- Estimación de edad y género
- Captura de evidencia
- Procesamiento en tiempo real
## Tecnologías utilizadas

- Python 3.10
- OpenCV
- DeepFace
- face_recognition
- TensorFlow
- tf-keras

## Requisitos Previos
Antes de comenzar debes asegurarte de tener instalado lo siguiente:

1) **Python 3.10 (64 bits)**
2) **Git** Esto es opcional, solo es por si llegas a clonar el repositorio.
3) **Win 10/11**

## Setup
Crea un entorno virtual desde la raiz del proyecto, abre una terminal y ejecuta lo siguiente:
1) python -m venv .venv
2) Crea un venv (.\.venv\Scripts\Activate.ps1)
3) Instala dependencias:
   1) pip install --upgrade pip (en caso de error ejecutar python.exe -m pip install --upgrade pip)
   2) python -m pip install -U tf-keras
   2) pip install -r requirements.txt
      1) Esto te deberia instalar lo siguiente:
         1) OpenCV
         2) Face_Recognition(dlib)
         3) DeepFace
         4) Numpy y dependencias necesarias
         5) Este paso es obligatorio para poder evitar problemas de compatibilidad con TensorFlow/Keras en DeepFace
         .\.venv\Scripts\python.exe -m pip install -U tf-keras
Verificar instalacion de tf-keras
.\.venv\Scripts\python.exe -c "import tf_keras; print('tf_keras OK')"

NOTA: Es necesario instalar VS Build Tools y seleccionar
1.- Desktop development with C++
2.- MSVC v143 Build Tools
3.- W 10/11 SDK
4.- C++ CMake tools for Windows
Ademas de que este proyecto requiere tf-keras instalado manualmente debido a compatibilidades internas de DeepFace y TensorFlow.
## Agrega Rostros
Pon imágenes en ./faces (ej: alice.jpg). El nombre del archivo será el label.

## Para ejecutar
Desde la raíz del proyecto:
python -m src.main

 Si deseas cerrar o salir presiona "q".
