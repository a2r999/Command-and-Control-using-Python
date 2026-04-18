PyC2 : Lightweight Command & Control tool.

Author: Abhijit Rekhi


This repository contains a lightweight, synchronous Python Command and Control (C2) tool. It was developed to demonstrate the fundamental networking mechanics of remote administration tools and malware, specifically focusing on socket programming, JSON-based metadata handshakes, and binary chunking for file exfiltration.


## Architecture
The tool consists of three standalone Python scripts:
 * scanner.py: A minimalist TCP port scanner used for initial network reconnaissance. Applies targeted timeouts to rapidly identify listening C2 servers or vulnerable services.
 * listener.py: The central C2 server. It binds to a designated port, accepts incoming connections from the payload, and provides an interactive shell. It handles JSON-structured data to seamlessly switch between standard stdout/stderr streams and binary file transfer modes.
 * payload.py: This establishes a persistent outbound TCP connection to the listener.
   * OpSec Feature: If renamed to payload.pyw and executed on a Windows host, it leverages pythonw.exe and specific subprocess creation flags (0x08000000) to execute entirely in the background without spawning visible console windows.
Features
 * Remote Command Execution (RCE): Maps standard operating system commands through a reverse shell via subprocess.Popen.
 * Reliable File Exfiltration: Custom file-transfer implementation that handles large files by sending data in 4096-byte chunks, preventing memory buffer overflows.
 * Structured Handshakes: Uses JSON for metadata transfer (filename, filesize) prior to raw binary transmission, ensuring the listener correctly parses incoming data streams.
 * Cross-Platform Capability: Core networking logic relies exclusively on Python standard libraries, making it compatible across Windows, Linux, and macOS environments.

## Setup & Installation
It is recommended to run this tool within an isolated virtual environment.
1. Clone the repository and navigate to the directory
mkdir C2_Project && cd C2_Project

2. Initialize a Python virtual environment
python -m venv .venv

3. Activate the environment
 On Windows:
.venv\Scripts\activate
 On Linux/macOS:
source .venv/bin/activate

4. Ensure pip is updated (no external dependencies required)
python -m pip install --upgrade pip

## Usage Guide
1. Initial Reconnaissance
Use the scanner to verify target status or confirm your listener port is open.
python scanner.py <TARGET_IP>

2. Start the Listener
Initialize the C2 server to await incoming connections. By default, it listens on 0.0.0.0:4444.
python listener.py

3. Deploy the Payload
Execute the payload on the target machine. Ensure the CALLBACK_IP variable in the script is set to the Listener's IP address.
## Standard execution
python payload.py

## Stealth execution (Windows only, requires .pyw extension)
pythonw payload.pyw

4. Interacting and Exfiltrating
Once the connection is established, the Listener will drop into an interactive shell Shell> .
 * Standard Commands: Type any valid OS command (e.g., whoami, dir, ifconfig).
 * File Transfer: Use the custom download syntax to exfiltrate files. The file will be saved locally with a downloaded_ prefix.
   Shell> download C:\path\to\target\secret.pdf

 * Terminate: Use the exit command to safely terminate the connection.

## ⚠️ Legal & Ethical Disclaimer
This tool is strictly for educational purposes and authorized Red Team engagements. Do not deploy this software on any network or system where you do not have explicit, documented permission. The authors and associated entities assume no liability for misuse.
