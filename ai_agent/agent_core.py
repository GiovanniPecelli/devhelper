# ai_agent/agent_core.py
from pathlib import Path
import shutil
import pyperclip
from dotenv import load_dotenv
import os
import google.generativeai as genai


# -----------------------
# Helper per ricerca .env
# -----------------------
def find_project_root(start_path: Path = None) -> Path:
    """
    Cerca la root del progetto risalendo da start_path (default = cwd).
    La root viene individuata se contiene uno dei marker ('.git', 'pyproject.toml', 'setup.py', 'requirements.txt', 'Pipfile', 'package.json').
    Se nessun marker è trovato, ritorna la path di partenza risolta.
    """
    path = (Path(start_path) if start_path else Path.cwd()).resolve()
    markers = {'.git', 'pyproject.toml', 'setup.py', 'requirements.txt', 'Pipfile', 'package.json'}
    for parent in [path] + list(path.parents):
        if any((parent / marker).exists() for marker in markers):
            return parent
    return path


def load_api_key_with_fallbacks() -> tuple:
    """
    Order of precedence:
    1. Environment variable GOOGLE_API_KEY
    2. .env in project root (detected by find_project_root)
    3. user home file ~/.devhelper.env
    4. user home ~/.env
    Returns: (api_key_or_None, source_description_or_None)
    """
    # 1) env var (highest precedence)
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        return api_key, "env-var"

    # 2) project .env at detected project root
    project_root = find_project_root()
    project_env = project_root / ".env"
    if project_env.exists():
        load_dotenv(project_env)
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            return api_key, f"project:{project_root}"

    # 3) home-level devhelper config
    home_devhelper = Path.home() / ".devhelper.env"
    if home_devhelper.exists():
        load_dotenv(home_devhelper)
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            return api_key, f"home:{home_devhelper}"

    # 4) generic home .env
    home_env = Path.home() / ".env"
    if home_env.exists():
        load_dotenv(home_env)
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            return api_key, f"home_env:{home_env}"

    return None, None


