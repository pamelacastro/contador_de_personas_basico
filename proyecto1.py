from collections import defaultdict

import cv2
import numpy as np

from ultralytics import YOLO
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

def left_click_detect(event, x, y, flags, points3): #funcion que va guardando los puntos del poligono al realizar con el click izquierdo
    if (event == cv2.EVENT_LBUTTONDOWN):
        print(f"\tClick on {x}, {y}")
        points2.append([x,y])
        #print(points2)
        #return points

# Carga el YOLOv8 model
model = YOLO('yolov8n.pt')

# Abre el archivo del video
video_path = "video.webm"
cap = cv2.VideoCapture(video_path)

# Store the track history
track_history = defaultdict(lambda: [])
# inicialización de variables para crear los poligonos y contar los IDs en el area
polygon = []
points2 = []
polig_tupla=[]
num_per=0
continua_contando=0
id=[]
condicion=True
img_instrucciones = cv2.imread('descarga.jpg') # carga la imagen con las instrucciones para el usuario
cv2.imshow('instrucciones',img_instrucciones)
# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        gris=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True)

        # Obtiene las cajas y IDs de seguimiento
        boxes = results[0].boxes.xywh.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist()

        # Visualize the results on the frame
        annotated_frame = results[0].plot()
        # Plot the tracks
        for box, track_id in zip(boxes, track_ids):
            x, y, w, h = box
            bbox_center = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2  # Bbox center
            track = track_history[track_id]
            track.append((float(x), float(y)))  # x, y center point
            #print (track)
            if len(track) > 30:  # retain 90 tracks for 90 frames
                track.pop(0)

            # Draw the tracking lines
            points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
            cv2.polylines(annotated_frame, [points], isClosed=False, color=(230, 230, 230), thickness=10)

            if (continua_contando==1): #cuenta el numero de IDs que ingresan en el area
                
                for i in range(len(track_history)):
                    if i!=0:
                        q=track_history[i]
                        if len(q) !=0:
                            q=q[-1]
                            Contor_polig = Polygon(polig_tupla)
                            
                            if i in id:
                                condicion=False # verifica si el id ingresa al area por primera vez o no
                            else:
                                condicion=True
                            if (Contor_polig .contains(Point(q)) and condicion): # detecta si un punto esta dentro de un poligono
                                num_per=num_per+1
                                id.append(i)
                            #print('Numero de personas', num_per)
                            num_str='Numero de personas que pasaron por el area: '+ str(num_per)
                            cv2.putText(annotated_frame, num_str, (20, 450), 1, 1.2, (150, 255, 100), 2) #escribe en el video el número de personas contadas
        
        

        cv2.drawContours(annotated_frame, polygon, -1, color=(0,255,0),thickness=3) #dibuja el poligono del area a analizar
        # Display the annotated frame
        cv2.imshow("YOLOv8 Tracking", annotated_frame)
                
        

        key = cv2.waitKey(25)
        if (key == ord('q')):
            break
        if (key== ord('p') and continua_contando==0): # establece los parametros para iniciar el conteo de personas
            polygon = [np.int32(points2)]
            print('las coordenadas son ', points2)
            
            polig_tupla=[]
            l1=len(points2)
            for i in range(l1):
                polig_tupla.append(tuple(points2[i]))

            continua_contando=1
        
        
        if (key== ord('n')): #reinicia los valores y parametros para iniciar un nuevo poligono
            continua_contando=0
            polig_tupla=[]
            l1=0
            points2=[]
            num_per=0
            id=[]
            polygon =[]
            cv2.drawContours(annotated_frame, polygon, -1, color=(0,255,0),thickness=3) 

        cv2.setMouseCallback('YOLOv8 Tracking', left_click_detect, points2)

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()

#Referencias:
#https://omes-va.com/deteccion-movimiento-area/
#https://docs.ultralytics.com/es/guides/region-counting/