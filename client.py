"""
P2P File Sharing - Client with Command-Line Interface
"""

import socket
import threading
import json
import os
import shutil
from pathlib import Path


class P2PClient:
    def __init__(self, hostname, server_host='127.0.0.1', server_port=5000, client_port=6000):
        self.hostname = hostname
        self.server_host = server_host
        self.server_port = server_port
        self.client_port = client_port
        self.repository_path = Path(f"client_repo_{hostname}")
        self.repository_path.mkdir(exist_ok=True)
        
        self.running = False
        self.peer_server_socket = None
        
    def connect_to_server(self):
        """Connect to central server and register"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.server_host, self.server_port))
            
            # Register with server
            register_request = {
                'command': 'register',
                'hostname': self.hostname,
                'ip': '127.0.0.1',
                'port': self.client_port
            }
            
            sock.send(json.dumps(register_request).encode('utf-8'))
            response = json.loads(sock.recv(4096).decode('utf-8'))
            sock.close()
            
            return response['status'] == 'success', response.get('message', 'Unknown error')
        except Exception as e:
            return False, str(e)
            
    def start_peer_server(self):
        """Start server to handle incoming file requests from peers"""
        try:
            self.peer_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.peer_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.peer_server_socket.bind(('0.0.0.0', self.client_port))
            self.peer_server_socket.listen(5)
            self.running = True
            
            accept_thread = threading.Thread(target=self.accept_peer_connections, daemon=True)
            accept_thread.start()
            
            print(f"[CLIENT] Peer server started on port {self.client_port}")
        except Exception as e:
            print(f"[ERROR] Failed to start peer server: {e}")
            return False
        return True
        
    def accept_peer_connections(self):
        """Accept connections from other peers"""
        while self.running:
            try:
                peer_socket, address = self.peer_server_socket.accept()
                print(f"[CLIENT] Incoming connection from {address}")
                thread = threading.Thread(
                    target=self.handle_peer_request,
                    args=(peer_socket,),
                    daemon=True
                )
                thread.start()
            except Exception as e:
                if self.running:
                    print(f"[ERROR] Error accepting peer connection: {e}")
                    
    def handle_peer_request(self, peer_socket):
        """Handle file download request from peer"""
        try:
            data = peer_socket.recv(4096).decode('utf-8')
            request = json.loads(data)
            
            if request['command'] == 'download':
                filename = request['filename']
                filepath = self.repository_path / filename
                
                if filepath.exists():
                    # Send file
                    with open(filepath, 'rb') as f:
                        file_data = f.read()
                        
                    response = {
                        'status': 'success',
                        'filename': filename,
                        'size': len(file_data)
                    }
                    peer_socket.send(json.dumps(response).encode('utf-8'))
                    peer_socket.recv(1024)  # Wait for acknowledgment
                    
                    # Send file data
                    peer_socket.sendall(file_data)
                    print(f"[CLIENT] Sent file '{filename}' to peer")
                else:
                    response = {'status': 'error', 'message': 'File not found'}
                    peer_socket.send(json.dumps(response).encode('utf-8'))
                    
        except Exception as e:
            print(f"[ERROR] Error handling peer request: {e}")
        finally:
            peer_socket.close()
            
    def publish(self, local_path, filename):
        """Publish a file to the repository"""
        try:
            # Check if local file exists
            if not os.path.exists(local_path):
                return False, f"Local file not found: {local_path}"
            
            # Copy file to repository
            dest_path = self.repository_path / filename
            shutil.copy2(local_path, dest_path)
            print(f"[CLIENT] Copied '{local_path}' to repository as '{filename}'")
            
            # Notify server
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.server_host, self.server_port))
            
            request = {
                'command': 'publish',
                'hostname': self.hostname,
                'filename': filename
            }
            
            sock.send(json.dumps(request).encode('utf-8'))
            response = json.loads(sock.recv(4096).decode('utf-8'))
            sock.close()
            
            if response['status'] == 'success':
                print(f"[CLIENT] Published '{filename}' to server")
                return True, "File published successfully"
            else:
                return False, response.get('message', 'Unknown error')
                
        except Exception as e:
            return False, str(e)
            
    def fetch(self, filename):
        """Fetch a file from a peer"""
        try:
            print(f"[CLIENT] Fetching '{filename}'...")
            
            # Ask server for peers with the file
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.server_host, self.server_port))
            
            request = {
                'command': 'fetch',
                'hostname': self.hostname,
                'filename': filename
            }
            
            sock.send(json.dumps(request).encode('utf-8'))
            response = json.loads(sock.recv(4096).decode('utf-8'))
            sock.close()
            
            if response['status'] != 'success':
                return False, response.get('message', 'Unknown error')
                
            peers = response['peers']
            if not peers:
                return False, 'No peers found with the file'
                
            print(f"[CLIENT] Found {len(peers)} peer(s) with the file:")
            for i, peer in enumerate(peers, 1):
                print(f"  {i}. {peer['hostname']} ({peer['ip']}:{peer['port']})")
            
            # Try to download from first peer
            peer = peers[0]
            print(f"[CLIENT] Downloading from {peer['hostname']}...")
            success, message = self.download_from_peer(peer, filename)
            
            if success:
                # Publish the downloaded file
                local_path = str(self.repository_path / filename)
                self.publish(local_path, filename)
                print(f"[CLIENT] Successfully fetched '{filename}'")
                
            return success, message
            
        except Exception as e:
            return False, str(e)
            
    def download_from_peer(self, peer, filename):
        """Download a file from a specific peer"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((peer['ip'], peer['port']))
            
            request = {
                'command': 'download',
                'filename': filename
            }
            
            sock.send(json.dumps(request).encode('utf-8'))
            response = json.loads(sock.recv(4096).decode('utf-8'))
            
            if response['status'] != 'success':
                sock.close()
                return False, response.get('message', 'Unknown error')
                
            # Send acknowledgment
            sock.send(b'OK')
            
            # Receive file data
            file_size = response['size']
            file_data = b''
            
            while len(file_data) < file_size:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                file_data += chunk
                
            sock.close()
            
            # Save file
            filepath = self.repository_path / filename
            with open(filepath, 'wb') as f:
                f.write(file_data)
                
            return True, f'File downloaded from {peer["hostname"]}'
            
        except Exception as e:
            return False, str(e)
            
    def list_repository_files(self):
        """List files in the local repository"""
        files = [f.name for f in self.repository_path.iterdir() if f.is_file()]
        return files
        
    def stop(self):
        """Stop the peer server"""
        self.running = False
        if self.peer_server_socket:
            self.peer_server_socket.close()