# -----------------------
# AgentCore
# -----------------------
class AgentCore:
    """Core dell'agente AI per sviluppatori"""

    def __init__(self, model_name="gemini-1.5-flash"):
        # Carica la chiave API con fallback multipli
        api_key, source = load_api_key_with_fallbacks()
        if not api_key:
            # Messaggio d'errore esplicativo con soluzioni suggerite
            raise ValueError(
                "❌ Errore: La chiave API non trovata.\n"
                "Assicurati di avere la variabile d'ambiente GOOGLE_API_KEY o un file .env nella root del progetto.\n\n"
                "Opzioni:\n"
                " - Creare un file .env nella root del progetto contenente: GOOGLE_API_KEY=la_tua_api_key\n"
                " - Impostare la variabile d'ambiente (Windows PowerShell):\n"
                "     [Environment]::SetEnvironmentVariable(\"GOOGLE_API_KEY\",\"la_tua_api_key\",\"User\")\n"
                " - Oppure creare un file globale in %USERPROFILE%/.devhelper.env con la stessa riga.\n"
            )

        # Configura Google Gemini
        genai.configure(api_key=api_key)
        self._api_key_source = source  # utile per debug / logging

        # Inizializza modello e backup directory
        self.model = genai.GenerativeModel(model_name)
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)

    # --- resto delle funzioni invariate ---
    def backup_file(self, file_path: str) -> Path:
        """Crea un backup del file specificato"""
        src = Path(file_path)
        if not src.exists():
            raise FileNotFoundError(f"File non trovato: {file_path}")
        dst = self.backup_dir / f"{src.name}.bak"
        shutil.copy2(src, dst)
        return dst

    def read_file(self, file_path: str) -> str:
        """Legge il contenuto di un file"""
        path = Path(file_path)
        if not path.exists():
            return f"Errore: file {file_path} non trovato."
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                with open(path, "r", encoding="latin-1") as f:
                    return f.read()
            except Exception as e:
                return f"Errore nella lettura del file: {str(e)}"

    def write_file(self, file_path: str, content: str):
        """Scrive contenuto in un file"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    def list_project_files(self, directory=".", max_depth=1):
        """
        Restituisce i file fino a una profondità massima 
        (default 1 = root + prime sottocartelle)
        """
        base_path = Path(directory).resolve()
        files = []

        # Cartelle da escludere
        exclude_dirs = {'.git', '__pycache__', '.venv', 'node_modules', '.pytest_cache'}

        for path in base_path.rglob("*"):
            if path.is_file():
                # Salta file in cartelle escluse
                if any(excluded in path.parts for excluded in exclude_dirs):
                    continue

                # Calcolo profondità relativa
                depth = len(path.relative_to(base_path).parts)
                if depth <= max_depth:
                    files.append(str(path))
        return sorted(files)

    def copy_file_to_clipboard(self, file_path: str) -> str:
        """Copia il contenuto di un file negli appunti"""
        content = self.read_file(file_path)
        if content.startswith("Errore"):
            return content
        try:
            pyperclip.copy(content)
            return f"Contenuto di {file_path} copiato negli appunti!"
        except Exception as e:
            return f"Errore nel copiare negli appunti: {str(e)}"

    def ask(self, prompt: str) -> str:
        """Risponde a un prompt generico"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Errore nell'elaborazione: {str(e)}"

    def modify_file(self, file_path: str, instruction: str) -> str:
        """Modifica un file con il modello AI e salva la nuova versione"""
        try:
            backup_path = self.backup_file(file_path)
            content = self.read_file(file_path)

            if content.startswith("Errore"):
                return content

            full_prompt = f"""
Sei un assistente di coding esperto.
Ecco il file originale:

--- INIZIO FILE ---
{content}
--- FINE FILE ---

Istruzione per modificarlo:
{instruction}

IMPORTANTE: Rispondi SOLO con il nuovo contenuto completo del file, senza spiegazioni aggiuntive.
"""
            response = self.model.generate_content(full_prompt)
            new_content = response.text

            # Rimuovi eventuali markdown code blocks
            if new_content.startswith("```"):
                lines = new_content.split('\n')
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines[-1].strip() == "```":
                    lines = lines[:-1]
                new_content = '\n'.join(lines)

            self.write_file(file_path, new_content)
            return f"Modifica completata! Backup salvato in {backup_path}"

        except Exception as e:
            return f"Errore nella modifica del file: {str(e)}"

    def analyze_file(self, file_path: str) -> str:
        """Analizza un file e fornisce suggerimenti"""
        content = self.read_file(file_path)
        if content.startswith("Errore"):
            return content

        prompt = f"""
Analizza questo file di codice e fornisci:
1. Una breve descrizione di cosa fa
2. Eventuali problemi o miglioramenti possibili
3. Suggerimenti per ottimizzazioni

File: {file_path}
--- CONTENUTO ---
{content}
--- FINE CONTENUTO ---
"""
        return self.ask(prompt)

    def generate_documentation(self, file_path: str) -> str:
        """Genera documentazione per un file"""
        content = self.read_file(file_path)
        if content.startswith("Errore"):
            return content

        prompt = f"""
Genera una documentazione completa per questo file di codice.
Includi:
- Descrizione generale
- Funzioni/classi principali e loro scopo
- Parametri e tipi di ritorno
- Esempi di utilizzo se appropriato

File: {file_path}
--- CONTENUTO ---
{content}
--- FINE CONTENUTO ---
"""
        return self.ask(prompt)

    def find_bugs(self, file_path: str) -> str:
        """Cerca potenziali bug nel codice"""
        content = self.read_file(file_path)
        if content.startswith("Errore"):
            return content

        prompt = f"""
Analizza questo codice cercando potenziali bug, errori di logica, 
problemi di sicurezza e best practices non seguite.
Fornisci suggerimenti specifici per risolvere i problemi trovati.

File: {file_path}
--- CONTENUTO ---
{content}
--- FINE CONTENUTO ---
"""
        return self.ask(prompt)