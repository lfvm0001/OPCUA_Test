from opcua import Client
import time

def start_client():
    
    url = "opc.tcp://172.16.102.43:4840" #IP:port 
   #url = "opc.tcp://192.168.0.100:4840" #IP:port
    client = Client(url)
    
    try:
        client.connect()
        print("Client connected")
        
        root = client.get_root_node()  
        tempID = root.get_child(["0:Objects", "3:Pi1", "3:temp"])
        ledID = root.get_child(["0:Objects", "3:Pi1", "3:led"])
        
        temp = client.get_node(tempID)
        led = client.get_node(ledID)
          
        temperature = 25
        
        while temperature<30:
        
            temp.set_value(temperature)
            temperature += 1
            time.sleep(2)

        print("Disconecting")
        client.disconnect()
    
    except:
        print("Something went wrong")
        
if __name__ == "__main__":
    start_client()