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
        tempID = root.get_child(["0:Objects", "3:PC", "3:temp"])
        timeID = root.get_child(["0:Objects", "3:PC", "3:timeStamp"])
        
        tempS = client.get_node(tempID)
        timeS = client.get_node(timeID)
          
        temperature = 20
        
        while temperature<30:
        
            TIME = datetime.datetime.now()
            
            tempS.set_value(temperature)
            timeS.set_value(TIME)
        
            temperature += 1
            time.sleep(2)

        print("Disconecting")
        client.disconnect()
    
    except:
        print("Something went wrong")
        
if __name__ == "__main__":
    start_client()