import socket
from Crypto.Cipher import AES
import tqdm
import rsa
host = input("Enter ip address:")
port = int(input("Enter port number:"))
server =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
server.bind((host,port))
server.listen()

client,addr = server.accept()
rsa_public,rsa_private = rsa.newkeys(1024)

rsa_public_bytes = rsa_public.save_pkcs1()
client.send(rsa_public_bytes)

AES_key = rsa.decrypt(client.recv(128),rsa_private)
AES_nonce = rsa.decrypt(client.recv(128),rsa_private)

ciper = AES.new(AES_key, AES.MODE_EAX,AES_nonce)


file_name,file_size,data = client.recv(1024).decode("latin-1").split("<separator>")
data = data.encode("latin-1")
f = open(str(file_name), "wb")
progess = tqdm.tqdm(unit="B", desc=file_name,unit_scale=True,unit_divisor=1000,total=int(file_size))
done = False
file_bytes = b""
while not done:
    if file_bytes[-5:] == b"<END>":
        done = True
    else:
        file_bytes += data
    progess.update(1024)
    data = client.recv(1024)

f.write(ciper.decrypt(file_bytes[:-5]))
f.close()
server.close()