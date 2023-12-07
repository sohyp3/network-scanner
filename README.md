 # Network Scanner
 a Simple tool that scans the network using `fping` then scans each device's port using `nmap` then saves it to a csv files

# Requirements:
1. `linux`
2. `python3`
3. `nmap`
4. `fping`

### The Commands in use:
1. `fping -q -a -g [network/subnet] -r 0`
2. `nmap -sS -n --host-timeout 30s [deviceip]`



