#import sshInfo
def checkip(sshInfo):
    status=1
    response=""
    #print(str(sshInfo.func()))
    invalid_ip=["10.10.300.10","127.0.0.1","198.51.100.2","192.168.1"]
    parsed_ip=[]
    valid_ip=[]
    for router in sshInfo:
        ip=str(sshInfo[router]["IP address"])
        #print(ip)
        valid_ip.append(ip)
        for i in range(len(invalid_ip)):
            if (invalid_ip[i] in ip or invalid_ip[i]==ip):
                #print("Found an invalid ip:"+ip)
                #print("Program exiting")
                response="Found an invalid ip:"+ip
                status=0

    if(status==1):
        response="No invalid IPs found"
    return response,valid_ip



