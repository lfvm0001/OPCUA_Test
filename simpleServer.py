from opcua import Server
from random import randint
import datetime
import time

server = Server()

url = "opc.tcp://127.0.01:4840" #IP:port
server.set_endpoint(url)

name = "OPCUA_SERVER_TEST"
addspace = server.register_namespace(name)

node = server.get_objects_node()
param = node.add_object(addspace, "Parameters")

temp = param.add_variable(addspace, "Temperature", 0)
timeS = param.add_variable(addspace, "Time Stamp", 0)

temp.set_writable()
timeS.set_writable()

server.start()
print("Server started at {}".format(url))

while True:
    Temperature = randint(10,50)
    TIME = datetime.datetime.now()

    print(Temperature,TIME)
    
    temp.set_value(Temperature)
    timeS.set_value(TIME)
    
    time.sleep(2)