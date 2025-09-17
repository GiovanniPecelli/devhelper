from pathlib import Path
import shutil
import pyperclip
from dotenv import load_dotenv
import os
import google.generativeai as genai

# ================= CONFIG =================
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("La chiave API non trovata. Mettila nel file .env con GOOGLE_API_KEY=...")

genai.configure(api_key=api_key)

BACKUP_DIR = Path("backups")
BACKUP_DIR.mkdir(exist_ok=True)

# ================= FUNZIONI DI SUPPORTO =================
def backup_file(file_path: str) -> Path:
    src = Path(file_path)
    if not src.exists():
        raise FileNotFoundError(f"File non trovato: {file_path}")
    dst = BACKUP_DIR / f"{src.name}.bak"
    shutil.copy2(src, dst)
    return dst

def read_file(file_path: str) -> str:
    path = Path(file_path)
    if not path.exists():
        return f"Errore: file {file_path} non trovato."
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(file_path: str, content: str):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def list_project_files(directory=".", max_depth=1):
    """
    Restituisce i file fino a una profondità massima (default 1 = root + prime sottocartelle)
    """
    base_path = Path(directory).resolve()
    files = []

    for path in base_path.rglob("*"):
        if path.is_file():
            # calcolo profondità relativa
            depth = len(path.relative_to(base_path).parts)
            if depth <= max_depth:
                files.append(str(path))
    return files

def copy_file_to_clipboard(file_path: str) -> str:
    content = read_file(file_path)
    if content.startswith("Errore"):
        return content
    pyperclip.copy(content)
    return f"Contenuto di {file_path} copiato negli appunti!"

# ================= CLASSE AGENTE =================
class Agent:
    def __init__(self, name: str, model_name="gemini-1.5-flash"):
        self.name = name
        self.model = genai.GenerativeModel(model_name)

    def ask(self, prompt: str) -> str:
        """Risponde a un prompt generico"""
        response = self.model.generate_content(prompt)
        return response.text

    def modify_file(self, file_path: str, instruction: str) -> str:
        """Modifica un file con il modello AI e salva la nuova versione"""
        backup_path = backup_file(file_path)
        content = read_file(file_path)
        full_prompt = f"""
Sei un assistente di coding.
Ecco il file originale:

{content}

Istruzione per modificarlo:
{instruction}

Rispondi solo con il nuovo contenuto del file.
"""
        response = self.model.generate_content(full_prompt)
        new_content = response.text
        write_file(file_path, new_content)
        return f"Modifica completata! Backup salvato in {backup_path}"