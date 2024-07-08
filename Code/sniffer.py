from scapy.all import sniff, Ether, get_if_list
from datetime import datetime

def get_interface_list():
    try:
        return get_if_list()
    except Exception as e:
        print(f"Error fetching interface list: {str(e)}")
        return []

def start_sniffing(iface, process_packet):
    try:
        sniff(prn=process_packet, iface=iface, store=False)
    except Exception as e:
        print(f"Error: {str(e)}")

def process_packet(packet, tree_sniffer):
    if packet.haslayer(Ether):
        pkt_time = datetime.now().strftime("%H:%M:%S")
        src_mac = packet[Ether].src
        dst_mac = packet[Ether].dst
        protocol = packet[Ether].type
        
        protocol_str = "Unknown"
        if protocol == 0x0800:
            protocol_str = "IPv4"
        elif protocol == 0x0806:
            protocol_str = "ARP"
        elif protocol == 0x86DD:
            protocol_str = "IPv6"
        
        tree_sniffer.insert("", "end", values=(pkt_time, src_mac, dst_mac, protocol_str))
