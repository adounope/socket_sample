import socket

# return socket address in format of 192.168.1.1:22
def addr_format(addr):
    return f'{addr[0]}:{addr[1]}'
def addr_str(socket):
    laddr = addr_format(socket.getsockname())
    raddr = addr_format(socket.getpeername())
    return laddr, raddr

# Function to receive messages
def tcp_receive(client_socket, action, len=1024):
    _, raddr = addr_str(client_socket)
    while True:
        try:
            data = client_socket.recv(len)
            if not data:
                print(f"Disconnected from {raddr}")
                break
            action(client_socket, data)
        except Exception as e:
            print(f"Error receiving from {raddr}: {e}")
            break

# Function to send messages
def tcp_send(client_socket, action):
    _, raddr = addr_str(client_socket)
    while True:
        try:
            message = action(client_socket)
            client_socket.sendall(message)
        except Exception as e:
            print(f"Error sending to {raddr}: {e}")
            break

def tcp_accept(server_socket, action):
    while True:
        try:
            # print('waiting to accept connections')
            client_socket, _ = server_socket.accept()
            _, raddr = addr_str(client_socket)
            print(f"Accepted connection from {raddr}")
            action(client_socket)
        except Exception as e:
            #intended for a self connection to unblock accept()
            print(f'Exception at tcp_accept: {e}')
            break

def tcp_connect(client_socket, target_addr):
    raddr = f'{target_addr[0]}:{target_addr[1]}'
    try:
        print('trying connect')
        client_socket.connect(target_addr)
        laddr, raddr  = addr_str(client_socket)
        print(f"Connected {laddr} to {raddr}")
    except Exception as e:
        print(f"Connection to {raddr} failed: {e}")
        exit()

def udp_recieve(sock, len: int, action = lambda data, addr: print(f'recieved from{addr}\n{data}')):
    while True:
        data, addr = sock.recvfrom(len)
        action(data, addr)
def udp_send(sock, addr, message_src = lambda: input()):
    while True:
        message = message_src()
        sock.sendto(message, addr)