from agent_core import Agent, list_project_files, read_file, copy_file_to_clipboard

agent = Agent("DevHelper")

print("🤖 Agente DevHelper avviato!")
print("Comandi disponibili: list, read [file], modify [file], copy [file], ask [domanda], quit")

while True:
    command = input("\n>> ").strip()
    
    if command.lower() in ["quit", "exit"]:
        print("👋 Arrivederci!")
        break

    elif command == "list":
        files = list_project_files()
        print("📂 Lista dei file nel progetto:")
        for f in files:
            print(f"  {f}")

    elif command.startswith("read "):
        file_path = command.split(" ", 1)[1]
        print(read_file(file_path))

    elif command.startswith("modify "):
        file_path = command.split(" ", 1)[1]
        instruction = input("📝 Istruzione per l'agente: ")
        try:
            risultato = agent.modify_file(file_path, instruction)
            print(risultato)
        except Exception as e:
            print("Errore:", e)

    elif command.startswith("copy "):
        file_path = command.split(" ", 1)[1]
        print(copy_file_to_clipboard(file_path))

    elif command.startswith("ask "):
        prompt = command.split(" ", 1)[1]
        print(agent.ask(prompt))

    else:
        print("Comando non riconosciuto. Prova: list, read, modify, copy, ask, quit")