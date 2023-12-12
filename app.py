import os, sys,re,subprocess,csv,ipaddress
from get_network import main

def exec_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr


def check():
    req_packages = ['nmap', 'fping']
    should_e = False
    for pack in req_packages:
        out,err = exec_cmd(f'which {pack}')
        if err:
            print(f"plase install {pack}")
            should_e = True

    if os.geteuid() != 0:
        print('run the code with sudo')
        should_e = True
    if should_e:
        sys.exit()

    # the reason im writing in every loop instead of saving it to a list then save it, if a problem happened you dont loose all the data, and its being run  in device and its powerfull enough


ips_file = 'ips.csv'
def get_ips(network_ip):
    ips = []
    with open (ips_file,"w"):
        pass

    ip_output,err = exec_cmd(f"fping -q -a -g {network_ip} -r 0")
    ip_list = ip_output.split('\n')

    for ip in ip_list:

        with open(ips_file ,'a') as f:
            writer = csv.writer(f)
            writer.writerow([ip])


open_ports_file = "ports.csv"

def scan_ips():
    with open(open_ports_file,'w') as f:
        pass
        
    with open(ips_file,'r') as f:
        reader = csv.reader(f)
        for ip in reader:
            if ip and len(str(ip).split('.')) == 4:
                out = exec_cmd(f"nmap -sS -n --host-timeout 30s {ip[0]}")
                print(out)
                ports,mac_addr = extract_info( out)
                data = [ip[0],ports,mac_addr]
                with open(open_ports_file,"a") as f:
                    writer = csv.writer(f)
                    writer.writerow(data)

def extract_info(nmap_output_tuple):

    nmap_output = nmap_output_tuple[0]
    mac_address_search = re.search(r"MAC Address: ([\w:]+) \((.+)\)", nmap_output)
    if mac_address_search:
        mac_address = mac_address_search.group(1) + "-" + mac_address_search.group(2)
    else:
        mac_address = "Not Found"
        device_name = "Not Found"

    open_ports = re.findall(r"(\d+/tcp)\s+open\s+(\S+)", nmap_output)
    open_ports_services = [(port.split('/')[0], service) for port, service in open_ports]
    


    return open_ports_services, mac_address


check()


while True:
    auto_ip = input("Do you want to automaticly get the ip?(Y/n) ")
    if auto_ip.lower() =="n":
        network_ip = input("Enter the network IP with the CIDR: (ex: 192.168.1.1/24) ")
        network_ip = network_ip.replace(" ", "")
        if "/" in network_ip:
            split_ip = network_ip.split('/')
            if len(split_ip) == 2:
                try:
                    ipaddress.ip_address(split_ip[0])
                    int(split_ip[1])
                    break
                except:
                    pass
        print('Enter Something valid... \nyou can run - python3 get_network.py - to get your network ip! ')

    else:
        network_ip = main()
        break

get_ips(network_ip)
scan_ips()

