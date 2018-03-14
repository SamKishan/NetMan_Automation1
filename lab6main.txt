import sshInfo
import validateIP
import connectivity
import bgp
a=validateIP.checkip(sshInfo.func())
status,ips=connectivity.connectivity(a)
bgp.bgp_func(status,ips)

