from opcua import Client, ua
import datetime
import os.path
import time
import sys
import re


def start_client(file):  
    

    url = "opc.tcp://172.16.1.166:4840"

    client = Client(url)
    client.set_security_string("Basic256Sha256,SignAndEncrypt,certificate.pem,key.pem")


    client.connect()
    print("Client connected")
    
    node = client.get_root_node()
    nodes = []
    
    for childId in node.get_children():
        ch = client.get_node(childId)
        print(ch.get_node_class())
        if ch.get_node_class() == ua.NodeClass.Object:
            print("objeto")
            print(ch)
            nodes.append(ch)
        elif ch.get_node_class() == ua.NodeClass.Variable:
            print("var")
            print(ch)
    
    print(nodes)
    client.export_xml(nodes,'file1111.xml')
            
        
    while True:

        time.sleep(0.1)


if __name__ == "__main__":

    if len(sys.argv) == 2:
       
       file = sys.argv[1]
       
       if os.path.isfile(file):

        start_client(file)
        
       else:
        print("File doesnt exist")
        
    else:
        print("ERROR: 1 file name is required")

    


   

   

