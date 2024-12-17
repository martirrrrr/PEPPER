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

        available_languages = speech_recognition.getAvailableLanguages()
        print("Lingue disponibili:", available_languages)

        
        speech_recognition.setLanguage("Italian")  # Lingua italiana

        # Proxy per il text-to-speech (TTS)
        text_to_speech = ALProxy("ALTextToSpeech", ip, port)

        # Lista di parole che Pepper deve riconoscere
        vocabulary = ["si", "no", "aiuto"]

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
                confidence = word_recognized[1] # Confidenza del riconoscimento
                if confidence >= 0.5:  # Filtro per evitare falsi positivi
                    print("Hai detto:", recognized_word)
                    text_to_speech.say("Hai detto" + recognized_word)
                    
                    if recognized_word == vocabulary[0]:
                        text_to_speech.say("Perfetto! Continuiamo con la meditazione guidata.")
                        meditation_exercise(tts=text_to_speech, motion=None, sound=None)
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
# Funzione per l'esercizio di respirazione
def breathing_exercise(tts, ip, port, sound=None):
    motion = ALProxy("ALMotion", ip, port)
    posture = ALProxy("ALRobotPosture", ip, port)

    tts.say("Inizio")
    time.sleep(2)
    time.sleep(5)  # Pausa iniziale per ambientarsi

    tts.say("Mossa 1")
    motion.setStiffnesses(["Head", "LArm", "RArm", "LLeg", "RLeg"], [0.1]*5)
    motion.setAngles("Head", 0.1, 0.1)  # Movimento della testa in avanti
    time.sleep(4)

    tts.say("Mossa 2")
    motion.setAngles("Head", -0.1, 0.1)  # Movimento della testa all'indietro
    time.sleep(4)

    tts.say("Concentrazione")
    for _ in range(2):
        tts.say("Inspira... 1... 2... 3... 4...")
        time.sleep(4)
        tts.say("Espira... 1... 2... 3... 4...")
        time.sleep(4)

    tts.say("Step due finito")

# Funzione per la meditazione guidata
def meditation_exercise(tts, ip, port, sound=None):
    motion = ALProxy("ALMotion", ip, port)
    tts.say("Step uno")
    time.sleep(2)
    time.sleep(5)

    # Movimenti di rilassamento
    motion.setAngles("Head", 0.2, 0.2)  # Movimento della testa verso l'alto
    time.sleep(3)
    motion.setAngles("Head", -0.2, 0.2)  # Movimento della testa verso il basso
    time.sleep(3)

    tts.say("Step uno finito")
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
