import socket
import string
import itertools

# IP e porta do servidor
HOST = "10.10.168.119"
PORT = 1337

# Flag conhecida (a usada para codificar)
known_flag = "THM{thisisafakeflag}"

def recv_until(sock, delimiter=b"\n"):
    data = b""
    while not data.endswith(delimiter):
        chunk = sock.recv(1)
        if not chunk:
            break
        data += chunk
    return data.decode()

def brute_force_key(xored_hex, flag):
    xored_bytes = bytes.fromhex(xored_hex)
    charset = string.ascii_letters + string.digits

    print("[*] Brute-forcing the key...")
    for candidate in itertools.product(charset, repeat=5):
        key = ''.join(candidate)
        decrypted = ''.join(
            chr(xored_bytes[i] ^ ord(key[i % len(key)])) for i in range(len(flag))
        )
        if decrypted == flag:
            print(f"[+] Found key: {key}")
            return key
    return None

def main():
    with socket.create_connection((HOST, PORT)) as sock:
        # Recebe primeira linha com a string codificada
        line1 = recv_until(sock)
        print("[SERVER]", line1.strip())

        # Extrai o hex codificado
        if "flag 1:" in line1:
            encoded_hex = line1.strip().split("flag 1:")[1].strip()
        else:
            print("[-] Não foi possível extrair o hex.")
            return

        # Recebe o prompt
        prompt = recv_until(sock)
        print("[SERVER]", prompt.strip())

        # Quebra a chave
        key = brute_force_key(encoded_hex, known_flag)

        if not key:
            print("[-] Chave não encontrada.")
            return

        # Envia a chave
        sock.sendall((key + "\n").encode())

        # Recebe resposta final
        while True:
            try:
                response = recv_until(sock)
                if not response:
                    break
                print("[SERVER]", response.strip())
            except:
                break

if __name__ == "__main__":
    main()
