"""
P2P File Sharing - Server with GUI
"""

import socket
import threading
import json
import time
from datetime import datetime
import tkinter as tk
from tkinter import ttk, scrolledtext


class P2PServer:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.clients = {}  # {hostname: {'ip': ip, 'port': port, 'files': [filenames], 'last_seen': timestamp}}
        self.lock = threading.Lock()
        self.running = False
        self.server_socket = None
        self.log_callback = None
        
    def set_log_callback(self, callback):
        """Set callback function for logging"""
        self.log_callback = callback
        
    def log(self, message):
        """Log message to callback if available"""
        if self.log_callback:
            self.log_callback(message)
        else:
            print(message)
        
    def start(self):
        """Start the server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            self.log(f"[SERVER] Started on {self.host}:{self.port}")
            
            # Start accepting connections
            accept_thread = threading.Thread(target=self.accept_connections, daemon=True)
            accept_thread.start()
            
            return True
        except Exception as e:
            self.log(f"[SERVER] Error starting server: {e}")
            return False
        
    def accept_connections(self):
        """Accept incoming client connections"""
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                self.log(f"[SERVER] New connection from {address}")
                
                # Handle client in a new thread
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address),
                    daemon=True
                )
                client_thread.start()
            except Exception as e:
                if self.running:
                    self.log(f"[SERVER] Error accepting connection: {e}")
                    
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
            self.log(f"[SERVER] Error handling client {address}: {e}")
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
            
        self.log(f"[SERVER] Registered client: {hostname} ({ip}:{port})")
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
                
        self.log(f"[SERVER] {hostname} published: {filename}")
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
            self.log(f"[SERVER] Found {len(peers)} peer(s) with file: {filename}")
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
            try:
                self.server_socket.close()
            except:
                pass
        self.log("[SERVER] Stopped")
        
    def get_client_list(self):
        """Get list of connected clients"""
        with self.lock:
            return dict(self.clients)


class ServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("P2P File Sharing - Server")
        self.root.geometry("800x600")
        
        self.server = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the GUI"""
        # Server settings frame
        settings_frame = ttk.LabelFrame(self.root, text="Server Settings", padding=10)
        settings_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(settings_frame, text="Host:").grid(row=0, column=0, sticky='w', padx=5)
        self.host_entry = ttk.Entry(settings_frame, width=20)
        self.host_entry.insert(0, "0.0.0.0")
        self.host_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(settings_frame, text="Port:").grid(row=0, column=2, sticky='w', padx=5)
        self.port_entry = ttk.Entry(settings_frame, width=10)
        self.port_entry.insert(0, "5000")
        self.port_entry.grid(row=0, column=3, padx=5)
        
        self.start_btn = ttk.Button(settings_frame, text="Start Server", command=self.start_server)
        self.start_btn.grid(row=0, column=4, padx=5)
        
        self.stop_btn = ttk.Button(settings_frame, text="Stop Server", command=self.stop_server, state='disabled')
        self.stop_btn.grid(row=0, column=5, padx=5)
        
        self.status_label = ttk.Label(settings_frame, text="Server not running", foreground="red")
        self.status_label.grid(row=1, column=0, columnspan=6, pady=5)
        
        # Commands frame
        commands_frame = ttk.LabelFrame(self.root, text="Server Commands", padding=10)
        commands_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(commands_frame, text="Hostname:").pack(side='left', padx=5)
        self.hostname_entry = ttk.Entry(commands_frame, width=20)
        self.hostname_entry.pack(side='left', padx=5)
        
        ttk.Button(commands_frame, text="Discover", command=self.discover_command).pack(side='left', padx=2)
        ttk.Button(commands_frame, text="Ping", command=self.ping_command).pack(side='left', padx=2)
        ttk.Button(commands_frame, text="List Clients", command=self.list_command).pack(side='left', padx=2)
        ttk.Button(commands_frame, text="Clear Log", command=self.clear_log).pack(side='left', padx=2)
        
        # Clients list frame
        clients_frame = ttk.LabelFrame(self.root, text="Connected Clients", padding=5)
        clients_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create treeview for clients
        columns = ('Hostname', 'IP', 'Port', 'Files', 'Last Seen')
        self.clients_tree = ttk.Treeview(clients_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.clients_tree.heading(col, text=col)
            
        self.clients_tree.column('Hostname', width=120)
        self.clients_tree.column('IP', width=120)
        self.clients_tree.column('Port', width=80)
        self.clients_tree.column('Files', width=80)
        self.clients_tree.column('Last Seen', width=150)
        
        scrollbar = ttk.Scrollbar(clients_frame, orient='vertical', command=self.clients_tree.yview)
        self.clients_tree.config(yscrollcommand=scrollbar.set)
        
        self.clients_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Auto-refresh button
        refresh_frame = ttk.Frame(self.root)
        refresh_frame.pack(fill='x', padx=10)
        ttk.Button(refresh_frame, text="Refresh Clients", command=self.refresh_clients).pack(side='left', padx=5)
        
        self.auto_refresh_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(refresh_frame, text="Auto-refresh (5s)", variable=self.auto_refresh_var).pack(side='left', padx=5)
        
        # Log frame
        log_frame = ttk.LabelFrame(self.root, text="Server Log", padding=5)
        log_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, state='disabled')
        self.log_text.pack(fill='both', expand=True)
        
        # Start auto-refresh
        self.auto_refresh()
        
    def log(self, message):
        """Add message to log"""
        self.log_text.config(state='normal')
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_text.insert('end', f"[{timestamp}] {message}\n")
        self.log_text.see('end')
        self.log_text.config(state='disabled')
        
    def clear_log(self):
        """Clear the log"""
        self.log_text.config(state='normal')
        self.log_text.delete('1.0', 'end')
        self.log_text.config(state='disabled')
        
    def start_server(self):
        """Start the server"""
        host = self.host_entry.get().strip()
        try:
            port = int(self.port_entry.get().strip())
        except ValueError:
            self.log("Invalid port number")
            return
            
        self.server = P2PServer(host, port)
        self.server.set_log_callback(self.log)
        
        if self.server.start():
            self.status_label.config(text=f"Server running on {host}:{port}", foreground="green")
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.host_entry.config(state='disabled')
            self.port_entry.config(state='disabled')
        else:
            self.log("Failed to start server")
            
    def stop_server(self):
        """Stop the server"""
        if self.server:
            self.server.stop()
            self.status_label.config(text="Server stopped", foreground="red")
            self.start_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            self.host_entry.config(state='normal')
            self.port_entry.config(state='normal')
            self.refresh_clients()
            
    def discover_command(self):
        """Execute discover command"""
        if not self.server or not self.server.running:
            self.log("Server is not running")
            return
            
        hostname = self.hostname_entry.get().strip()
        if not hostname:
            self.log("Please enter a hostname")
            return
            
        result = self.server.handle_discover({'hostname': hostname})
        
        if result['status'] == 'success':
            self.log(f"Files on {hostname}:")
            for f in result['files']:
                self.log(f"  - {f}")
        else:
            self.log(f"Error: {result['message']}")
            
    def ping_command(self):
        """Execute ping command"""
        if not self.server or not self.server.running:
            self.log("Server is not running")
            return
            
        hostname = self.hostname_entry.get().strip()
        if not hostname:
            self.log("Please enter a hostname")
            return
            
        result = self.server.handle_ping({'hostname': hostname})
        
        if result['status'] == 'success':
            status = "ALIVE" if result['alive'] else "DEAD"
            self.log(f"{hostname} is {status} (last seen: {result['last_seen']})")
        else:
            self.log(f"Error: {result['message']}")
            
    def list_command(self):
        """Execute list command"""
        if not self.server or not self.server.running:
            self.log("Server is not running")
            return
            
        clients = self.server.get_client_list()
        
        if clients:
            self.log("Connected Clients:")
            for hostname, info in clients.items():
                self.log(f"  {hostname} ({info['ip']}:{info['port']}) - {len(info['files'])} files")
        else:
            self.log("No clients connected")
            
    def refresh_clients(self):
        """Refresh the clients list"""
        # Clear existing items
        for item in self.clients_tree.get_children():
            self.clients_tree.delete(item)
            
        if not self.server or not self.server.running:
            return
            
        clients = self.server.get_client_list()
        
        for hostname, info in clients.items():
            last_seen = datetime.fromtimestamp(info['last_seen']).strftime('%Y-%m-%d %H:%M:%S')
            self.clients_tree.insert('', 'end', values=(
                hostname,
                info['ip'],
                info['port'],
                len(info['files']),
                last_seen
            ))
            
    def auto_refresh(self):
        """Auto-refresh clients list"""
        if self.auto_refresh_var.get():
            self.refresh_clients()
        
        # Schedule next refresh
        self.root.after(5000, self.auto_refresh)


def main():
    root = tk.Tk()
    app = ServerGUI(root)
    
    def on_closing():
        if app.server and app.server.running:
            app.stop_server()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == '__main__':
    main()
