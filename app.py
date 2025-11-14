import os
import sys
import unicodedata
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk, filedialog, messagebox, PhotoImage

def resource_path(relative_path):
    try:
        base_path = sys.__MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Renomear:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Renomear Automático")
        self.window.geometry("600x200")
        self.style = ttk.Style()
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
    
        try:
            icon_path = resource_path('Image/renomear.png')
            if os.path.exists(icon_path):
                icon_image = PhotoImage(file=icon_path)
                self.window.iconphoto(True, icon_image)
                self.icon_image = icon_image
            else:
                print(f"Arquivo de ícone não encontrado em: {icon_path}")
        except Exception as e:
            print(f"Erro ao carregar ícone: {e}")

        title_Label = ttk.Label(self.window, text="Renomear Arquvios/ Diretórios", style='Header.TLabel')
        title_Label.pack(pady=(10, 5))

        main_frame = ttk.Frame(self.window)
        main_frame.pack(padx=1, pady=1, fill='both', expand=False)

        config_frame = ttk.LabelFrame(main_frame, text="Informe o caminho da pasta:")
        config_frame.pack(fill="x", padx=1, pady=1)

        ttk.Label(config_frame, text="Pasta:").grid(row=1, column=0, padx=5, pady=5)
        self.input_folder_var = tk.StringVar()
        ttk.Entry(config_frame, textvariable=self.input_folder_var, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(config_frame, text="Escolher", command=self.choose_input_folder).grid(row=1, column=2, padx=5, pady=5)

    def get_base_folder(self):
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.abspath(__file__))

    def choose_input_folder(self):
        folder = filedialog.askdirectory(initialdir=self.input_folder_var.get())
        if folder:
            self.input_folder_var.set(folder)
    

def normalizar_nome(nome: str) -> str:
    # Remover acentuação
    nfkd = unicodedata.normalize('NFKD', nome)
    nome_sem_acento = "".join([c for c in nfkd if not unicodedata.combining(c)])
    
    # Substituir cedilha
    nome_sem_acento = nome_sem_acento.replace("ç", "c").replace("Ç", "C")
    
    # Substitui vírgulas por .
    nome_sem_acento = nome_sem_acento.replace(",", ".")
    
    # Remover caracteres 
    caracteres_remover = [";", ":", "?", "!", "´", "`", "\"", "'", "“", "”", "°", "@", "&", "%", "$", "*", "#", "+", "/", "|"]
    for ch in caracteres_remover:
        nome_sem_acento = nome_sem_acento.replace(ch, "")
    
    #Troca o hífen por vazio
    nome_sem_acento = nome_sem_acento.replace("-", "")

    # Troca espaços por underline (opcional)
    nome_sem_acento = nome_sem_acento.replace(" ", "_")
    
    return nome_sem_acento

def corrigir_nomes(diretorio: str):
    for raiz, pastas, arquivos in os.walk(diretorio, topdown=False):
        # Renomear arquivos
        for arquivo in arquivos:
            caminho_antigo = os.path.join(raiz, arquivo)
            novo_nome = normalizar_nome(arquivo)
            caminho_novo = os.path.join(raiz, novo_nome)
            
            if caminho_antigo != caminho_novo:
                print(f"Arquivo: {arquivo} -> {novo_nome}")
                os.rename(caminho_antigo, caminho_novo)

        for pasta in pastas:
            caminho_antigo = os.path.join(raiz, pasta)
            novo_nome = normalizar_nome(pasta)
            caminho_novo = os.path.join(raiz, novo_nome)

            if caminho_antigo != caminho_novo:
                print(f"Pasta: {pasta} -> {novo_nome}")
                os.rename(caminho_antigo, caminho_novo)

# if __name__ == "__main__":
#     pasta = input("Digite o caminho da pasta: ").strip()
#     corrigir_nomes(pasta)
#     print("✅ Renomeação concluída!")

if __name__ == "__main__":
    app = Renomear()
    app.window.mainloop()