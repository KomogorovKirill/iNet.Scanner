#!/usr/bin/python3
#Created by Komogorov Kirill

from sys import platform
from subprocess import check_output
from re import search
import socket
import os
try:
    import scapy.all as scapy
except (ImportError, ModuleNotFoundError): #check module availability
    print('Start installing the module "scapy"\n')
    if platform == 'win32': #installation under windows
        os.system('pip install scapy')
    else: #installation under other OS
        os.system('pip3 install scapy')
    try:
        import scapy.all as scapy #module reconnection
    except (ImportError, ModuleNotFoundError): #if the module is not found in the repository
        print("module 'scapy' incorrectly imported")
        exit()
try:
    from termcolor import colored #same as with "scapy"
except (ImportError, ModuleNotFoundError):
    print('Start installing the module "termcolor"\n')
    if platform == 'win32':
        os.system('pip install termcolor')
    else:
        os.system('pip3 install termcolor')
    try:
        from termcolor import colored
    except (ImportError, MemoryError):
        print("module 'termcolor' incorrectly imported")
        exit()

print(colored(" _ _   _      _     ____", 'green'))
print(colored("(_) \ | | ___| |_  / ___|  ___ __ _ _ __  _ __   ___ _ __", 'green'))
print(colored("| |  \| |/ _ \ __| \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|", 'green'))
print(colored("| | |\  |  __/ |_ _ ___) | (_| (_| | | | | | | |  __/ |", 'green'))
print(colored("|_|_| \_|\___|\__(_)____/ \___\__,_|_| |_|_| |_|\___|_|", 'green'))
print('\t' * 5 + ' ' * 7 + colored('version 1.0', 'red') + '\n')

Range = input(colored("Enter the range of IP addresses: ", 'yellow')) #Enter and check range of IP addresses
if (search(r'([0-9]{1,3}.){3}[0-9]{1,3}/[\d]{1,2}', Range)) == None:
    print(colored("You don't enter range of IP addresses!", 'red'))
    exit()

Range_ports = input(colored("Enter range ports: ", 'yellow')).lower() #input port range
Port_list =[]
check_ports = True #ports check at IP address

if (search(r'([\d]+, )+[\d]+', Range_ports)) != None: #ports input validation
    ls = Range_ports.split(', ')
    for i in ls:
        if int(ls[i]) >= 1 and int(ls[i]) <= 65535:
            Port_list.append(ls[i])
        else:
            print(colored('\nPort ' + str(ls[i]) + ' incorrect', 'red'))
            del ls[i]

elif (search(r'[\d]+ - [\d]+', Range_ports)) != None:
    min_max = Range_ports.split(' - ')
    if (int(min_max[0]) >= 1) and (int(min_max[0]) <= 65535) and (int(min_max[1]) >= 1) and (int(min_max[1]) <= 65535):
        if min_max[0] < min_max[1]:
            min_port = min_max[0]
            max_port = min_max[1]
        else:
            min_port = min_max[1]
            max_port = min_max[0]
    else:
        print(colored('\nPorts range was entered incorrectly!', 'red'))
        exit()
    Port_list = [i for i in range(int(min_port), int(max_port) + 1)]
elif (search(r'[\d]+-[\d]+', Range_ports)) != None:
    min_max = Range_ports.split('-')
    if (int(min_max[0]) >= 1) and (int(min_max[0]) <= 65535) and (int(min_max[1]) >= 1) and (int(min_max[1]) <= 65535):
        if int(min_max[0]) < int(min_max[1]):
            min_port = min_max[0]
            max_port = min_max[1]
        else:
            min_port = min_max[1]
            max_port = min_max[0]
    else:
        print(colored('\nPorts range was entered incorrectly!', 'red'))
        exit()
    Port_list = [i for i in range(int(min_port), int(max_port) + 1)]
elif (search(r'[\d]+', Range_ports)) != None:
    if (int(Range_ports) >= 1) and (int(Range_ports) <= 65535):
        Port_list = Range_ports
    else:
        print(colored("\nSuch port does't exist!", 'red'))
        exit()
elif (Range_ports == 'not') or (Range_ports == 'no'): #ignore ports check
    check_ports = False
elif Range_ports == 'all': #all ports (1-65535)
    Port_list = [i for i in range(1, 65536)]
else:
    print(colored('\nEntered incorrectly range  ports!', 'red'))
    exit()

def scan(ip): #receive function IP, host name and MAC adress
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    client_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc, "host": socket.gethostbyaddr(element[1].psrc)}
        client_list.append(client_dict)
    return client_list

def ports(host, list_ports): #open ports search function
    connection = socket.socket()
    port_list_post = []
    for port in range(0, len(list_ports)):
        try:
            connection.connect((host, int(list_ports[port])))
        except socket.error:
            continue
        else:
            port_list_post.append(list_ports[port])
    if len(port_list_post) == 0:
        return colored("All ports are closed!", 'red')
    elif len(port_list_post) == 65535:
        return 'All ports'
    else:
        return str(*port_list_post)

def get_my_info(): #function to receive and output IP and hostname of your device
    res = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #getting your IP at the expese of a third-party
    res.connect(("duckduckgo.com", 80))                    #request to 'www.duckduckgo.com' on port 80
    ip = res.getsockname()[0]
    res.close()
    name_host = socket.gethostname()
    my_ip_host = socket.gethostbyname_ex(name_host)
    host = str(list(my_ip_host)[0])
    return colored("\nYour IP and Hostname respectively: " + ip + ' ' + host, 'yellow')
try:    
    ip_mac_host = scan(Range)
except PermissionError: #check availability root rights for 'linux'
    print(colored('\nTo continue need your root rights!', 'red'))
    exit()

if len(ip_mac_host) == 0: #checking the range of IP addresses for their presence in a given network
    print(colored("\nThis range of IP addresses doesn't exit on the networck!", 'red'))
    exit()

#appearance of the displayed information
print(colored("_" * 85, 'green'))
if platform == 'win32':
    print(colored("IP\t\t\t\tMAC Address\t\t\tHost", 'green'))
else: 
    print(colored("IP\t\t\tMAC Address\t\t\tHost", 'green'))
print(colored("_" * 85, 'green'))
for i in range(len(ip_mac_host)):
    print(colored(ip_mac_host[i]["ip"] + "\t|\t" + ip_mac_host[i]["mac"] + "\t|\t" + ip_mac_host[i]["host"][0], 'green'))
    if check_ports:
        print(colored("Open ports: ", 'green') + ports(ip_mac_host[i]["ip"], Port_list))
    print(colored("_" * 85, 'green'))
print(get_my_info())
