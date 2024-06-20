# Network Scanner

## Overview
This Python-based network scanner allows you to scan your local network to identify connected devices, their IP addresses, MAC addresses, device names, and vendors. It utilizes ARP requests to map the network and provides options to save the results in various formats (JSON, XML, or plain text).
It also includes a packet sniffer, a scanner that pings every device on the network and a command to check for open ports on found devices

## Installation
### Prerequisites
- Python 3.x
- Nmap (Download page: https://nmap.org/download)
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
- Scan the local network using ARP requests.
- Lookup device vendor information via an API.
- Save scan results in different formats (JSON, XML, TXT).
- Display the scan results in a formatted table.
- Sniff packets on the network.
- Check for open ports on found devices.
- Scan by pinging each device on the network.

## Contribution
Contributions are welcome! Please feel free to submit a Pull Request.

## Contact
For any inquiries or issues, please open an issue on the [GitHub repository](https://github.com/dxmxtrxs/netscan).

---

Enjoy scanning your network!

---

**Disclaimer**: This tool is for educational purposes only. Use it responsibly and ensure you have permission to scan the network you are using.

## Note
You can get an API key by creating an account on https://macvendors.com


