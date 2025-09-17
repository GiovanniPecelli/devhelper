from ai_agent.agent_core import AgentCore

class DevHelper:
    """Wrapper per l'interfaccia interattiva dell'agente"""
    
    def __init__(self, name="DevHelper", model_name="gemini-1.5-flash"):
        self.name = name
        self.agent = AgentCore(model_name=model_name)
    
    def process_request(self, request: str) -> str:
        """Elabora una richiesta generica (utile per importazioni esterne)"""
        return self.agent.ask(request)

def main():
    """Interfaccia interattiva da terminale"""
    try:
        agent = AgentCore()
        print("🤖 DevHelper avviato!")
        print("Comandi disponibili:")
        print("  list [depth]           - Lista file del progetto")
        print("  read <file>           - Leggi contenuto file")
        print("  modify <file>         - Modifica file con AI")
        print("  copy <file>           - Copia file negli appunti")
        print("  analyze <file>        - Analizza file")
        print("  doc <file>            - Genera documentazione")
        print("  bugs <file>           - Cerca bug")
        print("  ask <domanda>         - Fai una domanda")
        print("  help                  - Mostra questo aiuto")
        print("  quit/exit             - Esci")
        
    except Exception as e:
        print(f"❌ Errore nell'inizializzazione: {e}")
        print("Assicurati di avere un file .env con GOOGLE_API_KEY=...")
        return

    while True:
        try:
            command = input("\n>> ").strip()

            if command.lower() in ["quit", "exit", "q"]:
                print("👋 Arrivederci!")
                break
            
            elif command.lower() in ["help", "h", "?"]:
                print("\n📋 Comandi disponibili:")
                print("  list [depth]     - Lista file (es: 'list 2' per profondità 2)")
                print("  read file.py     - Leggi contenuto di un file")
                print("  modify file.py   - Modifica file con AI")
                print("  copy file.py     - Copia file negli appunti")
                print("  analyze file.py  - Analizza codice")
                print("  doc file.py      - Genera documentazione")
                print("  bugs file.py     - Cerca potenziali bug")
                print("  ask domanda      - Fai una domanda generica")
                print("  quit            - Esci dal programma")

            elif command.startswith("list"):
                parts = command.split()
                depth = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 1
                files = agent.list_project_files(max_depth=depth)
                if files:
                    print(f"📂 Lista dei file nel progetto (profondità: {depth}):")
                    for f in files:
                        print(f"  {f}")
                else:
                    print("📂 Nessun file trovato nel progetto.")

            elif command.startswith("read "):
                file_path = command.split(" ", 1)[1].strip()
                content = agent.read_file(file_path)
                if content.startswith("Errore"):
                    print(f"❌ {content}")
                else:
                    print(f"\n📄 Contenuto di {file_path}:")
                    print("=" * 50)
                    print(content)
                    print("=" * 50)

            elif command.startswith("modify "):
                file_path = command.split(" ", 1)[1].strip()
                if not agent.read_file(file_path) or agent.read_file(file_path).startswith("Errore"):
                    print(f"❌ File {file_path} non trovato o non leggibile.")
                    continue
                    
                instruction = input("📝 Istruzione per l'agente: ").strip()
                if not instruction:
                    print("❌ Istruzione vuota, operazione annullata.")
                    continue
                    
                # Conferma
                confirm = input(f"⚠️  Sei sicuro di voler modificare {file_path}? (s/N): ").strip().lower()
                if confirm not in ['s', 'si', 'y', 'yes']:
                    print("❌ Operazione annullata.")
                    continue
                    
                print("🔄 Elaborazione in corso...")
                risultato = agent.modify_file(file_path, instruction)
                if risultato.startswith("Errore"):
                    print(f"❌ {risultato}")
                else:
                    print(f"✅ {risultato}")

            elif command.startswith("copy "):
                file_path = command.split(" ", 1)[1].strip()
                result = agent.copy_file_to_clipboard(file_path)
                if result.startswith("Errore"):
                    print(f"❌ {result}")
                else:
                    print(f"📋 {result}")

            elif command.startswith("analyze "):
                file_path = command.split(" ", 1)[1].strip()
                print("🔍 Analisi in corso...")
                result = agent.analyze_file(file_path)
                if result.startswith("Errore"):
                    print(f"❌ {result}")
                else:
                    print(f"\n🔍 Analisi di {file_path}:")
                    print("=" * 50)
                    print(result)
                    print("=" * 50)

            elif command.startswith("doc "):
                file_path = command.split(" ", 1)[1].strip()
                print("📚 Generazione documentazione...")
                result = agent.generate_documentation(file_path)
                if result.startswith("Errore"):
                    print(f"❌ {result}")
                else:
                    print(f"\n📚 Documentazione per {file_path}:")
                    print("=" * 50)
                    print(result)
                    print("=" * 50)

            elif command.startswith("bugs "):
                file_path = command.split(" ", 1)[1].strip()
                print("🐛 Ricerca bug...")
                result = agent.find_bugs(file_path)
                if result.startswith("Errore"):
                    print(f"❌ {result}")
                else:
                    print(f"\n🐛 Ricerca bug in {file_path}:")
                    print("=" * 50)
                    print(result)
                    print("=" * 50)

            elif command.startswith("ask "):
                prompt = command.split(" ", 1)[1].strip()
                if not prompt:
                    print("❌ Domanda vuota.")
                    continue
                print("🤖 Elaborazione...")
                response = agent.ask(prompt)
                print(f"\n🤖 DevHelper risponde:")
                print("=" * 50)
                print(response)
                print("=" * 50)

            elif command.strip() == "":
                continue  # Ignora input vuoti

            else:
                print(f"❌ Comando '{command}' non riconosciuto.")
                print("💡 Digita 'help' per vedere i comandi disponibili.")

        except KeyboardInterrupt:
            print("\n\n👋 Arrivederci!")
            break
        except Exception as e:
            print(f"❌ Errore imprevisto: {e}")
            print("💡 Digita 'help' per vedere i comandi disponibili.")


if __name__ == "__main__":
    main()