import SimpleHTTPServer
import SocketServer

PORT = 8080

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print ("serving at port " + str(PORT))

# test that we can load the secret
try:
    stream = open("password", "r")
    print ("password is " + stream.read())
except:
    print ("couldn't load password")


httpd.serve_forever()
