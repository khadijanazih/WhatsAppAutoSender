from tkinter import messagebox
import time
import setup

import pywhatkit
import pyautogui
import pandas as pd

#global var
data_array = []
#global funcs
def show_error(title, message):
    messagebox.showinfo(title,message)

#app funcs
def get_file_download_url(file_name):
    extension =''
    if(setup._FIREBASE_DIR_ == 'images'):
        extension = 'jpg'
    else:
        if (setup._FIREBASE_DIR_ == 'files'):
            extension = 'pdf'
    blob = setup.bucket.blob(f'{setup._FIREBASE_DIR_}/{file_name}.{extension}')  # Access the specified file
    try:
        download_url = blob.public_url
        return download_url
    except Exception as e:
        print(f"An error occurred: {e}")


def process_excel_file(file_path):
    if file_path == '':
        show_error("Attention", "Aucun Fichier Selectionné")
        return
    global data_array
    new_data = []
    df = pd.read_excel(file_path, engine='openpyxl')

    for index, row in df.iterrows():
        print(f"Traitement de la ligne {index}: {row.to_dict()}")

        appellation = row["Appellation"]
        nom = row["Nom"]
        prenom = row["Prénom"]
        creance = f"{row["Montant"]:,.2f}".replace(",", " ").replace(".", ",")
        echeance = row["Echéance"].strftime("%d/%m/%Y")
        type_creance = row["Type de Créance"]
        envoye = row["Envoyé"]
        tel = f"+{row["Tél"]}"
        if envoye == "x":
            print(f"Ligne ignorée : {row.to_dict()}")
            continue
        lien = get_file_download_url(f'{tel}')

        if lien is None:
            print(f"Ligne ignorée : {row.to_dict()}")
            continue

        else:
            df.at[index, 'Envoyé'] = 'x'
            df.to_excel(file_path, index=False)
            #build  & store customer_message & customer_tel
            customer_message = build_message(appellation, nom, prenom, creance, type_creance, echeance, lien)
            customer_tel = tel
            #append customer data to 2d array
            new_data.append((customer_tel, customer_message))

    data_array.extend(new_data)
    print(len(data_array))
    return data_array

def build_message(appellation, nom, prenom, creance, type_creance, echeance, lien, signature='Centrale de Recouvrement Bancaire - CEREB'):
    message = f"Bonjour, {appellation} {nom} {prenom}, vous êtes redevable à l'ONEE - BE d'un montant de: *{creance}* Dhs de {type_creance}, échu le : *{echeance}* \n Veuillez consulter le lien suivant pour plus de détails: \n {lien}\n \n Salutations.\n\n\n {signature}"
    messagebox.showinfo("Message WhatsApp", message)
    return message

def send_message (message_array):
    for tel,message in message_array:
        print(tel)
        pywhatkit.sendwhatmsg_instantly(tel, message,10,True)
        time.sleep(8)
        pyautogui.press('enter')

