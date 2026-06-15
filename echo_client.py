
"""Cliente TCP de Eco (Echo Client)
----------------------------------
Envia um caractere por vez ao servidor, recebe o caractere
retransmitido (eco) e o exibe na saída padrão.

Encerra a conexão quando o usuário digita o caractere especial '#'.

Uso:
    python3 echo_client.py"""

import socket

# IMPORTANTE: altere para o endereço IP da máquina onde o
# servidor (echo_server.py) está em execução.
SERVER_HOST = '10.10.237.195.'
SERVER_PORT = 12345
CHAR_ENCERRAMENTO = '#'


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        print(f"[CLIENTE] Conectando a {SERVER_HOST}:{SERVER_PORT}...")
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("[CLIENTE] Conexão estabelecida com o servidor.")
        print(f"[CLIENTE] Digite caracteres para enviar. "
                f"Digite '{CHAR_ENCERRAMENTO}' para encerrar.\n")

        while True:
            entrada = input("Digite um caractere: ")

            if len(entrada) != 1:
                print("Por favor, digite exatamente um caractere.")
                continue

            client_socket.sendall(entrada.encode('utf-8'))

            dados = client_socket.recv(1)
            if not dados:
                print("[CLIENTE] Servidor encerrou a conexão.")
                break

            recebido = dados.decode('utf-8', errors='replace')
            print(f"[CLIENTE] Eco recebido do servidor: '{recebido}'")

            if entrada == CHAR_ENCERRAMENTO:
                print("[CLIENTE] Encerrando conexão.")
                break

        print("[CLIENTE] Conexão encerrada.")


if __name__ == "__main__":
    main()
