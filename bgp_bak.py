from netmiko import ConnectHandler
import configparser
import connectivity
import time
from prettytable import PrettyTable
status,ips=connectivity.connectivity()
print("status: "+str(status))
if(status==1):
    print("Pings successful")
else:
    print("Pings not successful")
config=configparser.ConfigParser()
config.read('test.conf')
routers=config.sections()
list_dict=[]

conf_2=configparser.ConfigParser()
conf_2.read('bgp.conf')
rout_ids=conf_2.sections()

for i in range(len(routers)):
    list_dict.append({
        'device_type':config[routers[i]]['device_type'],
        'ip':config[routers[i]]['ip'],
        'username':config[routers[i]]['username'],
        'password':config[routers[i]]['password'],        
        })

#Part 1: configure iBGP on both the routers
for i in range(len(list_dict)):
    net_connect=ConnectHandler(**list_dict[i])
    for r_id in rout_ids:
        if((list_dict[i]['ip'])==conf_2[r_id]['RouterID']):
            config_commands=[]
            config_commands.append("router bgp 100")
            for k in range(len(rout_ids)):
                if(rout_ids[k]==r_id):
                    nbor=rout_ids[k]
                    break    
            first_nbr=conf_2[nbor]["NeighbhorIP"].split("\"")[1]
            second_nbr=conf_2[nbor]["NeighbhorIP"].split("\"")[3]
            config_commands.append("neighbor "+str(first_nbr)+" remote-as 100")
            config_commands.append("neighbor "+str(first_nbr)+" update-source loopback1")
            config_commands.append("neighbor "+str(second_nbr)+" remote-as 100")
            config_commands.append("neighbor "+str(second_nbr)+" update-source loopback2")
            net_adv=conf_2[r_id]["NetworkListToAdvertise"]
            net_adv=net_adv.split("\"")
            print(type(str(net_adv)))
            config_commands.append("network "+str(net_adv[1])+" mask 255.255.255.255")
            config_commands.append("network "+str(net_adv[3])+" mask 255.255.255.255")
            #Second part
            '''show_commands=[]
            show_commands.append("do show ip bgp summary")
            show_commands.append("do show ip bgp")'''
            output=net_connect.send_config_set(config_commands)
        
            #show_output=net_connect.send_config_set(show_commands)
            #print(str(show_output))

#Show iBGP summary on both the routers
time.sleep(10)
status=PrettyTable()
status.field_names=["BGP Neighbor IP","BGP Neighbor AS","BGP Neighbor State"]

for i in range(len(list_dict)):
    net_connect=ConnectHandler(**list_dict[i])
    for r_id in rout_ids:
        if((list_dict[i]['ip'])==conf_2[r_id]['RouterID']):
            show_commands=[]
            show_commands.append("do show ip bgp summary")
            #show_commands.append("do show ip bgp")
            show_output=net_connect.send_config_set(show_commands)
            #print(show_output)     
            f=open("show_output.txt","w")
            f.write(show_output)
            f.close()
            f=open("show_output.txt","r")  
            content=f.readlines()
            start=0
            for line in content:      
                #print("line is:")
                #print(line)
                if(start==1):   
                    entry=line.split()
                    if(len(entry)>=8):
                        if(entry[len(entry)-1].isdigit()):
                            status.add_row([entry[0],entry[2],"Established"])
                        else:
                            status.add_row([entry[0],entry[2],entry[len(entry)-1]])                                        
                if("Neighbor" in line and "AS" in line and"MsgSent" in line):
                    start=1
                if("end" in line):
                    break
    try:
        print(str(list_dist[i]))
    except:
        pass
    print(status)      
    status.clear_rows()


#Saving running-config
for i in range(len(list_dict)):
    net_connect=ConnectHandler(**list_dict[i])
    for r_id in rout_ids:
        if((list_dict[i]['ip'])==conf_2[r_id]['RouterID']):
            conf_sav_cmd="do show run"
            output=net_connect.send_config_set(conf_sav_cmd)
            f=open("Router:"+str(r_id)+"-config.txt","w")
            f.write(output)
            f.close()
print("Names of the file containing configs are in the format \"Router:<Router>-config.txt") 

                        
