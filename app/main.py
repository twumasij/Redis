import socket  # noqa: F401
import threading


def process_data(data):
    data_list = data.strip().split("\r\n")
    length , *data_list = data_list
    length = length[1:]
    length = "".join(length)
    data_list = data_list[1::2]


    # Cheching is the command is echo 

    if data_list[0].lower() == "echo":
        data_list = data_list[1:]

    data_list = " ".join(data_list)


  
    
    return length, data_list



def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage

    response = "+PONG\r\n"
    
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    print("Server started waiting for connections...")

    while True:
        conn , addr =  server_socket.accept() # wait for client

        print(f"accepted connection - {addr[0]}:{str(addr[1])}")
        # connect(conn, response)
        thread = threading.Thread(target = connect, args = [conn , response])
        thread.start()

        

def connect(conn: socket.socket, response: str) -> None:
    with conn:
        while True:
            try:
                data = conn.recv(1024).decode()
                if not data:  # Client closed the connection
                    break
               
                print(f"received - {data.encode()}")

                print(data.split())
                print(process_data(data))


                if data.upper() == "*1\r\n$4\r\nPING\r\n":
                        response = "+PONG\r\n"
                else:
                    _,response = process_data(data)
                    response = "+" + response + "\r\n"
                
                
                print(f"responding with - {response}")

                conn.send(response.encode())
            except (ConnectionResetError, BrokenPipeError):
                # Handle disconnection or broken pipe errors
                print("Client disconnected or connection error")
                break

if __name__ == "__main__":
    main()
