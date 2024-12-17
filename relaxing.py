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
    Funzione che utilizza Pepper per riconoscere le parole 'sì', 'no' e 'aiuto'.
    """
    try:
        # Proxy per il riconoscimento vocale
        speech_recognition = ALProxy("ALSpeechRecognition", ip, port)
        speech_recognition.setLanguage("Italian")  # Lingua italiana

        # Proxy per il text-to-speech (TTS)
        text_to_speech = ALProxy("ALTextToSpeech", ip, port)

        # Proxy per il memory per rilevare gli eventi
        memory = ALProxy("ALMemory", ip, port)

        # Imposta il vocabolario con sole tre parole
        vocabulary = ["sì", "no", "aiuto"]
        speech_recognition.setVocabulary(vocabulary, False)
        print("[INFO] Vocabolario impostato: sì, no, aiuto.")

        # Attiva il riconoscimento vocale
        speech_recognition.subscribe("Meditation_ASR")
        print("[INFO] Pepper è in ascolto. Pronuncia una parola...")

        # Ciclo principale
        while True:
            word_recognized = memory.getData("WordRecognized")
            if word_recognized:
                recognized_word = word_recognized[0]
                confidence = word_recognized[1]
                
                if confidence > 0.5:
                    print(f"[INFO] Hai detto: {recognized_word}")
                    
                    if recognized_word == "sì":
                        text_to_speech.say("Perfetto! Continuiamo con la meditazione guidata.")
                        breathing_exercise(text_to_speech)
                    
                    elif recognized_word == "no":
                        text_to_speech.say("Va bene. Facciamo una pausa. Chiamami se hai bisogno.")
                    
                    elif recognized_word == "aiuto":
                        text_to_speech.say("Sono qui per aiutarti. Posso guidarti in un esercizio di respirazione o rilassamento. Di' sì per iniziare.")
                
                # Reset dell'evento
                memory.insertData("WordRecognized", None)

    except KeyboardInterrupt:
        print("\n[INFO] Programma interrotto manualmente.")
        speech_recognition.unsubscribe("Meditation_ASR")
        text_to_speech.say("Alla prossima!")

    except Exception as e:
        print("[ERRORE] Si è verificato un problema:", e)

# Guida l'utente in un esercizio di respirazione profonda
def breathing_exercise(tts, motion, sound):
    tts.say("Trova una posizione comoda e chiudi gli occhi, se ti va.")
    time.sleep(2)
    #play_relaxing_sound(sound)
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


if __name__ == "__main__":
    # Parametri di connessione di Pepper
    ROBOT_IP = "192.168.1.104"  # Sostituisci con l'indirizzo IP di Pepper
    ROBOT_PORT = 9559           # Porta predefinita di Pepper

    speech_recognition(ROBOT_IP, ROBOT_PORT)
