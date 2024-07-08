import time
import requests
import subprocess
from scapy.all import ARP, Ether, srp
import dicttoxml
import json
import socket
import sys

# Function to get the current time formatted as a string
def time_format():
    return time.strftime("%d-%m-%Y_%H:%M:%S")

# Function to make an API request and return a device's manufacturer by MAC address
def api_lookup(mac_address: str, vV_switch: bool) -> str:
    url = f"https://api.macvendors.com/v1/lookup/{mac_address}"
    headers = {"Authorization": "Bearer API_KEY"}
    if vV_switch:
        print("Header for API lookup created")
    api = requests.get(url=url, headers=headers)
    if vV_switch:
        print("API call made")
    if "errors" in api.json():
        if vV_switch:
            print("Vendor was not found")
        return "Unknown"
    else:
        if vV_switch:
            print("Vendor was found successfully")
        return api.json()["data"]["organization_name"]

# Function to get the router's IP address
def get_router_ip(v_switch: bool, vV_switch: bool) -> str:
    get_ip_out = subprocess.run("netstat -rn | grep 'default' | awk '{print $2}'", shell=True, capture_output=True, text=True)
    if v_switch:
        print("Getting router IP")
    ip_out = get_ip_out.stdout
    ip_out = ip_out.split("\n")
    found = False
    for item in ip_out:
        try:
            if len(item.split(".")) == 4:
                ip_out = item
                found = True
                break
            else:
                continue
        except:
            continue
    if found:
        if vV_switch:
            print("Got router IP")
        return ip_out
    else:
        print(f"Unsuccessful automatic router IP finder :(\nResult:\n{ip_out}")
        sys.exit()

# Function to create an ARP table map
def arp_table_mapper(ip_addresses, v_switch: bool, vV_switch: bool) -> dict:
    arp_table_map = {}
    try:
        arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_addresses)
        if v_switch:
            print("Requested ARP packet")
        responses, _ = srp(arp_request, timeout=2, verbose=False)
        if vV_switch:
            print("Collected ARP responses")
        id_counter = 0
        if v_switch:
            print("API calls started")
        for _, response in responses:
            arp_table_map[id_counter] = {
                'ip': response.psrc,
                'mac_address': response.hwsrc,
                'device_name': get_device_name(response.psrc, vV_switch),
                'vendor': api_lookup(response.hwsrc, vV_switch)
            }
            id_counter += 1
        if v_switch:
            print("API calls done")
    except Exception as e:
        print("Error retrieving ARP table:", e)
    return arp_table_map

# Function to get the device name from its IP address
def get_device_name(ip_address, vV_switch: bool):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip_address)
        if vV_switch:
            print("Hostname for IP", ip_address, "is", hostname)
        return hostname
    except socket.herror:
        if vV_switch:
            print("Failed to get hostname for:", ip_address)
        return "Unknown"

# Function to get the subnet mask
def get_sub_mask(v_switch: bool) -> str:
    if v_switch:
        print("Getting subnet mask..")
    def subnet_mask_calculation(subnet_mask):
        mask_octets = subnet_mask.split('.')
        binary_mask = ''.join(format(int(octet), '08b') for octet in mask_octets)
        cidr = sum(bit == '1' for bit in binary_mask)
        return cidr
    sub_mask = subprocess.run("ipconfig getoption en0 subnet_mask", shell=True, capture_output=True, text=True)
    sub_mask = sub_mask.stdout.split("\n")[0]
    if v_switch:
        print("Subnet mask found successfully!")
    return str(subnet_mask_calculation(sub_mask))

# Function to save the scan result in the specified format
def save(scan_result: dict, form: str, file_name: str, v_switch: bool):
    if v_switch:
        print("Saving file..")
    if form == "json":
        with open(f"{file_name}.json", "w") as file:
            json.dump(scan_result, file, indent=4)
    elif form == "xml":
        with open(f"{file_name}.xml", "w") as file:
            xml_data = dicttoxml.dicttoxml(scan_result)
            file.write(xml_data.decode('utf-8'))
    else:
        with open(f"{file_name}.txt", "w") as file:
            file.write(str(scan_result))
    if v_switch:
        print(f"File saved successfully as a {form} file.")

# Function to display the scan result
def display_result(mapped_network: dict, save_file: bool, save_type: str, file_name: str, v_switch: bool):
    if v_switch:
        print("\n")
    print("\033[91mID\tIP ADDRESS\tMAC ADDRESS\t\tDEVICE NAME\t\tVENDOR\033[0m")
    for identifier, content in mapped_network.items():
        tmp_line = f"{identifier}\t{content['ip']}\t{content['mac_address']}\t{content['device_name']} \t\t{content['vendor']}"
        print(tmp_line)
    if save_file:
        save(scan_result=mapped_network, form=save_type, file_name=file_name, v_switch=v_switch)

# Main scan function
def scan(v_switch: bool = False, vV_switch: bool = False, save_file: bool = False, save_type: str = "json", file_name: str = time_format()) -> dict:
    router_ip = get_router_ip(v_switch, vV_switch)
    subnet_mask = get_sub_mask(v_switch)
    result = arp_table_mapper(f"{router_ip}/{subnet_mask}", v_switch, vV_switch)
    display_result(result, save_file, save_type, file_name, v_switch)
    return result
