import os
import socket
import threading

HOSTNAME = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDRESS = (HOSTNAME, PORT)
FORMAT = 'utf-8'
dir_name = 'server_files'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)


def handle_client(conn, addr):
    files_list = []
    
    data = conn.recv(1024).decode(FORMAT)

    # Sending files to client
    if (data == 'download'):
        # Get the names of all the files from folder
        try:
            files_list = os.listdir(dir_name)
        except:
            print('[ERROR] Error occured getting files list')

        if (len(files_list) != 0):

            # Write the names of all those files in a single string format and send it to client
            try:
                files_string = ''
                for i, file in enumerate(files_list, start=1):
                    files_string += f'{i}. {file}\n'
                conn.send(files_string.encode(FORMAT))
            except:
                print('[ERROR] Error occured while sending files list to client')

            # Get the client requested file content and send it to client
            file_opt = int(conn.recv(1024).decode(FORMAT))-1
            print(f'{addr[0]} requested {files_list[file_opt]}')
            try:
                with open(f'{dir_name}/{files_list[file_opt]}', 'rb') as f:
                    # Send data in chunks
                    chunk = f.read(1024)
                    while chunk:
                        conn.sendall(chunk)
                        chunk = f.read(1024)
            except:
                print('[ERROR] Error occured while sending file to client')

        else:
            conn.send('Server empty'.encode(FORMAT))

    # Receiving files from client
    elif (data.split(' ')[0] == 'upload'):
        filename = data.split(' ')[1]
        
        try:
            with open(f'{dir_name}/{filename}', 'wb') as f:
                while True:
                    # Receive data in chunks
                    chunk = conn.recv(1024)
                    if not chunk:
                        break
                    f.write(chunk)

            print(f'{filename} received from client {addr[0]}.')

        except:
            print(f'[ERROR] Error occured while receiving file from client {addr[0]}')
            # Send error message to client if any error occurs while saving file at server
            conn.send('[SERVER ERROR] Error occured while saving file at server'.encode(FORMAT))

    # Close the client connection
    conn.close()
        

def start_server():
    server.listen()
    print(f'Server started at {HOSTNAME}:{PORT}...')

    # Create a directory to store files
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    while True:
        try:
            conn, addr = server.accept()
            print(f'New client connected {addr}')

            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
        except Exception as e:
            print(f'[ERROR] Error connecting client {addr}: {e}')


if __name__ == '__main__':
    try:
        start_server()
    except KeyboardInterrupt:
        server.close()
        print('Server closed.')