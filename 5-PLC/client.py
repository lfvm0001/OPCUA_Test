from opcua import Client
import time

def start_client():
    
    url = "opc.tcp://172.16.1.166:4840" #IP:port 
    client = Client(url)
    
    try:
        client.connect()
        print("Client connected")
        
        temp = client.get_node("ns=2; i=2")
        timeS = client.get_node("ns=2; i=3")
        
        cont = 0
        while cont<20:
            Temperature = temp.get_value()
            print(Temperature)
    
            timeStamp = timeS.get_value()
            print(timeStamp)
            
            time.sleep(2)
            cont += 1
            
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