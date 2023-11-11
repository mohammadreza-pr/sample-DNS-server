# Sample-DNS-server
### Done as a part of the Computer Networks course at Sharif University Fall 1402.
A DNS server that is capable of responding to A type DNS queries on the server where it is deployed. By running this server, you have the ability to create and manage your own DNS mapping, allowing you to customize and control the resolution of domain names to IP addresses.
# DNS Server Setup Guide

## 1. Prepare DNS Records

Put your DNS records in the `/etc/hosts` file. Open the file using a text editor and add entries in the format:

```plaintext
<IP Address>    <Domain Name>
```
For example: <br>
```
192.168.1.100    example.com
192.168.1.101    subdomain.example.com
```
## 2. Run the DNS Server
Execute the ClientHandler.py file using Python. Open your terminal and navigate to the directory where the file is located. Run the following command:
```bash
python ClientHandler.py
```

## 3. DNS Server Configuration
. The DNS server is now listening on port 5353 UDP.<br>
. Ensure that no other application is using the same port to avoid conflicts.

## 4. Testing
You can test the DNS server by querying it using a tool like dig or nslookup. For example:
```
dig @127.0.0.1 -p 5353 example.com
```