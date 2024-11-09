import socket
import json
import os

def salvar_em_arquivo(dados, formato):
    diretorio = "AP1"
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
    nome_arquivo = os.path.join(diretorio, f"mensagem.{formato}")
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.write(dados)
    print(f"Salvou dados no formato {formato} em {nome_arquivo}")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 65432))
        s.listen()
        print("Servidor está ouvindo na porta 65432...\n")
        conn, addr = s.accept()
        with conn:
            print(f"Conectado por {addr}")
            dados = conn.recv(1024)
            if not dados:
                print("Nenhum dado recebido.")
                return
            print("Dados recebidos do cliente.\n")
            recebidos = json.loads(dados.decode('utf-8'))
            
            for formato, mensagem in recebidos.items():
                print(f"Salvando dados no formato {formato}...")
                salvar_em_arquivo(mensagem, formato)
                print(f"Dados salvos no formato {formato}.\n")

if __name__ == "__main__":
    main()