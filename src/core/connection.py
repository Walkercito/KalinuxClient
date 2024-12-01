import socket
import threading


class TCPConnection:
    def __init__(self, host="0.0.0.0", port: int = 9876):
        self.host = host
        self.port = port
        self.client_socket = None
        self.server_socket = None
        self.connected_peers = {}

    def start_server(self):
        """Starts the server and listens for incoming connections"""
        def _server_thread():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                # Add these socket options to allow port reuse
                server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                server_socket.bind((self.host, self.port))
                server_socket.listen(5)
                print(f"Server listening on {self.host}:{self.port}")

                while True:
                    client_socket, client_address = server_socket.accept()
                    threading.Thread(target=self._handle_connection, 
                                  args=(client_socket, client_address),
                                  daemon=True).start()

        threading.Thread(target=_server_thread, daemon=True).start()
    
    
    def _handle_connection(self, client_socket):
        """ Handles the connection with the client """
        
        with client_socket:
            data = client_socket.recv(1024)
            if data:
                print(f"Received data: {data.decode('utf-8')}")

    
    def peer_to_peer(self, ip, port: int = 9876):
        """ Establishes a connection with a peer """

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((ip, port))
                client_socket.sendall(b"Hello, peer!")
                print(f"Connection  established with {ip}:{port}")

        except Exception as e:
            print(f"Error connecting: {e}")