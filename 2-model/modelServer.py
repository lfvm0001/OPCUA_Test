from opcua import Server
import time

def start_server():   

    server = Server()

   #url = "opc.tcp://172.16.102.43:4840" #IP:port 
    url = "opc.tcp://192.168.0.100:4840" #IP:port
    server.set_endpoint(url)

    name = "OPCUA_SERVER_TEST"
    addspace = server.register_namespace(name)
    
    node = server.get_objects_node()
    server.import_xml('data_model.xml')
    
    server.start()
    print("Server started at {}".format(url))
    
    try: 
        while True:
            time.sleep(1)    

    finally:
        server.stop()

if __name__ == "__main__":
    start_server()


    

   