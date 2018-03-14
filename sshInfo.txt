import os
import sys
import json
from prettytable import PrettyTable
def func():
    filename="sshInfo.json"
    ssh_info=PrettyTable(["Router","username","password","IP address"])
    if(os.path.isfile(filename)==0):
        print("Error! The json file containing the router login credentials is not present")
        sys.exit()
    ip=[]
    json_file="sshInfo.json"
    json_data=open(json_file)
    ssh_data=json.load(json_data)
    for route in ssh_data:
        ssh_info.add_row([str(route),str(ssh_data[route]["username"]),str(ssh_data[route]["password"]),str(ssh_data[route]["IP address"])])
    #print(ssh_info)

    return (ssh_data)

#func()
