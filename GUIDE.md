# P2P File Sharing Application - Complete Guide

**Course:** Computer Networks, Semester 1, 2023-2024  
**Assignment:** Network Application Development  
**Date:** October 29, 2025

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Project Overview](#project-overview)
3. [Installation](#installation)
4. [Usage Guide](#usage-guide)
5. [Features](#features)
6. [Architecture](#architecture)
7. [Protocol Specification](#protocol-specification)
8. [Testing](#testing)
9. [File Structure](#file-structure)
10. [Troubleshooting](#troubleshooting)
11. [Advanced Topics](#advanced-topics)

---

# Quick Start

## Three Simple Steps to Get Started

### Step 1: Start the Server

**Option A: Server with GUI (Recommended)**
```bash
python server_gui.py
```
Then click the "Start Server" button in the GUI window.

**Option B: Command-line Server**
```bash
python server.py
```

### Step 2: Start First Client

```bash
python client_gui.py
```

**In the GUI:**
- Hostname: `client1`
- Server: `127.0.0.1:5000`
- Client Port: `6000`
- Click **"Connect"**
- Click **"Browse"** to select a file
- Click **"Publish"** to share it

### Step 3: Start Second Client

Open another terminal:
```bash
python client_gui.py
```

**In the GUI:**
- Hostname: `client2`
- Server: `127.0.0.1:5000`
- Client Port: `6001`
- Click **"Connect"**
- Enter `client1` in "Discover from:" field
- Click **"Discover Files"**
- **Double-click any file** to fetch it automatically!

**That's it!** You now have a working P2P file sharing system! 🎉

---

# Project Overview

## What is This?

A **Peer-to-Peer (P2P) File Sharing Application** where:
- A **central server** coordinates clients but doesn't store files
- **Clients** share files directly with each other
- Files are transferred **peer-to-peer** without server involvement
- Both server and client have **modern GUI interfaces**

## Key Concepts

### Centralized Coordination
- Server tracks which clients are online
- Server knows what files each client has
- Server provides peer lookup service

### Decentralized Transfer
- Files transfer directly between clients
- No server bottleneck for file data
- Efficient bandwidth usage

### Multi-threaded Design
- Server handles multiple clients simultaneously
- Clients can upload/download concurrently
- Non-blocking operations

---

# Installation

## Requirements

- **Python 3.7 or higher**
- **Tkinter** (usually included with Python)
- **Standard library only** (no external packages needed)

## Setup

### Windows
```bash
# Python and tkinter usually pre-installed
# If needed, reinstall Python from python.org with "tcl/tk" option checked
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3 python3-tk
```

### macOS
```bash
# Python 3 from Homebrew includes tkinter
brew install python-tk
```

## Verify Installation

```bash
python --version        # Should show 3.7+
python -m tkinter       # Should open a small test window
```

---

# Usage Guide

## Server GUI Usage

### Starting the Server

1. **Run the server GUI:**
   ```bash
   python server_gui.py
   ```

2. **Configure settings** (optional):
   - Host: `0.0.0.0` (listen on all interfaces)
   - Port: `5000` (default)

3. **Start the server:**
   - Click **"Start Server"** button
   - Status should show "Server running" in green

### Server Features

#### Connected Clients Table
- Real-time view of all connected clients
- Shows: Hostname, IP, Port, File Count, Last Seen
- Auto-refreshes every 5 seconds

#### Server Commands

**Discover Files:**
1. Enter hostname (e.g., "client1")
2. Click **"Discover"** button
3. See list of files in the log

**Ping Host:**
1. Enter hostname
2. Click **"Ping"** button
3. See alive/dead status and last seen time

**List All Clients:**
- Click **"List Clients"** button
- See all connected clients in the log

**Clear Log:**
- Click **"Clear Log"** to clean the activity log

### Server Commands (CLI Version)

If using `server.py` instead:

```bash
Server> list                    # List all clients
Server> discover client1        # Show files on client1
Server> ping client1           # Check if client1 is alive
Server> quit                   # Stop server
```

---

## Client GUI Usage

### Connecting to Server

1. **Run the client GUI:**
   ```bash
   python client_gui.py
   ```

2. **Enter connection details:**
   - **Hostname:** Unique name (e.g., `client1`, `client2`)
   - **Server:** `127.0.0.1:5000` (or server IP:port)
   - **Client Port:** Unique port (e.g., `6000`, `6001`, `6002`)

3. **Connect:**
   - Click **"Connect"** button
   - Status should show "Connected as [hostname]" in green

### Publishing Files

**Method 1: Browse and Publish**
1. Click **"Browse"** button
2. Select a file from your computer
3. Filename auto-fills (edit if desired)
4. Click **"Publish"** button
5. File appears in "Local Repository" list

**Method 2: Direct Path**
1. Type file path in "Publish File" field
2. Enter desired filename
3. Click **"Publish"** button

### Fetching Files (New Easy Way!)

**Discover and Double-Click:**
1. Enter hostname in "Discover from:" field (e.g., `client1`)
2. Click **"Discover Files"** button
3. See available files in "Available Files" list
4. **Double-click any file** to fetch it automatically!
5. File appears in your "Local Repository"

**Manual Fetch (Old Way):**
1. Type filename in "Fetch File:" field
2. Click **"Fetch"** button
3. File is downloaded

### Repository Management

**Local Repository:**
- Shows all files you have published
- Click **"Refresh Repository"** to update the list

**Available Files:**
- Shows files from last discovery
- Double-click to fetch
- Updates each time you discover

---

# Features

## Complete Feature List

### Server Features ✅

#### Core Functionality
- ✅ Track connected clients
- ✅ Store file metadata (not actual files)
- ✅ Handle client registration
- ✅ Provide peer lookup service
- ✅ Multi-threaded connection handling
- ✅ TCP/IP socket communication

#### Server GUI Features
- ✅ Start/Stop server button
- ✅ Real-time client list with auto-refresh
- ✅ Visual command execution (Discover, Ping, List)
- ✅ Activity log with timestamps
- ✅ Connection status indicator
- ✅ Configurable host and port

#### Server CLI Features
- ✅ Command-line interface
- ✅ `discover <hostname>` - List files on host
- ✅ `ping <hostname>` - Check if host is alive
- ✅ `list` - Show all connected clients
- ✅ `quit` - Graceful shutdown

### Client Features ✅

#### Core Functionality
- ✅ Connect to central server
- ✅ Register with hostname and port
- ✅ Publish files to repository
- ✅ Fetch files from peers
- ✅ Direct P2P file transfer
- ✅ Multi-threaded peer server
- ✅ Handle concurrent downloads

#### Client GUI Features
- ✅ Modern graphical interface
- ✅ Connection management panel
- ✅ File browser integration
- ✅ One-click publish
- ✅ **Discover files from other clients** 🆕
- ✅ **Available files list** 🆕
- ✅ **Double-click to fetch** 🆕
- ✅ Local repository viewer
- ✅ Real-time activity log
- ✅ Connection status indicator
- ✅ Error handling and feedback

### Protocol Features ✅

#### Client-Server Protocol
- ✅ JSON message format
- ✅ UTF-8 encoding
- ✅ TCP transport
- ✅ Commands: REGISTER, PUBLISH, FETCH, DISCOVER, PING
- ✅ Status codes (success/error)
- ✅ Error handling

#### Peer-to-Peer Protocol
- ✅ DOWNLOAD command
- ✅ Metadata exchange
- ✅ Binary file transfer
- ✅ Chunked transmission (4KB chunks)
- ✅ Acknowledgment phase

### Additional Features 🌟

- ✅ Automated test suite (8 tests)
- ✅ Demo script
- ✅ Interactive launchers (Windows/Linux)
- ✅ Comprehensive documentation
- ✅ Sample test file
- ✅ Auto-refresh capabilities
- ✅ Visual feedback

---

# Architecture

## System Architecture

```
┌─────────────────────────────────────────┐
│         Central Server                  │
│         Port 5000                       │
│                                         │
│  Stores:                                │
│  - Client registry                      │
│  - File metadata (not actual files)     │
│  - Last seen timestamps                 │
│                                         │
│  Functions:                             │
│  - Client registration                  │
│  - Peer lookup                          │
│  - Discovery service                    │
│  - Status checking                      │
└───────────────┬─────────────────────────┘
                │
                │ JSON/TCP Protocol
                │ (Coordination Only)
                │
    ┌───────────┼───────────┬──────────┐
    │           │           │          │
┌───▼────┐  ┌──▼─────┐  ┌──▼────┐  ┌──▼────┐
│Client1 │  │Client2 │  │Client3│  │Client4│
│        │  │        │  │       │  │       │
│GUI     │  │GUI     │  │GUI    │  │GUI    │
│:6000   │  │:6001   │  │:6002  │  │:6003  │
│        │  │        │  │       │  │       │
│Files:  │  │Files:  │  │Files: │  │Files: │
│• a.txt │  │• b.pdf │  │• c.jpg│  │• d.mp4│
│• e.doc │  │• f.zip │  │• g.txt│  │• h.csv│
└────┬───┘  └───┬────┘  └───┬───┘  └───┬───┘
     │          │           │          │
     └──────────┴───────────┴──────────┘
              P2P File Transfer
         (Direct, Binary, No Server)
```

## Component Architecture

### Server Component

```
Server GUI
    │
    ├─ GUI Layer (Tkinter)
    │   ├─ Settings Panel
    │   ├─ Commands Panel
    │   ├─ Clients Table
    │   └─ Activity Log
    │
    └─ Server Core
        ├─ Socket Listener
        ├─ Client Handler (Threaded)
        ├─ Client Registry
        ├─ File Index
        └─ Command Processor
```

### Client Component

```
Client GUI
    │
    ├─ GUI Layer (Tkinter)
    │   ├─ Connection Panel
    │   ├─ Publish Section
    │   ├─ Discover Section (New!)
    │   ├─ Fetch Section
    │   ├─ Local Repository List
    │   ├─ Available Files List (New!)
    │   └─ Activity Log
    │
    └─ Client Core
        ├─ Server Connection Handler
        ├─ Peer Server (Threaded)
        ├─ File Manager
        ├─ Download Handler
        └─ Repository Manager
```

## Data Flow

### Registration Flow

```
Client                     Server
  |                          |
  |--- TCP Connect --------->|
  |                          |
  |--- REGISTER ------------>|
  |    {hostname, ip, port}  |
  |                          |
  |                     [Store Info]
  |                          |
  |<-- Response -------------|
  |    {status: success}     |
  |                          |
```

### Publish Flow

```
Client                     Server
  |                          |
  |--- PUBLISH ------------->|
  |    {hostname, filename}  |
  |                          |
  |                [Update File List]
  |                          |
  |<-- Response -------------|
  |    {status: success}     |
  |                          |
```

### Fetch Flow

```
Client2                Server               Client1
  |                      |                     |
  |--- FETCH ----------->|                     |
  |    {filename}        |                     |
  |                      |                     |
  |                 [Find Peers]               |
  |                      |                     |
  |<-- Peer List --------|                     |
  |    [{client1...}]    |                     |
  |                      |                     |
  |--- Direct P2P Connection ---------------->|
  |                                            |
  |--- DOWNLOAD -------------------------------->|
  |    {filename}                              |
  |                                            |
  |<-- Metadata --------------------------------|
  |    {size, ...}                             |
  |                                            |
  |--- ACK ----------------------------------->|
  |                                            |
  |<-- Binary File Data ------------------------|
  |    [file contents]                         |
  |                                            |
```

---

# Protocol Specification

## Overview

The application uses two protocols:
1. **Client-Server Protocol** - For coordination (JSON over TCP)
2. **Peer-to-Peer Protocol** - For file transfer (Binary over TCP)

## Client-Server Protocol

### Transport Layer
- **Protocol:** TCP
- **Port:** 5000 (default, configurable)
- **Encoding:** UTF-8
- **Format:** JSON

### Message Format

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
  "message": "description",
  "data": { }
}
```

### Commands

#### 1. REGISTER

**Request:**
```json
{
  "command": "register",
  "hostname": "client1",
  "ip": "192.168.1.100",
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

**Purpose:** Register a client with the server

#### 2. PUBLISH

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

**Purpose:** Notify server that a file is available

#### 3. FETCH

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
      "ip": "192.168.1.100",
      "port": 6000
    }
  ]
}
```

**Purpose:** Get list of peers that have the file

#### 4. DISCOVER

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
  "files": ["file1.txt", "file2.pdf"]
}
```

**Purpose:** List all files on a specific host

#### 5. PING

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
  "last_seen": "2025-10-29 14:30:45"
}
```

**Purpose:** Check if a host is alive

## Peer-to-Peer Protocol

### DOWNLOAD Command

**Phase 1: Request**
```json
{
  "command": "download",
  "filename": "document.pdf"
}
```

**Phase 2: Metadata Response**
```json
{
  "status": "success",
  "filename": "document.pdf",
  "size": 12345
}
```

**Phase 3: Acknowledgment**
```
"OK"
```

**Phase 4: File Transfer**
- Raw binary data
- Sent in 4096-byte chunks
- No encoding

---

# Testing

## Automated Test Suite

### Running Tests

```bash
python test_suite.py
```

### Test Cases

The test suite includes 8 comprehensive tests:

1. **Server Connection Test**
   - Verifies server is running and accepting connections

2. **Client Registration Test**
   - Tests client registration with server
   - Validates response format

3. **File Publish Test**
   - Tests file publishing functionality
   - Verifies server stores metadata

4. **Discover Command Test**
   - Tests discovery of files from a host
   - Validates file list response

5. **Ping Command Test**
   - Tests host alive checking
   - Validates timestamp and status

6. **Fetch Non-existent File Test**
   - Tests error handling for missing files
   - Validates error response

7. **Fetch Existing File Test**
   - Tests peer lookup for existing files
   - Validates peer list response

8. **Multiple Clients Test**
   - Tests concurrent client registrations
   - Validates scalability

### Demo Script

```bash
python demo.py
```

Demonstrates:
- Client registration
- File publishing
- Discovery commands
- Ping functionality
- Error handling

## Manual Testing

### Test Scenario 1: Basic File Sharing

1. **Start server:**
   ```bash
   python server_gui.py
   ```
   Click "Start Server"

2. **Start client1:**
   ```bash
   python client_gui.py
   ```
   - Connect as "client1", port 6000
   - Publish "test_file.txt"

3. **Start client2:**
   ```bash
   python client_gui.py
   ```
   - Connect as "client2", port 6001
   - Discover from "client1"
   - Double-click "test_file.txt" to fetch

4. **Verify:**
   - Check server GUI: See both clients connected
   - Check client2: File appears in Local Repository
   - Check logs: See transfer activity

### Test Scenario 2: Multiple Clients

1. Start server
2. Start 4-5 clients with unique names and ports
3. Each client publishes different files
4. Use discovery to find files
5. Fetch files from different clients
6. Verify all transfers complete successfully

---

# File Structure

```
init/
├── Core Application
│   ├── server.py                    # CLI server
│   ├── server_gui.py               # GUI server ⭐
│   └── client_gui.py               # GUI client with discover
│
├── Testing & Demo
│   ├── test_suite.py               # Automated tests
│   ├── demo.py                     # Demo script
│   └── test_file.txt               # Sample file
│
├── Launchers
│   ├── launcher.sh                 # Linux/Mac launcher
│   └── launcher.bat                # Windows launcher
│
├── Documentation
│   ├── GUIDE.md                    # This complete guide
│   └── requirements.txt            # Dependencies
│
└── Auto-generated
    ├── client_repo_client1/        # Client repositories
    ├── client_repo_client2/
    └── ...
```

---

# Troubleshooting

## Common Issues

### Server Won't Start

**Problem:** Error "Address already in use"

**Solution:**
- Another program is using port 5000
- Kill the process or use a different port
- Change port in server GUI settings

### Client Can't Connect

**Problem:** "Connection refused"

**Solution:**
1. Verify server is running
2. Check server address is correct (127.0.0.1:5000)
3. Check firewall settings
4. Verify network connectivity

### GUI Doesn't Open

**Problem:** "ModuleNotFoundError: No module named 'tkinter'"

**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Windows: Reinstall Python with tcl/tk option

# Mac: Install via Homebrew
brew install python-tk
```

### Port Already in Use

**Problem:** Client error "Address already in use"

**Solution:**
- Each client needs a unique port
- Use: 6000, 6001, 6002, 6003, etc.
- Change port in client connection settings

### File Not Found When Fetching

**Problem:** "No peers found with file"

**Solution:**
1. Verify file was published by another client
2. Use discovery to see available files
3. Check exact filename (case-sensitive)
4. Ensure source client is still connected

### Discovery Returns Empty

**Problem:** No files shown when discovering

**Solution:**
1. Verify hostname is correct
2. Ensure target client has published files
3. Check target client is connected
4. Use server's "List Clients" to see connected hosts

---

# Advanced Topics

## Running on Different Computers

### Server Configuration

1. **Find server IP:**
   ```bash
   # Linux/Mac
   ifconfig | grep inet
   
   # Windows
   ipconfig
   ```

2. **Start server:**
   - Use `0.0.0.0` as host (listens on all interfaces)
   - Note the actual IP address (e.g., 192.168.1.100)

3. **Configure firewall:**
   - Allow inbound connections on port 5000
   - Allow outbound connections for clients

### Client Configuration

1. **Update server address:**
   - Use server's actual IP instead of 127.0.0.1
   - Example: `192.168.1.100:5000`

2. **Connect normally:**
   - Everything else stays the same

## Security Considerations

### Current Implementation
⚠️ **This is an educational project** - Not production-ready

**No Security Features:**
- No encryption (data sent in plain text)
- No authentication (anyone can connect)
- No file integrity checks
- No access control

### Production Recommendations

For real-world use, add:

1. **Encryption:**
   - TLS/SSL for all connections
   - Encrypted file transfers

2. **Authentication:**
   - User login system
   - Token-based authentication
   - Password hashing

3. **Integrity:**
   - File checksums (SHA-256)
   - Verify after download
   - Digital signatures

4. **Access Control:**
   - Permission system
   - Private/public files
   - User groups

5. **Rate Limiting:**
   - Prevent DoS attacks
   - Bandwidth management
   - Connection limits

## Performance Optimization

### For Large Files

Currently uses 4KB chunks. For larger files:

```python
# Increase chunk size
CHUNK_SIZE = 65536  # 64KB

# Add progress callback
def download_with_progress(peer, filename, progress_callback):
    # Update progress during download
    pass
```

### For Many Clients

Current implementation uses linear search O(n):

```python
# Optimize with hash tables
clients = {}  # Already optimal for lookup

# Add indexing for file search
file_index = {}  # filename -> [clients]
```

### Concurrent Downloads

Already supported via threading. To improve:

```python
# Add connection pooling
# Add download queue
# Implement priority system
```

## Extension Ideas

### Phase 2 Enhancements

1. **Progress Bars**
   - Show download/upload progress
   - Estimated time remaining
   - Transfer speed

2. **File Metadata**
   - File size
   - File type
   - Creation date
   - Checksum

3. **Search Functionality**
   - Search files by name pattern
   - Filter by file type
   - Sort by size/date

4. **Multiple Server Support**
   - Connect to multiple servers
   - Server redundancy
   - Failover

5. **Resume Downloads**
   - Save partial downloads
   - Resume interrupted transfers
   - Byte-range requests

6. **Bandwidth Control**
   - Upload/download limits
   - Priority queues
   - QoS management

7. **User Profiles**
   - Save settings
   - Connection history
   - Favorites

8. **Statistics**
   - Files shared
   - Bytes transferred
   - Active time
   - Popular files

### Advanced Features

1. **DHT (Distributed Hash Table)**
   - Eliminate central server
   - Fully decentralized
   - Kademlia implementation

2. **Torrent-like Chunks**
   - Download from multiple peers
   - Parallel chunk transfer
   - Faster downloads

3. **NAT Traversal**
   - STUN/TURN support
   - Work behind firewalls
   - Hole punching

4. **Web Interface**
   - Browser-based client
   - HTML5/JavaScript
   - REST API

5. **Mobile Support**
   - Android app
   - iOS app
   - Cross-platform sync

---

## Assignment Compliance

### Required Features ✅

From assignment PDF - All implemented:

| Requirement | Status | Location |
|------------|--------|----------|
| Centralized server tracks clients | ✅ | `server.py`, `server_gui.py` |
| Server tracks files (metadata only) | ✅ | File index in server |
| Client file repositories | ✅ | `client_repo_*` directories |
| No file data to server | ✅ | Only JSON metadata sent |
| Server provides peer lookup | ✅ | FETCH command |
| Direct P2P file transfer | ✅ | Download from peer |
| Multi-threaded client | ✅ | Threading for downloads |
| `publish lname fname` | ✅ | GUI publish feature |
| `fetch fname` | ✅ | GUI fetch + double-click |
| `discover hostname` | ✅ | Server & client GUI |
| `ping hostname` | ✅ | Server GUI & CLI |
| TCP/IP protocol | ✅ | Socket programming |
| Custom application protocol | ✅ | JSON over TCP |

### Additional Value 🌟

Beyond requirements:

- ✅ Modern GUI for both server and client
- ✅ Real-time monitoring and updates
- ✅ Discover feature in client GUI
- ✅ Double-click to fetch files
- ✅ Visual feedback and logging
- ✅ Comprehensive testing
- ✅ Complete documentation
- ✅ Interactive launchers
- ✅ Demo and test scripts

---

## Quick Reference

### Server GUI Commands

| Action | Steps |
|--------|-------|
| Start server | Click "Start Server" |
| Stop server | Click "Stop Server" |
| Discover files | Enter hostname → Click "Discover" |
| Ping host | Enter hostname → Click "Ping" |
| List clients | Click "List Clients" |
| Clear log | Click "Clear Log" |
| Refresh clients | Click "Refresh Clients" |

### Client GUI Commands

| Action | Steps |
|--------|-------|
| Connect | Enter details → Click "Connect" |
| Publish file | Browse → Select file → Click "Publish" |
| Discover files | Enter hostname → Click "Discover Files" |
| Fetch file (easy) | Double-click file in Available Files |
| Fetch file (manual) | Type filename → Click "Fetch" |
| Refresh repo | Click "Refresh Repository" |

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Double-click | Fetch file from Available Files list |
| Enter | Submit current field |
| Tab | Move between fields |

### Default Ports

| Component | Port |
|-----------|------|
| Server | 5000 |
| Client 1 | 6000 |
| Client 2 | 6001 |
| Client 3 | 6002 |
| Client N | 6000 + N-1 |

---

## Support & Resources

### Getting Help

1. **Check this guide** - Most answers are here
2. **Review test suite** - See working examples
3. **Run demo script** - See system in action
4. **Check logs** - Both server and client logs show activity

### Learning Resources

- **Source Code** - Well-commented, easy to understand
- **Test Suite** - Shows all features in action
- **Demo Script** - Automated walkthrough
- **Protocol Spec** - See how communication works

---

## Conclusion

This P2P File Sharing Application successfully demonstrates:

✅ **Network Programming** - TCP/IP socket programming  
✅ **Protocol Design** - Custom application-layer protocol  
✅ **Distributed Systems** - P2P architecture with central coordination  
✅ **Concurrent Programming** - Multi-threading for scalability  
✅ **GUI Development** - Modern user interfaces  
✅ **Software Engineering** - Clean code, testing, documentation  

**Project Status:** ✅ Complete and ready for use!

### Quick Start Reminder

```bash
# Terminal 1: Start Server
python server_gui.py
# Click "Start Server"

# Terminal 2: Start Client 1
python client_gui.py
# Connect as "client1", port 6000

# Terminal 3: Start Client 2
python client_gui.py
# Connect as "client2", port 6001
# Discover from "client1"
# Double-click files to fetch!
```

**Enjoy your P2P file sharing experience!** 🎉📁🚀

---

*Last updated: October 29, 2025*  
*For Computer Networks Course - Assignment 1*
