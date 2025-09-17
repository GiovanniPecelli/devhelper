# 🤖 AI DevHelper

Un assistente AI per sviluppatori che utilizza Google Gemini per analizzare, modificare e migliorare il codice direttamente dal terminale.

## ✨ Caratteristiche

- 🔍 **Analisi automatica del codice** - Identifica problemi e suggerisce miglioramenti
- ✏️ **Modifica file con AI** - Modifica i tuoi file con istruzioni in linguaggio naturale
- 🐛 **Rilevamento bug** - Trova potenziali problemi nel codice
- 📚 **Generazione documentazione** - Crea documentazione automaticamente
- 📋 **Gestione file** - Lista, leggi e copia file facilmente
- 💾 **Backup automatico** - Ogni modifica crea un backup di sicurezza
- 🎯 **Interfaccia doppia** - Modalità interattiva e comandi singoli

## 🚀 Installazione

### Da GitHub (Consigliato)

```bash
pip install git+https://github.com/tuousername/devhelper.git
```

### Installazione locale per sviluppo

```bash
git clone https://github.com/tuousername/devhelper.git
cd devhelper
pip install -e .
```

## ⚙️ Configurazione

1. **Ottieni una API key di Google Gemini**:
   - Vai su [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Crea una nuova API key
   - Copiala

2. **Configura nel tuo progetto**:
   ```bash
   # Nel tuo progetto
   devhelper init
   ```
   Questo crea un file `.env` dove inserire:
   ```
   GOOGLE_API_KEY=la_tua_api_key_qui
   ```

## 📖 Utilizzo

### 🎮 Modalità Interattiva

Lancia l'interfaccia interattiva:

```bash
("se nel devhelper") python -m ai_agent.devhelper
devhelper
```

Comandi disponibili nell'interfaccia:
```
list [depth]      - Lista file del progetto
read <file>       - Leggi contenuto di un file  
modify <file>     - Modifica file con AI
copy <file>       - Copia file negli appunti
analyze <file>    - Analizza codice
doc <file>        - Genera documentazione
bugs <file>       - Cerca bug potenziali
ask <domanda>     - Fai una domanda generica
help              - Mostra aiuto
quit              - Esci
```

**Esempio di sessione:**
```
🤖 DevHelper avviato!
>> list 2
📂 Lista dei file nel progetto:
  main.py
  utils.py
  config.py

>> analyze main.py
🔍 Analisi di main.py:
Il codice presenta alcune aree di miglioramento...

>> modify utils.py
📝 Istruzione per l'agente: Aggiungi docstrings a tutte le funzioni
⚠️  Sei sicuro di voler modificare utils.py? (s/N): s
✅ Modifica completata! Backup salvato in backups/utils.py.bak
```

### ⚡ Comandi Singoli (CLI)

Se preferisci usare comandi singoli:

```bash
# Domande generiche
devhelper-cli ask "Come posso ottimizzare questo algoritmo?"

# Gestione file
devhelper-cli list              # Lista file progetto
devhelper-cli read main.py      # Leggi un file
devhelper-cli copy main.py      # Copia negli appunti

# Modifica con AI
devhelper-cli modify main.py "Aggiungi commenti e docstrings"

# Analisi codice  
devhelper-cli analyze main.py   # Analisi generale
devhelper-cli doc main.py       # Genera documentazione
devhelper-cli bugs main.py      # Cerca bug

# Setup
devhelper-cli init              # Inizializza in un progetto
```

## 🔧 Utilizzo Programmatico

Puoi anche importare DevHelper nei tuoi script Python:

```python
from ai_agent import DevHelper, AgentCore

# Interfaccia semplice
helper = DevHelper()
response = helper.process_request("Analizza questo codice per bug")

# Controllo completo
agent = AgentCore()
files = agent.list_project_files(max_depth=2)
analysis = agent.analyze_file("main.py")
agent.modify_file("utils.py", "Aggiungi type hints")
```

## 🛠️ Esempi Pratici

### Analizzare un progetto nuovo
```bash
cd /path/to/new/project
devhelper init
devhelper

>> list 2
>> analyze src/main.py
>> doc src/utils.py
```

### Refactoring guidato
```bash
devhelper

>> analyze legacy_code.py
>> modify legacy_code.py "Refactoring per migliorare leggibilità e performance"
>> bugs legacy_code.py  # Verifica dopo il refactoring
```

### Documentazione automatica
```bash
devhelper-cli doc api.py > docs/api.md
devhelper-cli doc utils.py > docs/utils.md
```

### Revisione codice
```bash
for file in *.py; do
    devhelper-cli bugs "$file" >> code_review.md
done
```

## 🎯 Funzionalità Avanzate

### Backup Automatico
- Ogni modifica crea automaticamente un backup in `backups/`
- I file vengono salvati come `nomefile.estensione.bak`

### Filtri Intelligenti
- Esclude automaticamente `.git`, `__pycache__`, `.venv`, `node_modules`
- Personalizzabile modificando il codice

### Gestione Errori
- Tutti i comandi hanno gestione errori robusta
- Conferme richieste per operazioni distruttive
- Messaggi di errore chiari e utili

## 🔒 Sicurezza e Privacy

- **API Key**: Mantenuta in locale nel file `.env`
- **Backup**: Creazione automatica prima di ogni modifica
- **Conferme**: Richieste per operazioni che modificano file
- **Privacy**: Il codice viene inviato solo a Google Gemini per l'elaborazione

## 🤝 Contribuire

1. Fai un fork del repository
2. Crea un branch per la tua feature: `git checkout -b feature/nuova-funzione`
3. Commit le modifiche: `git commit -am 'Aggiunge nuova funzione'`
4. Push al branch: `git push origin feature/nuova-funzione`
5. Apri una Pull Request

## 📝 Roadmap

- [ ] Supporto per più modelli AI (OpenAI, Claude, ecc.)
- [ ] Plugin system per funzionalità custom
- [ ] Interfaccia web opzionale
- [ ] Integrazione con IDE popolari
- [ ] Supporto per progetti multi-linguaggio
- [ ] Cache intelligente per risposte frequenti

## ❓ FAQ

**Q: Quanto costa usare Google Gemini?**  
A: Google Gemini ha un tier gratuito generoso. Controlla i [prezzi attuali](https://ai.google.dev/pricing).

**Q: I miei dati sono al sicuro?**  
A: Il codice viene inviato a Google solo per l'elaborazione. Non viene salvato sui loro server.

**Q: Posso usarlo con progetti privati?**  
A: Sì, funziona con qualsiasi progetto locale. Considera le policy di privacy della tua azienda.

**Q: Cosa succede se l'AI sbaglia?**  
A: Ogni modifica crea un backup automatico. Puoi sempre ripristinare la versione precedente.

## 📄 Licenza

MIT License - vedi il file [LICENSE](LICENSE) per i dettagli.

## 🙋‍♂️ Supporto

- 🐛 [Segnala bug](https://github.com/tuousername/devhelper/issues)
- 💡 [Richiedi funzionalità](https://github.com/tuousername/devhelper/issues)
- 📧 Email: tua@email.com

---

⭐ Se trovi utile questo progetto, lascia una stella su GitHub!

## 🎬 Demo

```bash
# Installa
pip install git+https://github.com/tuousername/devhelper.git

# Configura
devhelper init

# Usa!
devhelper
>> ask "Come posso migliorare le performance di questo algoritmo di sorting?"
>> modify sorting.py "Ottimizza per performance migliori"
>> analyze sorting.py
```

Fatto! Ora hai un assistente AI sempre a portata di terminale. 🚀