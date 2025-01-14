def perform_clap(motion_service):
    print("Eseguo il movimento di applauso...")

    # Nomi dei giunti per entrambe le braccia
    joint_names = [
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"
    ]
    
    # Posizione iniziale: mani aperte
    start_angles = [
        1.0, 0.2, -1.5, -0.5,  # Braccio sinistro
        1.0, -0.2, 1.5, 0.5    # Braccio destro
    ]
    
    # Posizione di battuta: mani chiuse al centro
    clap_angles = [
        1.0, 0.0, -1.2, -0.3,  # Braccio sinistro
        1.0, 0.0, 1.2, 0.3     # Braccio destro
    ]
    
    # Tempi di esecuzione per ogni movimento
    times = [0.6] * len(joint_names)
    
    # Numero di battute
    repetitions = 5
    
    for _ in range(repetitions):
        # Movimento: apri le braccia
        motion_service.angleInterpolation(joint_names, start_angles, times, True)
        # Movimento: chiudi le braccia (batti le mani)
        motion_service.angleInterpolation(joint_names, clap_angles, times, True)
    
    # Torna alla posizione iniziale
    motion_service.angleInterpolation(joint_names, start_angles, times, True)
    print("Applauso completato!")


def perform_prayer(motion_service):
    print("Eseguo il movimento di preghiera...")
    
    # Articolazioni per entrambe le braccia
    joint_names = [
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw",
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"
    ]
    
    # Angoli per la posizione di preghiera
    angles = [
        1.0, 0.2, -1.5, -0.5, 0.0,  # Braccio sinistro
        1.0, -0.2, 1.5, 0.5, 0.0   # Braccio destro
    ]
    
    # Tempi di esecuzione per ogni movimento
    times = [1.5] * len(joint_names)
    
    # Esegui il movimento
    motion_service.angleInterpolation(joint_names, angles, times, True)
    
    # Unire le mani
    print("Unisco le mani...")
    motion_service.angleInterpolation(["LHand", "RHand"], [0.0, 0.0], [1.0, 1.0], True)


def move_arms_in_wave(motion_service):
    """
    Movimento a onda con le braccia di Pepper.

    :param motion_service: Servizio ALMotion
    """
    print("[INFO] Movimento a onda con le braccia...")
    names = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", 
             "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]
    angles_list = [
        [0.0, 0.2, -1.0, -0.5, 0.0, -0.2, 1.0, 0.5],  # Posizione iniziale
        [-0.5, 0.5, -0.8, -0.3, 0.5, -0.5, 0.8, 0.3],  # Movimento
        [0.0, 0.2, -1.0, -0.5, 0.0, -0.2, 1.0, 0.5]   # Ritorno alla posizione
    ]
    times = [1.0, 2.0, 3.0]  # Tempi per ciascun step

    for angles in angles_list:
        motion_service.angleInterpolation(names, angles, [t for t in times], True)


def spin_torso(motion_service):
    """
    Rotazione del torso di Pepper.

    :param motion_service: Servizio ALMotion
    """
    print("[INFO] Rotazione del torso...")
    names = ["HipRoll", "HipPitch", "TorsoYaw"]
    angles_list = [
        [0.0, -0.2, 0.3],  # Rotazione iniziale
        [0.3, -0.1, -0.3],  # Rotazione opposta
        [0.0, 0.0, 0.0]     # Torna neutrale
    ]
    times = [1.0, 2.0, 3.0]

    for angles in angles_list:
        motion_service.angleInterpolation(names, angles, [t for t in times], True)


def step_side_to_side(motion_service):
    """
    Passo laterale a destra e sinistra con Pepper.

    :param motion_service: Servizio ALMotion
    """
    print("[INFO] Passo laterale...")
    names = ["LHipYawPitch", "RHipYawPitch"]
    angles_list = [
        [-0.2, 0.2],  # Passo a destra
        [0.2, -0.2],  # Passo a sinistra
        [0.0, 0.0]    # Torna alla posizione neutrale
    ]
    times = [1.0, 2.0, 3.0]

    for angles in angles_list:
        motion_service.angleInterpolation(names, angles, [t for t in times], True)


def nod_head(motion_service):
    """
    Movimento della testa di Pepper che annuisce.

    :param motion_service: Servizio ALMotion
    """
    print("[INFO] Movimento della testa...")
    names = ["HeadPitch", "HeadYaw"]
    angles_list = [
        [0.3, 0.0],  # Chin up
        [-0.3, 0.0], # Chin down
        [0.0, 0.0]   # Neutral
    ]
    times = [1.0, 2.0, 3.0]

    for angles in angles_list:
        motion_service.angleInterpolation(names, angles, [t for t in times], True)


def full_dance_routine(motion_service):
    """
    Esegue una routine completa di ballo.

    :param motion_service: Servizio ALMotion
    """
    print("[INFO] Inizio routine di ballo...")
    move_arms_in_wave(motion_service)
    spin_torso(motion_service)
    #step_side_to_side(motion_service)
    nod_head(motion_service)
    print("[INFO] Routine di ballo completata!")
