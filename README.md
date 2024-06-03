# Firewall-Lab
This repo has the purpose to provide the needed configuration files used to run a basic laboratory lesson about firewalls

To read the report and perform the exercises-> [Report](https://docs.google.com/document/d/1WYed3pWs76Oq41XXqbZ48H1vB2qYjUYB4goEMtY3PUY/edit?usp=sharing)

## Requirements
The basic requirements to run a custom topology and play with the linux firewall are Mininet and iptables. The custom topology are implemented using python APIs so also python is required.
```
$ sudo apt-get install mininet iptables iptables-persistent python3
```
To follow along the various exercises proposed in the report you'll need a few more packages to perform specific commands:
```
$ sudo apt install python3-scapy netcat hping3 pip libnetfilter-queue-dev tcpdump nmap psmisc
$ sudo pip3 install LibnetfilterQueue --break-system-packages



```
**Note:** The flag "--break-system-packages" should be executed only when working in a virtualized environment. 

## Usage 
To run a topology use the command
```
$ sudo python3 <filename>
```