def main():
    print("=" * 60)
    print("P2P File Sharing - Client")
    print("=" * 60)
    
    # Get client configuration
    hostname = input("Enter your hostname: ").strip()
    if not hostname:
        print("Error: Hostname is required")
        return
        
    server_host = input("Enter server address (default: 127.0.0.1): ").strip() or "127.0.0.1"
    server_port = input("Enter server port (default: 5000): ").strip() or "5000"
    client_port = input("Enter your client port (default: 6000): ").strip() or "6000"
    
    try:
        server_port = int(server_port)
        client_port = int(client_port)
    except ValueError:
        print("Error: Ports must be numbers")
        return
    
    # Create client
    client = P2PClient(hostname, server_host, server_port, client_port)
    
    # Start peer server
    if not client.start_peer_server():
        print("Failed to start peer server. Exiting.")
        return
    
    # Connect to central server
    print(f"\n[CLIENT] Connecting to server at {server_host}:{server_port}...")
    success, message = client.connect_to_server()
    
    if success:
        print(f"[CLIENT] Connected successfully: {message}")
    else:
        print(f"[ERROR] Connection failed: {message}")
        return
    
    # Command shell
    print("\n" + "=" * 60)
    print("Client Commands:")
    print("  publish <lname> <fname> - Publish a local file to repository")
    print("  fetch <fname>           - Fetch a file from peers")
    print("  list                    - List files in local repository")
    print("  quit                    - Exit client")
    print("=" * 60)
    
    try:
        while True:
            command = input(f"\n{hostname}> ").strip()
            
            if not command:
                continue
                
            parts = command.split()
            cmd = parts[0].lower()
            
            if cmd == 'quit':
                print("[CLIENT] Shutting down...")
                break
                
            elif cmd == 'publish':
                if len(parts) < 3:
                    print("Usage: publish <lname> <fname>")
                    print("  lname - local file path")
                    print("  fname - name to publish as")
                else:
                    lname = parts[1]
                    fname = parts[2]
                    success, message = client.publish(lname, fname)
                    if not success:
                        print(f"[ERROR] {message}")
                        
            elif cmd == 'fetch':
                if len(parts) < 2:
                    print("Usage: fetch <fname>")
                else:
                    fname = parts[1]
                    success, message = client.fetch(fname)
                    if not success:
                        print(f"[ERROR] {message}")
                        
            elif cmd == 'list':
                files = client.list_repository_files()
                if files:
                    print(f"\nLocal repository ({len(files)} files):")
                    for f in files:
                        filepath = client.repository_path / f
                        size = filepath.stat().st_size
                        print(f"  - {f} ({size} bytes)")
                else:
                    print("Repository is empty")
                    
            else:
                print(f"Unknown command: {cmd}")
                print("Type 'help' or see available commands above")
                
    except KeyboardInterrupt:
        print("\n[CLIENT] Interrupted by user")
    finally:
        client.stop()


if __name__ == '__main__':
    main()
