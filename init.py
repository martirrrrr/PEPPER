# init.py

from happy import main as happy_main
from sad import main as sad_main
from relax import main as relax_main
from neutral import main as neutral_main

def read_value(path):
    try:
        with open(path, 'r') as file:
            val = file.read().strip()
            return int(val)
    except FileNotFoundError:
        print(f"Error: file '{path}' not found.")
    except ValueError:
        print(f"Error: invalid file content'{path}'.")
    return None

def main():
    path = 'stat.txt'  # Sostituisci con il percorso corretto del tuo file
    val = read_val(path)

    if val is None:
        return

    if val == 0:
        happy_main()
    elif val == 1:
        sad_main()
    elif val == 2:
        relax_main()
    elif val == 3:
        neutral = neutral_main()
        if neutral == 0:
            happy_main()
        elif neutral == 1:
            sad_main()
        elif neutral == 2:
            relax_main()
        else:
            print("Invalid value returned by neutral.py .")
    else:
        print("Invalid.")

if __name__ == "__main__":
    main()
