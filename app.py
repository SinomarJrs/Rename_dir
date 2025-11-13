import os
import unicodedata

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

if __name__ == "__main__":
    pasta = input("Digite o caminho da pasta: ").strip()
    corrigir_nomes(pasta)
    print("✅ Renomeação concluída!")