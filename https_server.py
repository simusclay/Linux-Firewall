from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl

# Directory dei file che vuoi servire
directory = "/path/to/your/files"

# Imposta i percorsi dei file chiave e certificato
keyfile = "./Certificates/key.pm"
certfile = "./Certificates/cert.pem"

# Crea un server HTTPS personalizzato
server_address = ('', 443)
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(httpd.socket, keyfile=keyfile, certfile=certfile, server_side=True)

# Avvia il server
print("Server in esecuzione su https://localhost:443/")
httpd.serve_forever()

