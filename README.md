# contador_de_personas_basico

## Table of Contents
1. [Información General](#general-info)
2. [Instalación](#installation)
4. [FAQs](#faqs)
## Información General
***
Este proyecto usa la libreria de YOLO para el conteo de personas en un area de un video. El usuario puede establecer el area donde quiere contar las personas estableciendo un poligono estableciendo su ubicacion usando el mouse. A contibuacion se describe las teclas y acciones necesarias para interactuar con el programa mientras se esta ejecutando. 
Tecla q: cierra el programa
Click izquierdo del mouse: Haz click sobre el video para establecer los puntos para formar el polígono (mínimo 3 puntos).
Tecla p: Confirma con la tecla p para dibujar el polígono y empezar a contar las personas que pasan por el área
Tecla n: Para dibujar un nuevo polígono presiona la letra n.

## Instalacion
***
Instala las librerias necesarias para el programa 

$ pip install opencv-python
$ pip install ultralytics
$ pip install numpy
$ pip install shapely
```
## FAQs
***
Preguntas frecuencias
1. **Donde puedo encontrar mayor información sobre la libreria de detección y seguimiento de personas?**
https://docs.ultralytics.com/es/guides/region-counting/
2. **Como se realizo la detección de personas en el area?** 
Se utiliza la libreria shapely para detectar si un punto del tracking de un ID esta dentro del poligono creado por el usuario

3. **Puedo analizar mi propio video?**
Si solo asegurate de editar la linea de codigo número 21 video_path = "video.webm", con el nombre del archivo de video entre comillas. 

