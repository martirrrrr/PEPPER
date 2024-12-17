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

def breathing_exercise(talker):
    """
    Esercizio guidato di respirazione.
    """
    try:
        talker.say("Inspira lentamente...")
        time.sleep(4)
        talker.say("Trattieni il respiro per quattro secondi...")
        time.sleep(4)
        talker.say("Espira lentamente...")
        time.sleep(4)
        talker.say("Ripetiamo ancora una volta.")
        time.sleep(1)
        talker.say("Inspira...")
        time.sleep(4)
        talker.say("Espira...")
        time.sleep(4)
        talker.say("Esercizio di respirazione completato.")

    except Exception as e:
        print("[ERRORE] Durante la respirazione:", e)

if __name__ == "__main__":
    # Parametri di connessione di Pepper
    ROBOT_IP = "192.168.1.104"  # Sostituisci con l'indirizzo IP di Pepper
    ROBOT_PORT = 9559           # Porta predefinita di Pepper

    speech_recognition(ROBOT_IP, ROBOT_PORT)
