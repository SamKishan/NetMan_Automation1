These scripts allow for automation of iBGP(Internal Border Gateway Protocol) between two cisco routers (c3600) in the same autonomous systems.
"sshInfo.py" parses "sshInfo.json" to obtain the routers ssh credentials. "validateIP.py" makes sure all the IP addresses are valid. "connectivity.py" ensures there is IP connectivity between the routers. Lastly, "test2.py" is used to automate the configuration of iBGP between the routers. The "bgp.conf" file contains import BGP parameters for both the routers. 

These python scripts are imported as modules in the "lab6main.py" file. So, make sure all the python scripts along with the configuration files are present in the same directory/folder when you execute the code. 


To run the code: "python lab6main.py"


Notes: 
1) The loopback interfaces on R1 are 10.10.10.1/32 and 11.11.11.1/32.
2) The loopback interfaces on R2 are 20.20.20.1/32 and 22.22.22.1/32.
3) R1's fast ethernet interface address is 198.51.100.1
4) R2's fast ethernet interface address is 198.51.100.3
5) Make sure ssh is enabled on the routers. For help regarding this, refer to https://www.pluralsight.com/blog/tutorials/configure-secure-shell-ssh-on-cisco-router
6) The iBGP session is set up between the physical interfaces of the routers and NOT the loopback interfaces. However, the URL guide demonstrates how to set up iBGP between the loopback interfaces which is generally how iBGP is set up.
Note: Date of completion: 03-14-2018
For more information email me: saki8093@colorado.edu
