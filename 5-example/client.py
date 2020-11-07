from opcua import Client
import RPi.GPIO as GPIO 
import Adafruit_ADS1x15
import datetime
import os.path
import time
import sys
import re


def start_client(file):  
    
    #Inicializar ADC
    adc = Adafruit_ADS1x15.ADS1115()
    GAIN = 2/3

    #IP:Puerto
    #url = "opc.tcp://192.168.0.100:4840" #IP:port
    url = "opc.tcp://172.16.1.166:4840"

    client = Client(url)
    
    #Si se desea seguridad a la hora de conectarse, cargar el certificado y la key 
    #Deben estar en el mismo directorio 
    if not (os.path.isfile('certificate.pem') and os.path.isfile('key.pem')):
        print("No certificate or key found")
        print("Cant connect to server, try again")
        exit()
        
    client.set_security_string("Basic256Sha256,SignAndEncrypt,certificate.pem,key.pem")

    try:
        client.connect()
        print("Client connected")
        
        #Leer archivo para determinar los espacios con sus respectivos objetos y variables
        nameSpaces = []
        objects    = []
        variables  = []
        
        searchfile = open(file, "r")
        for line in searchfile:
            if "<Uri>" in line: 
                nameS = re.sub('</Uri>|<Uri>','',line)
                nameS = nameS.strip()

                nsIndex = client.get_namespace_index(nameS)
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
                            
                            #Escribir el valor de una de las variables: temp 
                            if dicVar["name"] == "temp" and dicVar["parentName"] == "Raspberry":
                                node = client.get_node("ns=" + str(dicVar["ns"]) + "; i=" + str(dicVar["id"]))
                                value = 100*adc.read_adc(0, gain=GAIN)*6.144/32765
                                node.set_value(value)
                                
                            #Escribir el valor de una de las variables: led 
                            if dicVar["name"] == "led" and dicVar["parentName"] == "Raspberry":
                                node = client.get_node("ns=" + str(dicVar["ns"]) + "; i=" + str(dicVar["id"]))
                                if (GPIO.input(10) == True):
                                    value = True
                                else:
                                    value = False
                                node.set_value(value)
                                
                            #Observar el valor de cada una de las variables 
                            if dicVar["ns"] == dicNs["index"] and dicVar["parentid"] == dicO["id"]:
                                node = client.get_node("ns=" + str(dicVar["ns"]) + "; i=" + str(dicVar["id"]))
                                value = node.get_value()
                                print("   " + dicVar["name"] + ": " + str(value))
                             
                            #Observar el valor de la variable led y encender y apagar el led acorde
                            if dicVar["name"] == "led" and dicVar["parentName"] == "Raspberry":
                                node = client.get_node("ns=" + str(dicVar["ns"]) + "; i=" + str(dicVar["id"]))
                                value = node.get_value()
                                if value == True:
                                    GPIO.output(8, GPIO.HIGH) 
                                else:
                                    GPIO.output(8, GPIO.LOW)
            
            print("*****************************************\n")
 
            time.sleep(0.1)
          
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
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD) 
        GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(10, GPIO.IN)
        
        start_client(file)
        
       else:
        print("File doesnt exist")
        
    else:
        print("ERROR: 1 file name is required")

    


   

   

