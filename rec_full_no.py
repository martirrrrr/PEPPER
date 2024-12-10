# -*- coding: utf-8 -*-
import time
from naoqi import ALProxy

def start_video_recording(video_recorder, filename):
    """
    Configura e avvia la registrazione video.
    """
    try:
        # Imposta tutti i parametri prima di iniziare la registrazione
        video_recorder.setCameraID(0)  # Fotocamera frontale
        video_recorder.setResolution(2)  # Risoluzione: 640x480
        video_recorder.setFrameRate(10)  # Frame rate: 10 fps
        video_recorder.setVideoFormat("MJPG")  # Formato video: MJPG
        
        # Avvia la registrazione video
        video_recorder.startRecording("/home/nao/recordings/cameras", filename)
        print("[INFO] Registrazione video avviata...")
    except Exception as e:
        print("[ERRORE] Si è verificato un problema durante la configurazione del video:", e)

def start_audio_recording(audio_recorder, filename):
    """
    Configura e avvia la registrazione audio.
    """
    audio_channels = [0, 0, 1, 0]  # Solo microfono centrale
    audio_recorder.startMicrophonesRecording("/home/nao/recordings/audio/" + filename + ".wav", "wav", 16000, audio_channels)
    print("[INFO] Registrazione audio avviata...")

def stop_video_recording(video_recorder):
    """
    Ferma la registrazione video.
    """
    try:
        video_info = video_recorder.stopRecording()
        print("[INFO] Registrazione video completata!")
        print("Video salvato in:", video_info[1])
        print("Numero di frame registrati:", video_info[0])
    except Exception as e:
        print("[ERRORE] Si è verificato un problema durante l'interruzione della registrazione video:", e)

def stop_audio_recording(audio_recorder):
    """
    Ferma la registrazione audio.
    """
    audio_recorder.stopMicrophonesRecording()
    print("[INFO] Registrazione audio completata!")

def record_audio_video(ip, port, video_filename, audio_filename):
    """
    Registra simultaneamente audio e video per 5 secondi.
    """
    try:
        # Connetti ai proxy di Pepper
        video_recorder = ALProxy("ALVideoRecorder", ip, port)
        audio_recorder = ALProxy("ALAudioRecorder", ip, port)
        
        # Avvia le registrazioni
        start_video_recording(video_recorder, video_filename)
        start_audio_recording(audio_recorder, audio_filename)
        
        # Aspetta 5 secondi per completare entrambe le registrazioni
        time.sleep(5)
        
        # Ferma entrambe le registrazioni
        stop_video_recording(video_recorder)
        stop_audio_recording(audio_recorder)
        
        print("[INFO] Registrazione audio e video completata con successo!")
    
    except Exception as e:
        print("[ERRORE] Si è verificato un problema:", e)

# Parametri del robot
ROBOT_IP = "192.168.1.104"  # Sostituisci con l'indirizzo IP di Pepper
ROBOT_PORT = 9559  # Porta predefinita di NAOqi
VIDEO_FILENAME = "pepper_video"  # Nome del file video (senza estensione)
AUDIO_FILENAME = "pepper_audio"  # Nome del file audio (senza estensione)

if __name__ == "__main__":
    record_audio_video(ROBOT_IP, ROBOT_PORT, VIDEO_FILENAME, AUDIO_FILENAME)

