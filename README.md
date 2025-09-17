Questo progetto contiene `DevHelper`, un agente AI per aiutarti a leggere, modificare e copiare file all'interno di un progetto Python.

## Comandi disponibili

- `list` → lista tutti i file del progetto
- `read [file]` → legge un file specifico
- `modify [file]` → modifica un file secondo un'istruzione
- `copy [file]` → copia il contenuto del file negli appunti
- `ask [domanda]` → chiedi qualcosa all'agente
- `quit` → esci dall'agente

## Backup
Ogni modifica fatta con `modify` genera automaticamente un backup nella cartella `backups/` con timestamp.

## Come usare
Esegui `main.py` e usa i comandi sopra per interagire con l'agente.

## IMPORT LIBRARIES from requirments.txt
execute this command in the terminal (in the main root): "pip install -r requirements.txt"
