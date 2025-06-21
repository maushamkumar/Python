import socket
import sys 
try: 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket connect successfully. ")
except socket.error as error:
    print(f"socket connection failed with error {error}")

# try:
#     ip = socket.gethostbyname('www.github.com')
#     print(f"GitHub IP address is: {ip}")
# except socket.gaierror as e:
#     print(f"DNS lookup failed: {e}")

port = 80 

try:
    host_id = socket.gethostbyname('www.github.com')
except socket.gaierror:
    print('error resloving the post ')
    sys.exit()
    
s.connect((host_id, port))
print(f"Socket has successfully connect to github on port == {host_id}")