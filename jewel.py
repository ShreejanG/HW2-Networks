#!/usr/bin/env python3

import socket
import sys
import selectors

from file_reader import FileReader

class Jewel:

    def __init__(self, port, file_path, file_reader):
        self.file_path = file_path
        self.file_reader = file_reader

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', port))

        s.listen(5)
        sel = selectors.DefaultSelector()
        sel.register(s, selectors.EVENT_READ, self.accept_and_read)

        while True: 
            events = sel.select() 
            for key, mask in events: 
                callback = key.data
                callback(key.fileobj, mask, self.file_reader)

    def accept_and_read(self, s, mask, file_reader):
        (client, address) = s.accept()
        #address = ('127.0.0.1', 52454)
        addrAddress = address[0]
        addrPort = address[1] 

        print("[CONN] Connection from", str(addrAddress), "on port", str(addrPort))

        data = client.recv(5120)
        parsedData = data.decode('utf-8').split('\r\n')

        request = parsedData[0].split(' ')
        # ['GET', '/test.txt', 'HTTP/1.1']
        requestType = request[0]
        requestPath = request[1] 

        cookies_list = [i for i in parsedData if i.startswith('Cookie')]
        if not cookies_list: 
            cookies = None
        else: 
            cookies = cookies_list[0].remove('Cookie: ')

        validRequests = ['GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE', 'COPY', 'OPTIONS', 'LINK', 'UNLINK', 'PURGE', 'LOCK', 'UNLOCK', 'PROFFIND', 'VIEW']

        if requestType not in validRequests: 
            print("[ERRO] [" + str(addrAddress) + ":" + str(addrPort) + "]", requestType, "request returned error 400")
            client.close() 
            return
        else: 
            print("[REQU] [" + str(addrAddress) + ":" + str(addrPort) +"]", requestType, "request for", requestPath)

            if requestType == "GET": 
                getResponse = file_reader.get(requestPath, cookies)
                headResponse = file_reader.head(requestPath, cookies)
                if type(getResponse) == str: getResponse = getResponse.encode()
                if not getResponse:
                    print("[ERRO] [" + str(addrAddress) + ":" + str(addrPort) + "]", requestType, "request returned error 404")
                    client.send("HTTP/1.1 404 File not found\r\n\r\n".encode())
                else:
                    client.send("HTTP/1.1 200 OK\r\n".encode() + headResponse.encode() + "\r\n".encode() + getResponse)

            elif requestType == "HEAD": 
                headResponse = file_reader.head(requestPath, cookies)
                if not headResponse:
                    print("[ERRO] [" + str(addrAddress) + ":" + str(addrPort) + "]", requestType, "request returned error 404")
                    client.send("HTTP/1.1 404 File not found\r\n\r\n".encode())
                else:
                    client.send("HTTP/1.1 200 OK\r\n".encode() + headResponse.encode() + "\r\n".encode())

            else: 
                print("[ERRO] [" + str(addrAddress) + ":" + str(addrPort) + "]", requestType, "request returned error 501")
                client.send("HTTP/1.1 501 Method Unimplemented\r\n\r\n".encode())

            client.close() 


if __name__ == "__main__":
    port = int(sys.argv[1])
    file_path = sys.argv[2]

    FR = FileReader(file_path)

    J = Jewel(port, file_path, FR)
