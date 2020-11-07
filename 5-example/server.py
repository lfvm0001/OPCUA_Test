from opcua import Server, ua
import datetime
import os.path
import time
import sys
import re

def start_server(file):  

    server = Server()
    
    #IP:port 
    #url = "opc.tcp://192.168.0.100:4840" 
    url = "opc.tcp://172.16.1.166:4840"

    #Configurar servidor en url definido e importar archivo de modelo de informacion 
    server.set_endpoint(url)
    server.import_xml(file)
 
    #Si se desea seguridad a la hora de conectarse, cargar el certificado y la key 
    #Deben estar en el mismo directorio y el cliente tambien debe tenerlos
    server.load_certificate("certificate.pem")
    server.load_private_key("key.pem")
    server.set_security_policy([ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt]) 
    
    #Iniciar servidor
    server.start()        
    print("Server started at {}\n".format(url))
    
    try:
    
        #Leer archivo para determinar los espacios con sus respectivos objetos y variables
        nameSpaces = []
        objects    = []
        variables  = []
        
        searchfile = open(file, "r")
        for line in searchfile:
            if "<Uri>" in line: 
                nameS = re.sub('</Uri>|<Uri>','',line)
                nameS = nameS.strip()

                nsIndex = server.get_namespace_index(nameS)
                dict_nameS = {"name": nameS, "index": nsIndex}
                nameSpaces.append(dict_nameS)
                
            if "<UAObject" in line:
                obj = re.sub('.*BrowseName="|".*','',line)
                obj = obj.strip()
                obj = re.split(":",obj)
                
                id = re.sub('.*NodeId="ns=\d;i=*|".*','',line)
                id = id.strip()
                
                dict_objs = {"i":int(obj[0])-1, "name":obj[1], "id":id}
                objects.append(dict_objs)
                
            if "<UAVariable" in line:
                var = re.sub('.*BrowseName="|".*','',line)
                var = var.strip()
                var = re.split(":",var)
                
                id = re.sub('.* NodeId="ns=\d;i=*|".*','',line)
                id = id.strip()
                
                parentid = re.sub('.*ParentNodeId="ns=\d;i=*|".*','',line)
                parentid = parentid.strip()
                
                dict_vars = {"i":int(var[0])-1, "name":var[1], "id":id, "parentid":parentid}
                variables.append(dict_vars)
         
        searchfile.close()
        
        for dicO in objects:
            dicO["ns"] = nameSpaces[dicO["i"]]["index"]
            for dicVar in variables:
                dicVar["ns"] = nameSpaces[dicVar["i"]]["index"]
                if dicVar["parentid"] == dicO["id"]:
                    dicVar["parentName"] = dicO["name"]
           
           
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
                                TIME = datetime.datetime.now()
                                node = server.get_node("ns=" + str(dicVar["ns"]) + "; i=" + str(dicVar["id"]))
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

    