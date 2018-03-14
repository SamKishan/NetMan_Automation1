#import validateIP
import sys 
import os
def connectivity(a):
    #a=validateIP.checkip()
    ips=a[1]
    if("No invalid" not  in a[0]):
        print("Invalid IP found. Program exiting")
        sys.exit()
    print("The Routers IPs are")
    print (ips)
    status=1
    for i in range(len(ips)):
        output=str(os.popen("ping -c 2 "+str(ips[i])).read())
        if("0% packet loss" not in output):
            print("output: ")
            print(output)
            print("No connectivity to "+str(ips[i]))
            status=0
    print(str(len(a)))
    return status,ips



