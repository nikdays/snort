#!/usr/bin/python3
import subprocess
#Function which will install the prerequisites.
def prereq():
	subprocess.run("sudo apt-get install bison flex gcc libdnet libdumbnet-dev libluajit-5.1-dev libnghttp2-dev libpcap-dev libpcre3-dev libssl-dev make openssl* wget zlib1g-dev -y",shell=True)

#function that will take care of daq
def daq1():
	subprocess.run("sudo mkdir /usr/src/snort_src",shell=True)
	subprocess.run("sudo rm -rf  /usr/src/snort_src/*",shell=True)
	subprocess.run("sudo wget https://www.snort.org/downloads/snort/daq-2.0.6.tar.gz -P /usr/src/snort_src",shell=True)
	subprocess.run("sudo tar -C /usr/src/snort_src/ -zxf /usr/src/snort_src/daq-2.0.6.tar.gz ",shell=True)
	subprocess.run("sudo rm -rf /usr/src/snort_src/daq-2.0.6.tar.gz ",shell=True)
	subprocess.run("cd /usr/src/snort_src/daq-2.0.6/ && ./configure",shell=True)
	subprocess.run("cd /usr/src/snort_src/daq-2.0.6/ && make",shell=True)
	subprocess.run("cd /usr/src/snort_src/daq-2.0.6/ && sudo make install",shell=True)

#define a function to install snort
def snrt():
	subprocess.run("sudo wget https://www.snort.org/downloads/snort/snort-2.9.15.1.tar.gz -P /usr/src/snort_src",shell=True)
	subprocess.run("sudo tar -C /usr/src/snort_src/ -zxf /usr/src/snort_src/snort-2.9.15.1.tar.gz ",shell=True)
	subprocess.run("sudo rm -rf /usr/src/snort_src/snort-2.9.15.1.tar.gz ",shell=True)
	subprocess.run("cd /usr/src/snort_src/snort-2.9.15.1 && sudo ./configure --enable-sourcefire",shell=True)
	subprocess.run("cd /usr/src/snort_src/snort-2.9.15.1 && sudo make",shell=True)
	subprocess.run("cd /usr/src/snort_src/snort-2.9.15.1 && sudo make install",shell=True)
	subprocess.run("ldconfig",shell=True)
	subprocess.run("sudo ln -s /usr/local/bin/snort/ /usr/sbin/snort",shell=True)
	subprocess.run("sudo groupadd snort",shell=True)
	subprocess.run("sudo useradd snort -r -s /usr/sbin/nologin -c SNORT_IDS -g snort",shell=True)


#funtion that will take  care of the  folders required by snort and also take care of the permission and and ownership of the folders
def admn():
#create files required by snort
	subprocess.run("mkdir -p /etc/snort/rules",shell=True)
	subprocess.run("mkdir -p /var/log/snort",shell=True)
	subprocess.run("mkdir -p /usr/local/lib/snort_dynamicrules",shell=True)
	subprocess.run("sudo cp /usr/src/snort_src/snort-2.9.15.1/etc/*.conf* /etc/snort/",shell=True)
	subprocess.run("sudo cp /usr/src/snort_src/snort-2.9.15.1/etc/*.map /etc/snort/",shell=True)
	subprocess.run("sudo touch /etc/snort/rules/white_list.rules",shell=True)
	subprocess.run("sudo touch /etc/snort/rules/black_list.rules",shell=True)
	subprocess.run("sudo touch /etc/snort/rules/local.rules",shell=True)

#permission and ownership
	subprocess.run("sudo chmod -R 5775 /etc/snort/",shell=True)
	subprocess.run("sudo chmod -R 5775 /var/log/snort/",shell=True)
	subprocess.run("sudo chmod -R 5775 /usr/local/lib/snort_dynamicrules",shell=True)
	subprocess.run("sudo chown -R snort:snort /etc/snort/",shell=True)
	subprocess.run("sudo chown -R snort:snort /var/log/snort",shell=True)
	subprocess.run("sudo chown -R snort:snort /usr/local/lib/snort_dynamicrules",shell=True)
	subprocess.run("cp /etc/snort/snort.conf /etc/snort/snort.conf.backup",shell=True)

	subprocess.run("snort -V",shell=True)

def main():
	prereq()
	daq1()
	snrt()
	admn()
if __name__=='__main__':
	main()














#define a function that will handle the snort.conf file
#f=open("/etc/snort/snort.conf","r")
#f2=open('/etc/snort/snort.demo','w')
#f2.close()
#f2=open("/etc/snort/snort.demo","a")





f=open("/etc/snort/snort.conf","r")
f2=open('/etc/snort/snort.demo','w')
f2.close()
f2=open("/etc/snort/snort.demo","a")
for line in f:
#define path for the rules file
	if line=="var RULE_PATH ../rules\n":
		f2.write("var RULE_PATH /etc/snort/rules\n")
	elif line=="var SO_RULE_PATH ../so_rules\n":
		f2.write("var SO_RULE_PATH /etc/snort/so_rules\n")
	elif line=="var PREPROC_RULE_PATH ../preproc_rules\n":
		f2.write('var PREPROC_RULE_PATH /etc/snort/preproc_rules\n')
	elif line=="var WHITE_LIST_PATH ../rules\n":
		f2.write("var WHITE_LIST_PATH /etc/snort/rules\n")
	elif line=="var BLACK_LIST_PATH ../rules\n":
		f2.write("var BLACK_LIST_PATH /etc/snort/rules\n")
#delete extra rules in the file which start with include
	elif line.startswith('include'):
		f2.write('')
#adding include rules which will include the following directory
	elif line=="# site specific rules\n":
		f2.write(line)
		f2.write("include $RULE_PATH/local.rules\n")
		f2.write("include $RULE_PATH/white_list.rules\n")
		f2.write("include $RULE_PATH/black_list.rules\n")
#write the rest of the lines of the snort.conf file as it is
	else:
		f2.write(line)
f.close()
f2.close()


import shutil
shutil.copy2('/etc/snort/snort.demo', '/etc/snort/snort.conf')
