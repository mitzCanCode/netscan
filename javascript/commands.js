// Array of available commands
const availableCommands = ["scan", "results", "sniff", "qscan", "help", "exit"];
let currentIndex = 0;

// Function to change the command text with fade in and fade out animation
function changeCommand() {
    const commandElement = document.querySelector('.command');

    setTimeout(() => {
        // Change the command text
        commandElement.textContent = availableCommands[currentIndex];
        currentIndex = (currentIndex + 1) % availableCommands.length;

        commandElement.style.opacity = 1; // Fade in

        // Check if the current command is "scan"
        if (commandElement.textContent === "scan") {
            // Update the content of the results span
            const resultsElement = document.querySelector('.results');
            resultsElement.innerHTML = `
<span class="scanning">Scanning...</span>
Getting router IP
Getting subnet mask..
Subnet mask found successfully!
Requested ARP packet
API calls started
API calls done

ID\tIP ADDRESS\tMAC ADDRESS\t\tDEVICE NAME\tVENDOR
0\t192.168.3.1\t76:ac:b9:16:49:3c\tDevice1\t\tVendor1
1\t192.168.3.2\t76:ac:b9:16:49:3c\tDevice2\t\tVendor2
2\t192.168.3.78\t8a:c7:d6:59:50:89\tDevice3\t\tVendor3
3\t192.168.3.85\t7a:72:1c:26:6a:01\tDevice4\t\tVendor4
4\t192.168.3.94\tee:d1:cd:3f:34:67\tDevice5\t\tVendor5
5\t192.168.3.134\t74:12:b3:34:ee:0d\tDevice6\t\tVendor6
6\t192.168.3.146\t04:d6:f4:cd:75:78\tDevice7\t\tVendor7
            `;
        } else if (commandElement.textContent === "sniff") {
            // Update the content of the results span for sniff command
            const resultsElement = document.querySelector('.results');
            resultsElement.innerHTML = `
Packet: Ether / IP / TCP 20.42.65.90:https > 192.168.3.74:63805 RA / Padding | Source IP: 20.42.65.90  |  Source MAC: 76:ac:b9:16:49:3c | Destination IP: 192.168.3.74  |  Destination MAC: 3c:22:fb:02:4b:b5 | Protocol: TCP | Time: 02-06-2024_11:26:04
--------------------------------------------------
Packet: Ether / IP / UDP 192.168.3.1:52974 > 255.255.255.255:scp_config / Raw / Padding | Source IP: 192.168.3.1  |  Source MAC: 76:ac:b9:16:49:3c | Destination IP: 255.255.255.255  |  Destination MAC: ff:ff:ff:ff:ff:ff | Protocol: UDP | Time: 02-06-2024_11:26:12
--------------------------------------------------
Packet: Ether / IP / TCP 20.201.28.148:https > 192.168.3.74:63952 PA / Raw | Source IP: 20.201.28.148  |  Source MAC: 76:ac:b9:16:49:3c | Destination IP: 192.168.3.74  |  Destination MAC: 3c:22:fb:02:4b:b5 | Protocol: TCP | Time: 02-06-2024_11:26:12
--------------------------------------------------
Packet: Ether / IP / TCP 20.201.28.148:https > 192.168.3.74:63952 PA / Raw | Source IP: 20.201.28.148  |  Source MAC: 76:ac:b9:16:49:3c | Destination IP: 192.168.3.74  |  Destination MAC: 3c:22:fb:02:4b:b5 | Protocol: TCP | Time: 02-06-2024_11:26:12
--------------------------------------------------
Packet: Ether / IP / TCP 20.201.28.148:https > 192.168.3.74:63952 FA | Source IP: 20.201.28.148  |  Source MAC: 76:ac:b9:16:49:3c | Destination IP: 192.168.3.74  |  Destination MAC: 3c:22:fb:02:4b:b5 | Protocol: TCP | Time: 02-06-2024_11:26:12
--------------------------------------------------
Packet: Ether / IP / TCP 192.168.3.74:63952 > 20.201.28.148:https A | Source IP: 192.168.3.74  |  Source MAC: 3c:22:fb:02:4b:b5 | Destination IP: 20.201.28.148  |  Destination MAC: 76:ac:b9:16:49:3c | Protocol: TCP | Time: 02-06-2024_11:26:12
--------------------------------------------------
Packet: Ether / IP / TCP 192.168.3.74:63952 > 20.201.28.148:https A | Source IP: 192.168.3.74  |  Source MAC: 3c:22:fb:02:4b:b5 | Destination IP: 20.201.28.148  |  Destination MAC: 76:ac:b9:16:49:3c | Protocol: TCP | Time: 02-06-2024_11:26:12
--------------------------------------------------
Packet: Ether / IP / TCP 192.168.3.74:63952 > 20.201.28.148:https FA | Source IP: 192.168.3.74  |  Source MAC: 3c:22:fb:02:4b:b5 | Destination IP: 20.201.28.148  |  Destination MAC: 76:ac:b9:16:49:3c | Protocol: TCP | Time: 02-06-2024_11:26:12
--------------------------------------------------
            `;
        } else if (commandElement.textContent === "results") {
            // Update the content of the results span for results command
            const resultsElement = document.querySelector('.results');
            resultsElement.innerHTML = `
ID\tIP ADDRESS\tMAC ADDRESS\t\tDEVICE NAME\tVENDOR
0\t192.168.3.1\t76:ac:b9:16:49:3c\tDevice1\t\tVendor1
1\t192.168.3.2\t76:ac:b9:16:49:3c\tDevice2\t\tVendor2
2\t192.168.3.78\t8a:c7:d6:59:50:89\tDevice3\t\tVendor3
3\t192.168.3.85\t7a:72:1c:26:6a:01\tDevice4\t\tVendor4
4\t192.168.3.94\tee:d1:cd:3f:34:67\tDevice5\t\tVendor5
5\t192.168.3.134\t74:12:b3:34:ee:0d\tDevice6\t\tVendor6
6\t192.168.3.146\t04:d6:f4:cd:75:78\tDevice7\t\tVendor7
            `;
        } else if (commandElement.textContent === "qscan") {
            // Check if the ID is 0
            // Update the content of the results span for ID 0
            const resultsElement = document.querySelector('.results');
            resultsElement.innerHTML = `
Total hosts up: 6
Total hosts down: 248
Hosts up:
192.168.3.2
192.168.3.78
192.168.3.85
192.168.3.94
192.168.3.134
192.168.3.146
            `;
        } else if (commandElement.textContent === "help") {
            // Check if the ID is 0
            // Update the content of the results span for ID 0
            const resultsElement = document.querySelector('.results');
            resultsElement.innerHTML = `
1. scan  - Initiate a network scan
2. check - Check detailed information about a device discovered during the scan
3. results - Display the results of the network scan
4. sniff - Sniff packets in the network
5. help - Display help information about commands or general usage
6. exit - Exit the program
            `;
        } else if (commandElement.textContent === "exit") {
            // Check if the ID is 0
            // Update the content of the results span for ID 0
            const resultsElement = document.querySelector('.results');
            resultsElement.innerHTML = `
Quitting...
            `;
        }
    }, 500); // 500 milliseconds for the fade out effect
}

// Call the function initially and then every 5 seconds
changeCommand(); // Initial call

setInterval(changeCommand, 5000); // Call every 5 seconds
