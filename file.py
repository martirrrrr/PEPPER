# -*- coding: utf-8 -*-
import time
from naoqi import ALProxy

def record_video(ip, port, filename):
    """
    Registra un video di 5 secondi dalla fotocamera frontale di Pepper e lo salva in formato AVI.

    :param ip: Indirizzo IP del robot Pepper
    :param port: Porta del robot (default: 9559)
    :param filename: Nome del file video da salvare (senza estensione)
    """
    try:
        # Connetti al servizio ALVideoRecorder
        video_recorder = ALProxy("ALVideoRecorder", ip, port)
        
        # Configura i parametri di registrazione
        video_recorder.setCameraID(0)  # 0: Fotocamera frontale
        video_recorder.setResolution(2)  # 2: 640x480 (kQVGA)
        video_recorder.setFrameRate(10)  # Frame rate: 10 fps
        video_recorder.setVideoFormat("MJPG")  # Formato video: MJPG (AVI)
        
        # Avvia la registrazione
        print("[INFO] Avvio registrazione video...")
        video_recorder.startRecording("/home/nao/recordings/cameras", filename)
        
        # Attendi 5 secondi per registrare il video
        time.sleep(5)
        
        # Ferma la registrazione e ottieni informazioni sul video salvato
        video_info = video_recorder.stopRecording()
        
        # Stampa informazioni sul file registrato
        print("[INFO] Registrazione completata!")
        print("Video salvato in:", video_info[1])  # Percorso completo del file
        print("Numero di frame registrati:", video_info[0])
    
    except Exception as e:
        print("[ERRORE] Si è verificato un problema:", e)

# Parametri del robot
ROBOT_IP = "192.168.1.104"  # Sostituisci con l'indirizzo IP di Pepper
ROBOT_PORT = 9559  # Porta predefinita di NAOqi
FILENAME = "pepper_video"  # Nome del file (senza estensione)

# Esegui la funzione
if __name__ == "__main__":
    record_video(ROBOT_IP, ROBOT_PORT, FILENAME)
