from opcua import Client
import RPi.GPIO as GPIO 
import time

def start_client():
    
    url = "opc.tcp://172.16.102.43:4840" #IP:port 
   #url = "opc.tcp://192.168.0.100:4840" #IP:port
    client = Client(url)
    
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)
    
    try:
        client.connect()
        print("Client connected")
        
        root = client.get_root_node()  
        statusID = root.get_child(["0:Objects", "3:led", "3:status"])
        
        status = client.get_node(statusID)
                  
        while True:
            
            led = status.get_value()
            
            if led == True:
                GPIO.output(8, GPIO.HIGH) 
            else:
                GPIO.output(8, GPIO.LOW)
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\nDisconnecting")
        client.disconnect()
        exit()
    
    except Exception:
        print("\nCant connect to server, try again")
        exit()
        
if __name__ == "__main__":
    start_client()