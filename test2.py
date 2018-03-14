from netmiko import ConnectHandler
import configparser
import connectivity
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
            config_commands.append("neighbor "+str(conf_2[nbor]["NeighbhorIP"])+" remote-as 100")
            config_commands.append("neighbor "+str(conf_2[nbor]["NeighbhorIP"])+" update-source loopback1")
            net_adv=conf_2[r_id]["NetworkListToAdvertise"]
            net_adv=net_adv.split("\"")
            print(type(str(net_adv)))
            config_commands.append("network "+str(net_adv[1])+" mask 255.255.255.255")
            #config_commands=["exit","conf t","do show ip route"]
            output=net_connect.send_config_set(config_commands)
            print(str(output))

