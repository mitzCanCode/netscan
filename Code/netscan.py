import sys  # Importing sys module for system-specific parameters and functions
import time  # Importing time module for time-related functions
from scanner import scan  # Importing the scan function from the scanner module. Used for scanning the network.
from sniffer import sniff_network  # Importing the sniff function from the sniffer module. Used for sniffing packets in the network
from quick_scanner import quick_scan  # Importing the quick_scan function from the quick_scanner module
import os  # Importing os module. Used to check if the user is running the script as root.
from port_scan import scan_ports 

from datetime import datetime  # Importing datetime module for date and time manipulation

# This function is used to display the ASCII art of this project
def print_logo():
    line1 = r"       _____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ _____"
    line2 = r"      //___//___//___//___//___//___//___//___//___//___//___//___//___//___//___//___//"
    line3 = r"     //___//                _  __ ___ _____  ___  __   _   _  __                //___//"
    line4 = r"    //___// _/7  _/7  _/7  / |/ // _//_  _/,' _/,'_/ .' \ / |/ /_/7  _/7  _/7  //___//"
    line5 = r"   //___// /_ _7/_ _7/_ _7/ || // _/  / / _\ `./ /_ / o // || //_ _7/_ _7/_ _7//___//"
    line6 = r"  //___//   //   //   // /_/|_//___/ /_/ /___,'|__//_n_//_/|_/  //   //   // //___//"
    line7 = r" //___//___ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____//___//"
    line8 = r"//___//___//___//___//___//___//___//___//___//___//___//___//___//___//___//___//"
    
    lines = [line1, line2, line3, line4, line5, line6, line7, line8]  # Storing all lines in a list

    # Iterating through all the lines and printing with rainbow coloring
    for line in lines:
        print(f"\033[91m{line}\033[0m")  # Using ANSI escape codes for color formatting
        time.sleep(0.07)  # Adding a delay for a cool effect


# Function to format current date and time
def time_format() -> str:
    return time.strftime("%d-%m-%Y_%H:%M:%S")


