from netmiko import ConnectHandler
import configparser
import connectivity
import time
from prettytable import PrettyTable
import os
from threading import Thread

def cmd_execute(command,group,net_connect):
    if(group=="bgp"):
        output=str(net_connect.send_config_set(["router bgp 100",command]))
    else:
        output=str(net_connect.send_config_set(command))
    if("%" in output):
        print("Error")
        print(output)
        return 0,output
    else:
        return 1,output



def iBGP_config(list_dict,i,rout_ids,conf_2):
    net_connect=ConnectHandler(**list_dict[i])
    for r_id in rout_ids: 
        if((list_dict[i]['ip'])==conf_2[r_id]['RouterID']):
            config_commands=[]
            for k in range(len(rout_ids)):
                if(rout_ids[k]==r_id):
                    nbor=rout_ids[k]
                    break    
            first_nbr=conf_2[nbor]["NeighbhorIP"]
            #second_nbr=conf_2[nbor]["NeighbhorIP"].split("\"")[3]
            config_commands.append("neighbor "+str(first_nbr)+" remote-as 100")
            #config_commands.append("neighbor "+str(second_nbr)+" remote-as 100")
            #config_commands.append("neighbor "+str(second_nbr)+" update-source loopback2")
            net_adv=conf_2[r_id]["NetworkListToAdvertise"]
            net_adv=net_adv.split("\"")
            config_commands.append("network "+str(net_adv[1])+" mask 255.255.255.255")
            config_commands.append("network "+str(net_adv[3])+" mask 255.255.255.255")
            config_commands.append("neighbor "+str(first_nbr)+" update-source loopback1")
            for l in range(len(config_commands)):
                group="bgp"
                status,output=cmd_execute(config_commands[l],group,net_connect)
                if(status==0):
                    print("Error in execution!!!")
                    break    

def iBGP_summary(list_dict,i,rout_ids,conf_2,stat):
    net_connect=ConnectHandler(**list_dict[i])
    for r_id in rout_ids:
        if((list_dict[i]['ip'])==conf_2[r_id]['RouterID']):
            show_commands=[]
            show_commands.append("do show ip bgp summary")
            for m in range(len(show_commands)):
                status,show_output=cmd_execute(show_commands[m],"normal",net_connect)
                if(status==0):
                    print("Error in command")
                    break
                f=open("show_output.txt","w+")
                f.write(show_output)
                f.close()
            f=open("show_output.txt","r")  
            content=f.readlines()
            start=0
            os.remove("show_output.txt")
            for line in content:      
                if(start==1):   
                    entry=line.split()
                    if(len(entry)>=8):
                        if(entry[len(entry)-1].isdigit()):
                            stat.add_row([entry[0],entry[2],"Established"])
                        else:
                            stat.add_row([entry[0],entry[2],entry[len(entry)-1]])                                        
                if("Neighbor" in line and "AS" in line and"MsgSent" in line):
                    start=1
                if("end" in line):
                    break
    try:
        print(str(list_dist[i]))
    except:
        pass
    print("\nRouter: R"+str(i+1))
    print(stat)      
    stat.clear_rows()



def iBGP_ConfSave(list_dict,i,rout_ids,conf_2):
    net_connect=ConnectHandler(**list_dict[i])
    for r_id in rout_ids:
        if((list_dict[i]['ip'])==conf_2[r_id]['RouterID']):
            conf_sav_cmd=[]
            conf_sav_cmd.append("do show run")
            for i in range(len(conf_sav_cmd)):
                status,output=cmd_execute(conf_sav_cmd[i],"normal",net_connect)
                if(status==0):
                    print("Error in execution")
                    break
                f=open("Router:"+str(r_id)+"-config.txt","w")
                f.write(output)
                f.close()





def bgp_func(status,ips):
    if(status==1):
        print("IP connectivity to routers:yes")
    else:
        print("Error: No IP connectivity to routers")
    config=configparser.ConfigParser()
    config.read('test.conf')
    routers=config.sections()
    list_dict=[]

    conf_2=configparser.ConfigParser()
    conf_2.read('bgp.conf')
    rout_ids=conf_2.sections()

    print("------------------------------------------------")
    print("This process takes under 2  minutes to complete.")
    print("------------------------------------------------")
    def cmd_execute(command,group):
        if(group=="bgp"):
            output=str(net_connect.send_config_set(["router bgp 100",command]))
        else:
            output=str(net_connect.send_config_set(command))
        if("%" in output):
            print("Error")
            print(output)
            return 0,output
        else:
            return 1,output




    for i in range(len(routers)):
        list_dict.append({
            'device_type':config[routers[i]]['device_type'],
            'ip':config[routers[i]]['ip'],
            'username':config[routers[i]]['username'],
            'password':config[routers[i]]['password'],        
            })


    #Part 1: configure iBGP on both the routers
    for i in range(len(list_dict)):
        t=Thread(target=iBGP_config,args=(list_dict,i,rout_ids,conf_2))
        t.start()
    time.sleep(10)
    stat=PrettyTable()
    stat.field_names=["BGP Neighbor IP","BGP Neighbor AS","BGP Neighbor State"]
    print("Waiting for iBGP configuration to fully complete")
    time.sleep(25)
    for i in range(len(list_dict)):
        t_2=Thread(target=iBGP_summary,args=(list_dict,i,rout_ids,conf_2,stat))
        t_2.start()

    #Saving running-config
    for i in range(len(list_dict)):
        t_3=Thread(target=iBGP_ConfSave,args=(list_dict,i,rout_ids,conf_2))
        t_3.start()
    print("Names of the file containing configs are in the format \"Router:<Router>-config.txt") 

    time.sleep(30)
    print("Config file names:")
    output=os.system("ls | grep \"Router\"")
    print(output)
                            
