from netmiko import ConnectHandler
import connectivity
status=connectivity.connectivity()
print("status: "+str(status))
if(status==1):
    print("Pings successful")
else:
    print("Pings not successful")
R1 = {
    'device_type' : 'cisco_ios',
    'ip' : '198.51.100.1',
    'username' : 'samkishan',
    'password' : 'Qwerty_1234',
}

R2 = {
    'device_type' : 'cisco_ios',
    'ip' : '198.51.100.3',
    'username' : 'samkishan',
    'password' : 'Qwerty_1234',
}

net_connect_r1=ConnectHandler(**R1)
<<<<<<< HEAD
config_commands_r1=["ip route 20.20.20.1 255.255.255.255 198.51.100.3","ip route 22.22.22.1 255.255.255.255 198.51.100.3"]
output_r1=net_connect_r1.send_config_set(config_commands_r1)
print(str(output_r1))
net_connect_r2=ConnectHandler(**R2)
config_commands_r2=["ip route 10.10.10.1 255.255.255.255 198.51.100.1","ip route 11.11.11.1 255.255.255.255 198.51.100.1"]
=======
config_commands_r1=["conf t","ip route 20.20.20.1 255.255.255.255 198.51.100.3","ip route 22.22.22.1 255.255.255.255 198.51.100.3"]
output_r1=net_connect_r1.send_config_set(config_commands_r1)
print(str(output_r1))
net_connect_r2=ConnectHandler(**R2)
config_commands_r2=["conf t","ip route 10.10.10.1 255.255.255.255 198.51.100.1","ip route 11.11.11.1 255.255.255.255 198.51.100.1"]
>>>>>>> 321da22d11eda7f9b3dd456f80cf3654c68a0daa
output_r2=net_connect_r2.send_config_set(config_commands_r2)
print(str(output_r2))


