from opcua import Server, ua
from readXML import read_file
import datetime
import os.path
import time
import sys

def start_server(file):  

    server = Server()
    
    #IP:port 
    #url = "opc.tcp://192.168.0.100:4840" 
    url = "opc.tcp://172.16.1.166:4840"

    #Configurar servidor en url definido e importar archivo de modelo de informacion 
    server.set_endpoint(url)
    server.import_xml(file)
 
    #Si se desea seguridad a la hora de conectarse, cargar el certificado y key 
    #Deben estar en el mismo directorio y el cliente tambien debe tenerlos
    server.load_certificate("certificate.pem")
    server.load_private_key("key.pem")
    server.set_security_policy([ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt]) 
    
    #Iniciar servidor
    server.start()        
    print("Server started at {}\n".format(url))
    
    try:
    
        #Leer archivo para determinar los espacios con sus respectivos objetos y variables
        response = read_file(server, file)
        nameSpaces = response[0]
        objects    = response[1]
        variables  = response[2]

        #Aca van las acciones del servidor
        while True:
            
            #Recorrer los arreglos para imprimir las variables
            print("*****************************************")           
            for dicNs in nameSpaces:
                print("---------" + dicNs["name"] + "---------")
                
                for dicO in objects:
                    if dicO["ns"] == dicNs["index"]: 
                        print(" " + dicO["name"])
                        
                        for dicVar in variables:
                            
                            #Escribir el valor de una de las variables
                            if dicVar["name"] == "timeStamp" and dicVar["parentName"] == "Other":
                                node = server.get_node("ns=" + str(dicVar["ns"]) + "; i=" + str(dicVar["id"]))
                                TIME = datetime.datetime.now()
                                node.set_value(TIME)
                                
                            #Observar el valor de cada una de las variables 
                            if dicVar["ns"] == dicNs["index"] and dicVar["parentid"] == dicO["id"]:
                                node = server.get_node("ns=" + str(dicVar["ns"]) + "; i=" + str(dicVar["id"]))
                                value = node.get_value()
                                print("   " + dicVar["name"] + ": " + str(value))

            print("*****************************************\n")
 
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\nDisconnecting")
        server.stop()
        exit()

if __name__ == "__main__":

    if len(sys.argv) == 2:
       
       file = sys.argv[1]
       
       if os.path.isfile(file):
        start_server(file)
        
       else:
        print("File doesnt exist")
        
    else:
        print("ERROR: 1 file name is required")

    