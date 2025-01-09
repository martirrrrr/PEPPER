#!/bin/bash

# Percorso del file contenente il valore
file_path="stat.txt"

# Verifica se il file esiste
if [[ ! -f "$file_path" ]]; then
    echo "Errore: il file '$file_path' non esiste."
    exit 1
fi

# Legge il contenuto del file
value=$(<"$file_path")

# Verifica se il contenuto è un numero intero
if ! [[ "$value" =~ ^[0-9]+$ ]]; then
    echo "Errore: il contenuto di '$file_path' non è un numero valido."
    exit 1
fi

# Esegue lo script corrispondente al valore
case "$value" in
    0)
        echo "Eseguo happy.sh"
        ./happy.sh
        ;;
    1)
        echo "Eseguo relax.sh"
        ./relax.sh
        ;;
    2)
        echo "Eseguo sad.sh"
        ./sad.sh
        ;;
    *)
        echo "Valore non valido: $value. Nessun programma eseguito."
        ;;
esac
