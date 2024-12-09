from naoqi import ALProxy
import time

def perform_empathic_action_with_voice(ip, port):
    try:
        # Creazione dei proxy
        motion = ALProxy("ALMotion", ip, port)
        posture = ALProxy("ALRobotPosture", ip, port)
        tts = ALProxy("ALTextToSpeech", ip, port)
        asr = ALProxy("ALSpeechRecognition", ip, port)
        
        # Risvegliare Pepper
        motion.wakeUp()
        
        # Mettere Pepper in posizione iniziale
        posture.goToPosture("Stand", 0.8)
        
        # Inclinare la testa come gesto empatico
        print("[INFO] Inclinando la testa...")
        motion.setAngles("HeadPitch", 0.3, 0.2)  # Inclina la testa in avanti
        motion.setAngles("HeadYaw", 0.2, 0.2)    # Inclina leggermente la testa di lato
        time.sleep(2)
        
        # Dire qualcosa di confortante
        print("[INFO] Parlando...")
        comforting_message = (
            "I'm here for you. Everything will be okay. "
            "Sometimes we all need a little support, and I'm here to help."
        )
        tts.say(comforting_message)
        
        # Rimettere la testa in posizione neutra
        print("[INFO] Riposizionando la testa...")
        motion.setAngles("HeadPitch", 0.0, 0.2)  # Torna alla posizione neutra
        motion.setAngles("HeadYaw", 0.0, 0.2)
        time.sleep(2)
        
        # Chiedere se vuole giocare
        print("[INFO] Chiedendo se vuole giocare...")
        tts.say("Would you like to play a game? Please say yes or no.")
        
        # Inizializzare il riconoscimento vocale
        asr.setLanguage("English")  # Imposta la lingua (può essere cambiata in base alla lingua preferita)
        asr.setVocabulary(["yes", "no"], False)  # Aggiungi parole chiave per riconoscere "yes" e "no"
        asr.subscribe("Test_ASR")
        
        # Attendere la risposta dell'utente
        response = None
        start_time = time.time()
        while time.time() - start_time < 5:  # Limita l'ascolto a 5 secondi
            if asr.hasRecognizedWord():
                response = asr.getResult()
                break
        
        # Gestire la risposta
        if response == "yes":
            tts.say("Great! Let's have some fun!")
        elif response == "no":
            tts.say("Okay, no worries. I'm here if you change your mind.")
        else:
            tts.say("Sorry, I didn't catch that. Could you please say yes or no?")
        
        # Fermare il riconoscimento vocale
        asr.unsubscribe("Test_ASR")
        
        # Mettere Pepper a riposo
        motion.rest()
        print("[INFO] Azione completata!")
    
    except Exception as e:
        print("[ERRORE] Si è verificato un problema:", e)

# Parametri di connessione
ROBOT_IP = "192.168.1.104"  # Sostituisci con l'IP di Pepper
#ROBOT_IP = "192.168.0.67"
ROBOT_PORT = 9559  # Porta predefinita di NAOqi

# Esegui l'azione empatica con riconoscimento vocale
perform_empathic_action_with_voice(ROBOT_IP, ROBOT_PORT)
