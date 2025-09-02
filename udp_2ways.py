import socket
import src.socket_tools as skt
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind(('0.0.0.0', 25567)) #ip:port (self) to listen
# note: binding does not work in WSL (port will be translated by windows)

target_addr = ("192.168.86.187", 25567) # ip: port (external) to send
rtaddr_str = skt.addr_format(target_addr)

def receive_action(data, addr):
    raddr_str = skt.addr_format(addr)
    print(f'\nrecieved from {raddr_str}: {data.decode()}')
    #sock.sendto(f'message received: {data.decode()}'.encode(), addr)
def message_source():
    return input(f'\nsend to {rtaddr_str}: ').encode()

receive_thread = threading.Thread(target=
    skt.udp_recieve, args=(sock, 1024, receive_action)
)
send_thread = threading.Thread(target=
    skt.udp_send, args=(sock, target_addr, message_source)
)
send_thread.start()
receive_thread.start()
send_thread.join()
receive_thread.join()
sock.close()