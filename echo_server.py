"""
Servidor TCP de Eco (Echo Server)
----------------------------------
Recebe um caractere por vez do cliente, exibe na saída padrão
e retransmite o mesmo caractere de volta ao cliente.

Encerra a conexão quando recebe o caractere especial '#'.

Uso:
    python3 echo_server.py
"""

import socket

HOST = '0.0.0.0'   # Escuta em todas as interfaces de rede da máquina
PORT = 12345       # Porta TCP utilizada pela aplicação
CHAR_ENCERRAMENTO = '#'  # Caractere especial que finaliza a conexão


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Permite reutilizar o endereço/porta rapidamente após reiniciar o programa
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_socket.bind((HOST, PORT))
        server_socket.listen(1)

        print(f"[SERVIDOR] Escutando em {HOST}:{PORT}")
        print("[SERVIDOR] Aguardando conexão do cliente...")

        conn, addr = server_socket.accept()
        print(f"[SERVIDOR] Conexão estabelecida com {addr}")

        with conn:
            while True:
                dados = conn.recv(1)  # lê 1 byte por vez

                if not dados:
                    # Cliente fechou a conexão sem enviar o caractere especial
                    print("[SERVIDOR] Cliente desconectou.")
                    break

                caractere = dados.decode('utf-8', errors='replace')
                print(f"[SERVIDOR] Caractere recebido: '{caractere}'")

                # Retransmite (eco) o mesmo caractere ao cliente
                conn.sendall(dados)

                if caractere == CHAR_ENCERRAMENTO:
                    print("[SERVIDOR] Caractere de encerramento recebido. "
                        "Fechando conexão.")
                    break

        print("[SERVIDOR] Conexão encerrada.")


if __name__ == "__main__":
    main()
