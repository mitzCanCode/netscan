import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
from datetime import datetime
import os
import sys
from scanner import scan
from port_scan import scan_ports
from sniffer import start_sniffing, stop_sniffing, process_packet, get_interface_list, packet_store  # Import the updated functions
from scapy.utils import hexdump

def check_admin():
    if os.name == 'nt':
        # Windows
        is_admin = os.system("net session >nul 2>&1")
        if is_admin != 0:
            show_warning()
            sys.exit(0)
    else:
        # Unix/Linux/MacOS
        is_admin = os.geteuid() == 0
        if not is_admin:
            show_warning()
            sys.exit(0)

def show_warning():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showwarning("Warning", "You must run this program as root/admin.")
    root.destroy()

def scan_network():
    try:
        status_label.config(text="Scanning network...")
        progress_bar.pack(pady=10, fill=tk.X)
        progress_bar.start()
        threading.Thread(target=perform_scan).start()
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")
        progress_bar.stop()
        progress_bar.pack_forget()

def perform_scan():
    try:
        save_file = save_file_var.get()
        save_type = ""
        if save_file:
            if save_type_var.get() == 1:
                save_type = "json"
            elif save_type_var.get() == 2:
                save_type = "xml"
            elif save_type_var.get() == 3:
                save_type = "txt"
        
        file_name = file_name_entry.get().strip()
        if not file_name:
            current_time = datetime.now()
            file_name = f"scan-{current_time.strftime('%H-%M-%d-%m-%Y')}"
        
        sample_dict = scan(v_switch=True, vV_switch=True, save_file=save_file, save_type=save_type, file_name=file_name)
        
        for row in tree.get_children():
            tree.delete(row)
        
        for key, value in sample_dict.items():
            tree.insert("", "end", values=(key, value['ip'], value['mac_address'], value['device_name'], value['vendor']))
        
        status_label.config(text="Scan complete.")
        progress_bar.stop()
        progress_bar.pack_forget()
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")
        progress_bar.stop()
        progress_bar.pack_forget()

def show_hide_file_format():
    if save_file_var.get():
        json_radio.pack(anchor=tk.W)
        xml_radio.pack(anchor=tk.W)
        txt_radio.pack(anchor=tk.W)
        file_name_label.pack(anchor=tk.W)
        file_name_entry.pack(anchor=tk.W)
    else:
        json_radio.pack_forget()
        xml_radio.pack_forget()
        txt_radio.pack_forget()
        file_name_label.pack_forget()
        file_name_entry.pack_forget()

def show_device_details(event):
    selected_item = tree.selection()[0]
    device_info = tree.item(selected_item, "values")
    ip_address = device_info[1]
    
    detail_window = tk.Toplevel(root)
    detail_window.title(f"Details for {device_info[3]} ({ip_address})")
    detail_window.geometry("400x300")
    
    details = f"ID: {device_info[0]}\nIP Address: {ip_address}\nMAC Address: {device_info[2]}\nDevice Name: {device_info[3]}\nVendor: {device_info[4]}"
    ttk.Label(detail_window, text=details).pack(pady=10)

    def run_port_scan():
        result = scan_ports(ip_address)
        found_ports_str = ""
        if result:
            for found_port in result:
                if found_ports_str:
                    found_ports_str += f"\nPort: {found_port[0]} {found_port[1]}"
                else:
                    found_ports_str += f"\nPort: {found_port[0]} {found_port[1]}"
        else:
            found_ports_str = "No open ports found"
            
        ports_text.set(found_ports_str)
    
    ports_text = tk.StringVar()
    ports_text.set("Ports will be displayed here.")
    
    ttk.Label(detail_window, text="Port Scan Results:").pack(pady=(10, 0))
    ttk.Label(detail_window, textvariable=ports_text).pack(pady=5)
    ttk.Button(detail_window, text="Run Port Scan", command=run_port_scan).pack(pady=10)

def start_packet_sniffing():
    try:
        iface = interface_combobox.get().strip()
        if not iface:
            status_label_sniffer.config(text="Please select a network interface.")
            return
        
        status_label_sniffer.config(text=f"Starting packet sniffing on interface {iface}...")
        
        # Clear existing entries in the Treeview
        for item in tree_sniffer.get_children():
            tree_sniffer.delete(item)
        
        # Start packet sniffing and process each packet
        threading.Thread(target=start_sniffing, args=(iface, lambda pkt: process_packet(pkt, tree_sniffer))).start()
        
        # Hide the start button once sniffing has started
        start_button.pack_forget()
        # Show the stop button
        stop_button.pack(side=tk.RIGHT, padx=10)
    except Exception as e:
        status_label_sniffer.config(text=f"Error: {str(e)}")

def stop_sniffing_action():
    stop_sniffing()
    status_label_sniffer.config(text="Packet sniffer stopped.")
    
    # Hide the stop button after stopping sniffing
    stop_button.pack_forget()
    # Show the start button
    start_button.pack(side=tk.RIGHT, padx=10)

