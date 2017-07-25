import socket, select

'''

TODO:
- errorhandling
- testit

'''

#Datan broadcast kaikille yhdistetyille clienteille
#Käytetään seuraavassa funktiossa kun uusi viesti vastaanotetaan clientiltä
def broadcast_data (sock, message):
    #Vastaanotettu message välitetään kaikille muille yhteydessä oleville clienteille
    #lähettänyt socket on pois listasta
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                #Jos client sulkee yhteyden tai tapahtuu muuten virhetilanne
                #pistoke suljetaan ja poistetaan yhteyslistasta
                socket.close()
                CONNECTION_LIST.remove(socket)

def get_name(sock):
    j = 0
    for i in CONNECTION_LIST:
        j = j+1
        if i==sock:
            return j-2
    return 0

if __name__ == "__main__":

    # lista avatuista socketeista (clienteistä)
    CONNECTION_LIST = []
    USERS_LIST = []
    RECV_BUFFER = 4096 #Voisi olla suurempi?
    PORT = 5000 #portti muutetaan itse määriteltäväksi

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)



    #Uudet clientit lisätään listaan
    CONNECTION_LIST.append(server_socket)

    #Aloitusilmoitus serverin käynnistyessä
    print("Chat server started on port " + str(PORT))
    #Serverin toimintasilmukka
    while 1:
        # lista socketeista valitaan selectillä
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])

        for sock in read_sockets:
            #uusi yhteys
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print("Client connected from address {}".format(str(addr)))
                #nicknamen postaus
                USERS_LIST.append([addr, "Anonyymi"])
                string_to_broadcast = "{}  entered room".format(addr)
                string_to_broadcast = str.encode(string_to_broadcast)
                broadcast_data(sockfd, string_to_broadcast)
                continue

            #vastaanotettu viesti välitetään
            else:
                # Vastaanotettu data prosessoidaan
                # Mikäli ei onnistu, ilmoitetaan muille yhteyksille clientin olevan offline
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        #lähetysmuotoilu
                        data = bytes.decode(data)
                        if data.split(" ")[0] == "\changename":
                            try:
                                print("User changed name from " + USERS_LIST[get_name(sock)][1] + " to " +  data.split(" ")[1].strip("\n"))
                                USERS_LIST[get_name(sock)][1]=data.split(" ")[1].strip("\n")
                            except:
                                continue
                        elif data.strip("\n") == "\disconnect":
                            broadcast_data(sock, "Client {} is offline".format(addr))
                            print("Client {} is offline".format(addr))
                            sock.close()
                            try:
                                CONNECTION_LIST.remove(sock)
                            except:
                                print("Socket was not removed from list.")
                            continue
                        else:
                            string_to_broadcast = "\r" + '<' + USERS_LIST[get_name(sock)][1] + '> ' + data
                            print('{} : {}'.format(str(addr), str(string_to_broadcast).strip("\n").strip("\r")))
                            string_to_broadcast = str.encode(string_to_broadcast)
                            broadcast_data(sock, string_to_broadcast)

                except:
                    #ilmoitus clientin ollessa offline
                    broadcast_data(sock, "Client {} is offline".format(addr))
                    print("Client {} is offline".format(addr))
                    sock.close()
                    try:
                        CONNECTION_LIST.remove(sock)
                    except:
                        print("Socket was not removed from list.")
                    continue

    server_socket.close()
