import csv
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

def luhn_check(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    checksum = 0
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10 == 0

def load_bin_info(file_path):
    bin_info = {}
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            formatted_row = {
                'bin': row.get('bin', 'Unknown BIN'),
                'bank': row.get('bank', 'Unknown Bank'),
                'country': row.get('country', 'Unknown Country'),
                'type': row.get('type', 'Unknown Type'),
                'level': row.get('level', 'Unknown Level')
            }
            bin_number = formatted_row['bin']
            bin_info[bin_number] = {
                "bank": formatted_row['bank'],
                "country": formatted_row['country'],
                "type": formatted_row['type'],
                "level": formatted_row['level']
            }
    return bin_info

def get_bin_info(card_number, bin_info):
    bin_number = card_number[:6]
    return bin_info.get(bin_number, "Unknown BIN")

def check_card():
    card_number = card_number_entry.get()
    expiration_date = expiration_date_entry.get()
    cvv = cvv_entry.get()
    
    if not (card_number and expiration_date and cvv):
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return
    
    if not luhn_check(card_number):
        messagebox.showerror("Invalid Card", "The card number is invalid.")
        return
    
    # Vérification de la date d'expiration
    current_date = datetime.now()
    try:
        expiration_date_dt = datetime.strptime(expiration_date, "%m/%y")
    except ValueError:
        messagebox.showerror("Invalid Expiration Date", "Please enter expiration date in MM/YY format.")
        return
    
    if expiration_date_dt < current_date:
        messagebox.showerror("Expired Card", "La carte a expiré.")
        return
    
    bin_information = get_bin_info(card_number, bin_info)
    risk = calculate_risk(bin_information)
    
    info_message = (f"Numéro de Carte: {card_number}\n"
                    f"Date d'Expiration: {expiration_date_dt.strftime('%m/%y')}\n"
                    f"CVV: {cvv}\n\n"
                    f"Information BIN: {bin_information}\n\n"
                    f"RISK: {risk}")
    
    messagebox.showinfo("Card Info", info_message)

def calculate_risk(bin_info):
    if bin_info == "Unknown BIN":
        return "Unknown RISK"
    
    level = bin_info['level'].upper()
    if level == "PLATINUM":
        return "75%"
    elif level == "TITANIUM":
        return "80%"
    elif level == "BUSINESS":
        return "50%"
    elif level == "CLASSIC":
        return "15%"
    elif level == "GOLD":
        return "30%"
    else:
        return "Unknown RISK"

# Charger les informations du BIN depuis le fichier CSV
bin_info = load_bin_info('C:/Users/TRIPLEMONSTRE/Downloads/1337/TOOLS/BINCHECKER/bin_info.csv')

# Création de la fenêtre principale
root = tk.Tk()
root.title("Credit Card Checker by zEus")
root.geometry("400x200")  # Définir la taille de la fenêtre

# Création des champs de saisie et des étiquettes
tk.Label(root, text="Numéro de Carte", font=("Trebuchet MS", 14)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
tk.Label(root, text="Date d'expiration (MM/YY)", font=("Helvetica", 14)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
tk.Label(root, text="CVV", font=("Helvetica", 14)).grid(row=2, column=0, padx=10, pady=10, sticky="e")

card_number_entry = tk.Entry(root, font=("Helvetica", 14))
expiration_date_entry = tk.Entry(root, font=("Helvetica", 14))
cvv_entry = tk.Entry(root, font=("Helvetica", 14))

card_number_entry.grid(row=0, column=1, padx=10, pady=10)
expiration_date_entry.grid(row=1, column=1, padx=10, pady=10)
cvv_entry.grid(row=2, column=1, padx=10, pady=10)

# Bouton de vérification
tk.Button(root, text='Check Card', command=check_card, font=("Helvetica", 14)).grid(row=3, columnspan=2, pady=10)

# Lancement de la boucle principale
root.mainloop()
