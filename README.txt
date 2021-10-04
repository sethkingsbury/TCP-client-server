Python TCP Client/Server Socket programming application

Client requests text files from the server. The server finds the corresponding file in its directory and sends it to
the client via a TCP stream.

Important files:

    server.py - Python file for running the server, takes port number as an argument
         arguments: port number - must be between 1024 and 64000

    client.py - Python file for running the client

        arguments: hostname - localhost works locally
                   port number - must be between 1024 and 64000
                   filename - name of the file being requested from the server, file must not already exist in the same
                              directory as the client file

Test text files have been provided in servers directory these are medicine.txt, quotes.txt and welding.txt.

Execution flow:

    python server.py "port number"
    python client.py "hostname" "port" "filename"


