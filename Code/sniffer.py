import os  # Importing the 'os' module to interact with the operating system
import sys  # Importing the 'sys' module to access system-specific parameters and functions
from scapy.all import sniff  # Importing the 'sniff' function from the 'scapy' library for packet sniffing
from scapy.layers.inet import IP, TCP, UDP  # Importing specific layers from scapy for handling IP, TCP, and UDP packets
from scapy.layers.l2 import ARP, Ether  # Importing ARP and Ether layers from scapy for handling Ethernet and ARP packets
import time

packet_list = []  # Initializing an empty list to store packet information

# Function to get the current time formatted as a string
def time_format():
    return time.strftime("%d-%m-%Y_%H:%M:%S")

def packet_callback(packet):  # Defining a callback function to process each sniffed packet
    global packet_list  # Accessing the global packet_list variable to store packet information
    
    # Initializing variables to store packet information
    protocol = "Unknown"
    src_ip = "N/A"
    dst_ip = "N/A"
    src_mac = "N/A"
    dst_mac = "N/A"
    
    if packet.haslayer(Ether):  # Checking if the packet has an Ethernet layer
        ether_layer = packet.getlayer(Ether)  # Extracting the Ethernet layer
        src_mac = ether_layer.src  # Extracting the source MAC address
        dst_mac = ether_layer.dst  # Extracting the destination MAC address
    
    if packet.haslayer(IP):  # Checking if the packet has an IP layer
        ip_layer = packet.getlayer(IP)  # Extracting the IP layer
        src_ip = ip_layer.src  # Extracting the source IP address
        dst_ip = ip_layer.dst  # Extracting the destination IP address
        
    if packet.haslayer(TCP):  # Checking if the packet has a TCP layer
        protocol = "TCP"
    elif packet.haslayer(UDP):  # Checking if the packet has a UDP layer
        protocol = "UDP"
    elif packet.haslayer(ARP):  # Checking if the packet has an ARP layer
        protocol = "ARP"
    elif packet.haslayer(IP):  # Checking if the packet has an IP layer (if not already detected)
        protocol = "IP"
    else:  # If the protocol is not recognized
        protocol = packet.getlayer(0).name  # Extracting the name of the first layer
    
    # Creating a string to represent packet information
    packet_info = f"Packet: {packet.summary()} | Source IP: {src_ip}  |  Source MAC: {src_mac} | Destination IP: {dst_ip}  |  Destination MAC: {dst_mac} | Protocol: {protocol} | Time: {time_format()}"
    packet_list.append(packet_info)  # Appending packet information to the packet_list
    print(packet_info)  # Printing packet information
    print("-" * 50)  # Printing a separator line

def sniff_network(save: bool = False, name: str = "sniffed_packets.txt"):  # Defining a function to start sniffing on the network
    # Start sniffing on the network interface (replace 'eth0' with your interface)
    sniff(prn=packet_callback, store=0)  # Calling the 'sniff' function to capture packets and invoke the callback function
    
    # If save flag is True, save sniffed packets to a file
    if save == True:
        with open(name, "w") as file:  # Opening a file in write mode to save packet information
            temp_packets = "\n".join(packet_list)  # Joining packet information into a single string
            file.write(temp_packets)  # Writing packet information to the file
    

if __name__ == "__main__":  # Executing the following code if the script is run directly
    sniff_network()  # Calling the sniff_network function to start packet sniffing
