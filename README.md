******************************************************************************************************************************************
                                                       iNet.Scanner.py
******************************************************************************************************************************************

His progect create on Python3.

Used side modules:

  1. 'termcolor' for colorize notifications

  2. 'scapy' for working with channel and network layer protocols

After downloading the program, go to the directory with it and enter “chmod + x iNet.Scanner.py”, then run it “./iNet.Scanner.py”

The program requires root rights! Although it works on Windows, I recommend using one of Linux.
The program first receives a range of IP addresses, consisting of an IP router and through '/' the number of IP addresses.
Next, you need to specify the ports (this number is from 1 to 65535).
Examples:
1) if you specify one number, only this port will be checked
2) ports can be specified with a comma
3) ports can be specified by specifying the range '<min port> - <max port>'
4) 'аll' displays all ports
As a result of the check, only open ports are displayed.

The program displays the result in the form of a table with the IP address, MAC address, host name of the device and open ports.
Below the table, your local IP address and host name are displayed.

Installation commands for Linux:
1) git clone https://github.com/KomogorovKirill/iNet.Scanner.git
2) cd iNet.Scanner
3) chmod +x iNet.Scanner.py
4) ./iNet.Scanner.py
