import socket

# List of common ports to scan
common_ports = {
    20: "FTP-Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    67: "DHCP",
    68: "DHCP",
    69: "TFTP",
    80: "HTTP",
    110: "POP3",
    119: "NNTP",
    123: "NTP",
    135: "RPC",
    137: "NetBIOS",
    138: "NetBIOS",
    139: "NetBIOS",
    143: "IMAP",
    161: "SNMP",
    162: "SNMP-Trap",
    179: "BGP",
    194: "IRC",
    201: "AppleTalk",
    443: "HTTPS",
    445: "SMB",
    465: "SMTPS",
    500: "IKE",
    514: "Syslog",
    515: "LPD",
    520: "RIP",
    587: "SMTP-Submission",
    631: "IPP",
    636: "LDAPS",
    993: "IMAPS",
    995: "POP3S",
    1025: "NFS or IIS",
    1026: "Windows-Messenger",
    1027: "Windows-Messenger",
    1433: "MSSQL",
    1434: "MSSQL",
    1723: "PPTP",
    1900: "SSDP",
    2000: "Cisco-SCCP",
    2002: "Globe",
    2049: "NFS",
    2121: "FTP-Proxy",
    3306: "MySQL",
    3389: "RDP",
    3689: "iTunes",
    3690: "Subversion",
    4045: "NFS-Lock",
    5060: "SIP",
    5900: "VNC",
    6000: "X11",
    6667: "IRC",
    8000: "HTTP-Alternative",
    8080: "HTTP-Proxy",
    8443: "HTTPS-Alt",
    8888: "HTTP-Alt",
    25565: "Minecraft"
}

def scan_ports(ip):
    print("Scan started")
    open_ports = []
    for port, service in common_ports.items():
        print(f"Scanning {port}({service})")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Timeout of 1 second
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append((port, service))
        sock.close()
    return open_ports

def main():
    ip = input("Enter the IP address to scan: ")
    print(f"Scanning {ip} for common ports...")
    open_ports = scan_ports(ip)
    if open_ports:
        print(f"Open ports on {ip}:")
        for port, service in open_ports:
            print(f"Port {port}: {service}")
    else:
        print(f"No common ports are open on {ip}.")

if __name__ == "__main__":
    main()
