#PROTOCOL
IP = 'localhost'
PORT = 59847

def receive_data(socket):
    data = b''
    while b'\r\n\r\n' not in data:
        data += socket.recv(1)

    return data.decode()


def send_data(socket, message):
    message += '\r\n\r\n'
    socket.sendall(message.encode())

def colors():
    colors = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'reset': '\033[0m'
    }
    return colors
