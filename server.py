"""
P2P File Sharing - Central Server
Tracks connected clients and their file repositories
"""

import socket
import threading
import json
import time
from datetime import datetime


class P2PServer:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.clients = {}  # {hostname: {'ip': ip, 'port': port, 'files': [filenames], 'last_seen': timestamp}}
        self.lock = threading.Lock()
        self.running = False
        self.server_socket = None
        
    def start(self):
        """Start the server"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        
        print(f"[SERVER] Started on {self.host}:{self.port}")
        
        # Start accepting connections
        accept_thread = threading.Thread(target=self.accept_connections, daemon=True)
        accept_thread.start()
        
    def accept_connections(self):
        """Accept incoming client connections"""
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                print(f"[SERVER] New connection from {address}")
                
                # Handle client in a new thread
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address),
                    daemon=True
                )
                client_thread.start()
            except Exception as e:
                if self.running:
                    print(f"[SERVER] Error accepting connection: {e}")
                    
    def handle_client(self, client_socket, address):
        """Handle client requests"""
        try:
            while self.running:
                data = client_socket.recv(4096).decode('utf-8')
                if not data:
                    break
                    
                try:
                    request = json.loads(data)
                    command = request.get('command')
                    
                    if command == 'register':
                        response = self.handle_register(request)
                    elif command == 'publish':
                        response = self.handle_publish(request)
                    elif command == 'fetch':
                        response = self.handle_fetch(request)
                    elif command == 'discover':
                        response = self.handle_discover(request)
                    elif command == 'ping':
                        response = self.handle_ping(request)
                    else:
                        response = {'status': 'error', 'message': 'Unknown command'}
                        
                    client_socket.send(json.dumps(response).encode('utf-8'))
                    
                except json.JSONDecodeError:
                    error_response = {'status': 'error', 'message': 'Invalid JSON'}
                    client_socket.send(json.dumps(error_response).encode('utf-8'))
                    
        except Exception as e:
            print(f"[SERVER] Error handling client {address}: {e}")
        finally:
            client_socket.close()
            
    def handle_register(self, request):
        """Register a new client"""
        hostname = request.get('hostname')
        ip = request.get('ip')
        port = request.get('port')
        
        with self.lock:
            self.clients[hostname] = {
                'ip': ip,
                'port': port,
                'files': [],
                'last_seen': time.time()
            }
            
        print(f"[SERVER] Registered client: {hostname} ({ip}:{port})")
        return {'status': 'success', 'message': 'Client registered'}
        
    def handle_publish(self, request):
        """Handle file publish from client"""
        hostname = request.get('hostname')
        filename = request.get('filename')
        
        with self.lock:
            if hostname not in self.clients:
                return {'status': 'error', 'message': 'Client not registered'}
                
            if filename not in self.clients[hostname]['files']:
                self.clients[hostname]['files'].append(filename)
                self.clients[hostname]['last_seen'] = time.time()
                
        print(f"[SERVER] {hostname} published: {filename}")
        return {'status': 'success', 'message': f'File {filename} published'}
        
    def handle_fetch(self, request):
        """Handle fetch request - return list of clients with the file"""
        filename = request.get('filename')
        requesting_hostname = request.get('hostname')
        
        peers = []
        with self.lock:
            for hostname, info in self.clients.items():
                if filename in info['files'] and hostname != requesting_hostname:
                    peers.append({
                        'hostname': hostname,
                        'ip': info['ip'],
                        'port': info['port']
                    })
                    
        if peers:
            print(f"[SERVER] Found {len(peers)} peer(s) with file: {filename}")
            return {'status': 'success', 'peers': peers}
        else:
            return {'status': 'error', 'message': f'No peers found with file: {filename}'}
            
    def handle_discover(self, request):
        """Discover files from a specific hostname"""
        hostname = request.get('hostname')
        
        with self.lock:
            if hostname in self.clients:
                files = self.clients[hostname]['files']
                return {
                    'status': 'success',
                    'hostname': hostname,
                    'files': files
                }
            else:
                return {'status': 'error', 'message': f'Host {hostname} not found'}
                
    def handle_ping(self, request):
        """Check if a host is alive"""
        hostname = request.get('hostname')
        
        with self.lock:
            if hostname in self.clients:
                last_seen = self.clients[hostname]['last_seen']
                current_time = time.time()
                time_diff = current_time - last_seen
                
                # Consider alive if seen in last 60 seconds
                is_alive = time_diff < 60
                
                return {
                    'status': 'success',
                    'hostname': hostname,
                    'alive': is_alive,
                    'last_seen': datetime.fromtimestamp(last_seen).strftime('%Y-%m-%d %H:%M:%S')
                }
            else:
                return {'status': 'error', 'message': f'Host {hostname} not found'}
                
    def stop(self):
        """Stop the server"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("[SERVER] Stopped")
        
    def get_client_list(self):
        """Get list of connected clients"""
        with self.lock:
            return dict(self.clients)


def main():
    server = P2PServer(host='0.0.0.0', port=5000)
    server.start()
    
    print("\nServer Commands:")
    print("  discover <hostname> - Discover files from a host")
    print("  ping <hostname> - Check if a host is alive")
    print("  list - List all connected clients")
    print("  quit - Stop the server")
    
    try:
        while True:
            command = input("\nServer> ").strip()
            
            if not command:
                continue
                
            parts = command.split(maxsplit=1)
            cmd = parts[0].lower()
            
            if cmd == 'quit':
                break
            elif cmd == 'list':
                clients = server.get_client_list()
                if clients:
                    print("\nConnected Clients:")
                    for hostname, info in clients.items():
                        print(f"  {hostname} ({info['ip']}:{info['port']}) - {len(info['files'])} files")
                else:
                    print("No clients connected")
            elif cmd == 'discover' and len(parts) > 1:
                hostname = parts[1]
                result = server.handle_discover({'hostname': hostname})
                if result['status'] == 'success':
                    print(f"\nFiles on {hostname}:")
                    for f in result['files']:
                        print(f"  - {f}")
                else:
                    print(f"Error: {result['message']}")
            elif cmd == 'ping' and len(parts) > 1:
                hostname = parts[1]
                result = server.handle_ping({'hostname': hostname})
                if result['status'] == 'success':
                    status = "ALIVE" if result['alive'] else "DEAD"
                    print(f"{hostname} is {status} (last seen: {result['last_seen']})")
                else:
                    print(f"Error: {result['message']}")
            else:
                print("Unknown command")
                
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down...")
    finally:
        server.stop()


if __name__ == '__main__':
    main()
