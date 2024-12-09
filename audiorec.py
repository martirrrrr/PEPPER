# -*- coding: utf-8 -*-
import time
from naoqi import ALProxy

def record_audio(ip, port, filename, duration=5):
    """
    Registra un file audio WAV da Pepper e lo salva nella memoria interna.

    :param ip: Indirizzo IP di Pepper
    :param port: Porta di NAOqi (default: 9559)
    :param filename: Nome del file audio (senza estensione)
    :param duration: Durata della registrazione in secondi
    """
    try:
        # Connessione al servizio ALAudioRecorder
        audio_recorder = ALProxy("ALAudioRecorder", ip, port)
        
        # Inizia la registrazione
        print("[INFO] Inizio registrazione audio...")
        audio_recorder.startMicrophonesRecording("/home/nao/recordings/audio", filename, 16000, "wav")
        
        # Attendi per la durata specificata
        time.sleep(duration)
        
        # Ferma la registrazione
        audio_recorder.stopMicrophonesRecording()
        
        print("[INFO] Registrazione completata!")
        print("Audio salvato come:", filename + ".wav")
    
    except Exception as e:
        print("[ERRORE] Si è verificato un problema:", e)

# Parametri del robot
ROBOT_IP = "192.168.1.100"  # Sostituisci con l'indirizzo IP di Pepper
ROBOT_PORT = 9559  # Porta predefinita di NAOqi
FILENAME = "pepper_audio"  # Nome del file audio (senza estensione)

# Esegui la funzione
if __name__ == "__main__":
    record_audio(ROBOT_IP, ROBOT_PORT, FILENAME)
