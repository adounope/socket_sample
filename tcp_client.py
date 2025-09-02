import socket
import threading
import src.socket_tools as skt

# target_addr = ('192.168.86.187', 25567)
ip = input('enter target ip: ')
port = input('enter target port: ')
target_addr = (ip, int(port))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
skt.tcp_connect(client_socket, target_addr)

def send_action(client_socket):
    laddr, raddr = skt.addr_str(client_socket)
    return input(f'\nSend {laddr} -> {raddr}: ').encode()
def receive_action(client_socket, data):
    laddr, raddr = skt.addr_str(client_socket)
    print(f"\nReceived {laddr} <- {raddr}: {data.decode()}")

# Start threads for sending and receiving
receive_thread = threading.Thread(target=skt.tcp_receive, args=(client_socket, receive_action))
send_thread = threading.Thread(target=skt.tcp_send, args=(client_socket, send_action))
receive_thread.start()
send_thread.start()
receive_thread.join()
send_thread.join()

# Clean up
print('closing client socket')
client_socket.close()