# -*- coding: utf-8 -*-
import time
import threading
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
        print("[INFO] Registrazione video completata!")
        print("Video salvato in:", video_info[1])  # Percorso completo del file
        print("Numero di frame registrati:", video_info[0])
    
    except Exception as e:
        print("[ERRORE] Si è verificato un problema con la registrazione video:", e)

def record_audio(ip, port, filename):
    """
    Registra un file audio di 5 secondi dai microfoni di Pepper e lo salva in formato WAV.

    :param ip: Indirizzo IP del robot Pepper
    :param port: Porta del robot (default: 9559)
    :param filename: Nome del file audio da salvare (senza estensione)
    """
    try:
        # Connetti al servizio ALAudioRecorder
        audio_recorder = ALProxy("ALAudioRecorder", ip, port)
        
        # Configura i parametri di registrazione
        audio_channels = [0, 0, 1, 0]  # Solo il microfono centrale
        audio_recorder.startMicrophonesRecording(f"/home/nao/recordings/audio/{filename}.wav", "wav", 16000, audio_channels)
        
        # Avvia la registrazione
        print("[INFO] Avvio registrazione audio...")
        
        # Attendi 5 secondi per registrare l'audio
        time.sleep(5)
        
        # Ferma la registrazione
        audio_recorder.stopMicrophonesRecording()
        print("[INFO] Registrazione audio completata!")
        print("Audio salvato in: /home/nao/recordings/audio/{}.wav".format(filename))
    
    except Exception as e:
        print("[ERRORE] Si è verificato un problema con la registrazione audio:", e)

# Parametri del robot
ROBOT_IP = "192.168.1.104"  # Sostituisci con l'indirizzo IP di Pepper
ROBOT_PORT = 9559  # Porta predefinita di NAOqi
VIDEO_FILENAME = "pepper_video"  # Nome del file video (senza estensione)
AUDIO_FILENAME = "pepper_audio"  # Nome del file audio (senza estensione)

if __name__ == "__main__":
    # Avvia la registrazione audio e video in parallelo utilizzando thread
    video_thread = threading.Thread(target=record_video, args=(ROBOT_IP, ROBOT_PORT, VIDEO_FILENAME))
    audio_thread = threading.Thread(target=record_audio, args=(ROBOT_IP, ROBOT_PORT, AUDIO_FILENAME))
    
    video_thread.start()
    audio_thread.start()
    
    # Aspetta che entrambe le registrazioni siano completate
    video_thread.join()
    audio_thread.join()
    
    print("[INFO] Registrazione audio e video completata con successo!")
