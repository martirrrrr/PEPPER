import time
from naoqi import ALProxy

def record_audio(ip, port, filename, duration=5):
    try:
        # Creazione del proxy per il microfono
        audio_recorder = ALProxy("ALAudioRecorder", ip, port)
        
        # Verifica se il microfono  pronto
        if not audio_recorder.isRecording():
            print("[INFO] Inizio registrazione audio...")
            # Avvia la registrazione
            audio_recorder.startMicrophonesRecording("/home/nao/recordings/audio", filename, 16000, "wav")
            time.sleep(duration)
            # Ferma la registrazione
            audio_recorder.stopMicrophonesRecording()
            print("[INFO] Registrazione completata!")
            print("Audio salvato come:", filename + ".wav")
        else:
            print("[ERRORE] Il microfono sta già registrando un altro file.")
    except Exception as e:
        print("[ERRORE] Si è verificato un problema durante la registrazione:", e)

# Parametri di connessione
ROBOT_IP = "192.168.1.104"  # Sostituisci con l'IP di Pepper
ROBOT_PORT = 9559  # Porta predefinita di NAOqi
FILENAME = "pepper_audio"  # Nome del file audio
DURATION = 5  # Durata della registrazione in secondi

# Avvia la registrazione
record_audio(ROBOT_IP, ROBOT_PORT, FILENAME, DURATION)
