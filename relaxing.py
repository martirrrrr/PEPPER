# -*- coding: utf-8 -*-
from naoqi import ALProxy
import time

def play_relaxing_sound(sound):
    try:
        sound.playFile("/path/to/relaxing_sound.wav")  # Inserisci il percorso del file audio
    except Exception as e:
        print("Errore nel riprodurre il suono:", e)

def speech_recognition(ip, port):
    """
    Funzione che utilizza Pepper per riconoscere parole e ripeterle.
    Si ferma dopo tre richieste di nuove parole.
    """
    try:
        # Proxy per il riconoscimento vocale
        speech_recognition = ALProxy("ALSpeechRecognition", ip, port)
        speech_recognition.setLanguage("Italian")  # Lingua italiana

        # Proxy per il text-to-speech (TTS)
        text_to_speech = ALProxy("ALTextToSpeech", ip, port)

        # Lista di parole che Pepper deve riconoscere
        vocabulary = ["sì", "no", "aiuto"]

        # Proxy per il memory per rilevare gli eventi
        memory = ALProxy("ALMemory", ip, port)

        # Assicurati che il motore ASR sia disattivato
        try:
            speech_recognition.pause(True)
            speech_recognition.unsubscribe("Test_ASR")
        except RuntimeError:
            print("[INFO] Il modulo 'Test_ASR' non era sottoscritto. Procedo...")

                # Imposta il vocabolario
        speech_recognition.setVocabulary(vocabulary, False)  # False per evitare il riconoscimento casuale
        print("[INFO] Vocabolario impostato con successo.")

        # Riattiva il motore ASR
        speech_recognition.subscribe("Test_ASR")
        speech_recognition.pause(False)
        
        text_to_speech.say("Benvenuto")
        print("[INFO] Riconoscimento vocale attivato. Pronuncia una parola...")


                # Contatore delle interazioni
        interaction = 1  # Numero massimo di richieste
        
        text_to_speech.say("Vogliamo incominciare?")

        while interaction:
            # Aspetta che Pepper riconosca una parola
            word_recognized = memory.getData("WordRecognized")
            if word_recognized:
                recognized_word = word_recognized[0]  # La parola riconosciuta
                confidence = word_recognized[1]      # Confidenza del riconoscimento
                if confidence > 0.5:  # Filtro per evitare falsi positivi
                    print("Hai detto:", recognized_word)
                    text_to_speech.say("Hai detto", recognized_word)
                    
                    if recognized_word == vocabulary[0]:
                        text_to_speech.say("Perfetto! Continuiamo con la meditazione guidata.")
                        breathing_exercise(text_to_speech)
                        interaction = 0
                    
                    elif recognized_word == vocabulary[1]:
                        text_to_speech.say("Va bene. Facciamo una pausa. Chiamami se hai bisogno.")
                        interaction = 0
                    
                    elif recognized_word == vocabulary[2]:
                        text_to_speech.say("Sono qui per aiutarti. Posso guidarti in un esercizio di respirazione o rilassamento. Di' sì per iniziare.")
                
                memory.insertData("WordRecognized", None)  # Reset dell'evento

        print("[INFO] Programma terminato.")
        text_to_speech.say("Grazie per aver giocato con me! Alla prossima!")
        speech_recognition.unsubscribe("Test_ASR")  # Disabilita il riconoscimento vocale

    except Exception as e:
        print("[ERRORE] Si è verificato un problema:", e)


# Guida l'utente in un esercizio di respirazione profonda
def breathing_exercise(tts, motion, sound):
    #tts.say("Trova una posizione comoda e chiudi gli occhi, se ti va.")
    tts.say("Inizio")
    time.sleep(2)
    #play_relaxing_sound(sound)
    time.sleep(5)  # Lascia un po' di tempo per ambientarsi

    tts.say("Mossa 1")
    #tts.say("Ora iniziamo con un respiro profondo. Inspira lentamente...")
    motion.setStiffnesses(["Head", "LArm", "RArm", "LLeg", "RLeg"], [0.1]*5)
    # Movimento della testa in avanti per stimolare l'inspirazione
    motion.setAngles("Head", [0.1], 0.1)
    time.sleep(4)  # Tempo per inspirare

    tts.say("Mossa 2")
    #tts.say("...espira lentamente... 1... 2... 3... 4...")
    motion.setAngles("Head", [-0.1], 0.1)
    time.sleep(4)  # Tempo per espirare

    # Ripetizione dell'esercizio
    tts.say("Concentrazione")
    #tts.say("Ripeti il respiro profondo, concentrandoti sull'aria che entra e esce.")
    for _ in range(2):
        tts.say("Inspira... 1... 2... 3... 4...")
        time.sleep(4)
        tts.say("Espira... 1... 2... 3... 4...")
        time.sleep(4)

    tts.say("Step due finito")
    #tts.say("Perfetto, ora concentrati sul tuo corpo. Senti il tuo corpo che si rilassa ad ogni respiro.")

# Funzione per guidare la meditazione e rilassamento
def meditation_exercise(tts, motion, sound):
    #tts.say("Iniziamo un esercizio di meditazione e rilassamento.")
    tts.say("Step uno")
    time.sleep(2)
    #tts.say("Immagina di essere su una spiaggia tranquilla. Il suono delle onde ti rilassa...")
    time.sleep(5)

    # Movimenti di rilassamento di Pepper
    #tts.say("Pepper ti guiderà ora con dei movimenti rilassanti.")
    time.sleep(2)
    motion.setAngles("Head", [0.2], 0.2)  # Inclinazione della testa per mostrare calma
    time.sleep(3)
    motion.setAngles("Head", [-0.2], 0.2)
    time.sleep(3)

    tts.say("Step uno finito")
    #tts.say("Concentrati sul tuo corpo. Rilassa ogni parte, partendo dalla testa e scendendo giù verso i piedi.")
    time.sleep(4)

    # Esercizio di rilassamento progressivo muscolare
    """
    tts.say("Senti i tuoi muscoli che si rilassano, partendo dalla fronte.")
    time.sleep(2)
    tts.say("Ora rilassa gli occhi, poi il viso...")
    time.sleep(2)
    tts.say("Senti la tensione che lascia il tuo corpo, concentrati sulle spalle, braccia, mani.")
    time.sleep(5)
    """

    tts.say("Step due")
    #tts.say("Ti invito a fare un altro ciclo di respirazione profonda...")
    breathing_exercise(tts, motion, sound)

    # Incoraggiamento finale
    tts.say("Fine")
    #tts.say("Bravo! Continua a respirare lentamente e sentiti in pace. Sei pronto per una nuova giornata di serenità.")
    time.sleep(3)


if __name__ == "__main__":
    # Parametri di connessione di Pepper
    ROBOT_IP = "192.168.1.104"  # Sostituisci con l'indirizzo IP di Pepper
    ROBOT_PORT = 9559           # Porta predefinita di Pepper
    #text_to_speech.say("Benvenuto in questa sessione di meditazione.")
    speech_recognition(ROBOT_IP, ROBOT_PORT)
