"""
Test script for P2P File Sharing Application
Run this after starting the server to verify functionality
"""

import socket
import json
import time
import os
from pathlib import Path


def send_request(host, port, request):
    """Send a request to server and get response"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.send(json.dumps(request).encode('utf-8'))
        response = json.loads(sock.recv(4096).decode('utf-8'))
        sock.close()
        return response
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def test_server_connection(host='127.0.0.1', port=5000):
    """Test 1: Server Connection"""
    print("\n=== Test 1: Server Connection ===")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((host, port))
        sock.close()
        print("✓ Server is running and accepting connections")
        return True
    except Exception as e:
        print(f"✗ Cannot connect to server: {e}")
        return False


def test_client_registration(host='127.0.0.1', port=5000):
    """Test 2: Client Registration"""
    print("\n=== Test 2: Client Registration ===")
    
    request = {
        'command': 'register',
        'hostname': 'test_client',
        'ip': '127.0.0.1',
        'port': 7000
    }
    
    response = send_request(host, port, request)
    
    if response['status'] == 'success':
        print(f"✓ Client registered successfully: {response['message']}")
        return True
    else:
        print(f"✗ Registration failed: {response.get('message', 'Unknown error')}")
        return False


def test_file_publish(host='127.0.0.1', port=5000):
    """Test 3: File Publishing"""
    print("\n=== Test 3: File Publishing ===")
    
    # First register
    test_client_registration(host, port)
    
    request = {
        'command': 'publish',
        'hostname': 'test_client',
        'filename': 'test_file.txt'
    }
    
    response = send_request(host, port, request)
    
    if response['status'] == 'success':
        print(f"✓ File published successfully: {response['message']}")
        return True
    else:
        print(f"✗ Publishing failed: {response.get('message', 'Unknown error')}")
        return False


def test_discover(host='127.0.0.1', port=5000):
    """Test 4: Discover Command"""
    print("\n=== Test 4: Discover Files ===")
    
    request = {
        'command': 'discover',
        'hostname': 'test_client'
    }
    
    response = send_request(host, port, request)
    
    if response['status'] == 'success':
        files = response.get('files', [])
        print(f"✓ Discovered {len(files)} files from test_client:")
        for f in files:
            print(f"  - {f}")
        return True
    else:
        print(f"✗ Discovery failed: {response.get('message', 'Unknown error')}")
        return False


def test_ping(host='127.0.0.1', port=5000):
    """Test 5: Ping Command"""
    print("\n=== Test 5: Ping Host ===")
    
    request = {
        'command': 'ping',
        'hostname': 'test_client'
    }
    
    response = send_request(host, port, request)
    
    if response['status'] == 'success':
        alive = response.get('alive', False)
        last_seen = response.get('last_seen', 'Unknown')
        status = "ALIVE" if alive else "DEAD"
        print(f"✓ Host test_client is {status}")
        print(f"  Last seen: {last_seen}")
        return True
    else:
        print(f"✗ Ping failed: {response.get('message', 'Unknown error')}")
        return False


def test_fetch_nonexistent(host='127.0.0.1', port=5000):
    """Test 6: Fetch Non-existent File"""
    print("\n=== Test 6: Fetch Non-existent File ===")
    
    request = {
        'command': 'fetch',
        'hostname': 'test_client',
        'filename': 'nonexistent_file.txt'
    }
    
    response = send_request(host, port, request)
    
    if response['status'] == 'error':
        print(f"✓ Correctly returned error for non-existent file: {response['message']}")
        return True
    else:
        print(f"✗ Should have returned error for non-existent file")
        return False


def test_fetch_existing(host='127.0.0.1', port=5000):
    """Test 7: Fetch Existing File"""
    print("\n=== Test 7: Fetch Existing File ===")
    
    # First publish from test_client
    test_file_publish(host, port)
    
    # Register a second client
    request = {
        'command': 'register',
        'hostname': 'test_client2',
        'ip': '127.0.0.1',
        'port': 7001
    }
    send_request(host, port, request)
    
    # Try to fetch
    request = {
        'command': 'fetch',
        'hostname': 'test_client2',
        'filename': 'test_file.txt'
    }
    
    response = send_request(host, port, request)
    
    if response['status'] == 'success':
        peers = response.get('peers', [])
        print(f"✓ Found {len(peers)} peer(s) with the file:")
        for peer in peers:
            print(f"  - {peer['hostname']} ({peer['ip']}:{peer['port']})")
        return True
    else:
        print(f"✗ Fetch failed: {response.get('message', 'Unknown error')}")
        return False


def test_multiple_clients(host='127.0.0.1', port=5000):
    """Test 8: Multiple Client Registration"""
    print("\n=== Test 8: Multiple Clients ===")
    
    clients = ['client1', 'client2', 'client3', 'client4']
    success_count = 0
    
    for i, client in enumerate(clients):
        request = {
            'command': 'register',
            'hostname': client,
            'ip': '127.0.0.1',
            'port': 8000 + i
        }
        
        response = send_request(host, port, request)
        
        if response['status'] == 'success':
            success_count += 1
            print(f"✓ {client} registered")
        else:
            print(f"✗ {client} failed to register")
    
    if success_count == len(clients):
        print(f"\n✓ All {len(clients)} clients registered successfully")
        return True
    else:
        print(f"\n✗ Only {success_count}/{len(clients)} clients registered")
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("P2P File Sharing Application - Test Suite")
    print("=" * 60)
    print("\nMake sure the server is running on 127.0.0.1:5000")
    print("Press Enter to start tests...")
    input()
    
    tests = [
        test_server_connection,
        test_client_registration,
        test_file_publish,
        test_discover,
        test_ping,
        test_fetch_nonexistent,
        test_fetch_existing,
        test_multiple_clients
    ]
    
    results = []
    
    for test in tests:
        try:
            result = test()
            results.append(result)
            time.sleep(0.5)  # Small delay between tests
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nTests Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n✓ All tests passed! 🎉")
    else:
        print(f"\n✗ {total - passed} test(s) failed")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    run_all_tests()
