import click
from pathlib import Path
from .agent_core import AgentCore
import sys

@click.group()
@click.version_option(version="0.1.0")
def main():
    """DevHelper - Assistente AI per sviluppatori"""
    pass

@main.command()
@click.argument('prompt', required=True)
@click.option('--model', default='gemini-1.5-flash', help='Modello AI da utilizzare')
def ask(prompt, model):
    """Fai una domanda generica al devhelper"""
    try:
        agent = AgentCore(model_name=model)
        response = agent.ask(prompt)
        click.echo(f"\n🤖 DevHelper risponde:\n{response}\n")
    except Exception as e:
        click.echo(f"❌ Errore: {str(e)}", err=True)
        sys.exit(1)

@main.command()
@click.option('--depth', '-d', default=1, help='Profondità di scansione delle cartelle')
@click.option('--directory', default='.', help='Directory da scansionare')
def list(depth, directory):
    """Elenca i file del progetto"""
    try:
        agent = AgentCore()
        files = agent.list_project_files(directory=directory, max_depth=depth)
        
        if not files:
            click.echo("📂 Nessun file trovato nel progetto.")
            return
            
        click.echo(f"📂 Lista dei file nel progetto (profondità: {depth}):")
        for file_path in files:
            # Mostra path relativo più pulito
            rel_path = Path(file_path).relative_to(Path(directory).resolve())
            click.echo(f"  {rel_path}")
            
    except Exception as e:
        click.echo(f"❌ Errore: {str(e)}", err=True)
        sys.exit(1)

@main.command()
@click.argument('file_path')
def read(file_path):
    """Leggi il contenuto di un file"""
    try:
        agent = AgentCore()
        content = agent.read_file(file_path)
        
        if content.startswith("Errore"):
            click.echo(f"❌ {content}", err=True)
            sys.exit(1)
            
        click.echo(f"\n📄 Contenuto di {file_path}:")
        click.echo("=" * 50)
        click.echo(content)
        click.echo("=" * 50)
        
    except Exception as e:
        click.echo(f"❌ Errore: {str(e)}", err=True)
        sys.exit(1)

@main.command()
@click.argument('file_path')
def copy(file_path):
    """Copia il contenuto di un file negli appunti"""
    try:
        agent = AgentCore()
        result = agent.copy_file_to_clipboard(file_path)
        
        if result.startswith("Errore"):
            click.echo(f"❌ {result}", err=True)
            sys.exit(1)
            
        click.echo(f"📋 {result}")
        
    except Exception as e:
        click.echo(f"❌ Errore: {str(e)}", err=True)
        sys.exit(1)

@main.command()
@click.argument('file_path')
@click.argument('instruction')
@click.option('--model', default='gemini-1.5-flash', help='Modello AI da utilizzare')
def modify(file_path, instruction, model):
    """Modifica un file usando l'AI"""
    try:
        agent = AgentCore(model_name=model)
        
        # Conferma prima di modificare
        if not click.confirm(f"Sei sicuro di voler modificare {file_path}?"):
            click.echo("Operazione annullata.")
            return
            
        result = agent.modify_file(file_path, instruction)
        
        if result.startswith("Errore"):
            click.echo(f"❌ {result}", err=True)
            sys.exit(1)
            
        click.echo(f"✅ {result}")
        
    except Exception as e:
        click.echo(f"❌ Errore: {str(e)}", err=True)
        sys.exit(1)

@main.command()
@click.argument('file_path')
@click.option('--model', default='gemini-1.5-flash', help='Modello AI da utilizzare')
def analyze(file_path, model):
    """Analizza un file di codice"""
    try:
        agent = AgentCore(model_name=model)
        result = agent.analyze_file(file_path)
        
        if result.startswith("Errore"):
            click.echo(f"❌ {result}", err=True)
            sys.exit(1)
            
        click.echo(f"\n🔍 Analisi di {file_path}:")
        click.echo("=" * 50)
        click.echo(result)
        click.echo("=" * 50)
        
    except Exception as e:
        click.echo(f"❌ Errore: {str(e)}", err=True)
        sys.exit(1)

@main.command()
@click.argument('file_path')
@click.option('--model', default='gemini-1.5-flash', help='Modello AI da utilizzare')
def doc(file_path, model):
    """Genera documentazione per un file"""
    try:
        agent = AgentCore(model_name=model)
        result = agent.generate_documentation(file_path)
        
        if result.startswith("Errore"):
            click.echo(f"❌ {result}", err=True)
            sys.exit(1)
            
        click.echo(f"\n📚 Documentazione per {file_path}:")
        click.echo("=" * 50)
        click.echo(result)
        click.echo("=" * 50)
        
    except Exception as e:
        click.echo(f"❌ Errore: {str(e)}", err=True)
        sys.exit(1)

@main.command()
@click.argument('file_path')
@click.option('--model', default='gemini-1.5-flash', help='Modello AI da utilizzare')
def bugs(file_path, model):
    """Cerca bug in un file"""
    try:
        agent = AgentCore(model_name=model)
        result = agent.find_bugs(file_path)
        
        if result.startswith("Errore"):
            click.echo(f"❌ {result}", err=True)
            sys.exit(1)
            
        click.echo(f"\n🐛 Ricerca bug in {file_path}:")
        click.echo("=" * 50)
        click.echo(result)
        click.echo("=" * 50)
        
    except Exception as e:
        click.echo(f"❌ Errore: {str(e)}", err=True)
        sys.exit(1)

@main.command()
def init():
    """Inizializza devhelper nel progetto corrente"""
    env_file = Path('.env')
    
    if env_file.exists():
        click.echo("✅ File .env già presente")
    else:
        env_content = """# DevHelper Configuration
GOOGLE_API_KEY=your_google_api_key_here

# Aggiungi qui altre configurazioni se necessario
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        click.echo("✅ File .env creato! Ricordati di aggiungere la tua API key di Google.")
    
    click.echo("""
🚀 DevHelper inizializzato!

Comandi disponibili:
- devhelper ask "domanda"          # Fai una domanda generica
- devhelper list                   # Elenca file del progetto
- devhelper read file.py           # Leggi un file
- devhelper copy file.py           # Copia file negli appunti
- devhelper modify file.py "fix"   # Modifica un file
- devhelper analyze file.py        # Analizza un file
- devhelper doc file.py            # Genera documentazione
- devhelper bugs file.py           # Cerca bug

Per aiuto sui comandi: devhelper --help
""")

if __name__ == '__main__':
    main()