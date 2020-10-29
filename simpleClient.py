from opcua import Client
import time

url = "opc.tcp://10.42.0.104:4840" #IP:port

client = Client(url)
client.connect()
print("Client connected")

while True:
    temp = client.get_node("ns=2; i=2")
    Temperature = temp.get_value()
    print(Temperature)
    
    timeS = client.get_node("ns=2; i=3")
    timeStamp = timeS.get_value()
    print(timeStamp)
    
    time.sleep(1)