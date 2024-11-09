import socket
import json
import xml.etree.ElementTree as ET
import yaml
import toml

def obter_mensagem():
    nome = input("Digite seu nome: ")
    cpf = input("Digite seu CPF: ")
    idade = input("Digite sua idade: ")
    mensagem = f"mensagem de teste de {nome}"
    return {
        "nome": nome,
        "cpf": cpf,
        "idade": idade,
        "mensagem": mensagem
    }

def serializar_mensagem(mensagem):
    print("\nSerializando mensagem em diferentes formatos...")
    serializado = {
        "json": json.dumps(mensagem),
        "csv": f"nome,cpf,idade,mensagem\n{mensagem['nome']},{mensagem['cpf']},{mensagem['idade']},{mensagem['mensagem']}",
        "xml": ET.tostring(ET.Element("root", {key: str(value) for key, value in mensagem.items()}), encoding='unicode'),
        "yaml": yaml.dump(mensagem),
        "toml": toml.dumps(mensagem)
    }
    print("Serialização completa.\n")
    return serializado

def main():
    print("Coletando informações do usuário...")
    mensagem = obter_mensagem()
    print("Informações do usuário coletadas.\n")
    
    mensagens_serializadas = serializar_mensagem(mensagem)
    
    print("Conectando ao servidor...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 65432))
        print("Conectado ao servidor.")
        s.sendall(json.dumps(mensagens_serializadas).encode('utf-8'))
        print("Dados enviados ao servidor.\n")

if __name__ == "__main__":
    main()