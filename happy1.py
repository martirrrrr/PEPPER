import qi
import time

def connect_to_pepper(robot_ip, port):
    """
    Connetti alla sessione NAOqi di Pepper.
    
    :param robot_ip: Indirizzo IP del robot Pepper
    :param port: Porta del robot
    :return: Oggetto session connesso
    """
    session = qi.Session()
    try:
        session.connect("tcp://"+str(robot_ip)+":"+str(port))
        print("[INFO] Connessione al robot stabilita.")
        return session
    except RuntimeError as e:
        print("[ERRORE] Impossibile connettersi a Pepper. Verifica l'indirizzo IP e la connessione di rete.")
        raise e

def perform_gesture(motion_service):
    """
    Esegue il gesto "ok" con la mano destra.
    
    :param motion_service: Servizio ALMotion
    """
    print("[INFO] Eseguo il gesto 'ok' con la mano destra...")
    #names = ["RHand", "RThumb1", "RThumb2"]
    names = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll","LWristYaw"]
    angles = [-0.5, 0.3, -1.0, -0.5, 0.0]  # Apri la mano e alza il pollice
    motion_service.angleInterpolation(names, angles, [1.0] * len(names), True)

def play_dance(motion_service, durata_canzone):
    """
    Esegue una breve coreografia durante la riproduzione della canzone.
    
    :param motion_service: Servizio ALMotion
    :param durata_canzone: Durata della coreografia in secondi
    """
    print("[INFO] Inizio coreografia...")
    start_time = time.time()
    while time.time() - start_time < durata_canzone:
        # Movimenti di esempio
        motion_service.angleInterpolation(["RShoulderPitch", "LShoulderPitch"], [0.5, 0.5], [1.0, 1.0], True)
        motion_service.angleInterpolation(["RShoulderRoll", "LShoulderRoll"], [-0.5, 0.5], [1.0, 1.0], True)
        motion_service.angleInterpolation(["RShoulderPitch", "LShoulderPitch"], [1.0, 1.0], [1.0, 1.0], True)
        motion_service.angleInterpolation(["RShoulderRoll", "LShoulderRoll"], [0.0, 0.0], [1.0, 1.0], True)
    print("[INFO] Coreografia completata.")

def main(robot_ip, port):
    """
    Esegue una sequenza di interazioni con Pepper.
    
    :param robot_ip: Indirizzo IP del robot Pepper
    :param port: Porta del robot (default: 9559)
    """
    try:
        # Connessione al robot
        session = connect_to_pepper(robot_ip, port)

        # Accesso ai servizi necessari
        tts_service = session.service("ALTextToSpeech")
        motion_service = session.service("ALMotion")
        audio_service = session.service("ALAudioPlayer")

        # Saluto iniziale
        tts_service.say("Mi fa piacere che tu sia felice in questo momento.")
        
        # Esegui il gesto "ok"
        perform_gesture(motion_service)
        
        # Chiede all'utente riguardo alla canzone
        tts_service.say("Che te ne pare di questa canzone?")

        # Avvia la riproduzione della canzone (decommenta e sostituisci con il file corretto)
         music_file = "/home/nao/music/song1.mp3"
         audio_service.playFile(music_file)

        # Durata della canzone in secondi
        durata_canzone = 30  # Modifica in base alla durata effettiva
        play_dance(motion_service, durata_canzone)

        # Conclusione
        tts_service.say("Spero che ti sia piaciuta la canzone. Arrivederci.")

    except Exception as e:
        print("[ERRORE] Si è verificato un problema:", e)

# Parametri del robot
ROBOT_IP = "192.168.0.104"  # Sostituisci con l'indirizzo IP di Pepper
ROBOT_PORT = 9559  # Porta predefinita di NAOqi

if __name__ == "__main__":
    main(ROBOT_IP, ROBOT_PORT)
