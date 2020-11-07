# OPC UA Tests in python

OPC UA python library is needed. Info: https://github.com/FreeOpcUa/python-opcua \
To generate data model, use opcua-modeler: https://github.com/FreeOpcUa/opcua-modeler \

To generate certificate and key (Taken from https://github.com/AndreasHeine/SecurePythonOpcUaServer): \
In server:\
   change ssl.conf (subjectAltname, country, organizationName, ...)\
   openssl genrsa -out key.pem 2048 \
   openssl req -x509 -days 36500 -new -out certificate.pem -key key.pem -config ssl.conf\
\
Copy certificate.pem and key.pem in client

