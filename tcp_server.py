import socket
import threading
import src.socket_tools as skt

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
port = 25567
listen_addr = ('0.0.0.0', port)
server_socket.bind(listen_addr) # claim local ip and port
server_socket.listen(1)          # set socket as listening mode
print(f"Server listening on {listen_addr[0]}:{listen_addr[1]}")


client_sockets = []
addresses = []
receive_threads = []

# Accept client connection
def accept_action(client_socket):
    # client_socket.settimeout(300) #allow 5 minutes
    receive_thread = threading.Thread(target=
        receive, args=(client_socket,)
    )
    addr = skt.addr_str(client_socket)
    client_sockets.append(client_socket)
    receive_threads.append(receive_thread)
    addresses.append(addr)
    receive_thread.start() # receive -> tcp_recieve # inf loop

def receive(client_socket):
    laddr, raddr = skt.addr_str(client_socket)
    def action(client_socket, data):
        print(f"\nReceived {laddr} <- {raddr}: {data.decode()}")
    skt.tcp_receive(client_socket, action, 1024) # inf loop
    # cleanup
    socket_idx = client_sockets.index(client_socket)
    client_socket.close()
    client_sockets.pop(socket_idx)
    receive_threads.pop(socket_idx)
    addresses.pop(socket_idx)

def command():
    while True:
        str = input('\nls, rm <num>, term,  num: ')
        if str == 'ls':
            for idx, address in enumerate(addresses):
                laddr, raddr = address
                print(f'{idx}, {laddr} --- {raddr}')
        if str[:2] == 'rm': # remove a connection
            str = str[3:]
            if not str.isnumeric():
                continue
            idx = int(str)
            client_sockets[idx].shutdown(socket.SHUT_RDWR)
            client_sockets[idx].close()
        elif str == 'term':
            break
        elif str.isnumeric():
            idx = int(str)
            if idx < 0 or idx >= len(client_sockets):
                continue
            laddr, raddr = skt.addr_str(client_sockets[idx])
            message = input(f'\nSend {laddr} -> {raddr}: ')
            try:
                client_sockets[idx].sendall(message.encode())
            except Exception as e:
                print(f"Error sending: {e}")

# Start threads for sending and receiving
command_thread = threading.Thread(target=command) # inf loop
accept_thread = threading.Thread(target=skt.tcp_accept, args=(server_socket, accept_action)) # inf loop
command_thread.start()
accept_thread.start()

# Wait for threads to finish
command_thread.join()
# Clean up
# server_socket.shutdown(socket.SHUT_RDWR)
server_socket.close()
print('//////self dummy connection')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # make a dummy self connect to unblock socket.accept()
    s.connect(('localhost', port))
for client_socket in client_sockets:
    client_socket.shutdown(socket.SHUT_RDWR)
    client_socket.close()
accept_thread.join()
for receive_thread in receive_threads:
    receive_thread.join()