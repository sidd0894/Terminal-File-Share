import os
import socket

SERVER = input('Enter server address: ')
while True:
    try:
        PORT = int(input('Port number: '))
        break
    except:
        print('Invalid port number.')

ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
download_dir = 'Downloads'
upload_dir = 'Uploads'

def start_client():

    # Downloding files from server
    if (down_up_opt == 1):

        # Create a folder if not present already to keep downloaded files separately
        if not os.path.exists(download_dir):
            os.mkdir(download_dir)

        client.send('download'.encode(FORMAT))
        files_string = client.recv(2048).decode(FORMAT)

        # If no files present at server
        if (files_string == 'Server empty'):
            print('No files present at server.')

        else:
            # Convert received string of files present on server to list and print the file names
            files_list = files_string.split('\n')
            print('\n'+files_string)
            
            while True:
                try:
                    # Take user input of which file to request on server
                    file_opt = int(input('Enter file number you want to download: '))

                    if (file_opt > 0 and file_opt < len(files_list)):
                        # Send the file number to server
                        client.send(f'{file_opt}'.encode(FORMAT))
                        break
                    else:
                        print('No file present there.')
                except:
                    print('Invalid input')

            # Receive file from server
            try:
                with open(f'{download_dir}/{(files_list[file_opt-1]).split(' ')[1]}', 'wb') as f:
                    print('Downloading file...')
                    while True:
                        # Receive data in chunks
                        chunk = client.recv(1024)
                        if not chunk:
                            break
                        f.write(chunk)

                    print('File downloaded successfully.')
            except Exception as e:
                print(f'[ERROR] Error occured while downloading file from server: {e}')


    # Uploading a file to server
    elif (down_up_opt == 2):

        # Create a folder if not present already to upload files from there
        if not os.path.exists(upload_dir):
            os.mkdir(upload_dir)

        # Get filename from user
        while True:
            filename = (input('Enter filename with extension: ')).strip()
            if (filename != '' and len(filename.split('.'))>1):
                client.send(f'upload {filename}'.encode(FORMAT))
                break
            else:
                print('Invalid file name')

        # Send the file to server
        try:
            with open(f'{upload_dir}/{filename}', 'rb') as f:
                # Send data in chunks
                chunk = f.read(1024)
                while chunk:
                    client.sendall(chunk)
                    chunk = f.read(1024)

        except Exception as e:
            print(f'[ERROR] Error occured while sending file at server: {e}')
            # Receive error message if error occured at server
            server_msg = client.recv(1024).decode(FORMAT)
            print(server_msg)


    # Close the connection from server
    client.close()


print('\nNOTE - For uploading files, first create an \'Uploads\' folder in the same directory and then upload files from there.\n')
# Get input from the user for the task to perform
while True:
    try:
        print('1- Download\n'+ '2- Upload\n'+ '3- exit')
        down_up_opt = int(input('Choose option (1/2/3): '))
        break
    except:
        print('Invalid input.')

if (down_up_opt != 3):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDRESS)
    start_client()

else:
    pass