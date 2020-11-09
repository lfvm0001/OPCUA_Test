from opcua import Client, ua
from opcua.common.ua_utils import get_nodes_of_namespace
import datetime
import os.path
import time
import sys
import re
nodes=[]

def get_nodes(client,node):
    for childId in node.get_children():
        ch = client.get_node(childId)
        if ch.get_node_class() == ua.NodeClass.Object:
            nodes.append(ch)
            get_nodes(client,ch)
        elif ch.get_node_class() == ua.NodeClass.Variable:
            nodes.append(ch)


def start_client():  
    

    url = "opc.tcp://172.16.102.43:4840"

    client = Client(url)


    client.connect()
    print("Client connected")
    
    
    
    root = client.get_root_node()
    x = root.get_children()
    get_nodes(client,x[0])
    
    #print(nodes)
    #client.export_xml(nodes,'file1111.xml')
    #print("done")
    # x=client.get_namespace_array()
    # namespaces = []
    # nodes = get_nodes_of_namespace(client,namespaces)
    client.export_xml(nodes, 'file.xml')
    print("done")

    while True:

        time.sleep(0.1)


if __name__ == "__main__":
    
    start_client()
        

    


   

   

