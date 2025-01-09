# -*- coding: utf-8 -*-
from naoqi import ALProxy
import time

def speech_recognition(ip, port):
    """
    Funzione che utilizza Pepper per riconoscere una parola e ripeterla.
    """
    try:
        # Proxy per il riconoscimento vocale
        speech_recognition = ALProxy("ALSpeechRecognition", ip, port)
        speech_recognition.setLanguage("Italian")  # Imposta la lingua italiana

        # Proxy per il text-to-speech (TTS)
        text_to_speech = ALProxy("ALTextToSpeech", ip, port)

        # Lista di parole che Pepper deve riconoscere
        vocabulary = ["meditare", "ballare", "ridere", "arrivederci"]

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
        print("[INFO] Riconoscimento vocale attivato. Pronuncia una parola...")

        # Variabile per controllare se una parola è stata riconosciuta
        word_recognized = False

        while not word_recognized:
            # Attendi che Pepper riconosca una parola
            recognized_data = memory.getData("WordRecognized")
            if recognized_data:
                recognized_word = recognized_data[0]  # La parola riconosciuta
                confidence = recognized_data[1]      # Confidenza del riconoscimento
                if confidence > 0.5:  # Filtro per evitare falsi positivi
                    print(f"[INFO] Hai detto: {recognized_word}")
                    text_to_speech.say(f"Hai detto {recognized_word}")
                    word_recognized = True  # Esci dal ciclo dopo aver riconosciuto una parola valida
                memory.insertData("WordRecognized", None)  # Reset dell'evento
            time.sleep(0.1)  # Piccola pausa per evitare un loop troppo veloce

        print("[INFO] Parola riconosciuta. Programma terminato.")
        speech_recognition.unsubscribe("Test_ASR")
      
        if recognized_word == vocabulary[0]: # meditare
          text_to_speech.say("Bene, incominciamo!")
          return 0
        elif recognized_word == vocabulary[1]: # ballare
          text_to_speech.say("Ottima scelta!")
          return 1
        elif recognized_word == vocabulary[2]: # ridere
          text_to_speech.say("Prova a non ridere!")
          return 2
        elif recognized_word == vocabulary[3]: # arrivederci
          text_to_speech.say("Grazie per aver parlato con me! Alla prossima!")  
          return
           # Disabilita il riconoscimento vocale

    except Exception as e:
        print("[ERRORE] Si è verificato un problema:", e)

if __name__ == "__main__":
    # Parametri di connessione di Pepper
    ROBOT_IP = "192.168.1.104"  # Sostituisci con l'indirizzo IP di Pepper
    ROBOT_PORT = 9559           # Porta predefinita di Pepper

    speech_recognition(ROBOT_IP, ROBOT_PORT)
