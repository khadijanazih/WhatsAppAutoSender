import tkinter as tk
from tkinter import filedialog
import  pandas as pd
import functions

selected_file_path = ""
data_array = []

def browse_file():
    global selected_file_path

    selected_file_path = filedialog.askopenfilename(title="Sélectionnez un fichier",filetypes=[("Fichiers Excel", "*.xlsx"), ("Tous les fichiers", "*.*")])
    if selected_file_path:filePath_lbl.config(text=f"Fichier sélectionné : {selected_file_path}")
    print(selected_file_path)
def process_excel_file(file_path):
    if file_path == '':
        filePath_lbl.config(text=f"Aucun fichier Selectionné!")
        return

    global data_array
    new_data = []

    df = pd.read_excel(file_path, engine='openpyxl')


    for index, row in df.iterrows():
        print(f"Traitement de la ligne {index}: {row.to_dict()}")

        appellation = row["Appellation"]
        nom = row["Nom"]
        prenom = row["Prénom"]
        montant = f"{row["Montant"]:,.2f}".replace(",", " ").replace(".", ",")
        echeance = row["Echéance"].strftime("%d/%m/%Y")
        envoye = row["Envoyé"]
        tel = f"+{row["Tél"]}"
        if envoye == "x":
            print(f"Ligne ignorée : {row.to_dict()}")
            continue

        lien = functions.get_file_download_url(f'images/{tel}.jpg')
        if lien is None:
            print(f"Ligne ignorée : {row.to_dict()}")
            continue

        else:
            df.at[index, 'Envoyé'] = 'x'
            df.to_excel(file_path, index=False)
            #build  & store customer_message & customer_tel
            customer_message = f"Bonjour {appellation} {nom} {prenom}, Vous êtes redevable à l'office de *{montant} DHs*, échu le *{echeance}*.\n\n Veuillez consulter le lien suivant: \n *{lien}* \n\n Salutations.\n\n\n Centrale de Recouvrement Bancaire - CEREB"
            customer_tel = tel
            print(customer_message)
            #append customer data to 2d array
            new_data.append((customer_tel, customer_message))

    data_array.extend(new_data)
    print(len(data_array))
    return data_array


root = tk.Tk()
root.title("WhatsApp AutoSender")

root.geometry("500x300")
root.resizable(False, False)
# Configurer les colonnes pour qu'elles occupent tout l'espace disponible
root.grid_columnconfigure(0, weight=1)  # Colonne 0 occupe tout l'espace disponible

welcome_lbl = tk.Label(root, text="Bienvenue dans WhtatsApp AutoSender !")
welcome_lbl.grid(row=1, column=0, columnspan=5, pady=10, sticky="ew")

fileBrowse_lbl = tk.Label(root, text="Préciser le Chemain du fichier ")
fileBrowse_lbl.grid(row=2, column=0, pady=5, padx = 1, sticky="w")

browse_btn = tk.Button(root, text="Parcourir", command=browse_file,background="black", fg="white",borderwidth=0)
browse_btn.grid(row=2, column=1, pady=5, padx=2)

process_btn = tk.Button(root, text="Traiter le fichier", command=lambda: process_excel_file(selected_file_path),background="black", fg="white",borderwidth=0)
process_btn.grid(row=2, column=2, pady=5, padx=5)

send_btn = tk.Button(root, text="Envoyer", command=lambda:functions.sendmsgs(data_array), background="black", fg="white",borderwidth=0)
send_btn.grid(row=2, column=3, pady=5, padx=5)

filePath_lbl = tk.Label(root)
filePath_lbl.grid(row=3, column=0, pady=5, padx = 1)
root.mainloop()