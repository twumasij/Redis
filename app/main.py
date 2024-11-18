import socket  # noqa: F401
import threading


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


        
# def connect(conn : socket.socket, response) -> None:
#     with conn:
#         connected: bool = True
#         while conn:
#             data = conn.recv(1024).decode()
#             match data:
#                 case "*1\r\n$4\r\nPING\r\n":
#                     response = "+PONG\r\n"

#             # print(f"received - {data}")
#             # print(f"responding with - {response}")
#             conn.send(response.encode())
        

def connect(conn: socket.socket, response: str) -> None:
    with conn:
        while True:
            try:
                data = conn.recv(1024).decode()
                if not data:  # Client closed the connection
                    break

                match data:
                    case "*1\r\n$4\r\nPING\r\n":
                        response = "+PONG\r\n"
                
                print(f"received - {data.encode()}")
                print(f"responding with - {response}")

                conn.send(response.encode())
            except (ConnectionResetError, BrokenPipeError):
                # Handle disconnection or broken pipe errors
                print("Client disconnected or connection error")
                break

if __name__ == "__main__":
    main()
