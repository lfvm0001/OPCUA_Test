from opcua import Client
import datetime
import time

def start_client():
    
    url = "opc.tcp://172.16.102.43:4840" #IP:port 
   #url = "opc.tcp://192.168.0.100:4840" #IP:port
    client = Client(url)
    
    try:
        client.connect()
        print("Client connected")
        
        root = client.get_root_node()  
        timeID = root.get_child(["0:Objects", "3:Ordenador1", "3:time"])
        
        timeS = client.get_node(timeID)

          
        cont = 0
        
        while cont<20:
            TIME = datetime.datetime.now()
            timeS.set_value(TIME)
        
            cont += 1
            time.sleep(2)

        print("Disconecting")
        client.disconnect()
    
    except:
        print("Something went wrong")
        
if __name__ == "__main__":
    start_client()