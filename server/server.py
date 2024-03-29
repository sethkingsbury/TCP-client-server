import socket
from datetime import datetime
import sys

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

def create_socket(host, port):
    
    if port < 1024 or port > 64000:
        raise Exception("invalid port number")
    
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        raise Exception("failed to create socket")
    
    try:
        server.bind((host, port))
    except socket.error:
        raise Exception("failed to bind socket")
    
    return server


def run_server(server_socket):
    
    try:
        server_socket.listen(1)
    except socket.error:
        raise Exception("Failed to begin listening")
    
    print("Listening...")
    
    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection from {address} has been established!\nPort number: {client_socket.getsockname()[1]}\nTime Received: {dt_string}")
        
        data = client_socket.recv(1024)
        validate_data(data)
        filename = data[5:].decode('utf-8')
        print(f"Received request for {filename}" )
        
        try:
            file = open(filename, 'r')
            data = file.read()
            status = 1
        except FileNotFoundError:
            data = ""
            status = 0
            print("File does not exist or cannot be opened")
        
        output_data = create_response_header(data, status)
        
        client_socket.send(output_data)
        client_socket.close()
            
        
        

def validate_data(data):
    if data[0] << 8 | data[1] != 0x497E:
        raise Exception("Invlaid data, MagicNo != 0x497E")
    elif (data[2] != 1):
        raise Exception("Invalid data, Type != 1")
    elif (data[3] << 8 | data[4] != len(data[5:])):
        raise Exception("Invalid data, filenameLen incorrect")
    
def create_response_header(data, status):
    magicNo = 0x497E
    header_type = 2
    data_length = len(data)
    
    b1 = magicNo >> 8
    b2 = magicNo & 0xff
    b3 = header_type
    b4 = status
    b5 = data_length >> 0xff
    b6 = (data_length >> 0xf) & 0xff
    b7 = (data_length >> 0x8) & 0xff
    b8 = data_length & 0xff
    
    output = bytearray([b1, b2, b3, b4, b5, b6, b7, b8])
    
    if status == 1:
        output += data.encode('utf-8')
    
    return output
 
def main():
    if len(sys.argv) != 2:
        raise Exception("Too few parameters at run time (Port number required)")
    port = int(sys.argv[1])
    host = '127.0.0.1'
    server = create_socket(host, port)
    run_server(server)
    
main()
