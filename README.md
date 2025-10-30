# 📚 P2P File Sharing Application

## 🎯 Quick Navigation

### 📖 **Main Documentation**
👉 **[DOCUMENTATION.md](DOCUMENTATION.md)** ⭐ **START HERE** ⭐

This single file contains **everything you need**:
- Quick Start Guide
- Complete Command Reference
- Protocol Specification
- Architecture Details
- Testing Instructions
- Troubleshooting
- Examples

---

## 🚀 Quick Start (3 Steps)

### 1. Start Server
```bash
python server.py
```

### 2. Start Client 1
```bash
python client.py
# hostname: client1, port: 6000
client1> publish test_file.txt myfile.txt
```

### 3. Start Client 2
```bash
python client.py
# hostname: client2, port: 6001
client2> fetch myfile.txt
```

✅ **Done!** File transferred peer-to-peer!

---

## 📁 Project Files

### Core Application
- **`server.py`** - Server with command-line interface
- **`client.py`** - Client with command-line interface

### Testing
- **`test_suite.py`** - Automated tests
- **`demo.py`** - Demonstration script
- **`test_file.txt`** - Sample file

### Utilities
- **`launcher.sh`** - Linux/Mac launcher
- **`launcher.bat`** - Windows launcher

### Documentation
- **`DOCUMENTATION.md`** - ⭐ Complete unified documentation (read this!)
- **`README.md`** - This index file

---

## ✅ Assignment Requirements

All requirements from the PDF are met:

### Client Commands
- ✅ `publish lname fname` - Publish local file to repository
- ✅ `fetch fname` - Fetch file from peers

### Server Commands
- ✅ `discover hostname` - Discover files on a host
- ✅ `ping hostname` - Check if host is alive

### Technical Requirements
- ✅ TCP/IP protocol stack
- ✅ P2P file transfers
- ✅ Multi-threaded operations
- ✅ Command-line interpreters only
- ✅ Centralized server for coordination
- ✅ Direct peer-to-peer file transfer

---

## 🔧 Command Reference

### Server
```
discover <hostname>   # List files on host
ping <hostname>       # Check if host is alive
list                  # List all clients
quit                  # Stop server
```

### Client
```
publish <lname> <fname>   # Publish local file
fetch <fname>             # Fetch file from peers
list                      # List local files
quit                      # Exit
```

---

## 🧪 Testing

### Automated
```bash
python test_suite.py
```

### Demo
```bash
python demo.py
```

### Manual
Follow the 3-step quick start above!

---

## 💡 Tips

1. **Always start server first**
2. **Each client needs unique hostname and port**
3. **Use absolute or relative file paths for publish**
4. **Check server output to monitor activity**
5. **Use `list` command to see local files**

---

## 🆘 Need Help?

**Read the complete documentation**: `DOCUMENTATION.md`

It contains everything from installation to troubleshooting!

---

## 🎉 Ready to Use!

**Everything you need is in `DOCUMENTATION.md`**

Start reading there, and you'll have everything from installation to advanced usage!

---

**Happy File Sharing!** 🚀📁
