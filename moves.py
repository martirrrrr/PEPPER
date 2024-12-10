# -*- coding: utf-8 -*-
from naoqi import ALProxy
import time

def execute_moves(ip, port):
    """
    Esegue una sequenza di movimenti su Pepper:
    - Alza braccio sinistro
    - Alza braccio destro
    - Pollice in su (gesto generico)
    - Incrocia le braccia
    - Riposa
    """
    try:
        # Crea il proxy per il controllo del motore e del posture
        motion = ALProxy("ALMotion", ip, port)
        posture = ALProxy("ALRobotPosture", ip, port)

        # Abilita i motori
        motion.wakeUp()

        # Porta Pepper nella posizione iniziale
        posture.goToPosture("StandInit", 0.5)

        # Alza il braccio sinistro
        print("[INFO] Alzando il braccio sinistro...")
        names = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw"]
        angles = [-0.5, 0.3, -1.0, -0.5, 0.0]  # Posizione del braccio sinistro alzato
        times = [1.0] * len(names)  # Tempo per ogni giunto
        motion.angleInterpolation(names, angles, times, True)
        time.sleep(1)

        # Alza il braccio destro
        print("[INFO] Alzando il braccio destro...")
        names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]
        angles = [-0.5, -0.3, 1.0, 0.5, 0.0]  # Posizione del braccio destro alzato
        times = [1.0] * len(names)  # Tempo per ogni giunto
        motion.angleInterpolation(names, angles, times, True)
        time.sleep(1)

        # Pollice in su (gesto generico con mano destra)
        print("[INFO] Gesto del pollice in su...")
        motion.openHand("RHand")  # Apre la mano destra
        time.sleep(1)
        motion.closeHand("RHand")  # Chiude la mano destra (simula un gesto)
        time.sleep(1)

        # Incrocia le braccia
        print("[INFO] Incrociando le braccia...")
        names = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
                 "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]
        angles = [0.5, 0.3, 0.0, -1.2,  # Posizione braccio sinistro
                  0.5, -0.3, 0.0, 1.2]  # Posizione braccio destro
        times = [1.0] * len(names)  # Tempo per ogni giunto
        motion.angleInterpolation(names, angles, times, True)
        time.sleep(1)

        # Torna alla posizione REST
        print("[INFO] Tornando alla posizione di riposo...")
        posture.goToPosture("SitRelax", 0.5)
        motion.rest()

        print("[INFO] Sequenza completata!")

    except Exception as e:
        print("[ERRORE] Si è verificato un problema:", e)


if __name__ == "__main__":
    # Parametri di connessione di Pepper
    ROBOT_IP = "192.168.1.104"  # Sostituisci con l'indirizzo IP di Pepper
    ROBOT_PORT = 9559           # Porta predefinita di Pepper

    execute_moves(ROBOT_IP, ROBOT_PORT)
