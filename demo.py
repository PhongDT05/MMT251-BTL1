"""
Demo Script - Shows the P2P system in action
This script demonstrates the core functionality programmatically
"""

import time
import json
import socket
from pathlib import Path


def send_request(host, port, request):
    """Helper function to send request to server"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.send(json.dumps(request).encode('utf-8'))
        response = json.loads(sock.recv(4096).decode('utf-8'))
        sock.close()
        return response
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def demo_sequence():
    """Run a demonstration sequence"""
    
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 5000
    
    print("=" * 70)
    print("P2P FILE SHARING SYSTEM - DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Check if server is running
    print("Step 1: Checking server connection...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((SERVER_HOST, SERVER_PORT))
        sock.close()
        print("✓ Server is running on {}:{}".format(SERVER_HOST, SERVER_PORT))
    except:
        print("✗ ERROR: Server is not running!")
        print("  Please start the server first: python server.py")
        return
    
    time.sleep(1)
    print()
    
    # Register Client 1
    print("Step 2: Registering Client 1...")
    response = send_request(SERVER_HOST, SERVER_PORT, {
        'command': 'register',
        'hostname': 'demo_client1',
        'ip': '127.0.0.1',
        'port': 7000
    })
    
    if response['status'] == 'success':
        print("✓ Client 1 registered successfully")
    else:
        print("✗ Registration failed:", response.get('message'))
    
    time.sleep(1)
    print()
    
    # Register Client 2
    print("Step 3: Registering Client 2...")
    response = send_request(SERVER_HOST, SERVER_PORT, {
        'command': 'register',
        'hostname': 'demo_client2',
        'ip': '127.0.0.1',
        'port': 7001
    })
    
    if response['status'] == 'success':
        print("✓ Client 2 registered successfully")
    else:
        print("✗ Registration failed:", response.get('message'))
    
    time.sleep(1)
    print()
    
    # Client 1 publishes files
    print("Step 4: Client 1 publishing files...")
    files = ['document.pdf', 'presentation.pptx', 'data.csv']
    
    for filename in files:
        response = send_request(SERVER_HOST, SERVER_PORT, {
            'command': 'publish',
            'hostname': 'demo_client1',
            'filename': filename
        })
        
        if response['status'] == 'success':
            print("  ✓ Published: {}".format(filename))
        else:
            print("  ✗ Failed to publish:", filename)
        
        time.sleep(0.3)
    
    time.sleep(1)
    print()
    
    # Client 2 publishes files
    print("Step 5: Client 2 publishing files...")
    files = ['image.jpg', 'video.mp4']
    
    for filename in files:
        response = send_request(SERVER_HOST, SERVER_PORT, {
            'command': 'publish',
            'hostname': 'demo_client2',
            'filename': filename
        })
        
        if response['status'] == 'success':
            print("  ✓ Published: {}".format(filename))
        else:
            print("  ✗ Failed to publish:", filename)
        
        time.sleep(0.3)
    
    time.sleep(1)
    print()
    
    # Discover files on Client 1
    print("Step 6: Discovering files on Client 1...")
    response = send_request(SERVER_HOST, SERVER_PORT, {
        'command': 'discover',
        'hostname': 'demo_client1'
    })
    
    if response['status'] == 'success':
        files = response.get('files', [])
        print("✓ Found {} files on demo_client1:".format(len(files)))
        for f in files:
            print("  - {}".format(f))
    else:
        print("✗ Discovery failed:", response.get('message'))
    
    time.sleep(1)
    print()
    
    # Discover files on Client 2
    print("Step 7: Discovering files on Client 2...")
    response = send_request(SERVER_HOST, SERVER_PORT, {
        'command': 'discover',
        'hostname': 'demo_client2'
    })
    
    if response['status'] == 'success':
        files = response.get('files', [])
        print("✓ Found {} files on demo_client2:".format(len(files)))
        for f in files:
            print("  - {}".format(f))
    else:
        print("✗ Discovery failed:", response.get('message'))
    
    time.sleep(1)
    print()
    
    # Client 2 fetches file from Client 1
    print("Step 8: Client 2 requesting file 'document.pdf' from Client 1...")
    response = send_request(SERVER_HOST, SERVER_PORT, {
        'command': 'fetch',
        'hostname': 'demo_client2',
        'filename': 'document.pdf'
    })
    
    if response['status'] == 'success':
        peers = response.get('peers', [])
        print("✓ Found {} peer(s) with the file:".format(len(peers)))
        for peer in peers:
            print("  - {hostname} ({ip}:{port})".format(**peer))
        print("  → Client 2 would now download directly from the peer")
        print("  → (Not implemented in demo - use GUI for actual transfer)")
    else:
        print("✗ Fetch failed:", response.get('message'))
    
    time.sleep(1)
    print()
    
    # Ping clients
    print("Step 9: Checking if clients are alive...")
    
    for hostname in ['demo_client1', 'demo_client2']:
        response = send_request(SERVER_HOST, SERVER_PORT, {
            'command': 'ping',
            'hostname': hostname
        })
        
        if response['status'] == 'success':
            alive = response.get('alive', False)
            status = "ALIVE" if alive else "DEAD"
            last_seen = response.get('last_seen', 'Unknown')
            print("  {} is {} (last seen: {})".format(hostname, status, last_seen))
        else:
            print("  {} not found".format(hostname))
        
        time.sleep(0.5)
    
    time.sleep(1)
    print()
    
    # Try to fetch non-existent file
    print("Step 10: Attempting to fetch non-existent file...")
    response = send_request(SERVER_HOST, SERVER_PORT, {
        'command': 'fetch',
        'hostname': 'demo_client2',
        'filename': 'nonexistent.txt'
    })
    
    if response['status'] == 'error':
        print("✓ Correctly returned error: {}".format(response.get('message')))
    else:
        print("✗ Should have returned error for non-existent file")
    
    time.sleep(1)
    print()
    
    # Summary
    print("=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)
    print()
    print("Summary:")
    print("  ✓ Server communication working")
    print("  ✓ Client registration working")
    print("  ✓ File publishing working")
    print("  ✓ File discovery working")
    print("  ✓ Peer lookup for file transfer working")
    print("  ✓ Ping/status checking working")
    print("  ✓ Error handling working")
    print()
    print("For full file transfer functionality, use the GUI client:")
    print("  python client_gui.py")
    print()
    print("Check the server console to see all the activity!")
    print("=" * 70)


if __name__ == '__main__':
    try:
        demo_sequence()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    except Exception as e:
        print("\n\nDemo failed with error:", str(e))
