###Server Startup
IP_ADDRESS = "0.0.0.0" #Your servers listening IP 0.0.0.0 is for all traffic, internet and local
PORT = 10023           #The port to listen to connections on

###Certificate Generation
HOST_NAME = 'localhost'   #The DNS name of your server. If you do not use one leave it as localhost
CERT_IP = ['10.0.0.64']     #Setting to my server machines local ip address... If you're going over the internet use your public IP Keep this as a list.
PASSWORD = b"password"