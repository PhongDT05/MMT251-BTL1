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
        self.peer_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.peer_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.peer_server_socket.bind(('0.0.0.0', self.client_port))
        self.peer_server_socket.listen(5)
        self.running = True
        
        accept_thread = threading.Thread(target=self.accept_peer_connections, daemon=True)
        accept_thread.start()
        
    def accept_peer_connections(self):
        """Accept connections from other peers"""
        while self.running:
            try:
                peer_socket, address = self.peer_server_socket.accept()
                thread = threading.Thread(
                    target=self.handle_peer_request,
                    args=(peer_socket,),
                    daemon=True
                )
                thread.start()
            except Exception as e:
                if self.running:
                    print(f"Error accepting peer connection: {e}")
                    
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
                else:
                    response = {'status': 'error', 'message': 'File not found'}
                    peer_socket.send(json.dumps(response).encode('utf-8'))
                    
        except Exception as e:
            print(f"Error handling peer request: {e}")
        finally:
            peer_socket.close()
            
    def publish(self, local_path, filename):
        """Publish a file to the repository"""
        try:
            # Copy file to repository
            dest_path = self.repository_path / filename
            shutil.copy2(local_path, dest_path)
            
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
            
            return response['status'] == 'success', response.get('message', 'Unknown error')
        except Exception as e:
            return False, str(e)
            
    def fetch(self, filename):
        """Fetch a file from a peer"""
        try:
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
                
            # Try to download from first peer
            peer = peers[0]
            success, message = self.download_from_peer(peer, filename)
            
            if success:
                # Publish the downloaded file
                self.publish(str(self.repository_path / filename), filename)
                
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
        return [f.name for f in self.repository_path.iterdir() if f.is_file()]
        
    def stop(self):
        """Stop the peer server"""
        self.running = False
        if self.peer_server_socket:
            self.peer_server_socket.close()


