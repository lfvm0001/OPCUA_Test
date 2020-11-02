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
        statusID = root.get_child(["0:Objects", "3:led", "3:status"])
        
        status = client.get_node(statusID)
                  
        while True:
            
            led = input("Apagar(A) o Encender(E): ")
            
            if led == "E" or led == "e":
                status.set_value(True) 
            elif led =="A" or led =="a":
                status.set_value(False)
            else:
                print("Ingrese A o E")
            

    except KeyboardInterrupt:
        print("\nDisconnecting")
        client.disconnect()
        exit()
    
    except Exception:
        print("\nCant connect to server, try again")
        exit()
        
if __name__ == "__main__":
    start_client()