# Sub process is imported to run commands on the terminal.
import subprocess
# This module will be used later to identify the manufacturer.
import requests
# Sys is imported in order to check what switches where added.
import sys
# Time is used later because of the free version of the api allowing only 2 requests a second,
# it is also used for printing the logo.
import time
# Date time is used to set a name for a file when no name is specified.
from datetime import datetime
# Dicttoxml is used to convert a dictionary to a xml file.
from dicttoxml import dicttoxml
# Json is used to convert a dictionary to a json file.
import json
# Rainbow text is used for the logo.
from rainbowtext import text


# This function is used to display the ascii art of this project
def print_logo():
    # A new line is printed to make the logo stick out.
    print("\n")
    # Applying to each line rainbow coloring.
    line1 = text("       _____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ _____")
    line2 = text("      //___//___//___//___//___//___//___//___//___//___//___//___//___//___//___//")
    line3 = text("     //___//                _  __ ___ _____  ___  __   _   _  __                //___//")
    line4 = text("    //___// _/7  _/7  _/7  / |/ // _//_  _/,' _/,'_/ .' \ / |/ /_/7  _/7  _/7  //___//")
    line5 = text("   //___// /_ _7/_ _7/_ _7/ || // _/  / / _\ `./ /_ / o // || //_ _7/_ _7/_ _7//___//")
    line6 = text("  //___//   //   //   // /_/|_//___/ /_/ /___,'|__//_n_//_/|_/  //   //   // //___//")
    line7 = text(" //___//___ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____//___//")
    line8 = text("//___//___//___//___//___//___//___//___//___//___//___//___//___//___//___//___//")
    
    
    lines = [line1,line2,line3,line4,line5,line6,line7,line8]

    # Iterating through all the lines.
    for line in lines:
        print(line)
        # A delay is added to add a cool effect.
        time.sleep(0.07)


# The help message.
help_message = """
Usage: python netscan.py [options]
Options:
  -d                Display device information after scan is finished.
  -s                Save device information to a file.
  -f <format>       Specify the output format when saving to a file.
                    Supported formats: json, xml, txt.
  -n <filename>      Specify the file name when saving to a file.
  -ip               Display IP addresses found during scanning.
  -c <count>        Specify the number of ping packets to send.
  -h                Display this help message.
Saving the scan:
  Action format:
    -s -n <filename> -f <format>
  -s                Save device information to a file.
  -n <filename>      Specify the file name when saving to a file.
  -f <format>       Specify the output format when saving to a file.
                    Supported formats: json, xml, txt.
  Notes:
    The switches do not need to be placed in a specific order.

"""


# A function used to get the networks subnet mask.
def get_sub_mask() -> str:
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
    return str(subnet_mask_calculation(sub_mask))


# A command used to find the routers ip.
def get_router_ip() -> str:
    # Runnning th command.
    get_ip_out = subprocess.run("netstat -rn | grep 'default' | awk '{print $2}'", shell=True, capture_output=True, text=True)
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
        return ip_out
    else:
        print(f"Unsuccessful automatic router ip founder :(\nResult:\n{ip_out}")
        sys.exit()


# A function that makes an api request and returns a devices manufacturer by their mac address.
def api_lookup(mac_address: str) -> str:
    # Specifying the url the request will be made to including the mac address.
    url = f"https://api.macvendors.com/v1/lookup/{mac_address}"
    # Specifying the headers as well as the api key.
    headers = {"Authorization": "Bearer API_KEY"}
    # Making the api request.
    api = requests.get(url= url, headers= headers)
    # Returning the json data more specifically the organisations name.
    time.sleep(0.5)
    # In the case of the API not being able to find the vendor it will return unknown.
    if "errors" in api.json():
        return "Unknown"
    # If no errors occur it will return the vendor.
    else:
        return api.json()["data"]["organization_name"]


# This function is used to ping all the devices found by nmap as well as get their mac address.
def scan_network(ip_add_lst: list, packets: int, save: bool, save_type: str, name: str, show: bool) -> dict:
    ip_mac = {}
    
    for ip in ip_add_lst:
        try:
            # Run ping and ARP commands
            ping_cmd = f"ping -c {packets} {ip}"
            arp_cmd = "arp -a | grep " + ip
            full_info = subprocess.run(f"{ping_cmd} ; {arp_cmd}", shell=True, capture_output=True, text=True, check=True)
            output_lines = full_info.stdout.splitlines()
            
            # Parse the output to get the IP and MAC address
            if len(output_lines) >= 2:
                ip_add = output_lines[-2].split('(')[-1].split(')')[0]
                mac = output_lines[-1].split()[3]
                
                if mac == "(incomplete)":
                    ip_mac[ip] = {"mac": "Unknown", "vendor": "Unknown"}
                else:
                    ip_mac[ip] = {"mac": mac, "vendor": api_lookup(mac_address=mac)}
                
                if show:
                    display(ip_mac)
                
                if save:
                    save(device_info=ip_mac, form=save_type, file_name=name)
            else:
                # Handle case when no data is found for this IP
                ip_mac[ip] = {"mac": "Unknown", "vendor": "Unknown"}
        
        except Exception as e:
            # Handle exceptions (e.g., command execution error)
            print(f"Error scanning {ip}: {str(e)}")
    
    return ip_mac






