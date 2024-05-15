# Rainbow text is used for the logo.
from rainbowtext import text  # Importing the rainbow text module for colorful text output
import sys  # Importing sys module for system-specific parameters and functions
import time  # Importing time module for time-related functions
from scan import scan  # Importing the scan function from the scan module

import datetime  # Importing datetime module for date and time manipulation
import subprocess  # Importing subprocess module to run shell commands from Python

# This function is used to display the ASCII art of this project
def print_logo():
    line1 = "       _____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ _____"
    line2 = "      //___//___//___//___//___//___//___//___//___//___//___//___//___//___//___//___//"
    line3 = "     //___//                _  __ ___ _____  ___  __   _   _  __                //___//"
    line4 = "    //___// _/7  _/7  _/7  / |/ // _//_  _/,' _/,'_/ .' \ / |/ /_/7  _/7  _/7  //___//"
    line5 = "   //___// /_ _7/_ _7/_ _7/ || // _/  / / _\ `./ /_ / o // || //_ _7/_ _7/_ _7//___//"
    line6 = "  //___//   //   //   // /_/|_//___/ /_/ /___,'|__//_n_//_/|_/  //   //   // //___//"
    line7 = " //___//___ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____//___//"
    line8 = "//___//___//___//___//___//___//___//___//___//___//___//___//___//___//___//___//"
    
    lines = [line1, line2, line3, line4, line5, line6, line7, line8]  # Storing all lines in a list

    # Iterating through all the lines and printing with rainbow coloring
    for line in lines:
        print(f"\033[91m{line}\033[0m")  # Using ANSI escape codes for color formatting
        time.sleep(0.07)  # Adding a delay for a cool effect


# The help message.
help_message = """
Usage: python netscan.py [options]
Options:
  -v                Base verbose result. 
  -s                Save device information to a file.
  -f <format>       Specify the output format when saving to a file.
                    Supported formats: json, xml, txt.
  -n <filename>      Specify the file name when saving to a file.
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

# Function to format current date and time
def time_format() -> str:
    dt = str(datetime.now())  # Converting current date and time to string
    dt = dt.split(" ")  # Splitting date and time
    time = dt[1].split(".")  # Splitting time to remove milliseconds
    del time[1]  # Deleting milliseconds
    dt = dt[0] + "-" + time[0]  # Joining date and time
    return dt  # Returning formatted date and time


def main():
    print_logo()  # Displaying the logo
    print("\n")  # Printing a new line
    
    while True:
        prompt = input("\033[91mnetscan\033[0m > ")  # Taking user input with colored prompt
        prompt = prompt.split()  # Splitting user input into a list of words
        if "exit" in prompt:  # If user wants to exit
            print(text("Quitting..."))  # Display quitting message
            sys.exit()  # Exit the program
        elif "help" in prompt:  # If user wants help
            if "-h" in prompt:  # If user wants specific help
                # Printing help message for help command
                print("\033[91mHelp Command Help:\033[0m")
                print("Usage: help [COMMAND]")
                print("Description: Display help information about a specific command or general usage.")
                print("Options:")
                print("  -h\t\tDisplay this help message")
                print("Example: help scan")
            else:
                # Printing available commands
                print("\033[91mAvailable Commands:\033[0m")
                print("1. scan\t\t- Initiate a network scan")
                print("2. check\t- Check detailed information about a device discovered during the scan")
                print("3. results\t- Display the results of the network scan")
                print("4. help\t\t- Display help information about commands or general usage")
                print("5. exit\t\t- Exit the program")          
        elif "scan" in prompt:  # If user wants to initiate a network scan
            if "-h" in prompt[1:]:  # If user wants help with scan command
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
                print("  -n NAME\tSpecify the name of the file to save scan results")
                print("Example: scan -v -s -f json -n my_scan_results")
                continue
            if "-v" in prompt[1:]:  # If verbose mode is enabled
                verbose = True  # Set verbose flag to True
            else:
                verbose = False  # Otherwise, set it to False

            if "-vV" in prompt[1:]:  # If very verbose mode is enabled
                verbose = True  # Set verbose flag to True
                very_verbose = True  # Set very verbose flag to True
            else:
                very_verbose = False  # Otherwise, set it to False

            if "-s" in prompt[1:]:  # If user wants to save scan results
                save_file = True  # Set save file flag to True
                if "-f" in prompt[1:]:  # If format is specified
                    if sys.argv[sys.argv.index("-f") + 1] == "json":  # If format is json
                        save_type = "json"  # Set save type to json
                    elif sys.argv[sys.argv.index("-f") + 1] == "xml":  # If format is xml
                        save_type = "xml"  # Set save type to xml
                    else:
                        save_type = "txt"  # Otherwise, set save type to txt

                if "-n" not in sys.argv[1:]:  # If filename is not specified
                    file_name = f"{time_format()}"  # Set filename to current date and time
                else:
                    file_name = sys.argv[sys.argv.index("-n") + 1]  # Set filename to specified value
            else:
                save_file = False  # Otherwise, set save file flag to False
                save_type = None  # Set save type to None
                file_name = None  # Set filename to None

            try:
                print("\n")
                print("\033[91mScanning...\033[0m")  # Display scanning message
                print("\n")

                # Call the scan function with specified options
                scan_result = scan(v_switch=verbose, vV_switch=very_verbose, save_file=save_file,
                                   save_type=save_type, file_name=file_name)
                print(scan_result)  # Print scan result
            except Exception as e:
                print("\nAn error occurred... :(")  # Print error message
                print(e)  # Print exception details
        elif "check" in prompt:  # If user wants to check detailed information about a device
            if "-h" in prompt[1:]:  # If user wants help with check command
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
                    # Run nmap scan on the specified device
                    result = subprocess.run(f"nmap {scan_result[id_to_check]['ip']}", shell=True, capture_output=True,
                                             text=True)
                    print(result.stdout)  # Print nmap scan results
                else:
                    print("An error occurred.\nTry running the scan again or enter a valid number.")
            except Exception as e:
                print("Enter a valid ID please.")  # Print error message
        elif "results" in prompt:  # If user wants to display scan results
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
        print("\033[91mQuitting...\033[0m")  # Print quitting message in case of keyboard interrupt
