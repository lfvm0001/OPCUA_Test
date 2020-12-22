from opcua import Client
import time

def start_client():

    url = "opc.tcp://192.168.0.100:4840"
    client = Client(url)
    
    try:
        client.connect()
        print("Client connected")
        
        root = client.get_root_node()  
        ledID = root.get_child(["0:Objects", "3:PC2", "3:led"])
        
        led = client.get_node(ledID)
          
        cnt = 0
        ledStatus = True
        
        while cnt<10:
        
            led.set_value(ledStatus)
            cnt += 1
            
            if ledStatus == True:
                ledStatus = False
            else:
                ledStatus = True
                
            time.sleep(2)

        print("\nDisconecting")
        client.disconnect()
    
    except KeyboardInterrupt:
        print("\nDisconnecting")
        client.disconnect()
        exit()
    
    except Exception:
        print("\nCant connect to server, try again")
        exit()
        
if __name__ == "__main__":
    start_client()