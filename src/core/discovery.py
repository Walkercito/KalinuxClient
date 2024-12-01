import json
import uuid
import socket
import threading

from src.core.connection import TCPConnection


class Core:
    def __init__(self, port: int = 9876):
        self.peers = []
        self.port = port
        self.running = False
        self.deviceID = str(uuid.uuid4())
        self.device_name = socket.gethostname()  # Use hostname as device name
        self.tcp_connection = TCPConnection(port = port)
    

    def list_available_devices(self):
        """Returns list of discovered devices"""
        if not self.peers:
            return "No devices found"
        return "\n".join([f"{idx}. {peer['name']} ({peer['ip']})" 
                         for idx, peer in enumerate(self.peers, 1)])
    

    def connect_to_peer(self, peer_index):
        """Establish P2P connection with selected peer"""
        # todo: implement peer selection and connection logic
        pass
    

    def start_discovery(self):
        """ Starts the discovery process using an UDP <broadcast> """

        def descovery_broadcast():
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as handler:
                handler.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                handler.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                handler.settimeout(2)
                broadcast_message = json.dumps(
                    {
                        "type": "discovery",
                        "name": self.device_name,
                        "device_id": self.deviceID,
                    }
                )
                while self.running:
                    handler.sendto(broadcast_message.encode("utf-8"), ("<broadcast>", self.port))
                    
                    try:
                        data, addr = handler.recvfrom(1024)
                        self._handle_discovery_response(data, addr)

                    except socket.timeout:
                        continue

        self.running = True
        threading.Thread(target = descovery_broadcast, daemon = True).start()


    def _handle_discovery_response(self, data, addr):
        """Handles the discovery response."""
        
        try:
            message = json.loads(data.decode("utf-8"))
            if message["type"] == "discovery" and message["device_id"] != self.deviceID and addr[0] not in [peer["ip"] for peer in self.peers]:
                peer = {"name": message["name"], "ip": addr[0]}
                self.peers.append(peer)
                print(f"Discovered: {peer['name']} at {peer['ip']}")
        
        except Exception as e:
            print(f"Error handling discovery response: {e}")


    
    def send_discovery_response(self):
        """ Sends a discovery response with information about the device """

        def listen_for_broadcast():
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as handler:
                handler.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                handler.bind(("", self.port))

                while self.running:
                    data, addr = handler.recvfrom(1024)
                    
                    try:
                        message = json.loads(data.decode("utf-8"))
                        if message["type"] == "discovery" and message["device_id"] != self.deviceID:
                            response = json.dumps(
                                {
                                    "type": "discovery",
                                    "name": self.device_name,
                                    "device_id": self.deviceID
                                }
                            )
                            handler.sendto(response.encode("utf-8"), addr)

                    except Exception as e:
                        print(f"Error while handling discovery response: {e}")

        self.running = True
        threading.Thread(target = listen_for_broadcast, daemon = True).start()

    
    def stop(self):
        """ Stops all core's processes """

        self.running = False



if __name__ == "__main__":
    core = Core()
    core.send_discovery_response()
    core.start_discovery()

    try:
        while True:
            pass

    except KeyboardInterrupt:
        core.stop()
        print("Core stopped")