def show_packet_details(event):
    selected_item = tree_sniffer.selection()[0]
    pkt_id = int(selected_item)
    packet = packet_store[pkt_id]
    
    detail_window = tk.Toplevel(root)
    detail_window.title(f"Packet Details (ID: {pkt_id})")
    detail_window.geometry("800x600")
    
    # Get packet summary
    pkt_summary = packet.summary()
    
    # Parse packet layers and fields
    pkt_details = []
    for layer in packet.layers():
        pkt_details.append(f"Layer: {layer}")
        for field, value in packet[layer].fields.items():
            pkt_details.append(f"{field.capitalize()}: {value}")
        pkt_details.append("")  # Blank line for separation
    
    # Get hexadecimal dump of the packet
    hex_dump = hexdump(packet, dump=True)
    
    summary_label = ttk.Label(detail_window, text=f"Packet Summary:\n{pkt_summary}")
    summary_label.pack(pady=10)
    
    details_text = tk.Text(detail_window, wrap=tk.WORD)
    details_text.insert(tk.END, "\n".join(pkt_details))
    details_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    
    hexdump_text = tk.Text(detail_window, wrap=tk.WORD)
    hexdump_text.insert(tk.END, hex_dump)
    hexdump_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

# Check if the user has admin rights before initializing the main application window
check_admin()

# Set up the main application window
root = tk.Tk()
root.title("Netscan")
root.geometry("1000x700")

# Create a notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True, fill=tk.BOTH)

# Create the network scan tab
network_scan_tab = ttk.Frame(notebook)
notebook.add(network_scan_tab, text="Network Scan")

tree_frame = ttk.Frame(network_scan_tab)
tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

columns = ("ID", "IP Address", "MAC Address", "Device Name", "Vendor")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER)

tree.pack(fill=tk.BOTH, expand=True)

tree.bind("<Double-1>", show_device_details)  # Bind double-click event

bottom_frame = ttk.Frame(network_scan_tab)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

status_label = ttk.Label(bottom_frame, text="Click 'Scan network' to start.")
status_label.pack(side=tk.LEFT, padx=10)

progress_bar = ttk.Progressbar(bottom_frame, mode='indeterminate')

display_button = ttk.Button(bottom_frame, text="Scan network", command=scan_network)
display_button.pack(side=tk.RIGHT, padx=10)

save_file_var = tk.BooleanVar()
save_file_checkbox = ttk.Checkbutton(bottom_frame, text="Save Scan Results", variable=save_file_var, command=show_hide_file_format)
save_file_checkbox.pack(side=tk.RIGHT, padx=10)

save_type_var = tk.IntVar()
json_radio = ttk.Radiobutton(bottom_frame, text="JSON", variable=save_type_var, value=1)
xml_radio = ttk.Radiobutton(bottom_frame, text="XML", variable=save_type_var, value=2)
txt_radio = ttk.Radiobutton(bottom_frame, text="TXT", variable=save_type_var, value=3)

file_name_label = ttk.Label(bottom_frame, text="File Name:")
file_name_entry = ttk.Entry(bottom_frame)

# Hide these elements initially
json_radio.pack_forget()
xml_radio.pack_forget()
txt_radio.pack_forget()
file_name_label.pack_forget()
file_name_entry.pack_forget()

# Create the packet sniffer tab
packet_sniffer_tab = ttk.Frame(notebook)
notebook.add(packet_sniffer_tab, text="Packet Sniffer")

sniffer_frame = ttk.Frame(packet_sniffer_tab)
sniffer_frame.pack(pady=10, fill=tk.BOTH, expand=True)

columns_sniffer = ("Time", "Source MAC", "Destination MAC", "Protocol")
tree_sniffer = ttk.Treeview(sniffer_frame, columns=columns_sniffer, show="headings")

for col in columns_sniffer:
    tree_sniffer.heading(col, text=col)
    tree_sniffer.column(col, anchor=tk.CENTER)

tree_sniffer.pack(fill=tk.BOTH, expand=True)

tree_sniffer.bind("<Double-1>", show_packet_details)  # Bind double-click event

bottom_frame_sniffer = ttk.Frame(packet_sniffer_tab)
bottom_frame_sniffer.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

status_label_sniffer = ttk.Label(bottom_frame_sniffer, text="Select an interface and click 'Start Sniffing' to begin.")
status_label_sniffer.pack(side=tk.LEFT, padx=10)

interface_label = ttk.Label(bottom_frame_sniffer, text="Interface:")
interface_label.pack(side=tk.LEFT, padx=10)

interface_list = get_interface_list()
interface_combobox = ttk.Combobox(bottom_frame_sniffer, values=interface_list, state="readonly")
interface_combobox.pack(side=tk.LEFT, padx=10)
interface_combobox.set(interface_list[0] if interface_list else "No interfaces found")

start_button = ttk.Button(bottom_frame_sniffer, text="Start Sniffing", command=start_packet_sniffing)
start_button.pack(side=tk.RIGHT, padx=10)

stop_button = ttk.Button(bottom_frame_sniffer, text="Stop Sniffing", command=stop_sniffing_action)
# Initially hide the stop button
stop_button.pack_forget()

root.mainloop()
