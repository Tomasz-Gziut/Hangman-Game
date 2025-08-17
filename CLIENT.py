import socket
from PROTOCOL import IP, PORT, receive_data, send_data, colors

color = colors()

def client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IP, PORT))

        while True:
            try:
                response = receive_data(s)
                print(f"{color['magenta']}Server:{color['reset']} {response}")

                if response.startswith("Congratulations") or response.startswith("Wrong guess. You have no more attempts left."):
                    break

                guessed_input = input(f"{color['cyan']}Your guess: {color['reset']}")
                send_data(s, guessed_input)

            except socket.error:
                pass

        s.close()

client()
