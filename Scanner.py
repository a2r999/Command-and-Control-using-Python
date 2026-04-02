import socket as net
import sys
from datetime import datetime

# Usage: python scanner.py 192.168.1.5
# If no IP is given, default to localhost for testing
target = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"

# Common ports to check
PORTS = {
    21: "FTP", 
    22: "SSH", 
    23: "TELNET", 
    53: "DNS", 
    80: "HTTP", 
    443: "HTTPS", 
    4444: "L33T_C2"
}

print("-" * 50)
print(f"Scanning Target: {target}")
print(f"Time started: {datetime.now()}")
print("-" * 50)

try:
    for port in PORTS:
        s = net.socket(net.AF_INET, net.SOCK_STREAM)
        net.setdefaulttimeout(1)
        
        # Returns 0 if connection succeeds, error code otherwise
        result = s.connect_ex((target, port))
        
        if result == 0:
            print(f"[+] Port {port} is OPEN ({PORTS[port]})")
        else:
            print(f"[-] Port {port} is CLOSED")
            
        s.close()
        
except KeyboardInterrupt:
    print("\nExiting Program !!!!")
    sys.exit()
except net.gaierror:
    print("\nHostname could not be resolved !!!!")
    sys.exit()
except net.error:
    print("\nServer not responding !!!!")
    sys.exit()
  
