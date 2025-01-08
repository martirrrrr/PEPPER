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
    music_file = "/home/nao/music/song1.mp3"
    audio_service.playFile(music_file)

    # Esegue la coreografia mentre la musica è in riproduzione
    dance_moves = [
        (["RShoulderPitch", "LShoulderPitch"], [0.5, 0.5], 1.0),
        (["RShoulderRoll", "LShoulderRoll"], [-0.5, 0.5], 1.0),
        (["RShoulderPitch", "LShoulderPitch"], [1.0, 1.0], 1.0),
        (["RShoulderRoll", "LShoulderRoll"], [0.0, 0.0], 1.0)
    ]

    for move in dance_moves:
        names, angles, duration = move
        motion_service.angleInterpolation(names, angles, [duration] * len(names), True)

    # Attende la fine della riproduzione musicale
    time.sleep(audio_service.getFileLength(music_file))

    # Chiede all'utente se la canzone è piaciuta
    tts_service.say("Ti è piaciuta la canzone? Per favore, rispondi con sì o no.")

    # Configura il riconoscimento vocale
    speech_recognition_service = session.service("ALSpeechRecognition")
    vocabulary = ["sì", "no"]
    speech_recognition_service.setVocabulary(vocabulary, False)
    speech_recognition_service.subscribe("MusicFeedback")

    # Funzione per gestire la risposta dell'utente
    def on_speech_recognized(value):
        if value in vocabulary:
            if value == "sì":
                tts_service.say("Arrivederci.")
            elif value == "no":
                tts_service.say("Proviamo un'altra canzone.")
                # Riproduce la seconda canzone e balla
                audio_service.playFile("/home/nao/music/song2.mp3")
                for move in dance_moves:
                    names, angles, duration = move
                    motion_service.angleInterpolation(names, angles, [duration] * len(names), True)
                tts_service.say("Spero che questa ti sia piaciuta. Arrivederci.")
            # Termina l'ascolto dopo aver ricevuto una risposta valida
            speech_recognition_service.unsubscribe("MusicFeedback")

    # Ascolta la risposta dell'utente
    memory_service = session.service("ALMemory")
    memory_service.subscribeToEvent("WordRecognized", "on_speech_recognized")

    # Attende la risposta dell'utente
    time.sleep(10)  # Attende 10 secondi per una risposta

if __name__ == "__main__":
    main()
