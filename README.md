***HOW TO***
*************
Download video/audio: (separati)


scp nao@192.168.1.104:/home/nao/recordings/cameras/pepper_video.avi ./pepper_video.avi


scp nao@192.168.1.104:/home/nao/recordings/microphones/pepper_audio.wav ./pepper_audio.wav

*************

Download video/audio: (uniti)


scp nao@192.168.1.104:/home/nao/recordings/cameras/pepper_video.avi ./pepper_video.avi

scp nao@192.168.1.104:/home/nao/recordings/microphones/pepper_audio.wav ./pepper_audio.wav

*************

init.py specificare il path di classification output (stat.txt)
Posizionare nella stessa cartella: init.py, sad.py, relax.py, neutral.py, happy.py.

Alternativo: init.sh per avviare tutto. E' richiesto che stat.txt sia presente in cartella.

*************

init.py -- serve per avviare il programma intero.
sad.py -- emozioni (barzellette)
relax.py -- meditazione 
happy.py -- balletto
neutral.py -- scegli tu (s.r.)
stat.txt -- output del modello

***TO FIX***
-- Sincronizzazione di musica e balletto in happy.py
-- Movimenti di meditazione vari da inserire in relax.py
-- aggiungere altre due canzoni (ed eventalmente balletti diversi)
