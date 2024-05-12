# Rainbow text is used for the logo.
from rainbowtext import text
import sys
import time
from scan import scan
import datetime


# This function is used to display the ascii art of this project
def print_logo():
    # Applying to each line rainbow coloring.
    line1 = "       _____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ _____"
    line2 = "      //___//___//___//___//___//___//___//___//___//___//___//___//___//___//___//___//"
    line3 = "     //___//                _  __ ___ _____  ___  __   _   _  __                //___//"
    line4 = "    //___// _/7  _/7  _/7  / |/ // _//_  _/,' _/,'_/ .' \ / |/ /_/7  _/7  _/7  //___//"
    line5 = "   //___// /_ _7/_ _7/_ _7/ || // _/  / / _\ `./ /_ / o // || //_ _7/_ _7/_ _7//___//"
    line6 = "  //___//   //   //   // /_/|_//___/ /_/ /___,'|__//_n_//_/|_/  //   //   // //___//"
    line7 = " //___//___ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____//___//"
    line8 = "//___//___//___//___//___//___//___//___//___//___//___//___//___//___//___//___//"
    
    
    lines = [line1,line2,line3,line4,line5,line6,line7,line8]

    # Iterating through all the lines.
    for line in lines:
        print(f"\033[91m{line}\033[0m")
        # A delay is added to add a cool effect.
        time.sleep(0.07)


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


def main():
    print_logo()
    
    if "-h" in sys.argv[1:]:
        print(help_message)
        sys.exit()
    
    if "-v" in sys.argv[1:]:
      verbose = True
    else: verbose = False
    
    if "-vV" in sys.argv[1:]:
      verbose = True
      very_verbose = True
    else: very_verbose = False
    
    
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
        
    try:
      # Starting the scan.
      print("\n")
      print("\033[91mScanning...\033[0m")
      print("\n")

      scan(v_switch = verbose, vV_switch = very_verbose, save_file = save_file, save_type = save_type, file_name = file_name)
    except Exception as e:
      print("\nAn error occured... :(")
      print(e)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(text("Quitting..."))
