from readXML import read_file
from opcua import Client
import RPi.GPIO as GPIO 
import Adafruit_ADS1x15
import os.path
import time
import sys


def start_client(file):  
    
    #Inicializar ADC
    adc = Adafruit_ADS1x15.ADS1115()
    GAIN = 2/3

    #IP:Puerto
    #url = "opc.tcp://192.168.0.100:4840" #IP:port
    url = "opc.tcp://172.16.1.166:4840"

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
        response = read_file(client, file)
        nameSpaces = response[0]
        objects    = response[1]
        variables  = response[2]
         
        #Aca van las acciones del cliente
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