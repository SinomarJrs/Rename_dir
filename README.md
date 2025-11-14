# Rename App

- Programa para renomear de forma automática arquivos ou diretórios 

    O Rename App, irá passar em todos os arquivos e todas as pastas do local informado renomeando os arqivos de acordo com as regras definidas.
    Para os arquivos que não forem alterados, será gerado um arquivo.txt informando o o motivo, nome do arquivo e local para que seja redefinido manualmente.

### Executável ###

- Para gerar o executável, utilizar o comando:
D:/Projetos/Rename_dir/.venv/Scripts/pyinstaller.exe --onefile --windowed --name "Rename App" --icon "Image/icon.ico" --add-data "Image;Image" app.py