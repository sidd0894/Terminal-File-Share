# Terminal File Share
This is a terminal based file sharing app where multiple users can connect to the server and send and receive files from server.

## About this Project
This Python project is made using `socket` module for sending and receiving data and `threading` module for managing multiple concurrent connections and ensuring that the server can handle communication with multiple clients simultaneously.

## How to run this project?
To run this follow the steps given below-
1. **Install python**: <br>
Get python from [python.org](https://www.python.org/downloads/) if you don't have it yet. This project is compatible with Python 3.x.

2. **Download or Clone the Repository**: <br>
Download the zip of this repository  from the green 'Code' button on top or you can clone this repository using the following command:
   ```
   git clone <repository-url>
   ```

3. **Navigate to the directory** where the repository is saved in your system, then go into the directory named `main` and open terminal in that directory.

4. Now run the command in the terminal accordingly:

    If you want to start a server:
    ```
    python server.py
    ```
    Or
    
    If you want to connect to a server as a client:
    ```
    python client.py
    ```
