import socket
import threading


def handle_client_connection(views_socket):
    try:
        data = views_socket.recv(1024)
        if not data:
            return

        received_data = data.decode("utf-8")
        print(f"Received data: {received_data}")

        # Processing and validation logic for received_data (if needed)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.connect(("localhost", 2738))
            server_socket.send(received_data.encode("utf-8"))

            acknowledgment = server_socket.recv(1024)
            print(f"Server Acknowledgment: {acknowledgment.decode('utf-8')}")

        views_socket.send(acknowledgment)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        views_socket.close()


def start_listener():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener_socket:
        listener_socket.bind(("localhost", 2847))
        listener_socket.listen(1)
        print("Client is listening for connections...")

        while True:
            try:
                views_socket, views_address = listener_socket.accept()
                print(f"Accepted connection from {views_address}")
                threading.Thread(
                    target=handle_client_connection, args=(views_socket,)
                ).start()
            except Exception as e:
                print(f"An error occurred: {e}")
                break


if __name__ == "__main__":
    start_listener()
