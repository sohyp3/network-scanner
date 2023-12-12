 # Network Scanner
 a Simple tool that scans the network for the connected devices using `fping` then scans each device's open port using `nmap` then saves it to a csv files

# Requirements:
1. `linux`
2. `python3`
3. `nmap`
4. `fping`
5. `net-tools` (_ifconfig_)

# To Run it:
* `git clone https://github.com/sohyp3/network-scanner`
* `cd network-scanner`
* `sudo python3 app.py`
* it will create two files
    1. `ips.csv` the ips of the devices in your network
    2. `ports.csv` the open ports for each ip

### The Commands the scripts uses:
1. `fping -q -a -g [network/subnet] -r 0`
2. `nmap -sS -n --host-timeout 30s [deviceip]`

