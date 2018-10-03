import sys
import socket
import getpass

def usage():
    print("USAGE: python client.py -h|--host host -p|--port port")
    print("EXAMPLE: python client.py -h 127.0.0.1 -p 3300")

def main():
    if len(sys.argv) == 5 and (sys.argv[1] == "-h" or sys.argv[1] == "--host") and (sys.argv[3] == "-p" or sys.argv[3] == "--port"):
        host = sys.argv[2]
        port = int(sys.argv[4])
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((host,port))

        receive_message = client.recv(4096).decode("utf-8")
        callback_message = input(receive_message)
        client.send(callback_message.encode("utf-8"))

        receive_message = client.recv(4096).decode("utf-8")
        callback_message = getpass.getpass(receive_message)
        client.send(callback_message.encode("utf-8"))
        
        receive_message = client.recv(4096).decode("utf-8")

        while receive_message != "BYE" :
            if receive_message.endswith(">"):
                callback_message = input(receive_message)
            else:
                print(receive_message)
                callback_message = ""
            client.send(callback_message.encode("utf-8"))
            receive_message = client.recv(4096).decode("utf-8")


        client.close()
    else:
        usage()


if __name__ == "__main__":
    main()