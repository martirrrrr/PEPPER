import qi
import time

def connect_to_pepper(robot_ip, port):
    """
    Connetti alla sessione NAOqi di Pepper.
    
    :param robot_ip: Indirizzo IP del robot Pepper
    :param port: Porta del robot
    :return: Oggetto session connesso
    """
    session = qi.Session()
    try:
        session.connect("tcp://"+str(robot_ip)+":"+str(port))
        print("[INFO] Connessione al robot stabilita.")
        return session
    except RuntimeError as e:
        print("[ERRORE] Impossibile connettersi a Pepper. Verifica l'indirizzo IP e la connessione di rete.")
        raise e

def perform_gesture(motion_service):
    """
    Esegue il gesto "ok" con la mano destra.
    
    :param motion_service: Servizio ALMotion
    """
    print("[INFO] Eseguo il gesto 'ok' con la mano destra...")
    names = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw"]
    angles = [-0.5, 0.3, -1.0, -0.5, 0.0]  # Apri la mano e alza il pollice
    motion_service.angleInterpolation(names, angles, [1.0] * len(names), True)

def play_dance(motion_service, durata_canzone):
    """
    Esegue una breve coreografia durante la riproduzione della canzone.
    
    :param motion_service: Servizio ALMotion
    :param durata_canzone: Durata della coreografia in secondi
    """
    print("[INFO] Inizio coreografia...")
    start_time = time.time()
    while time.time() - start_time < durata_canzone:
        # Movimenti di esempio
        motion_service.angleInterpolation(["RShoulderPitch", "LShoulderPitch"], [0.5, 0.5], [1.0, 1.0], True)
        motion_service.angleInterpolation(["RShoulderRoll", "LShoulderRoll"], [-0.5, 0.5], [1.0, 1.0], True)
        motion_service.angleInterpolation(["RShoulderPitch", "LShoulderPitch"], [1.0, 1.0], [1.0, 1.0], True)
        motion_service.angleInterpolation(["RShoulderRoll", "LShoulderRoll"], [0.0, 0.0], [1.0, 1.0], True)
    print("[INFO] Coreografia completata.")

def recognize_speech(speech_service, vocabulary):
    """
    Riconosce un comando vocale dall'utente.
    
    :param speech_service: Servizio ALSpeechRecognition
    :param vocabulary: Lista di parole da riconoscere
    :return: Parola riconosciuta
    """
    recognized_word = None
    try:
        speech_service.setVocabulary(vocabulary, False)
        speech_service.subscribe("MusicSelector")
        print("[INFO] In attesa di un comando vocale...")

        # Callback per il riconoscimento vocale
        def on_word_recognized(value):
            nonlocal recognized_word
            if value and isinstance(value, list) and len(value) > 1 and value[1] >= 0.5:
                recognized_word = value[0]
                print(f"[INFO] Comando vocale riconosciuto: {recognized_word}")

        # Connessione al segnale di riconoscimento vocale
        memory_service = session.service("ALMemory")
        memory_service.subscribeToEvent("WordRecognized", "on_word_recognized")

        # Attende fino a quando una parola viene riconosciuta
        while recognized_word is None:
            time.sleep(0.1)

        speech_service.unsubscribe("MusicSelector")
    except Exception as e:
        print("[ERRORE] Si è verificato un problema nel riconoscimento vocale:", e)
    return recognized_word

def main(robot_ip, port):
    """
    Esegue una sequenza di interazioni con Pepper.
    
    :param robot_ip: Indirizzo IP del robot Pepper
    :param port: Porta del robot (default: 9559)
    """
    try:
        # Connessione al robot
        session = connect_to_pepper(robot_ip, port)

        # Accesso ai servizi necessari
        tts_service = session.service("ALTextToSpeech")
        motion_service = session.service("ALMotion")
        audio_service = session.service("ALAudioPlayer")
        speech_service = session.service("ALSpeechRecognition")

        # Saluto iniziale
        tts_service.say("Ciao! Dimmi che tipo di musica preferisci: ritmata, classica o rock.")

        # Riconoscimento vocale per selezione della canzone
        vocabulary = ["ritmata", "classica", "rock"]
        user_choice = recognize_speech(speech_service, vocabulary)

        # Selezione del file musicale in base al comando vocale
        music_files = {
            "ritmata": "/home/nao/music/song1.mp3",
            "classica": "/home/nao/music/song2.mp3",
            "rock": "/home/nao/music/song3.mp3"
        }
        music_file = music_files.get(user_choice, None)

        if music_file:
            # Durata della canzone in secondi (modifica in base alla durata effettiva)
            durata_canzone = 30

            # Avvia la riproduzione della canzone in modo asincrono
            audio_service.playFile(music_file)

            # Avvia la coreografia
            play_dance(motion_service, durata_canzone)

            # Conclusione
            tts_service.say("Spero che ti sia piaciuta la canzone. Arrivederci.")
        else:
            tts_service.say("Mi dispiace, non ho riconosciuto il genere musicale richiesto.")

    except Exception as e:
        print("[ERRORE] Si è verificato un problema:", e)

# Parametri del robot
ROBOT_IP = "192.168.0.104"  # Sostituisci con l'indirizzo IP di Pepper
ROBOT_PORT = 9559  # Porta predefinita di NAOqi

if __name__ == "__main__":
    main(ROBOT_IP, ROBOT_PORT)
