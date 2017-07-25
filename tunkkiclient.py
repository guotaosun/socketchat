import socket, select, string, sys

'''
Ohjelman tämänhetkinen tila toteutettu tutorial-ohjeiden pohjalta.

TODO:
- nickname toimimaan
- mahdollisuus valita huone?
- vanhojen viestien vastaanottaminen
- testit
- errorhandling

'''

def prompt() :
    sys.stdout.write('<You> ')
    sys.stdout.flush()


if __name__ == "__main__":


    if(len(sys.argv) < 3) :
        print('Usage : python chatclient.py hostname port')
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # serveriin yhdistäminen

    try :
        s.connect((host, port))
    except :
        print('Unable to connect!!')
        sys.exit()

    print('Connected to remote host. Start sending messages!')
    prompt()

    while 1:
        socket_list = [sys.stdin, s]

        # Sockettilista

        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

        for sock in read_sockets:
            #viestin vastaanottaminen serveriltä
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print('\nDisconnected from chat server')
                    sys.exit()
                else :
                    #print data
                    output = bytes.decode(data)
                    sys.stdout.write(output)
                    prompt()

            #oman viestin lähetys
            else :
                msg = sys.stdin.readline()
                input = str.encode(msg)
                s.send(input)
                prompt()
