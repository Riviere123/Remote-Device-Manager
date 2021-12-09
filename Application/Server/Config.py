###Server Startup
IP_ADDRESS = ""           #Leave blank
PORT = 10023              #The port used for the server
SERVER_PASSWORD = "12345" #What the client will enter to connect to the server

###Certificate Generation
HOST_NAME = 'localhost'     
CERT_IP = ['10.0.0.64']   #Leave as a list
PASSWORD = b"password"    #What the password is to START the server


###Flask App
FLASK_SECRET_KEY = "Super_Secret_Key"     #Form encryption key NOTE:Set this in your env variables not here
FLASK_DEBUG = True                        #TURN OFF DEBUG FOR PRODUCTION SERVER
FLASK_PORT = 8000                         #The web servers port