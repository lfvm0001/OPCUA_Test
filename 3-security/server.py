from opcua import Server, ua
import time

def start_server():   

    server = Server()

    url = "opc.tcp://10.82.132.99:4840" 
    server.set_endpoint(url)

    name = "OPCUA_SERVER_TEST"
    addspace = server.register_namespace(name)
    
    server.load_certificate("certificate.der")
    server.load_private_key("key.pem")
    server.set_security_policy([ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt])
    
    node = server.get_objects_node()
    param = node.add_object(addspace, "Parameters")

    temp = param.add_variable(addspace, "Temperature", 0)
    
    temp.set_writable()

    server.start()
    print("Server started at {}".format(url))
    
    try:
        Temperature = 25
        while True:
            time.sleep(2)
            Temperature += 1
            
            temp.set_value(Temperature)
            
            print(Temperature)   
    
    except KeyboardInterrupt:
        print("\nDisconnecting")
        server.stop()
        exit()

if __name__ == "__main__":
    start_server()


    