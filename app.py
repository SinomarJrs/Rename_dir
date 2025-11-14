import os
import sys
import unicodedata
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, PhotoImage

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Renomear:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Rename App")
        self.window.geometry("470x150")
        self.window.resizable(False,False)
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

        title_Label = ttk.Label(self.window, text="Renomear Arquivos/Diretórios", style='Header.TLabel')
        title_Label.pack(pady=(10, 5))

        main_frame = ttk.Frame(self.window)
        main_frame.pack(padx=1, pady=1, fill='both', expand=False)

        config_frame = ttk.LabelFrame(main_frame, text="Informe o caminho da pasta:")
        config_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(config_frame, text="Pasta:").grid(row=1, column=0, padx=5, pady=5)
        self.input_folder_var = tk.StringVar()
        ttk.Entry(config_frame, textvariable=self.input_folder_var, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(config_frame, text="Escolher", command=self.choose_input_folder).grid(row=1, column=2, padx=5, pady=5)

        renomear_button = ttk.Button(main_frame, text="Corrigir Nomes", command=lambda: self.renomear_all())
        renomear_button.pack(padx=5, pady=5)
    
    def get_base_folder(self):
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.abspath(__file__))

    def choose_input_folder(self):
        folder = filedialog.askdirectory(initialdir=self.input_folder_var.get())
        if folder:
            self.input_folder_var.set(folder)

    def renomear_all(self):
        diretorio = self.input_folder_var.get()
        if not os.path.isdir(diretorio):
            messagebox.showerror("Erro", "O caminho informado não é um diretório válido.")
            return
        
        novo_diretorio = corrigir_nomes(diretorio)
        
        if novo_diretorio != diretorio:
             self.input_folder_var.set(novo_diretorio)


def normalizar_nome(nome: str) -> str:
    # Remove acentuação e corrige caracteres
    nfkd = unicodedata.normalize('NFKD', nome)
    nome_sem_acento = "".join([c for c in nfkd if not unicodedata.combining(c)])
    nome_sem_acento = nome_sem_acento.replace("ç", "c").replace("Ç", "C")
    nome_sem_acento = nome_sem_acento.replace(",", ".")
    nome_sem_acento = nome_sem_acento.replace(" ", "_")
    nome_sem_acento = nome_sem_acento.replace("__", "_")
    nome_sem_acento = nome_sem_acento.replace("_-_", "-")   
    caracteres_remover = [";", ":", "?", "!", "´", "`", "\"", "'", "“", "”", "°", "@", "&", "%", "$", "*", "#", "+", "/", "|"]
    for ch in caracteres_remover:
        nome_sem_acento = nome_sem_acento.replace(ch, "-")
    
    return nome_sem_acento

def corrigir_nomes(diretorio: str) -> str:
    renomeado = False
    erros = []
    
    for raiz, pastas, arquivos in os.walk(diretorio, topdown=False):
        #Renomear Arquivos
        for arquivo in arquivos:
            caminho_antigo = os.path.join(raiz, arquivo)
            novo_nome = normalizar_nome(arquivo)
            caminho_novo = os.path.join(raiz, novo_nome)
            
            if caminho_antigo != caminho_novo:
                print(f"Arquivo: {arquivo} -> {novo_nome}")
                try:
                    os.rename(caminho_antigo, caminho_novo)
                    renomeado = True
                except Exception as e:
                    print(f"Erro ao renomear arquivo {arquivo}: {e}")
                    erros.append(f"Arquivo: {arquivo}\nCaminho: {caminho_antigo}\nErro: {str(e)}\n")

        # Renomear Subdiretórios
        for pasta in pastas:
            caminho_antigo = os.path.join(raiz, pasta)
            novo_nome = normalizar_nome(pasta)
            caminho_novo = os.path.join(raiz, novo_nome)

            if caminho_antigo != caminho_novo:
                print(f"Pasta: {pasta} -> {novo_nome}")
                try:
                    os.rename(caminho_antigo, caminho_novo)
                    renomeado = True
                except Exception as e:
                    print(f"Erro ao renomear pasta {pasta}: {e}")
                    erros.append(f"Diretório: {pasta}\nCaminho: {caminho_antigo}\nErro: {str(e)}\n")

    # Renomear Diretório
    pasta_raiz = os.path.dirname(diretorio)
    nome_antigo = os.path.basename(diretorio)
    novo_nome = normalizar_nome(nome_antigo)
    caminho_antigo = diretorio
    caminho_novo = os.path.join(pasta_raiz, novo_nome)
    
    final_path = caminho_antigo

    if caminho_antigo != caminho_novo:
        print(f"Diretório Raiz: {nome_antigo} -> {novo_nome}")
        if not os.path.exists(caminho_novo):
            try:
                os.rename(caminho_antigo, caminho_novo)
                renomeado = True
                final_path = caminho_novo
            except Exception as e:
                print(f"Erro ao renomear diretório raiz {nome_antigo}: {e}")
                erros.append(f"Diretório Raiz: {nome_antigo}\nCaminho: {caminho_antigo}\nErro: {str(e)}\n")
        else:
             print(f"Aviso: O novo nome do diretório '{novo_nome}' já existe. Ignorando renomeação do diretório raiz.")

    # Gerar arquivo de erros
    if erros:
        arquivo_erros = os.path.join(final_path, "Log-Erros_renomeacao.txt")
        try:
            with open(arquivo_erros, "w", encoding="utf-8") as f:
                f.write("ERROS NA RENOMEAÇÃO DE ARQUIVOS E DIRETÓRIOS\n")
                f.write("=" * 50 + "\n\n")
                for erro in erros:
                    f.write(erro)
                    f.write("-" * 50 + "\n")
            print(f"Arquivo de erros gerado: {arquivo_erros}")
            messagebox.showwarning("Processo Concluído com Erros!", 
                                 f"A correção dos nomes foi finalizada.\n"
                                 f"Verifique o arquivo 'Log-Erros_renomeacao.txt' para detalhes.")
        except Exception as e:
            print(f"Erro ao gerar arquivo de erros: {e}")
            messagebox.showerror("Erro", f"Erro ao gerar arquivo de erros: {e}")
    elif renomeado:
        messagebox.showinfo("Processo Concluído!", "A correção dos nomes foi finalizada com sucesso ✅")
    else:
        messagebox.showinfo("Processo Concluído ✅", "Os arquivos, subdiretórios e direórios já estavam nomeados corretamente")
        
    return final_path

if __name__ == "__main__":
    app = Renomear()
    app.window.mainloop()