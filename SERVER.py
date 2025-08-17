import socket
import random
from PROTOCOL import IP, PORT, receive_data, send_data, colors

color = colors()

def read_words_from_file(file_path):
    with open(file_path, 'r') as file:
        words = file.read().upper().splitlines()
    return words

def play_game(client):
    words = read_words_from_file('Word_List.txt')
    random_word = random.choice(words)

    guessed_word = ['_' if letter.isalpha() else letter for letter in random_word]

    attempts = int(len(random_word) * 1.5)

    send_data(client, f"The word is {' '.join(guessed_word)}. Try to guess the word. You have {attempts} attempts")

    guessed_letters = []
    incorrect_letters = []

    while True:
        try:
            guessed_input = receive_data(client)
            print(f"\n{color['cyan']}Client guess:{color['reset']} {guessed_input}")

            if guessed_input.strip().lower() == 'pass':
                send_data(client, f"{color['black']}The word was{color['reset']} {random_word}")
                print(f"{color['black']}The word was{color['reset']} {random_word}")
                break

            guessed_input = guessed_input.upper()
            random_word = random_word.upper()

            guessed_input = guessed_input.replace(' ', '').replace('-', '')

            if not guessed_input.strip():
                send_data(client, "Try again.")
                print("Try again.")
                continue

            if guessed_input.strip() == random_word.replace(' ', '').replace('-', ''):
                guessed_word = list(random_word)
                send_data(client, f"{color['yellow']}Congratulations! You guessed it correctly. The word is {color['reset']}{random_word}{color['yellow']}.{color['reset']}")
                print(f"{color['yellow']}Congratulations! Client guessed it correctly. The word is {color['reset']}{random_word}{color['yellow']}.{color['reset']}")
                break

            guessed_letter = guessed_input.strip().lower()
            if guessed_letter in guessed_letters or guessed_letter in incorrect_letters:
                send_data(client, "You have already guessed that letter. Try again.")
                print("Client already guessed that letter. Try again.")
                continue

            if guessed_letter in random_word.lower() and guessed_letter not in [letter.lower() for letter in guessed_word]:
                guessed_word = [letter if letter.lower() == guessed_letter else guessed_word[i] for i, letter in enumerate(random_word)]

                if '_' not in guessed_word:
                    send_data(client,f"{color['yellow']}Congratulations! You guessed it correctly. The word is {color['reset']}{random_word}{color['yellow']}.{color['reset']}")
                    print(f"{color['yellow']}Congratulations! You guessed it correctly. The word is {color['reset']}{random_word}{color['yellow']}.{color['reset']}")
                    break
                else:
                    guessed_letters.append(guessed_letter)
                    send_data(client, f"{color['green']}Correct guess! The word: {color['reset']}{' '.join(guessed_word)}")
                    print(f"{color['green']}Correct guess! The word: {color['reset']}{' '.join(guessed_word)}")
            else:
                attempts -= 1
                if attempts == 0:
                    send_data(client, f"{color['red']}Wrong guess. You have no more attempts left. The word was {color['reset']}{random_word}{color['red']}.{color['reset']}")
                    print(f"{color['red']}Wrong guess. You have no more attempts left. The word was {color['reset']}{random_word}{color['red']}.{color['reset']}")
                    break
                else:
                    incorrect_letters.append(guessed_letter)
                    if attempts == 1:
                        send_data(client, f"{color['red']}Wrong guess. You have {color['reset']}{attempts}{color['red']} attempt left. The word: {color['reset']}{' '.join(guessed_word)}")
                        print(f"{color['red']}Wrong guess. You have {color['reset']}{attempts}{color['red']} attempt left. The word: {color['reset']}{' '.join(guessed_word)}")
                    else:
                        send_data(client, f"{color['red']}Wrong guess. You have {color['reset']}{attempts}{color['red']} attempts left. The word: {color['reset']}{' '.join(guessed_word)}")
                        print(f"{color['red']}Wrong guess. You have {color['reset']}{attempts}{color['red']} attempts left. The word: {color['reset']}{' '.join(guessed_word)}")

            print("\n--------------------------------------")
            print(f"{color['green']}Guessed Letters: {color['reset']}{', '.join(guessed_letters)}\n{color['red']}Incorrect Letters: {color['reset']}{', '.join(incorrect_letters)}\n{color['yellow']}Remaining Attempts: {color['reset']}{attempts}")
            print("--------------------------------------\n")
            print("===============================================================================================")

            bot_guess, guessed_word = bot_guess_random_letter(random_word, guessed_word, guessed_letters)
            guessed_letters.append(bot_guess)

            if '_' not in guessed_word:
                send_data(client, f"{color['yellow']}Congratulations! The word is {color['reset']}{random_word}{color['yellow']}.{color['reset']}")
                print(f"{color['yellow']}Congratulations! The word is {color['reset']}{random_word}{color['yellow']}.{color['reset']}")
                break
            else:
                send_data(client, f"{color['green']}Bot guessed: {color['reset']}{bot_guess}\n{color['green']}The word: {color['reset']}{' '.join(guessed_word)}")
                print(f"{color['green']}Bot guessed: {color['reset']}{bot_guess}\n{color['green']}The word: {color['reset']}{' '.join(guessed_word)}")
                send_data(client, f"{color['green']}Bot guessed: {color['reset']}{bot_guess}\n{color['green']}The word: {color['reset']}{' '.join(guessed_word)}")
                print(f"{color['green']}Bot guessed: {color['reset']}{bot_guess}\n{color['green']}The word: {color['reset']}{' '.join(guessed_word)}")

        except socket.error:
            pass

    client.close()

