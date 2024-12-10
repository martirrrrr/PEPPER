# -*- coding: utf-8 -*-
from naoqi import ALProxy

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
        vocabulary = ["sì", "no", "ciao", "grazie", "robot"]

        # Proxy per il memory per rilevare gli eventi
        memory = ALProxy("ALMemory", ip, port)

        # Verifica se il modulo è già sottoscritto
        try:
            speech_recognition.unsubscribe("Test_ASR")
        except RuntimeError:
            print("[INFO] Il modulo 'Test_ASR' non era sottoscritto. Procedo...")
         # False per evitare il riconoscimento casuale

        # Riavvia il riconoscimento vocale
        speech_recognition.subscribe("Test_ASR")
        print("[INFO] Riconoscimento vocale attivato. Pronuncia una parola...")

        # Imposta il vocabolario
        speech_recognition.setVocabulary(vocabulary, False) 
        # Contatore delle interazioni
        interaction_count = 0
        max_interactions = 3  # Numero massimo di richieste

        while interaction_count < max_interactions:
            # Aspetta che Pepper riconosca una parola
            word_recognized = memory.getData("WordRecognized")
            if word_recognized:
                recognized_word = word_recognized[0]  # La parola riconosciuta
                confidence = word_recognized[1]      # Confidenza del riconoscimento
                if confidence > 0.5:  # Filtro per evitare falsi positivi
                    print("[INFO] Hai detto: ", recognized_word)
                    text_to_speech.say("Hai detto ", recognized_word)
                    interaction_count += 1  # Incrementa il contatore
                memory.insertData("WordRecognized", None)  # Reset dell'evento

        print("[INFO] Raggiunto il limite delle interazioni. Programma terminato.")
        text_to_speech.say("Grazie per aver giocato con me! Alla prossima!")
        speech_recognition.unsubscribe("Test_ASR")  # Disabilita il riconoscimento vocale

    except Exception as e:
        print("[ERRORE] Si è verificato un problema:", e)

if __name__ == "__main__":
    # Parametri di connessione di Pepper
    ROBOT_IP = "192.168.1.104"  # Sostituisci con l'indirizzo IP di Pepper
    ROBOT_PORT = 9559           # Porta predefinita di Pepper

    speech_recognition(ROBOT_IP, ROBOT_PORT)
