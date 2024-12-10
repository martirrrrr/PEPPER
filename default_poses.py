# -*- coding: utf-8 -*-
import time
from naoqi import ALProxy

def go_to_all_postures(posture_proxy):
    """
    Esegue tutte le posture predefinite di Pepper in sequenza.

    :param posture_proxy: Proxy ALRobotPosture
    """
    # Elenco delle posture predefinite
    postures = [
        "Stand",       # Posizione eretta standard
        "StandInit",   # Posizione iniziale
        "StandZero",   # Articolazioni in posizione neutra
        "Crouch",      # Posizione accovacciata
        "Sit",         # Posizione seduta
        "SitRelax",    # Posizione seduta rilassata
        "LyingBelly",  # Posizione prona (pancia in giù)
        "LyingBack"    # Posizione supina (schiena a terra)
    ]
    
    for posture in postures:
        try:
            print "[INFO] Passando alla postura:", posture
            posture_proxy.goToPosture(posture, 0.5)  # Cambia postura con velocità 0.5
            time.sleep(2)  # Pausa di 2 secondi per visualizzare la postura
        except Exception as e:
            print "[ERRORE] Impossibile passare alla postura", posture, ":", e

def main():
    """
    Connette al robot e chiama tutte le posture predefinite.
    """
    # Parametri di connessione
    ROBOT_IP = "192.168.1.104"  # Sostituisci con l'IP del tuo robot Pepper
    ROBOT_PORT = 9559  # Porta predefinita di NAOqi

    try:
        # Connessione al proxy ALRobotPosture
        posture_proxy = ALProxy("ALRobotPosture", ROBOT_IP, ROBOT_PORT)
        
        # Esegui tutte le posture predefinite
        go_to_all_postures(posture_proxy)
        print "[INFO] Sequenza completata!"
    
    except Exception as e:
        print "[ERRORE] Non è stato possibile connettersi al robot:", e

if __name__ == "__main__":
    main()
