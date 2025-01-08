import qi
import time
import random

def main():
    # Connessione al robot
    session = qi.Session()
    try:
        session.connect("tcp://<indirizzo_ip_pepper>:9559")
    except RuntimeError:
        print("Impossibile connettersi a Pepper. Verifica l'indirizzo IP e la connessione di rete.")
        return

    # Accesso ai servizi necessari
    tts_service = session.service("ALTextToSpeech")
    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    # Disattiva la vita autonoma per evitare interferenze
    life_service = session.service("ALAutonomousLife")
    life_service.setState("disabled")

    # Porta Pepper in posizione eretta
    posture_service.goToPosture("StandInit", 0.5)

    # Lista di barzellette
    barzellette = [
        "Perché il pomodoro non riesce a dormire? Perché l'insalata... russa!",
        "Qual è il colmo per un giardiniere? Piantare in asso!",
        "Perché il computer va sempre in vacanza? Perché ha bisogno di un po' di byte!",
        "Qual è il colmo per un elettricista? Non essere al corrente!",
        "Perché le stelle non parlano? Perché sono troppo lontane per fare conversazione!",
        "Qual è il colmo per un matematico? Avere problemi con le soluzioni!",
        "Perché il libro di matematica era triste? Perché aveva troppi problemi!",
        "Qual è il colmo per un fotografo? Avere una vita negativa!",
        "Perché l'orologio è andato in prigione? Perché ha rubato del tempo!",
        "Qual è il colmo per un musicista? Perdere il ritmo della vita!"
    ]

    # Saluto empatico
    tts_service.say("Mi dispiace che tu ti senta triste. Vorrei raccontarti alcune barzellette per tirarti su di morale.")

    # Racconta le barzellette in ordine casuale
    random.shuffle(barzellette)
    for barzelletta in barzellette:
        tts_service.say(barzelletta)
        time.sleep(3)  # Pausa tra una barzelletta e l'altra

    # Messaggio finale
    tts_service.say("Spero che queste barzellette ti abbiano fatto sorridere. Ricorda, sono qui per te.")

    # Ripristina la vita autonoma
    life_service.setState("interactive")

if __name__ == "__main__":
    main()