def nmap(show_ip: bool) -> list:
    global nmap_raw
    global router_ip
    global subnet
    # Setting a local variable of the routers IP address.
    router_ip = get_router_ip()
    # Setting a local variable of the networks subnet mask.
    subnet = get_sub_mask()
    # Running a network map to find all the devices in the network.
    print(f"\nScanning {router_ip}/{subnet}...")
    nmap_out = subprocess.run(f"nmap -sP  {router_ip}/{subnet}", shell=True, capture_output=True, text=True)
    # Getting the output from the terminal.
    nmap_out = nmap_out.stdout
    nmap_raw = nmap_out
    # Notifying the user about the scan.
    print("Scan successfull!")
    # Splitting the output at every new line.
    nmap_out = nmap_out.split("\n")
    # Creating an ip 
    ip_addresses = []
    # Adding only the ip addresses scanned to a list.
    for ip in nmap_out[1:-1:2]:
        # Making a temp list of the output.
        temp = ip.split(" ")
        # The last item returned is always the ip so only the ip is added in the ip_addresses list.
        ip_addresses.append(temp[-1])
    # Returning the result of how many ip addresses were scanned and how many hosts are up
    # as well as the time it took. This line is returned by default by nmap.
    scanned = ip_addresses.pop(-1)
    print(scanned)
    # Checking if the user wants to print the IP addresses.
    if show_ip == True:
        print("IP adresses found:")
        # Iterating over each IP address
        for ip in ip_addresses:
            print(ip)
    # Returning the IP addresses
    return ip_addresses


def time_format() -> str:
    # Converting the current date and time to a string.
    dt = str(datetime.now())
    # Splitting the date and the time in order to modify the time.
    dt = dt.split(" ")
    # Splitting the time in order to delete the milliseconds.
    time = dt[1].split(".")
    # Deleting the milliseconds.
    del time[1]
    # Joining the date and time.
    dt = dt[0]+"-"+time[0]
    # Returning the date and time
    return dt


def save(device_info: dict, form: str, file_name: str):
    # Checking if the specified format is JSON
    if form == "json":
        with open(f"{file_name}.json","w") as file:
            # Writing to the json file
            json.dumps(device_info,file,indent= 4)
    # Checking if the specified format is XML
    elif form == "xml":
        with open(f"{file_name}.xml","w") as file:
            file.write(dicttoxml(device_info))
    # In the case of no file format being specified we write in a txt file
    else: 
        with open(f"{file_name}.txt","w") as file:
            file.write(device_info)
    print(f"File saved successfully as a {form} file.")


def display(device_info: dict) -> str:
    counter = 0
    count = {}
    for ip,info in device_info.items():
        # Printing the device number.
        print(f"device{counter}")
        # Printing the ip address.
        print(ip)
        
        print(info["mac"])
        print(info["vendor"])
        print("\n")
        if info["vendor"] in count:
            count[info["vendor"]] += 1
        else:
            count[info["vendor"]] = 1
        counter += 1
    print(count)


def main():
    print_logo()
    if "-h" in sys.argv[1:]:
        print(help_message)
        sys.exit()
    
    
    # Cheking if the user wants the output to be displayed
    if "-d" in sys.argv[1:]:
        show = True
    else:
        # In the case of the user not wanting the output to be displayed we set the show variable to false.
        show = False
    
    
    if "-s" in sys.argv[1:]:
        # Setting the save file variable to true so that when the program is run the is saved.
        save_file = True
        if "-f" in sys.argv[1:]:
            # Checking if the selected save form is json.
            if sys.argv[sys.argv.index("-f") + 1] == "json":
                save_type = "json"
            elif sys.argv[sys.argv.index("-f") + 1] == "xml":
                save_type = "xml"
            else:
                save_type = "txt"
        
        # In the case of there not being a specified name for the file the name is set to the time.
        if "-n" not in sys.argv [1:]:
            file_name = f"{time_format()}"
        # Other wise it is whatever is specified after the -n switch is called.
        else:
            file_name = sys.argv[sys.argv.index("-n") + 1]
    # In the case of the user not wanting to save the file.
    else:
        # The save file variable becomes False.
        save_file = False
        # The save type becomes None since no file will be saved.
        save_type = None
        # The file name becomes None if no file will be saved
        file_name = None
    
    if show != True and save_file != True:
        print("\n\nThe file needs to either be saved (\"-s\") or displayed (\"-d\"). Type \"-h\" for help.\n\n")
        sys.exit()

    # Checking to see if the user desires to view the ip addresses being pinged.
    if "-ip" in sys.argv[1:]:
        show_ip = True
    # If the user doesnt desire viewing the ip addresses being pinged nothing will be displayed.
    else:
        show_ip = False
    if "-c" in sys.argv[1:]:
    # Testing to see if the character one index after -c is an interger.
        try:
            # Setting the count variable to the number one index after the -c.
            count = int(sys.argv[sys.argv.index("-c") + 1])
        # If the user didn't enter an int or a float number the program runs with the default ping settings (5).
        except:
            count = 5

    # If the user didn't specify the ammount of packets to be sent the program runs with the default ping settings.
    else:
        count = 5
    # try:
    # Starting the scan.
    scan_network(ip_add_lst = nmap(show_ip=show_ip), packets = count, save = save_file, save_type= save_type, name = file_name, show=show)
    
    # except Exception as e:
    print(f"\nAn error occured nmap result:\n\n{nmap_raw}")
    print(f"\nScanned:\n{router_ip}/{subnet}")
    print(f"\nPython error:\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Quitting...")
