# FaceAnalyzer
FaceAnalyzer es una aplicación en Python para **reconocimiento facial en tiempo real** con un HUD visual.  
Permite identificar rostros conocidos y mostrar atributos básicos (edad, género y emoción) usando procesamiento en segundo plano.

## Requisitos Previos
Antes de comenzar debes asegurarte de tener instalado lo siguiente:

**Python 3.10 (64 bits)**
**Git** Esto es opcional, solo es por si llegas a clonar el repositorio.
**Win 10/11**

## Setup
Crea un entorno virtual desde la raiz del proyecto, abre una terminal y ejecuta lo siguiente:
1) python -m venv .venv
2) Crea un venv (.\.venv\Scripts\Activate.ps1)
3) Instala dependencias:
   pip install --upgrade pip
   pip install -r requirements.txt
Esto te deberia instalar lo siguiente:
1) OpenCV
Face_Recognition(dlib)
DeepFace
Numpy y dependencias necesarias

## Agrega Rostros
Pon imágenes en ./faces (ej: alice.jpg). El nombre del archivo será el label.

## Para ejecutar
Desde la raíz del proyecto:
python -m src.main

 Si deseas cerrar o salir presiona "q".