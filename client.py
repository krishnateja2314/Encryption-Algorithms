import os
import socket
from Crypto.Cipher import AES
import rsa
host = input("Enter ip address:")
port = int(input("Enter port number:"))
clint = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
clint.connect((host,port))

key = os.urandom(16)
nonce = os.urandom(16)

rsa_public = clint.recv(251)
rsa_public = rsa.PublicKey.load_pkcs1(rsa_public)

encripted_AES_key = rsa.encrypt(key,rsa_public)
encripted_AES_nonce = rsa.encrypt(nonce,rsa_public)

clint.send(encripted_AES_key)
clint.send(encripted_AES_nonce)

ciper = AES.new(key, AES.MODE_EAX, nonce)

file_name = input("Enter your file name:")

file_size = os.path.getsize(file_name)

with open(file_name,"rb") as f:
    data = f.read()

encripted_data = ciper.encrypt(data)

clint.send(f"{file_name}<separator>{file_size}<separator>".encode("latin-1"))
clint.sendall(encripted_data)
clint.send(b"<END>")
clint.close()
