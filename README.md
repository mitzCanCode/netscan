# Network Scanner

## Overview
This Python-based network scanner allows you to scan your local network to identify connected devices, their IP addresses, MAC addresses, device names, and vendors. It utilizes ARP requests to map the network and provides options to save the results in various formats (JSON, XML, or plain text). Additionally, it includes a packet sniffer, a port scanner, and a ping based scanner to find every device on the network.

## Installation
### Prerequisites
- Python 3.x
- Required Python packages:
  - `scapy`
  - `requests`
  - `dicttoxml`


### Installing Dependencies
```bash
pip install scapy requests dicttoxml 
```

### How to run
```bash
sudo python3 netscan.py
```
### Note
To run the script you must first set an API key at the function api_lookup in the scanner.py file. You can get an API key by creating an account on https://macvendors.com

## Capabilities 
This script includes functions to:
- Network Scanning: Scan the local network using ARP requests.
- Vendor Lookup: Lookup device vendor information via an API.
- Save Results: Save scan results in different formats (JSON, XML, TXT).
- Packet Sniffing: Sniff packets on the network.
- Ping Scan: Scan by pinging each device on the network.
- Port Scanning: Scan for open ports on devices in the network.

## Contribution
Contributions are welcome! Please feel free to submit a Pull Request.

## Contact
For any inquiries or issues, please open an issue on the [GitHub repository](https://github.com/dxmxtrxs/netscan).

---

Enjoy scanning your network!

---

**Disclaimer**: This tool is for educational purposes only. Use it responsibly and ensure you have permission to scan the network you are using.


