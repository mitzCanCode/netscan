# Network Scanner

## Overview
This Python-based network scanner allows you to scan your local network to identify connected devices, their IP addresses, MAC addresses, device names, and vendors. It utilizes ARP requests to map the network and provides options to save the results in various formats (JSON, XML, or plain text).

## Features
- **Network Scanning**: Identifies all devices connected to the local network.
- **Vendor Lookup**: Retrieves the vendor information for each device using its MAC address.
- **Device Information**: Displays IP address, MAC address, device name, and vendor for each device.
- **Save Results**: Save scan results in JSON, XML, or plain text format.
- **Verbose Output**: Optional verbose output for detailed logs.
- **Customizable File Name**: Specify custom file names for saved results.

## Installation
### Prerequisites
- Python 3.x
- Required Python packages:
  - `scapy`
  - `requests`
  - `dicttoxml`
  - `rainbowtext`

### Installing Dependencies
```bash
pip install scapy requests dicttoxml rainbowtext
```


### Customization
You can customize the scan by modifying the script directly. Here are some customization options:
- **API Key for MAC Vendor Lookup**: Replace the placeholder `YOUR_API_KEY` in the `api_lookup` function with your actual API key.
- **Verbose and Very Verbose Output**: Adjust the verbosity by using `-v` and `-vv` options.

## Code Overview
### Main Script: `netscan.py`
This script includes functions to:
- Display a colorful ASCII logo.
- Scan the local network using ARP requests.
- Lookup device vendor information via an API.
- Save scan results in different formats (JSON, XML, TXT).
- Display the scan results in a formatted table.

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

```

