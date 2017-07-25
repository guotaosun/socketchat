#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket, select, string, sys
from PyQt5.QtWidgets import QLabel, QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QLineEdit, QListWidget
from _thread import *
import time

class ChatWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        self.nickname = "Anonyymi"

        if(len(sys.argv) < 2) :
            print('Usage : python chatclient.py hostname')
            sys.exit()

        host = sys.argv[1]
        port = 5000
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(2)

        # serveriin yhdistäminen

        try :
            self.s.connect((host, port))
        except :
            print('Unable to connect')
            sys.exit()

        print('Connected to remote host. Start sending messages!')
        self.messageList.addItem('Connected to remote host. Start sending messages!')
        
        #self.socket_list = [sys.stdin, self.s]
        self.socket_list = [self.s]

        # Sockettilista
        
        start_new_thread(self.pollMessages, ())

        
    def initUI(self):
        
        self.messageField = QLineEdit()
        self.messageField.setPlaceholderText("Send a message:")
        self.sendButton = QPushButton("Send")
        self.messageList = QListWidget()
        #self.hostLabel = QLabel("Host:", self)
        #self.hostField = QLineEdit()
        #self.portLabel = QLabel("Port:", self)
        #self.portField = QLineEdit()
        self.nickLabel = QLabel("Change nickname:", self)
        #self.emptyLabel = QLabel(" ", self)
        self.nickField = QLineEdit()
        self.connectButton = QPushButton("Connect")
        self.nickButton = QPushButton("Change")
        self.nickButton.setAutoDefault(True)
        self.sendButton.setAutoDefault(True)

        self.messageField.returnPressed.connect(self.sendButton.click)
        self.nickField.returnPressed.connect(self.nickButton.click)
        self.sendButton.clicked.connect(self.sendButtonClicked)
        #self.connectButton.clicked.connect(self.connectButtonClicked)
        self.nickButton.clicked.connect(self.nickButtonClicked)

        hbox = QHBoxLayout()
        hbox.addWidget(self.messageField)
        hbox.addWidget(self.sendButton)

        connectLayout = QWidget()
        vbox1 = QVBoxLayout()
        #vbox1.addWidget(self.hostLabel)
        #vbox1.addWidget(self.hostField)
        #vbox1.addWidget(self.portLabel)
        #vbox1.addWidget(self.portField)
        #vbox1.addWidget(self.connectButton)
        #vbox1.addWidget(self.emptyLabel)
        vbox1.addWidget(self.nickLabel)
        vbox1.addWidget(self.nickField)
        vbox1.addWidget(self.nickButton)
        vbox1.addStretch(1)
        connectLayout.setLayout(vbox1)
        connectLayout.setFixedWidth(175)
        vbox3 = QHBoxLayout()
        vbox3.addWidget(connectLayout)

        hbox2 = QHBoxLayout()
        hbox2.addLayout(vbox3)
        hbox2.addWidget(self.messageList)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)
        
        self.resize(720, 480)
        self.center()
        
        self.setWindowTitle('Bestest cHAT APP evER')    
        self.show()
        
        
    def center(self):
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
        
    def pollMessages(self):
        
        while True:
            self.read_sockets, self.write_sockets, self.error_sockets = select.select(self.socket_list, [], [])
            
            for sock in self.read_sockets:
                
                #viestin vastaanottaminen serveriltä
                try:
                    data = sock.recv(4096)
                    print(data)
                    if not data :
                        print('Disconnected from chat server')
                        sys.exit()
                    else:
                        output = bytes.decode(data)
                        self.messageList.addItem(output)
                except:
                    pass
        
    def sendButtonClicked(self):
        
        if len(self.messageField.text()) > 0:
            message = self.messageField.text()
            message_to_send = message
            input = str.encode(message_to_send)
            
            message_to_write = "<" + self.nickname + " (You)> " + message
            self.messageList.addItem(message_to_write)
            self.messageField.clear()
        
            try:
                self.s.send(input)
            except:
                self.sendButtonClicked()
            
        return

    def connectButtonClicked(self):

        return

    def nickButtonClicked(self):

        string = "\changename " + self.nickField.text()

        self.nickname = self.nickField.text()

        try:
            input = str.encode(string)
            self.s.send(input)
        except:
            self.nickButtonClicked()
        
        self.messageList.addItem("Name changed to " + self.nickField.text())
        self.nickField.clear()

        

        return
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    cw = ChatWindow()
    
    sys.exit(app.exec_())
    
    