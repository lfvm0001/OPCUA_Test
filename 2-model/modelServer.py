from opcua import Server
import time

def start_server():   

    server = Server()
    url = "opc.tcp://192.168.0.108:4840"
    server.set_endpoint(url)
    
    server.import_xml('data_model.xml')
    
    server.start()
    print("Server started at {}".format(url))
    
    try: 
        while True:
            time.sleep(1)    

    except KeyboardInterrupt:
        print("\nDisconnecting")
        server.stop()
        exit()

if __name__ == "__main__":
    start_server()


    

   