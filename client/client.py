import socket
import os.path
import sys
    
def get_host(host):
    """Requests user to input host address as either an IPv4 or the host name
    which will be returned as an IP address"""
    try:        
        return socket.gethostbyname(host)   
    except socket.error:
        raise Exception("Invalid host entered!")   

def get_port(port_number):
    port_number = int(port_number)
    if port_number < 1024 or port_number > 64000:
        raise Exception("Invalid port number entered (must be between 1024 and 64000 inclusive)")
    else:
        return port_number
    
def check_file(filename):
    if os.path.exists(filename):
        try:
            file = open(filename)
            file.close()
            raise Exception("This file already exists on your computer!")
        except OSError:
            pass
        
def create_socket():
    try:
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        raise Exception("failed to create socket")    

def connect_socket(client, host, port):
    try:
        client.connect((host, port))
    except socket.error:
        client.close()
        raise Exception("Failed to connect to server")
    
def create_request_header(filename):
    magicNo = 0x497E
    header_type = 1
    filename_length = len(filename)
    
    b1 = magicNo >> 8
    b2 = magicNo & 0xff
    b3 = header_type
    b4 = filename_length >> 8
    b5 = filename_length & 0xff
    
    header = bytearray([b1, b2, b3, b4, b5])
    
    return header

def validate_data(data):
    
    output = False
    
    if data[0] << 8 | data[1] != 0x497E:
        raise Exception("Invlaid data, MagicNo != 0x497E")
    elif data[2] != 2:
        raise Exception("Invalid data, Type != 2")
    elif (data[4] << 0xff | data[5] << 0xf | data[6] << 8 | data[7]) != len(data[8:]):
        raise Exception("Invalid Data, DataLength incorrect")
    elif data[3] == 0:
        print("File not found on server")
    else:
        print("File Valid!")
        output = True
    
    return output, data[8:]
       
def main():
    if len(sys.argv) < 4:
        raise Exception("Too few parameters at run time (Host, Port and File required)")    
    host = get_host(sys.argv[1])
    port = get_port(sys.argv[2])
    filename = sys.argv[3]
    check_file(filename)
    s = create_socket()
    connect_socket(s, host, port)
    header = create_request_header(filename.encode('utf-8'))
    message = header + filename.encode('utf-8')
    
    s.send(message)
    
    data = s.recv(4096)
    valid, file_contents = validate_data(data)
    
    if valid:
        file = open(filename, 'w+')
        file.write(file_contents.decode('utf-8'))
        file.close()
    
main()
