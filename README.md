# Netscan

Netscan is a Python-based network utility tool with a graphical user interface (GUI) built using Tkinter. It provides functionalities for network scanning, port scanning, and packet sniffing.

## Features

- **Network Scanning**: Discover devices on your local network along with their IP addresses, MAC addresses, device names, and vendors.
- **Port Scanning**: Scan common ports on discovered devices to identify open ports and their associated services.
- **Packet Sniffing**: Capture network packets on a selected network interface and display the packet details.

## Requirements

- Python 3.x
- The following Python libraries:
  - `tkinter`
  - `requests`
  - `scapy`
  - `dicttoxml`
  - `json`
  - `threading`
  - `datetime`
  - `socket`
  - `subprocess`

## Installation

1. Clone the repository:

    ```sh
    git clone -b App https://github.com/dxmxtrxs/netscan.git
    ```

2. Install the required Python libraries:

    ```sh
    pip install scapy requests dicttoxml
    ```

3. Run the application with admin/root privileges:

    ```sh
    sudo python3 app.py  # Unix-based systems
    python app.py  # Windows systems (ensure you run the command prompt as administrator)
    ```

## Usage

### Network Scan

1. Open the application.
2. Navigate to the "Network Scan" tab.
3. Click the "Scan network" button to start scanning.
4. Optionally, you can save the scan results by selecting the "Save Scan Results" checkbox and choosing a file format (JSON, XML, TXT).

### Port Scan

1. Double-click on a device in the network scan results to view detailed information.
2. In the details window, click the "Run Port Scan" button to scan for open ports on the selected device.

### Packet Sniffer

1. Navigate to the "Packet Sniffer" tab.
2. Select a network interface from the dropdown menu.
3. Click "Start Sniffing" to begin capturing packets on the selected interface.
4. Click "Stop Sniffing" to stop packet capture.

## Files

- `app.py`: Main application file containing the GUI setup and main functionalities.
- `port_scan.py`: Contains the function for scanning common ports.
- `scanner.py`: Contains functions for network scanning and saving results.
- `sniffer.py`: Contains functions for packet sniffing and processing packets.


## Acknowledgements

- The `scapy` library is used for packet manipulation and network scanning.
- The `requests` library is used for making API calls to retrieve device vendor information.


### Note
To run the script you must first set an API key at the function api_lookup in the scanner.py file. You can get an API key by creating an account on https://macvendors.com


## Contribution
Contributions are welcome! Please feel free to submit a Pull Request.

## Contact
For any inquiries or issues, please open an issue on the [GitHub repository](https://github.com/dxmxtrxs/netscan).

---

Enjoy scanning your network!

---

**Disclaimer**: This tool is for educational purposes only. Use it responsibly and ensure you have permission to scan the network you are using.

