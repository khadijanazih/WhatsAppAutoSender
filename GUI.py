import tkinter as tk
from tkinter import filedialog
import functions as func

selected_file_path = ""
data_array = []


def browse_file():
    global selected_file_path
    selected_file_path = filedialog.askopenfilename(title="Sélectionnez un fichier",filetypes=[("Fichiers Excel", "*.xlsx"), ("Tous les fichiers", "*.*")])
    filePath_lbl.config(text=f"Fichier sélectionné : {selected_file_path}" if selected_file_path else "Aucun fichier sélectionné")
    print(selected_file_path)


root = tk.Tk()
root.title("WhatsApp AutoSender")

root.geometry("500x300")
root.resizable(False, False)
# Configurer les colonnes pour qu'elles occupent tout l'espace disponible
root.grid_columnconfigure(0, weight=1)  # Colonne 0 occupe tout l'espace disponible

welcome_lbl = tk.Label(root, text="Bienvenue dans WhtatsApp AutoSender !")
welcome_lbl.grid(row=1, column=0, columnspan=5, pady=10, sticky="ew")

fileBrowse_lbl = tk.Label(root, text="Préciser le Chemin du fichier ")
fileBrowse_lbl.grid(row=2, column=0, pady=5, padx = 1, sticky="w")

browse_btn = tk.Button(root, text="Parcourir", command=browse_file,background="black", fg="white",borderwidth=0)
browse_btn.grid(row=2, column=1, pady=5, padx=2)

process_btn = tk.Button(root, text="Traiter le fichier", command=lambda: func.process_excel_file(selected_file_path),background="black", fg="white",borderwidth=0)
process_btn.grid(row=2, column=2, pady=5, padx=5)

send_btn = tk.Button(root, text="Envoyer", command=lambda: func.send_message(func.data_array), background="black", fg="white", borderwidth=0)
send_btn.grid(row=2, column=3, pady=5, padx=5)

filePath_lbl = tk.Label(root)
filePath_lbl.grid(row=3, column=0, pady=5, padx = 1)
root.mainloop()