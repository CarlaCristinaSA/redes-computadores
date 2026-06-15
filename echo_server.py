import socket

HOST = '0.0.0.0'
PORT = 12345
CHAR_ENCERRAMENTO = '#'


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"[SERVIDOR] Escutando em {HOST}:{PORT}")
        print("[SERVIDOR] Aguardando conexão do cliente...")
        conn, addr = server_socket.accept()
        print(f"[SERVIDOR] Conexão estabelecida com {addr}")
        
        with conn:
            while True:
                dados = conn.recv(1)
                if not dados:
                    print("[SERVIDOR] Cliente desconectou.")
                    break
                caractere = dados.decode('utf-8', errors='replace')
                print(f"[SERVIDOR] Caractere recebido: '{caractere}'")
                conn.sendall(dados)
                if caractere == CHAR_ENCERRAMENTO:
                    print("[SERVIDOR] Caractere de encerramento recebido. "
                        "Fechando conexão.")
                    break
        print("[SERVIDOR] Conexão encerrada.")


if __name__ == "__main__":
    main()