def bot_guess_random_letter(random_word, guessed_word, guessed_letters):
    bot_guess = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    for i, letter in enumerate(random_word):
        if letter.lower() == bot_guess.lower():
            guessed_word[i] = letter

    return bot_guess, guessed_word

def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((IP, PORT))
        s.listen(5)

        client, addr = s.accept()
        print("===============================================================================================")
        print(f"{color['blue']}CONNECTED WITH {addr[0]}{color['reset']}")
        print("===============================================================================================")

        words = read_words_from_file('Word_List.txt')
        random_word = random.choice(words)

        guessed_word = ['_' if letter.isalpha() else letter for letter in random_word]

        attempts = int(len(random_word) * 1.5)

        send_data(client, f"The word is {' '.join(guessed_word)}. Try to guess the word. You have {attempts} attempts")

        guessed_letters = []
        incorrect_letters = []

        while True:
            try:
                guessed_input = receive_data(client)
                print(f"\n{color['cyan']}Client guess:{color['reset']} {guessed_input}")

                if guessed_input.strip().lower() == 'pass':
                    send_data(client, f"{color['black']}The word was{color['reset']} {random_word}")
                    print(f"{color['black']}The word was{color['reset']} {random_word}")
                    break

                guessed_input = guessed_input.upper()
                random_word = random_word.upper()

                guessed_input = guessed_input.replace(' ', '').replace('-', '')

                if not guessed_input.strip():
                    send_data(client, "Try again.")
                    print("Try again.")
                    continue

                bot_guess, guessed_word = bot_guess_random_letter(random_word, guessed_word, guessed_letters)
                guessed_letters.append(bot_guess)

                if guessed_input.strip() == random_word.replace(' ', '').replace('-', ''):
                    guessed_word = list(random_word)
                    send_data(client, f"{color['yellow']}Congratulations! You guessed it correctly. The word is {color['reset']}{random_word}{color['yellow']}.{color['reset']}")
                    print(f"{color['yellow']}Congratulations! Client guessed it correctly. The word is {color['reset']}{random_word}{color['yellow']}.{color['reset']}")
                    break

                guessed_letter = guessed_input.strip().lower()
                if guessed_letter in guessed_letters or guessed_letter in incorrect_letters:
                    send_data(client, "You have already guessed that letter. Try again.")
                    print("Client already guessed that letter. Try again.")
                    continue

                if guessed_letter in random_word.lower() and guessed_letter not in [letter.lower() for letter in guessed_word]:
                    guessed_word = [letter if letter.lower() == guessed_letter else guessed_word[i] for i, letter in enumerate(random_word)]

                    if '_' not in guessed_word:
                        send_data(client,f"{color['yellow']}Congratulations! You guessed it correctly. The word is {color['reset']}{random_word}{color['yellow']}.{color['reset']}")
                        print(f"{color['yellow']}Congratulations! You guessed it correctly. The word is {color['reset']}{random_word}{color['yellow']}.{color['reset']}")
                        break
                    else:
                        guessed_letters.append(guessed_letter)
                        send_data(client, f"{color['green']}Correct guess! The word: {color['reset']}{' '.join(guessed_word)}")
                        print(f"{color['green']}Correct guess! The word: {color['reset']}{' '.join(guessed_word)}")
                else:
                    attempts -= 1
                    if attempts == 0:
                        send_data(client, f"{color['red']}Wrong guess. You have no more attempts left. The word was {color['reset']}{random_word}{color['red']}.{color['reset']}")
                        print(f"{color['red']}Wrong guess. You have no more attempts left. The word was {color['reset']}{random_word}{color['red']}.{color['reset']}")
                        break
                    else:
                        incorrect_letters.append(guessed_letter)
                        if attempts == 1:
                            send_data(client, f"{color['red']}Wrong guess. You have {color['reset']}{attempts}{color['red']} attempt left. The word: {color['reset']}{' '.join(guessed_word)}")
                            print(f"{color['red']}Wrong guess. You have {color['reset']}{attempts}{color['red']} attempt left. The word: {color['reset']}{' '.join(guessed_word)}")
                        else:
                            send_data(client, f"{color['red']}Wrong guess. You have {color['reset']}{attempts}{color['red']} attempts left. The word: {color['reset']}{' '.join(guessed_word)}")
                            print(f"{color['red']}Wrong guess. You have {color['reset']}{attempts}{color['red']} attempts left. The word: {color['reset']}{' '.join(guessed_word)}")

                print("\n--------------------------------------")
                print(f"{color['green']}Guessed Letters: {color['reset']}{', '.join(guessed_letters)}\n{color['red']}Incorrect Letters: {color['reset']}{', '.join(incorrect_letters)}\n{color['yellow']}Remaining Attempts: {color['reset']}{attempts}")
                print("--------------------------------------\n")
                print("===============================================================================================")

                if '_' not in guessed_word:
                    send_data(client,
                              f"{color['yellow']}Congratulations! The word is {color['reset']}{random_word}{color['yellow']}.{color['reset']}")
                    print(
                        f"{color['yellow']}Congratulations! The word is {color['reset']}{random_word}{color['yellow']}.{color['reset']}")
                    break
                else:
                    send_data(client,
                              f"{color['green']}Bot guessed: {color['reset']}{bot_guess}\n{color['green']}The word: {color['reset']}{' '.join(guessed_word)}")
                    print(
                        f"{color['green']}Bot guessed: {color['reset']}{bot_guess}\n{color['green']}The word: {color['reset']}{' '.join(guessed_word)}")
            except socket.error:
                pass

        client.close()

server()
