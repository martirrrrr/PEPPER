# -*- coding: utf-8 -*-
import time
from naoqi import ALProxy

def set_pose(motion_proxy, posture_proxy, pose_name):
    """
    Imposta Pepper in una posa predefinita.
    
    :param motion_proxy: Proxy al servizio ALMotion
    :param posture_proxy: Proxy al servizio ALRobotPosture
    :param pose_name: Nome della posa da eseguire
    """
    if pose_name == "wave":
        # Saluto con la mano destra
        motion_proxy.angleInterpolationWithSpeed("RShoulderPitch", -1.0, 0.2)
        motion_proxy.angleInterpolationWithSpeed("RElbowRoll", 0.5, 0.2)
        motion_proxy.angleInterpolationWithSpeed("RWristYaw", 1.5, 0.2)
        time.sleep(2)  # Mantiene la posa per 2 secondi
        motion_proxy.angleInterpolationWithSpeed("RShoulderPitch", 1.5, 0.2)  # Torna alla posizione iniziale

    elif pose_name == "point":
        # Indica in avanti con il braccio destro
        motion_proxy.angleInterpolationWithSpeed("RShoulderPitch", 0.0, 0.2)
        motion_proxy.angleInterpolationWithSpeed("RShoulderRoll", -0.5, 0.2)
        motion_proxy.angleInterpolationWithSpeed("RElbowYaw", 1.5, 0.2)
        motion_proxy.angleInterpolationWithSpeed("RWristYaw", 0.0, 0.2)
        time.sleep(2)
        motion_proxy.angleInterpolationWithSpeed("RShoulderPitch", 1.5, 0.2)  # Torna alla posizione iniziale

    elif pose_name == "celebrate":
        # Alza entrambe le braccia come in un gesto celebrativo
        motion_proxy.angleInterpolationWithSpeed("LShoulderPitch", 0.0, 0.2)
        motion_proxy.angleInterpolationWithSpeed("RShoulderPitch", 0.0, 0.2)
        motion_proxy.angleInterpolationWithSpeed("LElbowRoll", -0.5, 0.2)
        motion_proxy.angleInterpolationWithSpeed("RElbowRoll", 0.5, 0.2)
        time.sleep(2)
        posture_proxy.goToPosture("StandInit", 0.5)  # Torna alla posizione iniziale

    elif pose_name == "sit":
        # Simula una posizione seduta
        posture_proxy.goToPosture("Sit", 0.5)
        time.sleep(2)

    else:
        print("[INFO] Posa non riconosciuta.")

def main(robot_ip, port):
    """
    Esegue una sequenza di pose su Pepper.
    
    :param robot_ip: Indirizzo IP del robot Pepper
    :param port: Porta del robot (default: 9559)
    """
    try:
        # Connetti ai proxy di Pepper
        motion_proxy = ALProxy("ALMotion", robot_ip, port)
        posture_proxy = ALProxy("ALRobotPosture", robot_ip, port)

        # Sblocca le giunture
        motion_proxy.wakeUp()
        
        # Esegui una sequenza di pose
        #print("[INFO] Eseguo la posa di saluto...")
        #set_pose(motion_proxy, posture_proxy, "wave")
        
        #print("[INFO] Eseguo la posa di indicazione...")
        #set_pose(motion_proxy, posture_proxy, "point")
        
        print("[INFO] Eseguo la posa celebrativa...")
        set_pose(motion_proxy, posture_proxy, "celebrate")
        
        #print("[INFO] Eseguo la posa seduta...")
        #set_pose(motion_proxy, posture_proxy, "sit")
        
        # Torna alla posizione iniziale
        posture_proxy.goToPosture("StandInit", 0.5)
        print("[INFO] Sequenza completata.")

        # Metti Pepper a riposo
        motion_proxy.rest()

    except Exception as e:
        print("[ERRORE] Si è verificato un problema:", e)

# Parametri del robot
ROBOT_IP = "192.168.1.104"  # Sostituisci con l'indirizzo IP di Pepper
ROBOT_PORT = 9559  # Porta predefinita di NAOqi

if __name__ == "__main__":
    main(ROBOT_IP, ROBOT_PORT)
