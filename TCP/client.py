import socket
import threading
import os
import base64

# Nickname choosing
nickname = input("Choose your nickname: ")
defaultpath = "./tcp/"

# Client - Server connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.6", 55555))

# Client revceiving method
def receive():
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            if message == "NICK":
                client.send(nickname.encode("ascii"))
            else:
                print(message)
        except Exception as e:
            print("An error occurred!", e)
            client.close()
            break

# Client "interface" / message sending method
def write():
    print( # Choice menu
        "Commands:\n'/pm [nickname] [message]'\n'/sendtxt [nickname] [filename]'\n'/sendfile [nickname] [filename]'\n'/exit'"
    )
    while True:
        message = input("")
        # In the write() function
        if message.startswith("/sendfile"):
            _, recipient_nickname, filename = message.split(" ", 2)
            fullpath = os.path.join(defaultpath, filename)
            try:
                with open(fullpath, "rb") as file:
                    file_data = file.read()
                    encoded_data = base64.b64encode(file_data)
                    # First, send the command with the recipient and the filename
                    header = f"/sendfile {recipient_nickname} {filename}"
                    client.send(header.encode("ascii"))
                    client.send(b" ")  # Delimiter or a separate message
                    # Then, send the encoded file data followed by 'EOF'
                    client.send(encoded_data)
                    client.send(b"EOF")
            except FileNotFoundError:
                print("File not found. Please check the filename and try again.")
            except Exception as e:
                print(f"An error occurred: {e}")
        elif message.startswith("/sendtxt"):
            try:
                _, recipient_nickname, filename = message.split(" ", 2)
                fullpath = os.path.join(defaultpath, filename)
                with open(fullpath, "r") as file:
                    contents = file.read()
                file_message = f"/sendtxt {recipient_nickname} {contents}"
                client.send(file_message.encode("ascii"))
            except FileNotFoundError:
                print("File not found. Please check the filename and try again.")
            except Exception as e:
                print(f"An error occurred: {e}")
        elif message:
            client.send(message.encode("ascii"))

# Starting threads
receive_thread = threading.Thread(target=receive)
write_thread = threading.Thread(target=write)
receive_thread.start()
write_thread.start()
