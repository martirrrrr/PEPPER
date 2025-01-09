# -*- coding: utf-8 -*-
from naoqi import ALProxy
import random

def tell_jokes_with_pepper(ip, port):
    """
    Funzione che permette a Pepper di raccontare barzellette e rispondere in base all'input dell'utente.
    """
    try:
        # Proxy per text-to-speech (TTS)
        text_to_speech = ALProxy("ALTextToSpeech", ip, port)

        # Proxy per il riconoscimento vocale
        speech_recognition = ALProxy("ALSpeechRecognition", ip, port)
        speech_recognition.setLanguage("Italian")  # Lingua italiana

        # Proxy per ALMemory
        memory = ALProxy("ALMemory", ip, port)

        # Assicurati che il motore ASR sia disattivato
        try:
            speech_recognition.pause(True)
            speech_recognition.unsubscribe("Test_ASR")
        except RuntimeError:
            print("[INFO] Il modulo 'Test_ASR' non era sottoscritto. Procedo...")

        # Lista di barzellette
        jokes = [
            "Why don’t skeletons fight each other? Because they don’t have the guts.",
            "What did one ocean say to the other ocean? Nothing, they just waved.",
            "Why did the scarecrow win an award? Because he was outstanding in his field.",
            "Why don’t eggs tell jokes? They might crack up.",
            "What’s orange and sounds like a parrot? A carrot.",
            "Why did the math book look sad? Because it had too many problems.",
            "Why can’t your nose be 12 inches long? Because then it would be a foot!",
            "What do you call fake spaghetti? An impasta.",
            "What do you call cheese that isn’t yours? Nacho cheese.",
            "Why don’t scientists trust atoms? Because they make up everything."
        ]

        barzellette =  [
             "Perché i pomodori non parlano? Perché sono sempre rossi dalla vergogna!",
            "Qual è il colmo per un elettricista? Non fare mai scintille con nessuno.",
            "Che cosa fa un matematico in mezzo alla giungla? Cerca il minimo comune multiplo!",
            "Perché le oche vanno sempre a piedi? Perché non hanno le chiavi della macchina!",
            "Sai perché il libro di matematica è triste? Perché ha troppi problemi!",
            "Che cosa fa un vigile urbano con un cappello da cowboy? Regola il traffico... in stile western!",
            "Cosa fa un pollo al cinema? Guarda un film... da paura!",
            "Sai perché i gatti non usano il computer? Perché hanno paura del mouse.",
            "Che cosa fanno due api su un motorino? Rombano!",
            "Perché il computer è sempre calmo? Perché ha il processore freddo."
        ]

        # Lista di parole che Pepper deve riconoscere
        vocabulary = ["sì", "no"]

        # Imposta il vocabolario
        speech_recognition.setVocabulary(vocabulary, False)  # False per evitare il riconoscimento casuale
        print("[INFO] Vocabolario impostato con successo.")

        # Riattiva il motore ASR
        speech_recognition.subscribe("Test_ASR")
        speech_recognition.pause(False)
        print("[INFO] Riconoscimento vocale attivato. Inizio il programma...")

        # Inizio interazione
        joke_index = 0
        text_to_speech.say(jokes[joke_index])  # Racconta la prima barzelletta
        joke_index += 1  # Passa alla prossima barzelletta

        while True:
            print("[INFO] Aspettando una risposta dall'utente...")
            word_recognized = memory.getData("WordRecognized")
            if word_recognized:
                recognized_word = word_recognized[0]  # La parola riconosciuta
                confidence = word_recognized[1]      # Confidenza del riconoscimento

                if confidence > 0.5:  # Filtro per evitare falsi positivi
                    print(f"[INFO] Hai detto: {recognized_word}")
                    
                    if recognized_word == "sì":
                        # Racconta un'altra barzelletta
                        if joke_index < len(jokes):
                            text_to_speech.say(jokes[joke_index])
                            joke_index += 1
                        else:
                            text_to_speech.say("Mi dispiace, ho finito le barzellette!")
                            break

                    elif recognized_word == "no":
                        # Saluta e termina il programma
                        text_to_speech.say("Va bene, è stato un piacere! Alla prossima!")
                        break

                # Reset dell'evento
                memory.insertData("WordRecognized", None)

        # Disabilita il riconoscimento vocale
        speech_recognition.unsubscribe("Test_ASR")

    except Exception as e:
        print("[ERRORE] Si è verificato un problema:", e)

if __name__ == "__main__":
    # Parametri di connessione di Pepper
    ROBOT_IP = "192.168.1.104"  # Sostituisci con l'indirizzo IP di Pepper
    ROBOT_PORT = 9559           # Porta predefinita di Pepper

    tell_jokes_with_pepper(ROBOT_IP, ROBOT_PORT)
