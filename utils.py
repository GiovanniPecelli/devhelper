import os
from pathlib import Path
import shutil

# Cartella backup
BACKUP_DIR = Path("backups")
BACKUP_DIR.mkdir(exist_ok=True)

# =================== Funzioni di utilità ===================

def list_project_files(directory="."):
    """Restituisce tutti i file presenti nel progetto (ricorsivo)."""
    file_list = []
    for path in Path(directory).rglob("*"):
        if path.is_file():
            file_list.append(str(path))
    return file_list

def read_file(file_path):
    """Legge e restituisce il contenuto di un file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File non trovato: {file_path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(file_path, content):
    """Scrive il contenuto nel file e crea backup automatico."""
    path = Path(file_path)
    if path.exists():
        backup_path = BACKUP_DIR / f"{path.name}.bak"
        shutil.copy2(path, backup_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)