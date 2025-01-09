import qi
import time

def main():
    # Connessione al robot
    session = qi.Session()
    try:
        session.connect("tcp://<indirizzo_ip_pepper>:9559")
    except RuntimeError:
        print("Impossibile connettersi a Pepper. Verifica l'indirizzo IP e la connessione di rete.")
        return

    # Accesso ai servizi necessari
    tts_service = session.service("ALTextToSpeech")
    motion_service = session.service("ALMotion")
    audio_service = session.service("ALAudioPlayer")

    # Saluto iniziale
    tts_service.say("Mi fa piacere che tu sia felice in questo momento.")

    # Esegue il gesto "ok" con la mano destra
    names = ["RHand", "RThumb1", "RThumb2"]
    angles = [1.0, 1.0, 1.0]  # Apri la mano e alza il pollice
    motion_service.angleInterpolation(names, angles, [1.0] * len(names), True)

    # Chiede all'utente riguardo alla canzone
    tts_service.say("Che te ne pare di questa canzone?")

    # Avvia la riproduzione della canzone
    #music_file = "/home/nao/music/song1.mp3"
    #audio_service.playFile(music_file)

    # Durata della canzone in secondi (modifica questo valore in base alla durata effettiva)
    #durata_canzone = 30

    # Inizia la coreografia
    start_time = time.time()
    while time.time() - start_time < durata_canzone:
        # Esempio di movimenti ripetuti
        motion_service.angleInterpolation(["RShoulderPitch", "LShoulderPitch"], [0.5, 0.5], [1.0, 1.0], True)
        motion_service.angleInterpolation(["RShoulderRoll", "LShoulderRoll"], [-0.5, 0.5], [1.0, 1.0], True)
        motion_service.angleInterpolation(["RShoulderPitch", "LShoulderPitch"], [1.0, 1.0], [1.0, 1.0], True)
        motion_service.angleInterpolation(["RShoulderRoll", "LShoulderRoll"], [0.0, 0.0], [1.0, 1.0], True)

    # Conclusione
    tts_service.say("Spero che ti sia piaciuta la canzone. Arrivederci.")

if __name__ == "__main__":
    main()
