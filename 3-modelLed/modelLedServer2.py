from opcua import Server
import RPi.GPIO as GPIO 
import time

def start_server():   

    server = Server()

   #url = "opc.tcp://172.16.102.43:4840" #IP:port 
    url = "opc.tcp://192.168.0.100:4840" #IP:port
    server.set_endpoint(url)
    
    server.import_xml('model_led.xml')
    
    server.start()
    print("Server started at {}".format(url))
    
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)
    
    try: 
        root = server.get_root_node()  
        statusID = root.get_child(["0:Objects", "3:led", "3:status"])
        
        status = server.get_node(statusID)
                  
        while True:
            
            led = status.get_value()
            
            if led == True:
                GPIO.output(8, GPIO.HIGH) 
            else:
                GPIO.output(8, GPIO.LOW)

    except KeyboardInterrupt:
        print("\nDisconnecting")
        server.stop()
        exit()

if __name__ == "__main__":
    start_server()


    

   