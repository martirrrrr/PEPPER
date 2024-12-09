from naoqi import ALProxy
import time

# Connessione a Pepper
def connect_to_pepper():
    ip = "192.168.1.100"  # Cambia con l'IP di Pepper
    port = 9559
    try:
        tts = ALProxy("ALTextToSpeech", ip, port)
        motion = ALProxy("ALMotion", ip, port)
        recognition = ALProxy("ALSpeechRecognition", ip, port)
        sound = ALProxy("ALAudioPlayer", ip, port)  # Per l'audio
        return tts, motion, recognition, sound
    except Exception as e:
        print("Errore nella connessione:", e)
        return None, None, None, None

# Funzione per riprodurre suoni rilassanti (suono della natura o musica meditativa)
def play_relaxing_sound(sound):
    try:
        sound.playFile("/path/to/relaxing_sound.wav")  # Inserisci il percorso del file audio
    except Exception as e:
        print("Errore nel riprodurre il suono:", e)

# Guida l'utente in un esercizio di respirazione profonda
def breathing_exercise(tts, motion, sound):
    tts.say("Trova una posizione comoda e chiudi gli occhi, se ti va.")
    time.sleep(2)
    play_relaxing_sound(sound)
    time.sleep(5)  # Lascia un po' di tempo per ambientarsi

    tts.say("Ora iniziamo con un respiro profondo. Inspira lentamente...")
    motion.setStiffnesses(["Head", "LArm", "RArm", "LLeg", "RLeg"], [0.1]*5)
    # Movimento della testa in avanti per stimolare l'inspirazione
    motion.setAngles("Head", [0.1], 0.1)
    time.sleep(4)  # Tempo per inspirare

    tts.say("...espira lentamente... 1... 2... 3... 4...")
    motion.setAngles("Head", [-0.1], 0.1)
    time.sleep(4)  # Tempo per espirare

    # Ripetizione dell'esercizio
    tts.say("Ripeti il respiro profondo, concentrandoti sull'aria che entra e esce.")
    for _ in range(3):
        tts.say("Inspira... 1... 2... 3... 4...")
        time.sleep(4)
        tts.say("Espira... 1... 2... 3... 4...")
        time.sleep(4)

    tts.say("Perfetto, ora concentrati sul tuo corpo. Senti il tuo corpo che si rilassa ad ogni respiro.")

# Funzione per guidare la meditazione e rilassamento
def meditation_exercise(tts, motion, sound):
    tts.say("Iniziamo un esercizio di meditazione e rilassamento.")
    time.sleep(2)
    tts.say("Immagina di essere su una spiaggia tranquilla. Il suono delle onde ti rilassa...")
    time.sleep(5)

    # Movimenti di rilassamento di Pepper
    tts.say("Pepper ti guiderà ora con dei movimenti rilassanti.")
    time.sleep(2)
    motion.setAngles("Head", [0.2], 0.2)  # Inclinazione della testa per mostrare calma
    time.sleep(3)
    motion.setAngles("Head", [-0.2], 0.2)
    time.sleep(3)

    tts.say("Concentrati sul tuo corpo. Rilassa ogni parte, partendo dalla testa e scendendo giù verso i piedi.")
    time.sleep(4)

    # Esercizio di rilassamento progressivo muscolare
    tts.say("Senti i tuoi muscoli che si rilassano, partendo dalla fronte.")
    time.sleep(2)
    tts.say("Ora rilassa gli occhi, poi il viso...")
    time.sleep(2)
    tts.say("Senti la tensione che lascia il tuo corpo, concentrati sulle spalle, braccia, mani.")
    time.sleep(5)

    tts.say("Ti invito a fare un altro ciclo di respirazione profonda...")
    breathing_exercise(tts, motion, sound)

    # Incoraggiamento finale
    tts.say("Bravo! Continua a respirare lentamente e sentiti in pace. Sei pronto per una nuova giornata di serenità.")
    time.sleep(3)

# Funzione per chiedere se l'utente vuole fare l'esercizio
def ask_if_user_wants_to_meditate(tts, recognition):
    tts.say("Ciao! Ti va di fare un esercizio di meditazione e rilassamento con me?")
    time.sleep(1)

    # Riconoscimento vocale per rispondere sì o no
    recognition.setLanguage("Italian")
    recognition.subscribe("MeditationGame")
    response = None
    try:
        response = recognition.waitForService(5000)  # Attendi fino a 5 secondi per la risposta
    except:
        pass

    if response:
        if "sì" in response.lower():
            tts.say("Ottimo, iniziamo subito!")
            meditation_exercise(tts, motion, sound)
        else:
            tts.say("Va bene, fammi sapere quando vuoi provare!")
    else:
        tts.say("Non ho sentito bene. Puoi ripetere?")

# Main loop per iniziare il gioco
def main():
    tts, motion, recognition, sound = connect_to_pepper()

    if tts is None:
        print("Errore nella connessione. Assicurati che Pepper sia acceso e raggiungibile.")
        return

    ask_if_user_wants_to_meditate(tts, recognition)

if __name__ == "__main__":
    main()
