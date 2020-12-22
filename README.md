# OPC UA Tests in python

OPC UA python library is needed. Info: https://github.com/FreeOpcUa/python-opcua \
To generate data model, use opcua-modeler: https://github.com/FreeOpcUa/opcua-modeler \
To generate certificate and key. Info:  https://github.com/AndreasHeine/SecurePythonOpcUaServer 


Create certificate (certificate.der) and key (key.pem) in server and client:\
   &nbsp; &nbsp; change ssl.conf (subjectAltname, country, organizationName, ...)\
   &nbsp; &nbsp; openssl genrsa -out key.pem 2048 \
   &nbsp; &nbsp; openssl req -x509 -days 36500 -new -out certificate.pem -key key.pem -config ssl.conf\
   &nbsp; &nbsp; openssl x509 -outform der -in certificate.pem -out certificate.der

