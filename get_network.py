import ipaddress
import subprocess,re




def check():
    pass


def subnet_to_cidr(subnet_mask):
    octets = subnet_mask.split('.')
    bit_count = sum(bin(int(octet)).count('1') for octet in octets)
    return f'/{bit_count}'



def get_network_address(ip, subnet_mask):
    interface = ipaddress.IPv4Interface(f'{ip}/{subnet_mask}')

    network_address = interface.network.network_address

    return str(network_address)


def parse_ifconfig():
    result = subprocess.run(['ifconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    interfaces = result.stdout.split('\n\n')

    network_info = {}

    for interface in interfaces:
        match_name = re.search(r'^(\w+)', interface, re.MULTILINE)
        if match_name:
            name = match_name.group(1)
            network_info[name] = {}
            match_ip = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', interface)
            if match_ip:
                network_info[name]['IP Address'] = match_ip.group(1)

            match_mask = re.search(r'netmask (\d+\.\d+\.\d+\.\d+)', interface)
            if match_mask:
                network_info[name]['Subnet Mask'] = match_mask.group(1)

    return network_info




def main():
    network_info = parse_ifconfig()
    for interface in network_info:
        print(f"Interface: {interface}")
        for key, value in network_info[interface].items():
            print(f" \t {key}: {value}")






    while True:

        print('===')
        choice = input("Select the network interface: (0 to select custom ip/mask) ")

        if choice == "0":
            device_ip= input("enter device IP: ")
            ipc = False # to check if its valid to break later
            try:
                ipaddress.ip_address(device_ip)
                ipc = True
            except ValueError:
                print("Enter a valid IP")


            subnet_mask= input("enter subnet mask: ")
            subc = False
            try:
                ipaddress.ip_address(subnet_mask)
                subc = True
            except ValueError:
                print("Enter a valid mask")
            
            if ipc and subc:
                break

        else:
            try:
                key,value = network_info[choice].items()
                device_ip = key[1]
                subnet_mask = value[1]
                print(f"Selected {choice}: \n ip : {device_ip}, subnet: {subnet_mask}")
                break
            except:
                print("doesn't exist")


    print('===')
    network_ip = get_network_address(device_ip, subnet_mask)
    subnet_cidr = subnet_to_cidr(subnet_mask)
    output_ip = network_ip + subnet_cidr



    print("\n===\n===\n")
    return output_ip


if __name__ == '__main__':
    output_ip = main()
    print(f"Network IP: {output_ip}")


