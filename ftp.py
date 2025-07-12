
 
# Fill Required Information

import paramiko

HOSTNAME = "192.168.1.13"
USERNAME = "nao"
PASSWORD = "nao"


ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=HOSTNAME, username=USERNAME, password=PASSWORD,allow_agent=False)
sftp_client = ssh_client.open_sftp()
path = './recordings/cameras/' 
sftp_client.chdir(path)

# transport = paramiko.Transport((HOSTNAME, 22))

#         #hard-coded
# transport.connect(username = USERNAME, password = PASSWORD)

# sftp = paramiko.SFTPClient.from_transport(transport)

# import sys
   #hard-coded
localpath = "image.jpg"
# sftp.put(localpath, path)
# sftp.chdir(path)
sftp_client.get('image.jpg', localpath)

sftp_client.close()
ssh_client.close()
print("Done")