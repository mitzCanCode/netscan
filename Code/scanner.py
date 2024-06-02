import time
import requests
import subprocess
from scapy.all import ARP, Ether, srp
from scapy.all import *
import dicttoxml
import json

# Function to get the current time formatted as a string
def time_format():
    return time.strftime("%d-%m-%Y_%H:%M:%S")

def scan(v_switch: bool = False, vV_switch: bool = False, save_file: bool = False, save_type: str = "json", file_name: str = time_format()) -> dict:
    # A function that makes an api request and returns a devices manufacturer by their mac address.
    def api_lookup(mac_address: str) -> str:
        # Specifying the url the request will be made to including the mac address.
        url = f"https://api.macvendors.com/v1/lookup/{mac_address}"
        # Specifying the headers as well as the api key.
        headers = {"Authorization": "Bearer API_KEY"}
        if vV_switch:
            print("Header for api lookup created")
        # Making the api request.
        api = requests.get(url= url, headers= headers)
        if vV_switch:
            print("API call made")
        # In the case of the API not being able to find the vendor it will return unknown.
        if "errors" in api.json():
            if vV_switch:
                print("Vendor was not found")
            return "Unknown"
        # If no errors occur it will return the vendor.
        else:
            if vV_switch:
                print("Vendor was found successfuly")
            return api.json()["data"]["organization_name"]
        

    # A command used to find the routers ip.
    def get_router_ip() -> str:
        # Runnning th command.
        get_ip_out = subprocess.run("netstat -rn | grep 'default' | awk '{print $2}'", shell=True, capture_output=True, text=True)
        if v_switch:
            print("Getting router IP")
        # Retrieving the output.
        ip_out = get_ip_out.stdout
        ip_out_raw = ip_out
        # Spliting the result at every line break.
        ip_out = ip_out.split("\n")
        # Checking if the router ip has the correct format.
        for item in ip_out:
            # Checking if there are 4 groups of numbers seperated by periods.
            try:
                if len(item.split(".")) == 4:
                    # If true the ip_out is set to whatever the item is.
                    ip_out = item
                    found = True
                    break
                # In the case of the item not having the form of an ip address
                else:
                    found = False
                    continue
            # If an error occurs when spliting the line then it means an ip address wasn't found
            except:
                found = False
                continue
        if found:
            if vV_switch:
                print("Got router IP")
            return ip_out
        else:
            print(f"Unsuccessful automatic router ip founder :(\nResult:\n{ip_out}")
            sys.exit()

    def arp_table_mapper(ip_addresses):
        arp_table_map = {}
        try:
            # Create ARP request packet
            arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_addresses)
            if v_switch:
                print("Requested ARP packet")

            # Send ARP request and collect responses
            responses, _ = srp(arp_request, timeout=2, verbose=False)
            if vV_switch:
                print("Collected ARP responses")

            # Counter for assigning IDs
            id_counter = 0
            
            if v_switch:
                print("API calls started")
            # Process responses and populate ARP table map
            for _, response in responses:
                arp_table_map[id_counter] = {
                    'ip' : response.psrc,
                    'mac_address': response.hwsrc,
                    'device_name': "get_device_name(response.psrc)",
                    'vendor': api_lookup(response.hwsrc)
                }
                id_counter += 1
            if v_switch:
                print("API calls done")
        except Exception as e:
            print("Error retrieving ARP table:", e)

        return arp_table_map

    def get_device_name(ip_address):
        try:
            # Query DNS for hostname
            hostname, _, _ = socket.gethostbyaddr(ip_address)
            if vV_switch:
                print("Hostname for IP", ip_address, "is", hostname)
            return hostname
        except socket.herror:
            if vV_switch:
                print("failed to get hostname for: ", ip_address)
            return "Unknown"


    # A function used to get the networks subnet mask.
    def get_sub_mask() -> str:
        if v_switch:
            print("Getting subnet mask..")
        # A function used to calculate the subnet mask of the network.
        def subnet_mask_calculation(subnet_mask):
            mask_octets = subnet_mask.split('.')
            binary_mask = ''.join(format(int(octet), '08b') for octet in mask_octets)
            cidr = sum(bit == '1' for bit in binary_mask)
            return cidr
        # Running the command.
        sub_mask = subprocess.run("ipconfig getoption en0 subnet_mask", shell=True, capture_output=True, text=True)
        # Getting the result.
        sub_mask = sub_mask.stdout
        # Spliting the result at every new line.
        sub_mask = sub_mask.split("\n")
        # The desired result is always at the first line.
        sub_mask = sub_mask[0]
        
        # Putting it all together in the desired form of the subnet mask.
        if v_switch:
            print("Subnet mask found successsfully!")
        return str(subnet_mask_calculation(sub_mask))
    
    def save(scan_result: dict, form: str, file_name: str):
        if v_switch:
            print("Saving file..")
        # Checking if the specified format is JSON
        if form == "json":
            with open(f"{file_name}.json","w") as file:
                # Writing to the json file
                json.dump(scan_result, file, indent= 4)
        # Checking if the specified format is XML
        elif form == "xml":
            with open(f"{file_name}.xml", "w") as file:
                xml_data = dicttoxml.dicttoxml(scan_result)
                file.write(xml_data.decode('utf-8'))
        # In the case of no file format being specified we write in a txt file
        else: 
            with open(f"{file_name}.txt","w") as file:
                file.write(str(scan_result))
        if v_switch:
            print(f"File saved successfully as a {form} file.")



    def display_result(mapped_network: dict):
        # If verbose is true add a gap from the logs because why not
        if v_switch:
            print("\n")
        # Print the top of the row 
        print("\033[91mID\tIP ADDRESS\tMAC ADDRESS\t\tDEVICE NAME\t\tVENDOR\033[0m")

        
        for identifier, content in mapped_network.items():
            tmp_line = f"{identifier}\t{content['ip']}\t{content['mac_address']}\t{content['device_name']} \t\t{content['vendor']}"
            print(tmp_line)
        if save_file:
            save(scan_result = mapped_network, form = save_type, file_name = file_name)
    result = arp_table_mapper(f"{get_router_ip()}/{get_sub_mask()}")
    display_result(result)
    return result