class P2PClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("P2P File Sharing Client")
        self.root.geometry("700x600")
        
        self.client = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the GUI"""
        # Connection frame
        conn_frame = ttk.LabelFrame(self.root, text="Connection Settings", padding=10)
        conn_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(conn_frame, text="Hostname:").grid(row=0, column=0, sticky='w', padx=5)
        self.hostname_entry = ttk.Entry(conn_frame, width=20)
        self.hostname_entry.insert(0, "client1")
        self.hostname_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(conn_frame, text="Server:").grid(row=0, column=2, sticky='w', padx=5)
        self.server_entry = ttk.Entry(conn_frame, width=20)
        self.server_entry.insert(0, "127.0.0.1:5000")
        self.server_entry.grid(row=0, column=3, padx=5)
        
        ttk.Label(conn_frame, text="Client Port:").grid(row=0, column=4, sticky='w', padx=5)
        self.port_entry = ttk.Entry(conn_frame, width=10)
        self.port_entry.insert(0, "6000")
        self.port_entry.grid(row=0, column=5, padx=5)
        
        self.connect_btn = ttk.Button(conn_frame, text="Connect", command=self.connect)
        self.connect_btn.grid(row=0, column=6, padx=5)
        
        self.status_label = ttk.Label(conn_frame, text="Not connected", foreground="red")
        self.status_label.grid(row=1, column=0, columnspan=7, pady=5)
        
        # Operations frame
        ops_frame = ttk.LabelFrame(self.root, text="Operations", padding=10)
        ops_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Publish section
        publish_frame = ttk.Frame(ops_frame)
        publish_frame.pack(fill='x', pady=5)
        
        ttk.Label(publish_frame, text="Publish File:").pack(side='left', padx=5)
        self.publish_path_entry = ttk.Entry(publish_frame, width=30)
        self.publish_path_entry.pack(side='left', padx=5)
        ttk.Button(publish_frame, text="Browse", command=self.browse_file).pack(side='left', padx=2)
        
        ttk.Label(publish_frame, text="As:").pack(side='left', padx=5)
        self.publish_name_entry = ttk.Entry(publish_frame, width=20)
        self.publish_name_entry.pack(side='left', padx=5)
        ttk.Button(publish_frame, text="Publish", command=self.publish_file).pack(side='left', padx=2)
        
        # Fetch section
        fetch_frame = ttk.Frame(ops_frame)
        fetch_frame.pack(fill='x', pady=5)
        
        ttk.Label(fetch_frame, text="Fetch File:").pack(side='left', padx=5)
        self.fetch_entry = ttk.Entry(fetch_frame, width=30)
        self.fetch_entry.pack(side='left', padx=5)
        ttk.Button(fetch_frame, text="Fetch", command=self.fetch_file).pack(side='left', padx=2)
        ttk.Button(fetch_frame, text="Refresh Repository", command=self.refresh_repository).pack(side='left', padx=2)
        
        # Repository list
        repo_frame = ttk.LabelFrame(ops_frame, text="Local Repository", padding=5)
        repo_frame.pack(fill='both', expand=True, pady=5)
        
        self.repo_listbox = tk.Listbox(repo_frame, height=8)
        repo_scrollbar = ttk.Scrollbar(repo_frame, orient='vertical', command=self.repo_listbox.yview)
        self.repo_listbox.config(yscrollcommand=repo_scrollbar.set)
        self.repo_listbox.pack(side='left', fill='both', expand=True)
        repo_scrollbar.pack(side='right', fill='y')
        
        # Log section
        log_frame = ttk.LabelFrame(self.root, text="Log", padding=5)
        log_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, state='disabled')
        self.log_text.pack(fill='both', expand=True)
        
    def log(self, message):
        """Add message to log"""
        self.log_text.config(state='normal')
        self.log_text.insert('end', f"{message}\n")
        self.log_text.see('end')
        self.log_text.config(state='disabled')
        
    def connect(self):
        """Connect to server"""
        hostname = self.hostname_entry.get().strip()
        server_addr = self.server_entry.get().strip()
        client_port = int(self.port_entry.get().strip())
        
        if not hostname:
            messagebox.showerror("Error", "Please enter a hostname")
            return
            
        try:
            server_host, server_port = server_addr.split(':')
            server_port = int(server_port)
        except:
            messagebox.showerror("Error", "Invalid server address format (use host:port)")
            return
            
        self.client = P2PClient(hostname, server_host, server_port, client_port)
        
        # Start peer server
        self.client.start_peer_server()
        self.log(f"Started peer server on port {client_port}")
        
        # Connect to central server
        success, message = self.client.connect_to_server()
        
        if success:
            self.status_label.config(text=f"Connected as {hostname}", foreground="green")
            self.connect_btn.config(state='disabled')
            self.log(f"Connected to server: {message}")
            self.refresh_repository()
        else:
            self.status_label.config(text=f"Connection failed: {message}", foreground="red")
            self.log(f"Connection failed: {message}")
            
    def browse_file(self):
        """Browse for a file to publish"""
        filename = filedialog.askopenfilename()
        if filename:
            self.publish_path_entry.delete(0, 'end')
            self.publish_path_entry.insert(0, filename)
            
            # Auto-fill the publish name
            name = os.path.basename(filename)
            self.publish_name_entry.delete(0, 'end')
            self.publish_name_entry.insert(0, name)
            
    def publish_file(self):
        """Publish a file"""
        if not self.client:
            messagebox.showerror("Error", "Not connected to server")
            return
            
        local_path = self.publish_path_entry.get().strip()
        filename = self.publish_name_entry.get().strip()
        
        if not local_path or not filename:
            messagebox.showerror("Error", "Please specify file path and name")
            return
            
        if not os.path.exists(local_path):
            messagebox.showerror("Error", "File does not exist")
            return
            
        success, message = self.client.publish(local_path, filename)
        
        if success:
            self.log(f"Published: {filename}")
            self.refresh_repository()
            messagebox.showinfo("Success", f"File '{filename}' published successfully")
        else:
            self.log(f"Publish failed: {message}")
            messagebox.showerror("Error", f"Failed to publish: {message}")
            
    def fetch_file(self):
        """Fetch a file from peers"""
        if not self.client:
            messagebox.showerror("Error", "Not connected to server")
            return
            
        filename = self.fetch_entry.get().strip()
        
        if not filename:
            messagebox.showerror("Error", "Please enter a filename to fetch")
            return
            
        self.log(f"Fetching: {filename}")
        success, message = self.client.fetch(filename)
        
        if success:
            self.log(f"Fetched successfully: {message}")
            self.refresh_repository()
            messagebox.showinfo("Success", f"File '{filename}' fetched successfully")
        else:
            self.log(f"Fetch failed: {message}")
            messagebox.showerror("Error", f"Failed to fetch: {message}")
            
    def refresh_repository(self):
        """Refresh the repository file list"""
        if not self.client:
            return
            
        self.repo_listbox.delete(0, 'end')
        files = self.client.list_repository_files()
        
        for f in files:
            self.repo_listbox.insert('end', f)
            
        self.log(f"Repository refreshed: {len(files)} files")


def main():
    root = tk.Tk()
    app = P2PClientGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
