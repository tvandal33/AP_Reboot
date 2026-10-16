from netmiko import ConnectHandler

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

power_inline = connection.send_command("show power inline | i AP", use_textfsm=True)
print(power_inline)


#Go from list of APs and reboot each one