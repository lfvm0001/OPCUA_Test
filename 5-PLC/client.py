from opcua import Client
import time

def start_client():
    
    url = "opc.tcp://10.82.132.99:4840"
    client = Client(url)
    client.set_security_string("Basic256Sha256,SignAndEncrypt,certificate.der,key.pem")
    
    try:
        client.connect()
        print("Client connected")
        
    except KeyboardInterrupt:
        print("\nDisconnecting")
        client.disconnect()
        exit()
    
    except Exception:
        print("\nCant connect to server, try again")
        exit()
    

        
if __name__ == "__main__":
    start_client()