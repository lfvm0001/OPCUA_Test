from opcua import Server, ua
from readXML import read_file
import RPi.GPIO as GPIO 
import Adafruit_ADS1x15
import os.path
import time
import sys


def start_server(file):  
    
    #Inicializar ADC
    adc = Adafruit_ADS1x15.ADS1115()
    GAIN = 2/3
    
    server = Server()
    
    #IP:port 
    url = "opc.tcp://10.82.132.99:4840"

    #Configurar servidor en url definido e importar archivo de modelo de informacion 
    server.set_endpoint(url)
    server.import_xml(file)
 
    #Si se desea seguridad a la hora de conectarse, cargar el certificado y key 
    #Deben estar en el mismo directorio y el cliente tambien debe tenerlos
    server.load_certificate("certificate.der")
    server.load_private_key("key.pem")
    server.set_security_policy([ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt]) 
    
    #Iniciar servidor
    server.start()        
    print("Server started at {}\n".format(url))
    
    
    try:       
        
        #Leer archivo para determinar los espacios con sus respectivos objetos y variables
        nameSpaces, objects, variables = read_file(server, file)
     
         
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
                            
                            #Escribir el valor de una de las variables: temp 
                            if dicVar["name"] == "temp" and dicVar["parentName"] == "Raspberry" and dicVar["nsName"]== "OPCUA_TEST":
                                node = server.get_node("ns=" + str(dicVar["ns"]) + "; i=" + str(dicVar["id"]))
                                value = 100*adc.read_adc(0, gain=GAIN)*6.144/32765
                                node.set_value(value)
                                
                            #Escribir el valor de una de las variables: led 
                            if dicVar["name"] == "led" and dicVar["parentName"] == "Raspberry" and dicVar["nsName"]== "OPCUA_TEST":
                                node = server.get_node("ns=" + str(dicVar["ns"]) + "; i=" + str(dicVar["id"]))
                                if (GPIO.input(10) == True):
                                    value = True
                                else:
                                    value = False
                                node.set_value(value)
                                
                            #Observar el valor de cada una de las variables 
                            if dicVar["ns"] == dicNs["index"] and dicVar["parentid"] == dicO["id"]:
                                node = server.get_node("ns=" + str(dicVar["ns"]) + "; i=" + str(dicVar["id"]))
                                value = node.get_value()
                                print("   " + dicVar["name"] + ": " + str(value))
                             
                            #Observar el valor de la variable led y encender y apagar el led acorde
                            if dicVar["name"] == "led" and dicVar["parentName"] == "Raspberry" and dicVar["nsName"]== "OPCUA_TEST":
                                node = server.get_node("ns=" + str(dicVar["ns"]) + "; i=" + str(dicVar["id"]))
                                value = node.get_value()
                                if value == True:
                                    GPIO.output(8, GPIO.HIGH) 
                                else:
                                    GPIO.output(8, GPIO.LOW)
            
            print("*****************************************\n")
 
            time.sleep(0.2)
          

    except KeyboardInterrupt:
        print("\nDisconnecting")
        server.stop()
        exit()

if __name__ == "__main__":

    if len(sys.argv) == 2:
       
       file = sys.argv[1]
       
       if os.path.isfile(file):
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD) 
        GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(10, GPIO.IN)
        
        start_server(file)
        
       else:
        print("File doesnt exist")
        
    else:
        print("ERROR: 1 file name is required")