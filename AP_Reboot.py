from netmiko import ConnectHandler
import time

# =========================
# SWITCH SETTINGS
# =========================

SWITCH = {
    "device_type": "cisco_ios",
    "host": "",
    "username": "",
    "password": "",
}
connection = None

print("Connecting to switch...")
connection = ConnectHandler(**SWITCH)

#Show Power Inline to search for APs, place in list

AP_LIST = []

power_inline = connection.send_command("show power inline", use_textfsm=True)

for intf in power_inline:
    if intf['device'] == 'C9120AXI-B':
        AP_LIST.append(intf['interface'])
print(AP_LIST)

shutdown_cmds = []
noshutdown_cmds = []

if AP_LIST == []:
    print("No APs found to reboot.")
    exit()

#Disable AP Switch Ports
print(f"Disabling{AP_LIST}...")
for intf in AP_LIST:
    shutdown_cmds.extend([
        f"interface {intf}",
        "shutdown"
    ])

connection.send_config_set(shutdown_cmds)

time.sleep(3)

#Enable AP Switch Ports
print(f"Enabling {AP_LIST}...")
for intf in AP_LIST:
    noshutdown_cmds.extend([
        f"interface {intf}",
        "no shutdown"
    ])

connection.send_config_set(noshutdown_cmds)


connection.disconnect()
print("\nDisconnected from switch.")
