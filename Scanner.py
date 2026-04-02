import socket as net
import socket as net
import sys
from datetime import datetime

target = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"

PORTS = {
    21: "FTP", 
    22: "SSH", 
    23: "TELNET", 
    53: "DNS", 
    80: "HTTP", 
    443: "HTTPS", 
    4444: "L33T_C2"
}

def start_scan():
    print("-" * 50)
    print(f"[*] Scanning Target: {target}")
    print(f"[*] Time started: {datetime.now()}")
    print("-" * 50)

    try:
        for port, service in PORTS.items():
            s = net.socket(net.AF_INET, net.SOCK_STREAM)
            s.settimeout(1) 
            
            result = s.connect_ex((target, port))
            
            if result == 0:
                print(f"[+] Port {port:<5} is OPEN   ({service})")
            else:
                print(f"[-] Port {port:<5} is CLOSED")
                
            s.close()
            
    except KeyboardInterrupt:
        print("\n[!] Scan aborted by user.")
        sys.exit()
    except net.gaierror:
        print("\n[!] Hostname could not be resolved.")
        sys.exit()
    except net.error:
        print("\n[!] Server not responding.")
        sys.exit()

if __name__ == "__main__":
    start_scan()
