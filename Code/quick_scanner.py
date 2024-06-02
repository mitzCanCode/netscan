import subprocess  # Import the subprocess module to run system commands
import sys  # Import the sys module for system-specific parameters and functions
import time  # Import the time module for time-related functions

# Function to get the current time formatted as a string
def time_format():
    return time.strftime("%d-%m-%Y_%H:%M:%S")  # Returns the current time in the specified format

# Main function to perform a quick network scan
def quick_scan(v_switch: bool = False, vV_switch: bool = False, save_file: bool = False, file_name: str = time_format(), timeout: float = 1.5) -> tuple:
    
    # Function to get the router's IP address
    def get_router_ip() -> str:
        if v_switch:
            print("Getting router IP...")
        
        # Run the command to get the router's IP
        get_ip_out = subprocess.run("netstat -rn | grep 'default' | awk '{print $2}'", shell=True, capture_output=True, text=True)
        ip_out = get_ip_out.stdout.strip().split("\n")
        
        # Check if the output contains a valid IP address
        for item in ip_out:
            try:
                if len(item.split(".")) == 4:
                    if vV_switch:
                        print(f"Got router IP: {item}")
                    return item
            except Exception as e:
                if vV_switch:
                    print(f"Error parsing IP: {e}")
                continue
        
        # If no valid IP is found, print an error message and exit
        print(f"Unsuccessful automatic router IP finder :(\nResult:\n{ip_out}")
        sys.exit()

    # Get the router IP address
    router_ip = get_router_ip()

    # Function to get the subnet mask
    def get_sub_mask() -> str:
        if v_switch:
            print("Getting subnet mask...")
        
        # Function to calculate the CIDR notation from the subnet mask
        def subnet_mask_calculation(subnet_mask):
            mask_octets = subnet_mask.split('.')  # Split the subnet mask into octets
            binary_mask = ''.join(format(int(octet), '08b') for octet in mask_octets)  # Convert each octet to binary and join them
            cidr = sum(bit == '1' for bit in binary_mask)  # Count the number of '1' bits in the binary mask
            return cidr
        
        # Run the command to get the subnet mask
        sub_mask = subprocess.run("ipconfig getoption en0 subnet_mask", shell=True, capture_output=True, text=True).stdout.strip()
        
        if v_switch:
            print(f"Subnet mask found: {sub_mask}")
        
        # Return the CIDR notation of the subnet mask
        return str(subnet_mask_calculation(sub_mask))

    # Get the subnet mask
    subnet_mask = get_sub_mask()

    # Function to get the network ID based on the subnet mask and router IP
    def get_net_id(subnet_mask: str, router_ip: str) -> str:
        split_router_ip = router_ip.split(".")
        if subnet_mask == "24":
            netid = f"{split_router_ip[0]}.{split_router_ip[1]}.{split_router_ip[2]}."
        elif subnet_mask == "16":
            netid = f"{split_router_ip[0]}.{split_router_ip[1]}."
        elif subnet_mask == "8":
            netid = f"{split_router_ip[0]}."
        else:
            print(" :( The tool only works with class A, B, and C networks")
            sys.exit()
        
        if vV_switch:
            print(f"Network ID calculated: {netid}")
        
        return netid

    # Get the network ID
    net_id = get_net_id(subnet_mask, router_ip)

    # Function to get active and inactive IP addresses in the network
    def get_ips(subnet_mask: str, net_id: str):
        active_ip_addresses = []  # List to store active IP addresses
        inactive_ip_addresses = []  # List to store inactive IP addresses
        
        # Function to ping an IP address and check if it is active
        def ping_ip(ip: str) -> bool:
            command = f'timeout {timeout} ping -c 1 -q {ip} && echo "true" || echo "false"'  # Command to ping the IP address
            checkIP = subprocess.run(command, shell=True, capture_output=True, text=True).stdout.strip().split("\n")[-1]
            return checkIP == "true"
        
        # Ping IP addresses based on the subnet mask
        if subnet_mask == "24":
            for i in range(1, 255):
                IP = f"{net_id}{i}"
                if v_switch:
                    print(f"Pinging IP: {IP}")
                if ping_ip(IP):
                    active_ip_addresses.append(IP)
                    if vV_switch:
                        print(f"IP {IP} is active")
                else:
                    if v_switch:
                        print(f"IP {IP} could not be contacted or took too long to respond")
                    inactive_ip_addresses.append(IP)
        
        elif subnet_mask == "16":
            for i in range(0, 255):
                for j in range(1, 256):
                    IP = f"{net_id}{i}.{j}"
                    if v_switch:
                        print(f"Pinging IP: {IP}")
                    if ping_ip(IP):
                        active_ip_addresses.append(IP)
                        if vV_switch:
                            print(f"IP {IP} is active")
                    else:
                        if v_switch:
                            print(f"IP {IP} could not be contacted or took too long to respond")
                        inactive_ip_addresses.append(IP)
        
        elif subnet_mask == "8":
            for i in range(0, 255):
                for j in range(0, 256):
                    for k in range(1, 256):
                        IP = f"{net_id}{i}.{j}.{k}"
                        if v_switch:
                            print(f"Pinging IP: {IP}")
                        if ping_ip(IP):
                            active_ip_addresses.append(IP)
                            if vV_switch:
                                print(f"IP {IP} is active")
                        else:
                            if v_switch:
                                print(f"IP {IP} could not be contacted or took too long to respond")
                            inactive_ip_addresses.append(IP)
        
        # Save the results to a file if save_file is True
        if save_file:
            with open(f"{file_name}.txt", "w") as f:
                hosts_up = [f"Host: {ip_address} was active." for ip_address in active_ip_addresses]
                hosts_down = [f"Host: {ip_address} was inactive or took too long to respond." for ip_address in inactive_ip_addresses]
                hosts_up_str = "\n".join(hosts_up)
                hosts_down_str = "\n".join(hosts_down)
                file_contents = f"Scan results for: {time_format()}\n\n" + hosts_up_str + "\n" + hosts_down_str
                f.write(file_contents)
            if v_switch:
                print(f"Results saved to {file_name}.txt")
        
        # Return the lists of active and inactive IP addresses
        return active_ip_addresses, inactive_ip_addresses

    # Get the active and inactive IP addresses and return them
    return get_ips(subnet_mask, net_id)

# Main block to run the quick_scan function and print the results
if __name__ == "__main__":
    active_hosts, inactive_hosts = quick_scan(vV_switch=True, v_switch=True, save_file=True, timeout=0.1)
    print("\n\nScan Results:\n")
    for host in active_hosts:
        print(f"Host: {host} is up")
    for host in inactive_hosts:
        print(f"Host: {host} is down or took too long to respond")
