from readXML import read_file
from opcua import Client
import datetime
import os.path
import time
import sys

def start_client(file):  
    
    #IP:Puerto
    #url = "opc.tcp://192.168.0.100:4840" #IP:port
    url = "opc.tcp://172.16.102.43:4840"

    client = Client(url)
    
    #Si se desea seguridad a la hora de conectarse, cargar el certificado y key 
    #Deben estar en el mismo directorio 
    if not (os.path.isfile('certificate.pem') and os.path.isfile('key.pem')):
        print("No certificate or key found")
        print("Cant connect to server, try again")
        exit()

    try:       
        client.set_security_string("Basic256Sha256,SignAndEncrypt,certificate.pem,key.pem")
        client.connect()
        print("Client connected")

        #Leer archivo para determinar los espacios con sus respectivos objetos y variables
        nameSpaces, objects, variables = read_file(client, file)

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
                                node = client.get_node("ns=" + str(dicVar["ns"]) + "; i=" + str(dicVar["id"]))
                                TIME = datetime.datetime.now()
                                node.set_value(TIME)
                                
                            #Observar el valor de cada una de las variables 
                            if dicVar["ns"] == dicNs["index"] and dicVar["parentid"] == dicO["id"]:
                                node = client.get_node("ns=" + str(dicVar["ns"]) + "; i=" + str(dicVar["id"]))
                                value = node.get_value()
                                print("   " + dicVar["name"] + ": " + str(value))

            print("*****************************************\n")

            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\nDisconnecting")
        client.disconnect()
        exit()
    
    except Exception:
        print("\nCant connect to server, try again")
        exit()

if __name__ == "__main__":

    if len(sys.argv) == 2:
       
       file = sys.argv[1]
       
       if os.path.isfile(file):
        start_client(file)
        
       else:
        print("File doesnt exist")
        
    else:
        print("ERROR: 1 file name is required")

    