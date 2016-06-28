#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  uprpm.py
#  
#  Copyright 2016 youcef sourani <youcef@yucef>
#
#  www.arfedora.blogspot.com
#
#  www.arfedora.com
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import os
import platform
import subprocess
import sys


def init_check():
	versions=["22","23","24","25"]
	if os.getuid()==0:
		sys.exit("Run Script Without Root Permissions.")
		
	if platform.linux_distribution()[0]!="Fedora" :
		sys.exit("Fedora Not Found.")
		
	if platform.linux_distribution()[1] not in versions:
		sys.exit("Version Not Supported.")
		
	if not sys.version.startswith("3"):
		sys.exit("Use Python 3 Try run python3 uprpm.py")

init_check()



def get_ip(interface):
	return [subprocess.Popen("ip add |grep %s |grep inet"%interface,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).communicate()[0].decode("utf-8").split()[1][0:-3],interface]
	
def wls_enps():
	count=0
	interface={}
	wl_enp=subprocess.Popen("ip add |grep wl;ip add|grep en",stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).communicate()[0].decode("utf-8").split()
	

	for word in wl_enp:
		if word.startswith("wl") or word.startswith("en"):
			if word not in interface.values():
				try :
					subprocess.Popen("ip add |grep %s |grep inet"%word,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).communicate()[0].decode("utf-8").split()[1][0:-3]
				except :
					continue
				count+=1
				interface.setdefault(str(count),word)
	

	while True:
		print ("Enter Number To Choise Interface || q To Exit :\n")
		for key,value in interface.items():
			print ("%s-%s.\n"%(key,value))
		answer=input()
		if answer in interface.keys():
			return get_ip(interface[answer])
		elif answer=="q" or answer=="Q":
			sys.exit("\nBye...\n")



home=os.getenv("HOME")

port=8080

ip_interface=wls_enps()
ip=ip_interface[0]
interface=ip_interface[1]









		





def install_createrepo():
	check=subprocess.call("createrepo --version &>/dev/null",shell=True)
	if check!=0:
		check=subprocess.call("sudo dnf install createrepo -y --best",shell=True)
		if check!=0:
			sys.exit("\n\nFail Check Your Internet || Check sudo .\n\n")




def make_folder():
	try:
		os.makedirs("%s/arfedora_rpm_repo"%home,exist_ok=True)
	except :
		sys.exit("Make %s/arfedora_rpm_repo fail."%home)





def cp_paks_make_repo():
	os.chdir("/var/cache/dnf")
	subprocess.call("find -iname *.rpm -exec cp -arvu \'{}\' %s/arfedora_rpm_repo \';\'"%home,shell=True)
	subprocess.call("createrepo --update %s/arfedora_rpm_repo"%home,shell=True)
	os.chdir("%s/arfedora_rpm_repo"%home)


def make_repo_file():
	repo="""[my_local_repo_%s]
name= my local repo
baseurl=http://%s:%s/
enable=1
gpgcheck=0
priority=10
"""%(interface,ip,str(port) )
	with open("%s/arfedora_rpm_repo/my_local_repo_%s.repo"%(home,interface),"w") as myfile:
		myfile.write(repo)
	print ("\n\nRepo File in %s/arfedora_rpm_repo/my_local_repo_%s.repo"%(home,interface))
	print ("\n\nIn Local Network Try : sudo curl -o  /etc/yum.repos.d/my_local_repo_%s.repo http://%s:%s/my_local_repo_%s.repo"%(interface,ip,str(port),interface ))




def start_server():
	global port
	print ("\n\nServer Link : http://%s:%s\n"%(ip,str(port) ) )
	check=subprocess.call("python3 -m http.server %s 2>/dev/null"%str(port),shell=True)
	if check!=0:
		port+=1
		subprocess.call("reset",shell=True)
		print ("\n[+]Server Fail New Port Set %s Restarting..........\n\n"%str(port))
		return main()




def main():
	install_createrepo()
	make_folder()
	cp_paks_make_repo()
	make_repo_file()
	start_server()
	
	

if __name__=="__main__":
	main()

