#!/bin/bash

# P2P File Sharing Application Launcher
# This script helps you start the server and clients easily

show_menu() {
    clear
    echo "=========================================="
    echo "  P2P File Sharing - Launcher"
    echo "=========================================="
    echo ""
    echo "1. Start Server"
    echo "2. Start Client (GUI)"
    echo "3. Run Test Suite"
    echo "4. View Documentation"
    echo "5. Clean Repository Files"
    echo "6. Exit"
    echo ""
    echo -n "Choose an option [1-6]: "
}

start_server() {
    echo ""
    echo "Starting server..."
    echo "Press Ctrl+C to stop"
    echo ""
    python3 server.py
}

start_client() {
    echo ""
    echo "Starting client..."
    echo "Make sure to:"
    echo "  1. Use a unique hostname (e.g., client1, client2, ...)"
    echo "  2. Use a unique port (e.g., 6000, 6001, 6002, ...)"
    echo ""
    python3 client.py
}

run_tests() {
    echo ""
    echo "Running test suite..."
    echo "Make sure the server is running first!"
    echo ""
    read -p "Is the server running? (y/n): " answer
    if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
        python3 test_suite.py
    else
        echo "Please start the server first (option 1)"
    fi
    echo ""
    read -p "Press Enter to continue..."
}

view_docs() {
    clear
    echo "=========================================="
    echo "  Documentation Files"
    echo "=========================================="
    echo ""
    echo "1. README.md - Main documentation"
    echo "2. QUICK_START.md - Quick start guide"
    echo "3. PROTOCOL_SPECIFICATION.md - Protocol details"
    echo ""
    echo "You can view these files with any text editor or markdown viewer"
    echo ""
    read -p "Press Enter to continue..."
}

clean_repos() {
    echo ""
    echo "This will delete all client repository directories"
    echo "  (client_repo_*)"
    echo ""
    read -p "Are you sure? (y/n): " answer
    if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
        rm -rf client_repo_*
        echo "Repository directories cleaned"
    else
        echo "Cancelled"
    fi
    echo ""
    read -p "Press Enter to continue..."
}

# Main loop
while true; do
    show_menu
    read choice
    
    case $choice in
        1)
            start_server
            ;;
        2)
            start_client
            ;;
        3)
            run_tests
            ;;
        4)
            view_docs
            ;;
        5)
            clean_repos
            ;;
        6)
            echo ""
            echo "Goodbye!"
            exit 0
            ;;
        *)
            echo ""
            echo "Invalid option. Please try again."
            sleep 2
            ;;
    esac
done