def main():
    if os.name == 'nt':
        # Windows
        is_admin = os.system("net session >nul 2>&1")
        if is_admin != 0:
            print("This script must be run as root.")
            sys.exit(1)
    else:
        # Unix/Linux/MacOS
        is_admin = os.geteuid() == 0
        if not is_admin:
            print("This script must be run as root.")
            sys.exit(1)
    
    
    print_logo()  # Displaying the logo
    print("\n")  # Printing a new line
    # Printing help message
    print("\033[91mAvailable Commands:\033[0m")
    print("1. scan\t\t- Initiate a network scan")
    print("2. qscan\t- Do a quick ping sweep to see which hosts are up and which are down")
    print("3. results\t- Display the results of the network scan")
    print("4. sniff\t- Sniff packets in the network")
    print("5. check\t- Run a port scan on a device discovered during a scan")
    print("6. help\t\t- Display help information about commands or general usage")
    print("7. exit\t\t- Exit the program")          
    print("For more inforamtion on a command use: [COMMAND] -h")
    print("\n")  # Printing a new line
    
    while True:
        # Setting all the variables back to default
        save_file = False
        file_name = time_format()
        verbose = False
        very_verbose = False
        save_type = "txt"
        timeout = 1.5
        
        prompt = input("\033[91mnetscan\033[0m > ")  # Taking user input with colored prompt
        prompt = prompt.split()  # Splitting user input into a list of words
        if "exit" in prompt:  # If user wants to exit
            print("\033[91mQuitting...\033[0m ")  # Display quitting message
            sys.exit()  # Exit the program
        elif "help" in prompt:  # If user wants help
            if "-h" in prompt:  # If user wants specific help
                # Printing help message for help command
                print("\033[91mHelp Command Help:\033[0m")
                print("Usage: help [options]")
                print("Description: Display all available commands.")
                print("Options:")
                print("  -h\t\tDisplay this help message")
            else:
                # Printing help message
                print("\033[91mAvailable Commands:\033[0m")
                print("1. scan\t\t- Initiate a network scan")
                print("2. qscan\t- Do a quick ping sweep to see which hosts are up and which are down")
                print("3. results\t- Display the results of the network scan")
                print("4. sniff\t- Sniff packets in the network")
                print("5. help\t\t- Display help information about commands or general usage")
                print("6. exit\t\t- Exit the program")          
                print("For more inforamtion on a command use: [COMMAND] -h")
        elif "sniff" in prompt:
            if "-h" in prompt:
                # Printing help message for sniff command
                print("\033[91mSniff Command Help:\033[0m")
                print("Usage: sniff [options]")
                print("Description: Sniff packets in the network")
                print("Options:")
                print("  -s\t\tSave scan results to a txt file")
                print("  -n NAME\tSpecify the name of the file to save scan results (File name must be one word)")
                print("Note:\n  To stop a scan, press Ctrl+C.")
                print("Example: sniff -s -n my_sniff_results")
            else:
                try:
                    if "-s" in prompt:
                        if "-n" in prompt:
                            try:
                                sniff_network(save=True, name=prompt[prompt.index("-n") + 1])
                            except: 
                                sniff_network(save=True, name=time_format())
                        else:
                            sniff_network(save=True, name=time_format())
                    else: 
                        sniff_network()                    
                except KeyboardInterrupt:
                    print("\n Stopping packet sniffer")
        elif "qscan" in prompt:
            if "-h" in prompt:
                # Printing help message for qscan command
                print("\033[91mQuick Scan Command Help:\033[0m")
                print("Usage: qscan [options]")
                print("Description: Perform a quick network scan to discover devices on the network.")
                print("Options:")
                print("  -h\t\tDisplay this help message")
                print("  -s\t\tSave scan results to a file")
                print("  -n NAME\tSpecify the name of the file to save scan results (File name must be one word)")
                print("  -v\t\tEnable verbose mode")
                print("  -vV\t\tEnable very verbose mode")
                print("  -t TIMEOUT\tSpecify the timeout of ping requests (in seconds)")
                print("Example: qscan -s -n my_quick_scan_results -v -t 2.0")
                continue

            else:
                if "-s" in prompt:
                    save_file = True
                if "-n" in prompt:
                    save_file = True
                    try:
                        file_name = prompt[prompt.index("-n") + 1]
                    except:
                        None
                if "-v" in prompt:
                    verbose = True
                if "-vV" in prompt:
                    very_verbose = True
                    verbose = True
                if "-t" in prompt:
                    try:
                        timeout = prompt[prompt.index("-t") + 1]
                        timeout = float(timeout)
                    except:
                        print("Invalid timeout")
                        print("Setting timeout to 1.5s")
                        timeout = 1.5
                try:
                    hosts_up, hosts_down = quick_scan(v_switch=verbose, vV_switch=very_verbose, save_file=save_file, file_name=file_name,timeout=timeout)
                    print(f"Total hosts up: {len(hosts_up)}")
                    print(f"Total hosts down: {len(hosts_down)}")
                    print("Hosts up:")
                    for host in hosts_up:
                        print(host)
                    if verbose:
                        print("Hosts down:")
                        for host in hosts_down:
                            print(host)
                except Exception as e:
                    print(e) 
        elif "check" in prompt:  # If user wants to check detailed information about a device
            if "-h" in prompt:  # If user wants help with check command
                # Printing help message for check command
                print("\033[91mCheck Command Help:\033[0m")
                print("Usage: check [ID]")
                print("Description: Check detailed information about a device discovered during the scan.")
                print("Options:")
                print("  -h\t\tDisplay this help message")
                print("Example: check 1")
                continue
            try:
                id_to_check = int(prompt[1])  # Get the ID of the device to check
                if id_to_check in scan_result and scan_result:  # If ID is valid and scan result is available
                    print("Checking IP address", scan_result[id_to_check]['ip'])  # Display IP address being checked
                    result = scan_ports(ip = scan_result[id_to_check]['ip'])
                    print(f"Scanning {scan_result[id_to_check]['ip']} for common ports...")
                    if result:
                        print(f"Open ports on {scan_result[id_to_check]['ip']}:")
                        for port, service in result:
                            print(f"Port {port}: {service}")
                    else:
                        print(f"No common ports are open on {scan_result[id_to_check]['ip']}.")
                else:
                    print("An error occurred.\nTry running the scan again or enter a valid number.")
            except Exception as e:
                print("Enter a valid ID please.")  # Print error message
        elif "scan" in prompt:  # If user wants to initiate a network scan
            if "-h" in prompt:  # If user wants help with scan command
                # Printing help message for scan command
                print("\033[91mScan Command Help:\033[0m")
                print("Usage: scan [options]")
                print("Description: Perform a network scan to discover devices on the network.")
                print("Options:")
                print("  -h\t\tDisplay this help message")
                print("  -v\t\tEnable verbose mode")
                print("  -vV\t\tEnable very verbose mode")
                print("  -s\t\tSave scan results to a file")
                print("  -f FORMAT\tSpecify the format for saving scan results (json, xml, or txt)")
                print("  -n NAME\tSpecify the name of the file to save scan results (File name must be one word)")
                print("Example: scan -v -s -f json -n my_scan_results")
                continue
            if "-v" in prompt:  # If verbose mode is enabled
                verbose = True  # Set verbose flag to True

            if "-vV" in prompt:  # If very verbose mode is enabled
                verbose = True  # Set verbose flag to True
                very_verbose = True  # Set very verbose flag to True

            if "-s" in prompt:  # If user wants to save scan results
                save_file = True  # Set save file flag to True

            if "-f" in prompt:  # If format is specified
                if prompt[prompt.index("-f") + 1] == "json":  # If format is json
                    save_type = "json"  # Set save type to json
                elif prompt[prompt.index("-f") + 1] == "xml":  # If format is xml
                    save_type = "xml"  # Set save type to xml  # Otherwise, set save type to txt
                save_file = True

            if "-n" in prompt:  # If filename is not specified # Set filename to current date and time
                    try:
                        file_name = prompt[prompt.index("-n") + 1]  # Set filename to specified value
                        save_file = True
                    except: None

            try:
                print("\n")
                print("\033[91mScanning...\033[0m")  # Display scanning message
                print("\n")

                # Call the scan function with specified options
                scan_result = scan(v_switch=verbose, vV_switch=very_verbose, save_file=save_file,
                                   save_type=save_type, file_name=file_name)
            except Exception as e:
                print("\nAn error occurred... :(")  # Print error message
                print(e)  # Print exception details
        elif "results" in prompt:  # If user wants to display scan results
            if "-h" in prompt:  # If user wants help with results command
                # Printing help message for results command
                print("\033[91mResults Command Help:\033[0m")
                print("Usage: results [options]")
                print("Description: Display the results of the previous network scan.")
                print("Options:")
                print("  -h\t\tDisplay this help message")
                print("Note:\n  To run the 'results' command a scan needs to have been completed first.")
                continue
            try:
                if scan_result:  # If scan result is available
                    # Print the header of the result table
                    print("\033[91mID\tIP ADDRESS\tMAC ADDRESS\t\tDEVICE NAME\t\tVENDOR\033[0m")
                    for identifier, content in scan_result.items():  # Iterate through scan result
                        # Construct and print each line of the result table
                        tmp_line = f"{identifier}\t{content['ip']}\t{content['mac_address']}\t{content['device_name']} \t\t{content['vendor']}"
                        print(tmp_line)
            except:
                print("You must run a scan first.")  # Print error message if no scan result
        else:
            print("Unknown command type \"help\" to see what commands are available")  # Print unknown command message

if __name__ == "__main__":
    try:
        main()  # Call the main function
    except KeyboardInterrupt:
        print("\n\033[91mQuitting...\033[0m")  # Print quitting message in case of keyboard interrupt
