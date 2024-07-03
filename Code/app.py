import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  # For showing message boxes
from scanner import scan  # Assuming you have a scan function in the scanner module
import threading
from datetime import datetime

# Function to scan the network and display the results
def scan_network():
    try:
        # Update status label and start progress bar
        status_label.config(text="Scanning network...")
        progress_bar.pack(pady=10, fill=tk.X)
        progress_bar.start()
        
        # Run the scan in a separate thread to keep the UI responsive
        threading.Thread(target=perform_scan).start()
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")
        progress_bar.stop()
        progress_bar.pack_forget()

def perform_scan():
    try:
        # Read the state of the save_file_checkbox
        save_file = save_file_var.get()
        
        # Determine the selected file format
        save_type = ""
        if save_file:
            if save_type_var.get() == 1:
                save_type = "json"
            elif save_type_var.get() == 2:
                save_type = "xml"
            elif save_type_var.get() == 3:
                save_type = "txt"
        
        # Get the filename from the entry widget
        file_name = file_name_entry.get().strip()  # Strip any leading/trailing whitespace
        
        # If filename is empty, generate a default filename
        if not file_name:
            current_time = datetime.now()
            file_name = f"scan-{current_time.strftime('%H-%M-%d-%m-%Y')}"
        
        sample_dict = scan(v_switch=True, vV_switch=True, save_file=save_file, save_type=save_type, file_name=file_name)
        
        # Clear any previous data in the treeview
        for row in tree.get_children():
            tree.delete(row)
        
        # Insert new data into the treeview
        for key, value in sample_dict.items():
            tree.insert("", "end", values=(key, value['ip'], value['mac_address'], value['device_name'], value['vendor']))
        
        # Update status label and stop progress bar
        status_label.config(text="Scan complete.")
        progress_bar.stop()
        progress_bar.pack_forget()
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")
        progress_bar.stop()
        progress_bar.pack_forget()

# Function to show or hide file format selection based on checkbox state
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

# Set up the main application window
root = tk.Tk()
root.title("Netscan")
root.geometry("1000x700")

# Create a frame to hold the Treeview widget
tree_frame = ttk.Frame(root)
tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

# Set up the Treeview widget
columns = ("ID", "IP Address", "MAC Address", "Device Name", "Vendor")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

# Define headings
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER)

# Pack the Treeview widget
tree.pack(fill=tk.BOTH, expand=True)

# Create a frame for the status and progress bar
bottom_frame = ttk.Frame(root)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

# Add a status label
status_label = ttk.Label(bottom_frame, text="Click 'Scan network' to start.")
status_label.pack(side=tk.LEFT, padx=10)

# Add a progress bar
progress_bar = ttk.Progressbar(bottom_frame, mode='indeterminate')

# Add a button to trigger the scan
display_button = ttk.Button(bottom_frame, text="Scan network", command=scan_network)
display_button.pack(side=tk.RIGHT, padx=10)

# Add a checkbox to save scan results to file
save_file_var = tk.BooleanVar()
save_file_checkbox = ttk.Checkbutton(bottom_frame, text="Save Scan Results", variable=save_file_var, command=show_hide_file_format)
save_file_checkbox.pack(side=tk.RIGHT, padx=10)

# Add radio buttons for selecting file format
save_type_var = tk.IntVar()
json_radio = ttk.Radiobutton(bottom_frame, text="JSON", variable=save_type_var, value=1)
xml_radio = ttk.Radiobutton(bottom_frame, text="XML", variable=save_type_var, value=2)
txt_radio = ttk.Radiobutton(bottom_frame, text="TXT", variable=save_type_var, value=3)

# Add entry widget for file name
file_name_label = ttk.Label(bottom_frame, text="File Name:")
file_name_label.pack(anchor=tk.W, pady=(10, 0))
file_name_entry = ttk.Entry(bottom_frame)
file_name_entry.pack(anchor=tk.W)

# Run the application
root.mainloop()
