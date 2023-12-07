import ipaddress

def get_network_address(ip, subnet_mask):
    interface = ipaddress.IPv4Interface(f'{ip}/{subnet_mask}')

    network_address = interface.network.network_address

    return str(network_address)

device_ip = '172.16.0.211'
subnet_mask = '255.255.252.0'

print("you can get the device ip/subnet mask by running ifconfig in the terminal")
while True:
    device_ip= input("enter device IP: ")
    try:
        ipaddress.ip_address(device_ip)
        break
    except ValueError:
        print("Enter a valid IP")


while True:
    subnet_mask= input("enter subnet mask: ")
    try:
        ipaddress.ip_address(subnet_mask)
        break
    except ValueError:
        print("Enter a valid mask")

network_ip = get_network_address(device_ip, subnet_mask)
print(f"Network IP: {network_ip}")

