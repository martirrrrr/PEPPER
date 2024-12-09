{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from naoqi import ALProxy\
import cv2\
import numpy as np\
import time\
\
# Parametri\
camera_id = 0  # 0: camera frontale, 1: camera inferiore\
resolution = 2  # 2: 640x480, 1: 320x240, 0: 160x120\
color_space = 13  # BGR color space\
fps = 10  # Frame per secondo\
duration = 5  # Durata della registrazione in secondi\
output_file = "/home/nao/video.avi"  # Percorso file di output nella memoria di Pepper\
\
# Connetti alla fotocamera\
ip_robot = "192.168.1.2"  # Sostituisci con l'indirizzo IP di Pepper\
port_robot = 9559\
video_proxy = ALProxy("ALVideoDevice", ip_robot, port_robot)\
\
# Registra una nuova sessione video\
subscriber_name = video_proxy.subscribeCamera(\
    "python_client", camera_id, resolution, color_space, fps\
)\
\
# Configura il codec e il writer per il file AVI\
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec per AVI\
frame_size = (640, 480) if resolution == 2 else (320, 240)\
out = cv2.VideoWriter(output_file, fourcc, fps, frame_size)\
\
# Registra i frame per 5 secondi\
start_time = time.time()\
while time.time() - start_time < duration:\
    frame = video_proxy.getImageRemote(subscriber_name)\
    if frame is None:\
        print("Errore: impossibile acquisire il frame")\
        break\
\
    # Estrai i dati del frame\
    width, height = frame[0], frame[1]\
    image_data = frame[6]\
    img = np.frombuffer(image_data, dtype=np.uint8).reshape((height, width, 3))\
\
    # Scrivi il frame nel file AVI\
    out.write(img)\
\
# Rilascia la risorsa della telecamera\
video_proxy.unsubscribe(subscriber_name)\
out.release()\
\
print("Video salvato come:", output_file)\
}