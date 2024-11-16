import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage

    pong = "+PONG\r\n"
    
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    conn , addr =  server_socket.accept() # wait for client

    with conn:
        conn.recv(1024)
        conn.send(pong.encode())
    


if __name__ == "__main__":
    main()
