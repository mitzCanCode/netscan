from scapy.all import sniff, Ether, get_if_list
from datetime import datetime

sniffing = False  # Global flag to control sniffing
packet_store = {}  # Store packets for later retrieval

def get_interface_list():
    try:
        return get_if_list()
    except Exception as e:
        print(f"Error fetching interface list: {str(e)}")
        return []

def start_sniffing(iface, process_packet):
    global sniffing
    sniffing = True
    try:
        sniff(prn=lambda pkt: process_packet(pkt) if sniffing else None, iface=iface, store=False, stop_filter=lambda x: not sniffing)
    except Exception as e:
        print(f"Error: {str(e)}")

def stop_sniffing():
    global sniffing
    sniffing = False

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
        
        pkt_id = len(packet_store)  # Unique identifier for the packet
        packet_store[pkt_id] = packet  # Store the packet
        
        tree_sniffer.insert("", "end", iid=pkt_id, values=(pkt_time, src_mac, dst_mac, protocol_str))
