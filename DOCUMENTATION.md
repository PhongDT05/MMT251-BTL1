# P2P File Sharing Application - Complete Documentation

## Table of Contents
1. [Quick Start](#quick-start)
2. [Overview](#overview)
3. [Requirements Met](#requirements-met)
4. [Installation](#installation)
5. [Command-Line Interface Guide](#command-line-interface-guide)
6. [Server Commands](#server-commands)
7. [Client Commands](#client-commands)
8. [Complete Usage Example](#complete-usage-example)
9. [Protocol Specification](#protocol-specification)
10. [Architecture](#architecture)
11. [Testing](#testing)
12. [Troubleshooting](#troubleshooting)
13. [Project Structure](#project-structure)

---

## Quick Start

### Three Simple Steps

#### Step 1: Start Server
Open Terminal 1:
```bash
python server.py
```

#### Step 2: Start Client 1
Open Terminal 2:
```bash
python client.py
# Enter: hostname=client1, port=6000
```

Publish a file:
```
client1> publish test_file.txt myfile.txt
```

#### Step 3: Start Client 2
Open Terminal 3:
```bash
python client.py
# Enter: hostname=client2, port=6001
```

Fetch the file:
```
client2> fetch myfile.txt
```

✅ **Done!** File transferred peer-to-peer!

---

## Overview

This is a **Peer-to-Peer (P2P) File Sharing Application** that uses:
- **Centralized server** for tracking clients and file metadata
- **Direct P2P connections** for actual file transfers
- **Command-line interpreters** for both server and client
- **TCP/IP protocol stack** for communication
- **Multi-threading** for concurrent operations

### Key Features

✅ **Server tracks clients and files** (metadata only)  
✅ **Direct peer-to-peer file transfers** (no server bottleneck)  
✅ **Command-line interface** for both server and client  
✅ **Multi-threaded** client for concurrent downloads  
✅ **Simple protocol** using JSON over TCP  

### System Architecture

```
┌─────────────────────────────────┐
│      Central Server             │
│      Port: 5000                 │
│                                 │
│  Tracks:                        │
│  - Connected clients            │
│  - File metadata (not files)    │
│                                 │
│  Commands:                      │
│  - discover <hostname>          │
│  - ping <hostname>              │
│  - list                         │
│  - quit                         │
└────────────┬────────────────────┘
             │
             │ Coordination (JSON/TCP)
             │
    ┌────────┼────────┬──────────┐
    │        │        │          │
┌───▼───┐ ┌──▼───┐ ┌─▼────┐ ┌───▼───┐
│Client1│ │Client2│ │Client3│ │Client4│
│:6000  │ │:6001  │ │:6002  │ │:6003  │
│       │ │       │ │       │ │       │
│ Repo  │ │ Repo  │ │ Repo  │ │ Repo  │
│Commands:│ │       │ │       │ │       │
│publish│ │publish│ │publish│ │publish│
│fetch  │ │fetch  │ │fetch  │ │fetch  │
│list   │ │list   │ │list   │ │list   │
│quit   │ │quit   │ │quit   │ │quit   │
└───────┘ └───────┘ └───────┘ └───────┘
    ↕                      ↕
    └──────────────────────┘
      P2P File Transfer
      (Binary/TCP - Direct)
```

---

## Requirements Met

### Assignment Requirements (100% Complete)

#### ✅ Client Command-Shell Interpreter
The client has a simple command-shell interpreter with:

- **`publish lname fname`** - A local file (stored in the client's file system at `lname`) is added to the client's repository as a file named `fname` and this information is conveyed to the server.

- **`fetch fname`** - Fetch some copy of the target file and add it to the local repository.

#### ✅ Server Command-Shell Interpreter
The server has a simple command-shell interpreter with:

- **`discover hostname`** - Discover the list of local files of the host named `hostname`

- **`ping hostname`** - Live check the host named `hostname`

#### ✅ Additional Requirements
- Centralized server keeps track of connected clients and their files
- Client informs server about files (metadata only, not actual data)
- Server identifies peers with requested files
- Direct P2P file transfer without server intervention
- Multi-threaded client for concurrent downloads
- TCP/IP protocol stack
- Custom application protocol

---

## Installation

### Requirements
- Python 3.7 or higher
- No external dependencies (uses standard library only)

### Setup
1. Download/clone all files to a directory
2. Ensure Python is installed:
   ```bash
   python --version
   ```
3. Ready to run! No installation needed.

---

## Command-Line Interface Guide

### Server Interface

#### Starting the Server
```bash
python server.py
```

You'll see:
```
[SERVER] Started on 0.0.0.0:5000

Server Commands:
  discover <hostname> - Discover files from a host
  ping <hostname> - Check if a host is alive
  list - List all connected clients
  quit - Stop the server

Server>
```

---

### Client Interface

#### Starting a Client
```bash
python client.py
```

#### Initial Configuration
You'll be prompted:
```
P2P File Sharing - Client
Enter your hostname: client1
Enter server address (default: 127.0.0.1): [press Enter]
Enter server port (default: 5000): [press Enter]
Enter your client port (default: 6000): [press Enter]
```

**Important:**
- Each client must have a **unique hostname**
- Each client must use a **unique port number**

After connection:
```
[CLIENT] Peer server started on port 6000
[CLIENT] Connecting to server at 127.0.0.1:5000...
[CLIENT] Connected successfully: Client registered

Client Commands:
  publish <lname> <fname> - Publish a local file to repository
  fetch <fname>           - Fetch a file from peers
  list                    - List files in local repository
  quit                    - Exit client

client1>
```

---

## Server Commands

### 1. `discover <hostname>`

**Purpose:** Discover the list of local files of a specific host

**Usage:**
```
Server> discover client1
```

**Output:**
```
Files on client1:
  - document.pdf
  - image.jpg
  - data.txt
```

**Example:**
```
Server> discover client2
Files on client2:
  - presentation.pptx
  - report.docx
```

---

### 2. `ping <hostname>`

**Purpose:** Live check if a host is alive and active

**Usage:**
```
Server> ping client1
```

**Output (Alive):**
```
client1 is ALIVE (last seen: 2023-10-30 14:30:45)
```

**Output (Dead):**
```
client1 is DEAD (last seen: 2023-10-30 13:15:22)
```

**Note:** Host is considered "alive" if active within last 60 seconds.

---

### 3. `list`

**Purpose:** List all connected clients (utility command)

**Usage:**
```
Server> list
```

**Output:**
```
Connected Clients:
  client1 (127.0.0.1:6000) - 3 files
  client2 (127.0.0.1:6001) - 2 files
  client3 (127.0.0.1:6002) - 5 files
```

---

### 4. `quit`

**Purpose:** Stop the server gracefully

**Usage:**
```
Server> quit
```

**Output:**
```
[SERVER] Stopped
```

---

## Client Commands

### 1. `publish <lname> <fname>`

**Purpose:** Publish a local file to the repository

**Parameters:**
- `lname` - Local file path (where the file is stored in your file system)
- `fname` - Repository file name (name to publish the file as)

**Usage Examples:**
```
client1> publish /home/user/document.pdf document.pdf
client1> publish C:\Users\name\file.txt myfile.txt
client1> publish test_file.txt shared_doc.txt
```

**What Happens:**
1. File is copied from `lname` to local repository (`client_repo_<hostname>/`)
2. Server is notified of the file availability (metadata only)
3. File is now available for other peers to fetch

**Output:**
```
[CLIENT] Copied 'test_file.txt' to repository as 'shared_doc.txt'
[CLIENT] Published 'shared_doc.txt' to server
```

---

### 2. `fetch <fname>`

**Purpose:** Fetch a file from other peers and add it to local repository

**Parameters:**
- `fname` - Name of the file to fetch

**Usage:**
```
client2> fetch document.pdf
```

**What Happens:**
1. Client asks server: "Who has this file?"
2. Server returns list of peers with the file
3. Client connects directly to a peer
4. File is downloaded via P2P (not through server)
5. Downloaded file is automatically published to server

**Output (Success):**
```
[CLIENT] Fetching 'document.pdf'...
[CLIENT] Found 2 peer(s) with the file:
  1. client1 (127.0.0.1:6000)
  2. client3 (127.0.0.1:6002)
[CLIENT] Downloading from client1...
[CLIENT] Copied '...' to repository as 'document.pdf'
[CLIENT] Published 'document.pdf' to server
[CLIENT] Successfully fetched 'document.pdf'
```

**Output (Error):**
```
[CLIENT] Fetching 'nonexistent.txt'...
[ERROR] No peers found with the file
```

---

### 3. `list`

**Purpose:** List all files in your local repository

**Usage:**
```
client1> list
```

**Output:**
```
Local repository (3 files):
  - document.pdf (524288 bytes)
  - image.jpg (102400 bytes)
  - data.txt (1024 bytes)
```

**Empty Repository:**
```
Repository is empty
```

---

### 4. `quit`

**Purpose:** Exit the client gracefully

**Usage:**
```
client1> quit
```

**Output:**
```
[CLIENT] Shutting down...
```

---

## Complete Usage Example

### Scenario: Three Clients Sharing Files

#### Terminal 1: Server
```bash
$ python server.py
========================================================
[SERVER] Started on 0.0.0.0:5000

Server Commands:
  discover <hostname> - Discover files from a host
  ping <hostname> - Check if a host is alive
  list - List all connected clients
  quit - Stop the server

Server>
```

#### Terminal 2: Client 1 (Publisher)
```bash
$ python client.py
============================================================
P2P File Sharing - Client
============================================================
Enter your hostname: client1
Enter server address (default: 127.0.0.1): 
Enter server port (default: 5000): 
Enter your client port (default: 6000): 

[CLIENT] Peer server started on port 6000
[CLIENT] Connecting to server at 127.0.0.1:5000...
[CLIENT] Connected successfully: Client registered

============================================================
Client Commands:
  publish <lname> <fname> - Publish a local file to repository
  fetch <fname>           - Fetch a file from peers
  list                    - List files in local repository
  quit                    - Exit client
============================================================

client1> publish test_file.txt document.txt
[CLIENT] Copied 'test_file.txt' to repository as 'document.txt'
[CLIENT] Published 'document.txt' to server

client1> list
Local repository (1 files):
  - document.txt (375 bytes)

client1>
```

#### Terminal 3: Client 2 (Fetcher)
```bash
$ python client.py
============================================================
P2P File Sharing - Client
============================================================
Enter your hostname: client2
Enter server address (default: 127.0.0.1): 
Enter server port (default: 5000): 
Enter your client port (default: 6000): 6001

[CLIENT] Peer server started on port 6001
[CLIENT] Connecting to server at 127.0.0.1:5000...
[CLIENT] Connected successfully: Client registered

============================================================
Client Commands:
  publish <lname> <fname> - Publish a local file to repository
  fetch <fname>           - Fetch a file from peers
  list                    - List files in local repository
  quit                    - Exit client
============================================================

client2> fetch document.txt
[CLIENT] Fetching 'document.txt'...
[CLIENT] Found 1 peer(s) with the file:
  1. client1 (127.0.0.1:6000)
[CLIENT] Downloading from client1...
[CLIENT] Copied 'client_repo_client2/document.txt' to repository as 'document.txt'
[CLIENT] Published 'document.txt' to server
[CLIENT] Successfully fetched 'document.txt'

client2> list
Local repository (1 files):
  - document.txt (375 bytes)

client2>
```

#### Terminal 4: Client 3 (Also Fetches)
```bash
$ python client.py
Enter your hostname: client3
Enter server address (default: 127.0.0.1): 
Enter server port (default: 5000): 
Enter your client port (default: 6000): 6002

[CLIENT] Peer server started on port 6002
[CLIENT] Connected successfully: Client registered

client3> fetch document.txt
[CLIENT] Fetching 'document.txt'...
[CLIENT] Found 2 peer(s) with the file:
  1. client1 (127.0.0.1:6000)
  2. client2 (127.0.0.1:6001)
[CLIENT] Downloading from client1...
[CLIENT] Successfully fetched 'document.txt'

client3>
```

#### Back to Terminal 1: Server Commands
```
Server> list
Connected Clients:
  client1 (127.0.0.1:6000) - 1 files
  client2 (127.0.0.1:6001) - 1 files
  client3 (127.0.0.1:6002) - 1 files

Server> discover client1
Files on client1:
  - document.txt

Server> discover client2
Files on client2:
  - document.txt

Server> discover client3
Files on client3:
  - document.txt

Server> ping client1
client1 is ALIVE (last seen: 2023-10-30 14:35:12)

Server> ping client2
client2 is ALIVE (last seen: 2023-10-30 14:35:15)

Server> ping client3
client3 is ALIVE (last seen: 2023-10-30 14:35:18)

Server> quit
[SERVER] Stopped
```

---

## Protocol Specification

### Overview

The system uses two protocols:
1. **Client-Server Protocol** - For coordination and metadata
2. **Peer-to-Peer Protocol** - For direct file transfers

Both use **JSON over TCP**.

---

### Client-Server Protocol

#### Transport
- **Protocol:** TCP
- **Port:** 5000 (configurable)
- **Encoding:** UTF-8
- **Format:** JSON

#### Message Format
**Request:**
```json
{
  "command": "string",
  "parameter1": "value1",
  "parameter2": "value2"
}
```

**Response:**
```json
{
  "status": "success" | "error",
  "message": "string",
  "data": { ... }
}
```

---

#### 1. REGISTER Command

**Purpose:** Register client with server

**Request:**
```json
{
  "command": "register",
  "hostname": "client1",
  "ip": "127.0.0.1",
  "port": 6000
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Client registered"
}
```

---

#### 2. PUBLISH Command

**Purpose:** Notify server of file availability

**Request:**
```json
{
  "command": "publish",
  "hostname": "client1",
  "filename": "document.pdf"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "File document.pdf published"
}
```

**Note:** Only metadata is sent, not the actual file data.

---

#### 3. FETCH Command

**Purpose:** Request list of peers with a file

**Request:**
```json
{
  "command": "fetch",
  "hostname": "client2",
  "filename": "document.pdf"
}
```

**Response:**
```json
{
  "status": "success",
  "peers": [
    {
      "hostname": "client1",
      "ip": "127.0.0.1",
      "port": 6000
    },
    {
      "hostname": "client3",
      "ip": "127.0.0.1",
      "port": 6002
    }
  ]
}
```

---

#### 4. DISCOVER Command

**Purpose:** List files on a host

**Request:**
```json
{
  "command": "discover",
  "hostname": "client1"
}
```

**Response:**
```json
{
  "status": "success",
  "hostname": "client1",
  "files": ["document.pdf", "image.jpg", "data.txt"]
}
```

---

#### 5. PING Command

**Purpose:** Check if host is alive

**Request:**
```json
{
  "command": "ping",
  "hostname": "client1"
}
```

**Response:**
```json
{
  "status": "success",
  "hostname": "client1",
  "alive": true,
  "last_seen": "2023-10-30 14:30:45"
}
```

---

### Peer-to-Peer Protocol

#### Transport
- **Protocol:** TCP
- **Port:** Client-specific (6000, 6001, 6002, ...)
- **Format:** JSON for metadata, binary for file data

#### File Download Flow

**Phase 1: Request (JSON)**
```json
{
  "command": "download",
  "filename": "document.pdf"
}
```

**Phase 2: Metadata Response (JSON)**
```json
{
  "status": "success",
  "filename": "document.pdf",
  "size": 12345
}
```

**Phase 3: Acknowledgment**
Client sends: `OK` (UTF-8 encoded)

**Phase 4: File Transfer**
Server sends raw binary data (file contents)

**Complete Flow:**
```
Requesting Client          Serving Peer
      |                         |
      |-- (1) Download Req ---->|
      |    {"command":"download"}
      |                         |
      |<- (2) Metadata Resp ----|
      |    {"size": 12345, ...} |
      |                         |
      |-- (3) ACK: "OK" ------->|
      |                         |
      |<- (4) Binary Data ------|
      |    [raw file bytes]     |
      |                         |
```

---

## Architecture

### System Components

#### 1. Central Server
- **File:** `server.py`
- **Port:** 5000 (default)
- **Function:** 
  - Track connected clients
  - Store file metadata (not actual files)
  - Provide peer lookup service
- **Storage:** In-memory (dictionary-based)
- **Concurrency:** Multi-threaded

#### 2. Client
- **File:** `client.py`
- **Port:** Client-specific (6000+)
- **Dual Role:**
  - **Client Mode:** Connect to server, query for files
  - **Peer Server Mode:** Accept connections from other peers
- **Storage:** Local filesystem (`client_repo_<hostname>/`)
- **Concurrency:** Multi-threaded peer server

---

### Data Flow

#### Publishing a File
```
Client1                   Server
   |                         |
   | Copy file to repo       |
   |------------------------>|
   |                         |
   |-- PUBLISH msg --------->|
   |   {filename}            |
   |                         |
   |                    Store metadata
   |                         |
   |<-- ACK -----------------|
   |                         |
```

#### Fetching a File
```
Client2       Server       Client1
   |             |             |
   |-- FETCH --->|             |
   |             |             |
   |         Lookup peers      |
   |             |             |
   |<- Peer list-|             |
   |   [Client1] |             |
   |             |             |
   |-- Connect P2P ----------->|
   |                           |
   |-- Download request ------>|
   |                           |
   |<- File data --------------|
   |   [binary stream]         |
   |                           |
   | Save to repo              |
   |                           |
   |-- PUBLISH -->|             |
   |   to server  |             |
```

---

### State Management

#### Server State (Per Client)
```python
{
  'hostname': 'client1',
  'ip': '127.0.0.1',
  'port': 6000,
  'files': ['file1.txt', 'file2.pdf'],
  'last_seen': 1698585045.123  # Unix timestamp
}
```

#### Client State
- **Repository:** `client_repo_<hostname>/` directory
- **Connection:** Ephemeral to server, persistent peer server
- **Files:** Stored as regular files in repository directory

---

## Testing

### Automated Testing

Run the test suite:
```bash
python test_suite.py
```

**Tests Include:**
1. Server connection
2. Client registration
3. File publishing
4. File discovery
5. Host ping
6. Fetch non-existent file (error case)
7. Fetch existing file
8. Multiple clients

**Expected Output:**
```
============================================================
P2P File Sharing Application - Test Suite
============================================================

Make sure the server is running on 127.0.0.1:5000
Press Enter to start tests...

=== Test 1: Server Connection ===
✓ Server is running and accepting connections

=== Test 2: Client Registration ===
✓ Client registered successfully

=== Test 3: File Publishing ===
✓ File published successfully

[... more tests ...]

============================================================
Test Summary
============================================================

Tests Passed: 8/8
Success Rate: 100.0%

✓ All tests passed! 🎉
============================================================
```

---

### Manual Testing

#### Test 1: Basic Publish and Fetch

1. Start server: `python server.py`
2. Start client1: `python client.py` (hostname: client1, port: 6000)
3. Publish file: `client1> publish test_file.txt file.txt`
4. Start client2: `python client.py` (hostname: client2, port: 6001)
5. Fetch file: `client2> fetch file.txt`
6. Verify: Both clients should have the file

#### Test 2: Server Commands

1. With clients running, use server commands:
   ```
   Server> list
   Server> discover client1
   Server> ping client1
   ```

#### Test 3: Multiple Clients

1. Start server
2. Start 3-4 clients with different hostnames/ports
3. Each client publishes different files
4. Each client fetches files from others
5. Use `discover` to verify file distribution

---

### Demo Script

Run automated demonstration:
```bash
python demo.py
```

This shows the system in action with simulated clients.

---

## Troubleshooting

### Common Issues

#### 1. "Connection refused" Error
```
[ERROR] Connection failed: Connection refused
```

**Cause:** Server is not running  
**Solution:** Start the server first: `python server.py`

---

#### 2. "Address already in use" Error
```
[ERROR] Failed to start peer server: Address already in use
```

**Cause:** Port is already occupied  
**Solution:** Use a different port number when starting the client

---

#### 3. "File not found" Error
```
[ERROR] Local file not found: test_file.txt
```

**Cause:** The file path is incorrect  
**Solution:** 
- Check the file exists
- Use correct path (absolute or relative)
- Check file name spelling

---

#### 4. "No peers found with file" Error
```
[ERROR] No peers found with the file
```

**Cause:** No other client has published that file  
**Solution:** 
- Make sure another client has published the file first
- Use `discover` command on server to check

---

#### 5. Client Can't Connect to Peer
```
[ERROR] Error downloading from peer
```

**Cause:** Target peer is not running or firewall blocking  
**Solution:**
- Verify peer client is still running
- Check firewall settings
- Try fetching from a different peer

---

### Tips

1. **Start server first** - Always start the server before clients
2. **Unique identifiers** - Each client needs unique hostname and port
3. **Check file paths** - Use absolute paths or ensure files are in current directory
4. **Multiple terminals** - Use separate terminal windows for each component
5. **Monitor server** - Use `list`, `discover`, `ping` to monitor system state

---

## Project Structure

### File Organization

```
init/
├── server.py              # Central server (command-line interface)
├── client.py              # Client (command-line interface)
├── test_suite.py          # Automated tests
├── demo.py                # Demonstration script
├── test_file.txt          # Sample test file
├── launcher.sh            # Linux/Mac launcher
├── launcher.bat           # Windows launcher
├── requirements.txt       # Python dependencies (none needed)
├── DOCUMENTATION.md       # This file (unified documentation)
└── client_repo_*/         # Auto-created client repositories
```

### Source Code

#### server.py
- ~270 lines
- Multi-threaded TCP server
- JSON message handling
- Client registry management
- Command-line interface

#### client.py
- ~400 lines
- Dual-mode operation (client + peer server)
- Command-line interface
- File publishing and fetching
- P2P file transfer
- Repository management

---

### Technical Specifications

**Language:** Python 3.7+  
**Dependencies:** None (standard library only)  
**Protocol:** Custom JSON over TCP  
**Concurrency:** Threading  
**Storage:** Filesystem-based  
**Network:** Socket programming  

**Standard Library Modules Used:**
- `socket` - Network communication
- `threading` - Concurrent operations
- `json` - Message encoding
- `os` - File operations
- `shutil` - File copying
- `pathlib` - Path handling

---

## Command Reference Summary

### Server Commands Quick Reference
| Command | Description | Example |
|---------|-------------|---------|
| `discover <hostname>` | List files on a host | `discover client1` |
| `ping <hostname>` | Check if host is alive | `ping client1` |
| `list` | List all connected clients | `list` |
| `quit` | Stop server | `quit` |

### Client Commands Quick Reference
| Command | Description | Example |
|---------|-------------|---------|
| `publish <lname> <fname>` | Publish local file | `publish file.txt doc.txt` |
| `fetch <fname>` | Fetch file from peers | `fetch doc.txt` |
| `list` | List local repository files | `list` |
| `quit` | Exit client | `quit` |

---

## Additional Features

Beyond the assignment requirements, this implementation includes:

- ✅ `list` command for both server and client
- ✅ Automatic file republishing after fetch
- ✅ File size display
- ✅ Peer selection (first available)
- ✅ Comprehensive error handling
- ✅ Activity logging
- ✅ Timestamp tracking
- ✅ Automated test suite
- ✅ Demo script
- ✅ Launcher scripts

---

## Limitations & Future Enhancements

### Current Limitations
- No authentication/encryption
- No file integrity checks (checksums)
- No resume support for interrupted downloads
- In-memory server state (lost on restart)
- Linear search for file lookup
- Simple peer selection (first available)

### Possible Enhancements
- TLS/SSL encryption
- User authentication
- File checksums (SHA-256)
- Resume/partial downloads
- Persistent server storage
- Smart peer selection (latency-based)
- Bandwidth management
- File compression
- Search functionality
- Web interface

---

## License & Credits

This is an educational project for the Computer Networks course, Assignment 1.

**Assignment:** Develop a Network Application  
**Course:** Computer Networks, Semester 1, 2023-2024  
**Type:** Peer-to-Peer File Sharing Application  

---

## Summary

This P2P File Sharing Application successfully implements:

✅ **All assignment requirements** (100% complete)  
✅ **Command-line interpreters** for server and client  
✅ **Exact command syntax** as specified  
✅ **P2P file transfers** (direct, no server bottleneck)  
✅ **Multi-threaded** operations  
✅ **TCP/IP** networking  
✅ **Custom protocol** (JSON over TCP)  
✅ **Well-documented** (this file)  
✅ **Thoroughly tested** (automated test suite)  
✅ **Easy to use** (simple commands)  

**Ready for demonstration and submission!** 🎉

---

**For questions or issues, refer to the [Troubleshooting](#troubleshooting) section.**

**End of Documentation**
