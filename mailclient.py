from socket import *
from base64 import * # when logging into the google's secure smtp server
from ssl import * # when logging into the google's secure smtp server
from getpass import * #so we can enter the password without it showing in the CLI

mailserver = ("smtp.gmail.com", 465)

# Create socket called clientSocket and establish a TCP connection with mailserver over SSL
clientSocket = socket(AF_INET, SOCK_STREAM);
clientSocket = wrap_socket(clientSocket, ssl_version=PROTOCOL_SSLv23)
clientSocket.connect(mailserver)

#Print server response
recv = clientSocket.recv(1024)
print recv
if recv[:3] != "220":
    print "220 reply not received from server."
    
# Send EHLO command and print server response.
ehloCommand = "EHLO smtp.google.com\r\n"
clientSocket.send(ehloCommand)

recv1 = clientSocket.recv(1024)
print recv1
if recv1[:3] != "250":
    print "250 reply not received from server."

# SEND AUTH LOGIN command and Base64 encoded username & password
command = "AUTH LOGIN\r\n"
clientSocket.send(command)
recv1 = clientSocket.recv(1024)
print recv1

whoareyou = raw_input("Who are you? ")
username = raw_input("username: ") #your gmail username (ex. foo@gmail.com)
clientSocket.send(b64encode(username) + "\r\n")
recv1 = clientSocket.recv(1024)
print recv1

password = getpass() #password you use for gmail login
clientSocket.send(b64encode(password) + "\r\n")
recv1 = clientSocket.recv(1024)

if recv1[:3] == "535":
    print "Hey idiot! You didn't enter your stuff right! Now we have to start over!"
    exit()

print recv1

#prepare email message
clientSocket.send("MAIL FROM: <" + username + ">\r\n")
recv1 = clientSocket.recv(1024)
print recv1

recipient = raw_input("who is this to? ")
clientSocket.send("RCPT TO: <" + recipient + ">\r\n")
recv1 = clientSocket.recv(1024)
print recv1

clientSocket.send("DATA\r\n")
recv1 = clientSocket.recv(1024)
print recv1

msg  = "from: " + whoareyou + " <" + username + ">\r\n"
msg += "to: <" + recipient + ">\r\n"
msg += "subject: Testing email from python\r\n"
msg += "Mime-Version: 1.0;\r\n"
msg += "Content-Type: text/html; charset=\"ISO-8859-1\";\r\n"
msg += "Content-Transfer-Encoding: 7bit;\r\n"
msg += raw_input("Say what you ned to say: ")
msg += "\r\n"
endmsg = "\r\n.\r\n"

clientSocket.send(msg)
clientSocket.send(endmsg)

clientSocket.send("QUIT\r\n");
recv1 = clientSocket.recv(1024)
print recv1

clientSocket.close()